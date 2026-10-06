#!/usr/bin/env python3
"""Local mirror of the Onshape FeatureScript (cad/scoop.fs) for the Probe #42 hood scoop.
Builds every printable part as a watertight STL from the same parameter set, without Onshape.
The FeatureScript is the design master; this script exists so parts can be regenerated when the
Onshape API is unavailable, and so anyone with Python can rebuild them.

    python3 local_build.py                 # writes stl/*.stl with the default parameters
    python3 local_build.py --out some/dir  # elsewhere
    python3 local_build.py --set roofTop=76 --set mouthW=200

Requires: numpy, trimesh, shapely, manifold3d, networkx   (pip install numpy trimesh shapely manifold3d networkx)
Local frame: x across the car (+x = your right when standing at the bumper), y rearward, z out of the hood.
"""
import argparse, json, os, sys
import numpy as np, trimesh
from trimesh.creation import extrude_polygon
from shapely.geometry import box as sbox, Polygon

# ---- parameters (mm; identical names and defaults to the FeatureScript) ----
DEFAULTS = dict(
    cutW=195, cutL=71, cutR=10, sleeveWall=2,
    skinT=0.8, innerGap=21, innerT=0.8, gasketT=1.5,
    baseW=244, baseFront=97, baseRear=84, baseR=10, baseT=6,
    bodyW=196, bodyFront=65, bodyRear=60, roofTop=72, wall=3, bodyR=4, chamferF=4, chamferR=10,
    mouthW=186, mouthR=4, lipR=2.5, bezelW=5,
    boltX=112, boltYF=80, boltYM=-4, boltYR=72, holeD=6.5, boltL=50, backingT=3,
    guideW=200, guideReach=50, guideAngle=45, cheekH=55, guideT=3,
    logoW=92,
)
# hood sag at the fitted site (local frame, tangent plane removed): z = D x^2 + E x y + F y^2  — from site_fit.json
SAG = dict(D=-0.000148, E=-0.000013, F=-0.000285)
# 4OGS wordmark polygons (SVG coordinates, y down) from esp32-race-logger/mechanical/reference/4ogs_logo.svg
LOGO_POLYS = [[(61.72, 41.62), (50.04, 78.15), (78.52, 78.15), (87.22, 71.87), (102.35, 24.54), (72.24, 24.54), (65.66, 29.29), (63.16, 37.11), (84.31, 37.11), (75.21, 65.58), (68.08, 65.58), (75.74, 41.62)],
              [(44.33, 7.58), (27.97, 7.58), (18.53, 37.11), (34.89, 37.11)],
              [(136.73, 41.62), (142.19, 24.54), (112.07, 24.54), (105.49, 29.29), (102.99, 37.11), (124.15, 37.11), (122.7, 41.62)],
              [(202.0, 7.58), (51.57, 7.58), (38.66, 47.93), (31.42, 47.93), (33.44, 41.62), (17.08, 41.62), (10.38, 62.59), (33.98, 62.59), (29.0, 78.15), (45.37, 78.15), (63.84, 20.36), (188.06, 20.36), (182.7, 37.11)],
              [(145.35, 29.29), (142.85, 37.11), (178.03, 37.11), (182.04, 24.54), (151.93, 24.54)],
              [(155.43, 41.62), (141.41, 41.62), (136.29, 57.61), (157.45, 57.61), (154.9, 65.58), (133.75, 65.58), (129.73, 78.15), (164.9, 78.15), (175.48, 45.08), (154.32, 45.08)],
              [(91.92, 71.73), (97.86, 78.15), (125.05, 78.15), (133.51, 51.67), (117.04, 51.67), (114.42, 59.86), (116.87, 59.86), (115.04, 65.58), (107.91, 65.58), (115.58, 41.62), (101.55, 41.62)]]

# ---- geometry helpers ----
def rrect(w, l, r, cx=0.0, cy=0.0):
    r = min(r, w / 2 - 1e-3, l / 2 - 1e-3)
    if r <= 0: return sbox(cx - w / 2, cy - l / 2, cx + w / 2, cy + l / 2)
    return sbox(cx - w / 2 + r, cy - l / 2 + r, cx + w / 2 - r, cy + l / 2 - r).buffer(r, join_style=1, resolution=16)
def ex(poly, z0, z1):
    m = extrude_polygon(poly, z1 - z0); m.apply_translation([0, 0, z0]); return m
def box(x0, y0, z0, x1, y1, z1): return ex(sbox(x0, y0, x1, y1), z0, z1)
def cyl(cx, cy, z0, z1, d):
    m = trimesh.creation.cylinder(radius=d / 2, height=z1 - z0, sections=48); m.apply_translation([cx, cy, (z0 + z1) / 2]); return m
def rrbox_y(w, h, r, cx, cz, y0, y1):
    """rounded rectangle in the x-z plane (corners rounded on edges parallel to y), extruded from y0 to y1"""
    m = ex(rrect(w, h, r, cx, cz), 0, y1 - y0)                         # built in (x, z) as (x, y), extruded along +z
    T = np.array([[1, 0, 0, 0], [0, 0, 1, y0], [0, 1, 0, 0], [0, 0, 0, 1]], float)   # (x, y, z) -> (x, z + y0, y)
    m.apply_transform(T); m.fix_normals(); return m
def wedge_x(x0, length, pts_yz):
    poly = Polygon(pts_yz); m = extrude_polygon(poly, length)          # built in (y, z) plane, extruded along +z -> x
    T = np.array([[0, 0, 1, x0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]], float)
    m.apply_transform(T); m.fix_normals(); return m
def U(*ms): return trimesh.boolean.union(list(ms), engine="manifold")
def D(a, *tools): return trimesh.boolean.difference([a, *tools], engine="manifold")
def heightfield_below(xs, ys, zfun, zbottom):
    """closed solid occupying zbottom <= z <= zfun(x, y) over the grid xs x ys"""
    X, Y = np.meshgrid(xs, ys); Z = zfun(X, Y); nx, ny = len(xs), len(ys)
    top = np.c_[X.ravel(), Y.ravel(), Z.ravel()]; bot = np.c_[X.ravel(), Y.ravel(), np.full(X.size, zbottom)]
    V = np.vstack([top, bot]); F = []
    idx = lambda i, j: i * nx + j; off = X.size
    for i in range(ny - 1):
        for j in range(nx - 1):
            a, b, c, d = idx(i, j), idx(i, j + 1), idx(i + 1, j + 1), idx(i + 1, j)
            F += [[a, b, c], [a, c, d], [off + a, off + c, off + b], [off + a, off + d, off + c]]
    for i in range(ny - 1):   # sides along x = const
        a, d = idx(i, 0), idx(i + 1, 0); F += [[a, off + a, off + d], [a, off + d, d]]
        a, d = idx(i, nx - 1), idx(i + 1, nx - 1); F += [[a, d, off + d], [a, off + d, off + a]]
    for j in range(nx - 1):   # sides along y = const
        a, b = idx(0, j), idx(0, j + 1); F += [[a, b, off + b], [a, off + b, off + a]]
        a, b = idx(ny - 1, j), idx(ny - 1, j + 1); F += [[a, off + a, off + b], [a, off + b, b]]
    m = trimesh.Trimesh(V, np.array(F), process=True); m.fix_normals(); return m

def build(P):
    mm = P
    cutW, cutL, cutR = P["cutW"], P["cutL"], P["cutR"]; sw = P["sleeveWall"]
    holeW, holeL, holeR = cutW + 2 * sw, cutL + 2 * sw, cutR + sw
    skinT, gap, innerT, gk = P["skinT"], P["innerGap"], P["innerT"], P["gasketT"]
    stackBottom = -(gk + skinT + gap + innerT)
    baseW, bF, bR, baseR, baseT = P["baseW"], -P["baseFront"], P["baseRear"], P["baseR"], P["baseT"]
    baseCy, baseL = (bF + bR) / 2, bR - bF
    bodyW, yF, yR, top, w, bodyR = P["bodyW"], -P["bodyFront"], P["bodyRear"], P["roofTop"], P["wall"], P["bodyR"]
    chF, chR, mouthW, mouthR, bzW = P["chamferF"], P["chamferR"], P["mouthW"], P["mouthR"], P["bezelW"]
    bx, yf, ym, yr, holeD, bkT = P["boltX"], -P["boltYF"], P["boltYM"], P["boltYR"], P["holeD"], P["backingT"]
    bolts = [(-bx, yf), (bx, yf), (-bx, ym), (bx, ym), (-bx, yr), (bx, yr), (0, yf), (0, yr)]
    guideW, reach, ang, cheekH, gt = P["guideW"], P["guideReach"], np.radians(P["guideAngle"]), P["cheekH"], P["guideT"]
    gTop = gk; z0 = gTop + baseT; mouthH = top - chF - bzW - gk - baseT
    parts = {}

    # ---- A body: flange (hood-matched) + cowl, one piece ----
    base = ex(rrect(baseW, baseL, baseR, 0, baseCy), gTop - 12, gTop + baseT)
    sag = lambda X, Y: gTop + SAG["D"] * X**2 + SAG["E"] * X * Y + SAG["F"] * Y**2
    below = heightfield_below(np.linspace(-baseW / 2 - 15, baseW / 2 + 15, 25), np.linspace(bF - 15, bR + 15, 21), sag, gTop - 40)
    base = D(base, below)
    tools = [ex(rrect(cutW, cutL, cutR), gTop - 20, gTop + baseT + 10)]
    tools += [cyl(x, y, gTop - 20, gTop + baseT + 10, holeD) for x, y in bolts]
    tools += [D(cyl(x, y, gTop + baseT - 0.6, gTop + baseT + 1, 14), cyl(x, y, gTop + baseT - 2, gTop + baseT + 2, 11)) for x, y in bolts]   # debossed rings
    tools += [ex(rrect(holeW + 0.4, holeL + 0.4, holeR), gTop - 2, gTop + 1.5)]                                                            # sleeve seat
    base = D(base, *tools)
    cowl = ex(rrect(bodyW, yR - yF, bodyR, 0, (yF + yR) / 2), z0, top)
    wedges = []
    if chF > 0: wedges.append(wedge_x(-bodyW / 2 - 2, bodyW + 4, [(yF - 2, top - chF - 2), (yF + chF + 2, top + 2), (yF - 2, top + 2)]))
    if chR > 0: wedges.append(wedge_x(-bodyW / 2 - 2, bodyW + 4, [(yR + 2, top - chR - 2), (yR - chR - 2, top + 2), (yR + 2, top + 2)]))
    if wedges: cowl = D(cowl, *wedges)
    cav = ex(rrect(bodyW - 2 * w, (yR - yF) - 2 * w, max(bodyR - w, 0.5), 0, (yF + yR) / 2), z0 - 1, top - w)
    wo = w * 1.4142; cw = []
    if chF > 0: cw.append(wedge_x(-bodyW / 2 - 2, bodyW + 4, [(yF - 2, top - chF - wo - 2), (yF + chF + wo + 2, top + 2), (yF - 2, top + 2)]))
    if chR > 0: cw.append(wedge_x(-bodyW / 2 - 2, bodyW + 4, [(yR + 2, top - chR - wo - 2), (yR - chR - wo - 2, top + 2), (yR + 2, top + 2)]))
    if cw: cav = D(cav, *cw)
    mouth = rrbox_y(mouthW, mouthH, mouthR, 0, z0 + mouthH / 2, yF - 5, yF + w + 2)
    rebate = rrbox_y(mouthW + 2 * bzW, mouthH + bzW + 0.01, mouthR + bzW, 0, z0 - 0.01 + (mouthH + bzW + 0.01) / 2, yF - 5, yF + 3)
    cowl = D(cowl, cav, mouth, rebate)
    # logo deboss (reads correctly standing in front of the car)
    xs = [x for p in LOGO_POLYS for x, _ in p]; ys = [y for p in LOGO_POLYS for _, y in p]
    sc = P["logoW"] / (max(xs) - min(xs)); cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    lc = (0.0, (yF + chF + yR - chR) / 2)
    logo = [ex(Polygon([(sc * (x - cx) + lc[0], -sc * (y - cy) + lc[1]) for x, y in p]), top - 0.6, top + 1) for p in LOGO_POLYS]
    cowl = D(cowl, *logo)
    parts["A_body"] = U(base, cowl)

    # ---- B bezel (flush frame, open at the sill) ----
    bz = rrbox_y(mouthW + 2 * bzW, mouthH + bzW, mouthR + bzW, 0, z0 + (mouthH + bzW) / 2, yF, yF + 3)
    bzi = rrbox_y(mouthW, mouthH + 1, mouthR, 0, z0 - 1 + (mouthH + 1) / 2, yF - 2, yF + 5)
    parts["B_bezel"] = D(bz, bzi)

    # ---- S throat sleeve ----
    zTopS, zBotS = gTop + 1.5 - 0.2, stackBottom - bkT
    parts["S_throat_sleeve"] = D(ex(rrect(holeW, holeL, holeR), zBotS, zTopS), ex(rrect(cutW, cutL, cutR), zBotS - 2, zTopS + 2))

    # ---- R rain cap (modelled 45 mm ahead of the mouth, like the FeatureScript) ----
    ey = -45.0
    capF = rrbox_y(mouthW + 2 * bzW, mouthH + bzW, mouthR + bzW, 0, z0 + (mouthH + bzW) / 2, yF + ey - 3, yF + ey)
    plug = rrbox_y(mouthW - 0.6, mouthH - 0.6, max(mouthR - 0.3, 0.5), 0, z0 + mouthH / 2, yF + ey - 0.5, yF + ey + 15)
    plug = D(plug, box(-mouthW / 2 + 3.3, yF + ey + 3, z0 + 3.3, mouthW / 2 - 3.3, yF + ey + 16, z0 + mouthH - 3.3))
    bumps = [box(s * mouthW / 4 - 10, yF + ey + 9, z0 + mouthH - 0.4, s * mouthW / 4 + 10, yF + ey + 12, z0 + mouthH + 0.3) for s in (-1, 1)]
    cap = U(capF, plug, *bumps)
    parts["R_rain_cap"] = D(cap, box(-15, yF + ey - 4, z0 - 1, 15, yF + ey + 1, z0 + 4))

    # ---- C guide: U-bracket + flap + inboard cheek ----
    zPlateTop = stackBottom - bkT - 0.5; armHalfW = bx + 13; hy = holeL / 2 + 24
    plate = ex(rrect(2 * armHalfW, hy + 22, 6, 0, (hy - 22) / 2), zPlateTop - gt, zPlateTop)
    plate = D(plate, ex(rrect(holeW + 6, holeL + 6, 12), zPlateTop - gt - 2, zPlateTop + 2),
              box(-(holeW / 2 + 3), -30, zPlateTop - gt - 2, holeW / 2 + 3, 0, zPlateTop + 2),
              *[cyl(x, y, zPlateTop - gt - 2, zPlateTop + 2, holeD) for x, y in bolts[2:4]])
    flap = box(-guideW / 2, hy - 3, zPlateTop - gt, guideW / 2, hy + reach, zPlateTop)
    Rz = trimesh.transformations.rotation_matrix(-ang, [1, 0, 0], point=[0, hy, zPlateTop - gt]); flap.apply_transform(Rz)
    zt = zPlateTop
    cheek = wedge_x(-guideW / 2, gt, [(hy - 20, zt - gt + 0.5), (hy + reach * np.cos(ang), zt - gt + 0.5), (hy + reach * np.cos(ang), zt - gt - reach * np.sin(ang)), (hy - 20, zt - gt - cheekH)])
    parts["C_guide_flap"] = U(plate, flap, cheek)

    # ---- D backing strips (metal, reference geometry) ----
    strips = []
    for y in (yf, yr):
        s = ex(rrect(2 * bx + 25, 25, 3, 0, y), stackBottom - bkT, stackBottom); strips.append(D(s, *[cyl(x, y, stackBottom - bkT - 2, stackBottom + 2, holeD) for x in (-bx, 0, bx)]))
    for x in (-bx, bx):
        s = ex(rrect(25, 110, 3, x, ym), stackBottom - bkT, stackBottom); strips.append(D(s, cyl(x, ym, stackBottom - bkT - 2, stackBottom + 2, holeD)))
    parts["D_backing_strips_reference"] = trimesh.util.concatenate(strips)

    # ---- T fit-check template (flat 2 mm) ----
    tz0 = -60.0
    tp = ex(rrect(baseW, baseL, baseR, 0, baseCy), tz0, tz0 + 2)
    tt = [ex(rrect(holeW, holeL, holeR), tz0 - 2, tz0 + 4)] + [cyl(x, y, tz0 - 2, tz0 + 4, holeD) for x, y in bolts]
    tt += [box(-1, -(holeL / 2) - 14, tz0 - 2, 1, -(holeL / 2) + 1, tz0 + 4), box(-1, holeL / 2 - 1, tz0 - 2, 1, holeL / 2 + 14, tz0 + 4),
           box(-(holeW / 2) - 14, -1, tz0 - 2, -(holeW / 2) + 1, 1, tz0 + 4), box(holeW / 2 - 1, -1, tz0 - 2, holeW / 2 + 14, 1, tz0 + 4),
           box(-6, bF - 1, tz0 - 2, 6, bF + 8, tz0 + 4), cyl(-50, bR - 10, tz0 - 2, tz0 + 4, 3), cyl(50, bR - 10, tz0 - 2, tz0 + 4, 3)]
    parts["T_fit_check_template"] = D(tp, *tt)
    derived = dict(mouthH=mouthH, mouth_area_cm2=(mouthW * mouthH - (4 - np.pi) * mouthR**2) / 100, throat_area_cm2=(cutW * cutL - (4 - np.pi) * cutR**2) / 100,
                   hood_cut=[holeW, holeL, holeR], stackBottom=stackBottom, bolts=bolts, nut_to_cowl_wall=bx - bodyW / 2)
    return parts, derived

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "stl")); ap.add_argument("--set", action="append", default=[])
    a = ap.parse_args(); P = dict(DEFAULTS)
    for kv in a.set: k, v = kv.split("="); P[k] = float(v)
    os.makedirs(a.out, exist_ok=True)
    parts, derived = build(P)
    for name, m in parts.items():
        m.export(os.path.join(a.out, name + ".stl"))
        print(f"{name:28s} watertight={m.is_watertight!s:5s} extents={np.round(m.extents, 1)}  volume={m.volume/1000:.1f} cm3")
    json.dump({"parameters": P, "derived": {k: (v if not isinstance(v, np.floating) else float(v)) for k, v in derived.items()}}, open(os.path.join(a.out, "parameters_used.json"), "w"), indent=1, default=float)
    print("derived:", {k: (round(float(v), 1) if isinstance(v, (int, float, np.floating)) else v) for k, v in derived.items()})
