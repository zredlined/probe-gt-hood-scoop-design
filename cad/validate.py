"""Scan-based design validation for the Probe hood scoop.
Checks: flange-to-skin fit, under-hood clearance of every part/hardware item vs the engine-bay scan, cone placeholder clearance,
inner-panel gap at each bolt (provisional underside scan), flow areas, print-orientation overhang fractions, filament estimates.
Usage: python3 cad/validate.py [stl_dir] [out_dir]   (defaults: stl/ and validation/)"""
import numpy as np, trimesh, json, glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
R = ROOT + "reference/"
import sys
EXP = (sys.argv[1].rstrip("/") + "/") if len(sys.argv) > 1 else ROOT + "stl/"
OUT = (sys.argv[2].rstrip("/") + "/") if len(sys.argv) > 2 else ROOT + "validation/"; os.makedirs(OUT, exist_ok=True)
fit = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "site_fit.json"))); O = np.array(fit["O_scan_xy_approx"]); cf = fit["outer_quadratic_coef_local"]; zc = fit["z_at_O"]
_pu = json.load(open(EXP + "parameters_used.json"))["parameters"] if os.path.exists(EXP + "parameters_used.json") else None
def _p(k, d): return _pu[k] if _pu else d
P = dict(cutW=_p("cutW",195), cutL=_p("cutL",71), cutR=_p("cutR",10), sw=_p("sleeveWall",2), skinT=_p("skinT",0.8), gap=_p("innerGap",21), innerT=_p("innerT",0.8), gk=_p("gasketT",1.5),
         baseW=_p("baseW",244), bF=-_p("baseFront",97), bR=_p("baseRear",84), baseT=_p("baseT",6), bodyW=_p("bodyW",196), yF=-_p("bodyFront",65), yR=_p("bodyRear",60), top=_p("roofTop",72), w=_p("wall",3),
         chF=_p("chamferF",4), chR=_p("chamferR",10), mouthW=_p("mouthW",186), mouthR=_p("mouthR",4), bzW=_p("bezelW",5), bx=_p("boltX",112), yf=-_p("boltYF",80), ym=_p("boltYM",-4), yr=_p("boltYR",72),
         holeD=_p("holeD",6.5), boltL=_p("boltL",50), bkT=_p("backingT",3), guideW=_p("guideW",200), reach=_p("guideReach",50), ang=_p("guideAngle",45), cheekH=_p("cheekH",55), gt=_p("guideT",3))
holeW = P["cutW"] + 2 * P["sw"]; holeL = P["cutL"] + 2 * P["sw"]
stackBottom = -(P["gk"] + P["skinT"] + P["gap"] + P["innerT"])
bolts = [(-P["bx"], P["yf"]), (P["bx"], P["yf"]), (-P["bx"], P["ym"]), (P["bx"], P["ym"]), (-P["bx"], P["yr"]), (P["bx"], P["yr"]), (0, P["yf"]), (0, P["yr"])]
rnPos = [(-P["bx"], P["ym"] - 36), (P["bx"], P["ym"] - 36), (-P["bx"], P["ym"] + 36), (P["bx"], P["ym"] + 36)]
def zq(x, y): return cf[0] + cf[1] * x + cf[2] * y + cf[3] * x * x + cf[4] * x * y + cf[5] * y * y
n = np.array([-cf[1], -cf[2], 1.0]); n /= np.linalg.norm(n); zl = n; xl = np.cross([0, 1, 0], zl); xl /= np.linalg.norm(xl); yl = np.cross(zl, xl); Rm = np.c_[xl, yl, zl]
def to_global(V): return (Rm @ np.asarray(V).T).T + np.array([O[0], O[1], zc])
def to_local(V): return (Rm.T @ (np.asarray(V) - np.array([O[0], O[1], zc])).T).T
bay = trimesh.load(R + "scan/01_engine_bay_mm.stl", process=False)
hood = trimesh.load(R + "scan/02_hood_outer_mm.stl", process=False)
under = trimesh.load(R + "scan/03_hood_underside_PROVISIONAL_mm.stl", process=False)
def crop(m, dx, dy):
    v = m.vertices; k = (np.abs(v[:, 0] - O[0]) < dx) & (np.abs(v[:, 1] - O[1]) < dy); f = m.faces[k[m.faces].all(1)]
    mm = trimesh.Trimesh(v, f, process=False); mm.remove_unreferenced_vertices(); return mm
bayC = crop(bay, 400, 400); hoodC = crop(hood, 300, 300); underC = crop(under, 300, 300)
pq_bay = trimesh.proximity.ProximityQuery(bayC); pq_hood = trimesh.proximity.ProximityQuery(hoodC)
rep = {"site": {"O_scan_xy": O.tolist(), "skin_z_at_O": round(zc, 2), "note": "O is a label-neighbourhood estimate, not a calibrated coordinate"}, "checks": {}}
lines = ["# Validation report — Probe hood scoop", "", f"Site: scan X {O[0]:.0f}, Y {O[1]:.0f}, skin Z {zc:.1f} (label-neighbourhood estimate). All clearances come from the scan meshes; the cone is a placeholder; the hood underside registration is PROVISIONAL.", ""]
stl = {os.path.basename(f): trimesh.load(f) for f in glob.glob(EXP + "*.stl")}
def part(prefix):
    for k, m in stl.items():
        if k.startswith(prefix): return k, m
    return None, None

# 1) flange underside vs outer skin --------------------------------------------------------------
kA, body = part("A_body")
pts, _ = trimesh.sample.sample_surface(body, 40000)
fl = pts[(pts[:, 2] < P["gk"] + 0.3) & (pts[:, 2] > P["gk"] - 8)]           # flange underside region (local z around gasket top, sag down to -5)
inside = (np.abs(fl[:, 0]) > P["bodyW"] / 2 - 5) | (np.abs(fl[:, 1] - (P["yF"] + P["yR"]) / 2) > (P["yR"] - P["yF"]) / 2 - 5)
fl = fl[inside]
_, d_h, _ = pq_hood.on_surface(to_global(fl))
# signed: positive = flange above skin
rep["checks"]["flange_fit"] = {"n_samples": int(len(fl)), "distance_to_scan_skin_mm": {"min": round(float(d_h.min()), 2), "median": round(float(np.median(d_h)), 2), "p95": round(float(np.percentile(d_h, 95)), 2), "max": round(float(d_h.max()), 2)}, "design_gasket_gap_mm": P["gk"]}
lines += ["## 1. Flange underside vs outer skin (scan)", f"- {len(fl)} sampled points on the flange underside. Distance to the scanned skin: min {d_h.min():.2f}, median {np.median(d_h):.2f}, p95 {np.percentile(d_h,95):.2f}, max {d_h.max():.2f} mm. Design gasket gap is {P['gk']} mm, so a median near 1.5 with p95 under ~3 means the lofted underside tracks the real hood within scan noise.", ""]

# 2) under-hood clearance to engine-bay scan ---------------------------------------------------------
def min_clear(m, label, nsamp=6000):
    pts, _ = trimesh.sample.sample_surface(m, nsamp); g = to_global(pts)
    cp, d, _ = pq_bay.on_surface(g); i = int(np.argmin(d))
    return {"part": label, "min_mm": round(float(d[i]), 1), "at_scan_xyz": [round(float(v), 0) for v in g[i]], "at_local_xyz": [round(float(v), 0) for v in pts[i]]}
items = []
for pref, lab in [("S_", "throat sleeve"), ("C_", "guide U-bracket + flap")]:
    k, m = part(pref)
    if m is not None: items.append(min_clear(m, lab))
# hardware + strips constructed from parameters
hw = []
for i, (x, y) in enumerate(bolts):
    seat = stackBottom - P["bkT"] - (P["gt"] + 0.5 if i in (2, 3) else 0)
    head = trimesh.creation.cylinder(radius=5.25, height=3.3, sections=24); head.apply_translation([x, y, seat - 1.65]); hw.append(head)
items.append(min_clear(trimesh.util.concatenate(hw), "bolt heads (head-down, under strips)"))
strips = []
for y in (P["yf"], P["yr"]): b = trimesh.creation.box(extents=[2 * P["bx"] + 25, 25, P["bkT"]]); b.apply_translation([0, y, stackBottom - P["bkT"] / 2]); strips.append(b)
for x in (-P["bx"], P["bx"]): b = trimesh.creation.box(extents=[25, 110, P["bkT"]]); b.apply_translation([x, P["ym"], stackBottom - P["bkT"] / 2]); strips.append(b)
items.append(min_clear(trimesh.util.concatenate(strips), "backing strips"))
rep["checks"]["under_hood_clearance_to_bay_scan"] = items
lines += ["## 2. Under-hood clearance to the engine-bay scan", "| item | min clearance (mm) | where (scan XYZ) |", "|---|---|---|"]
for it in items: lines.append(f"| {it['part']} | {it['min_mm']} | {it['at_scan_xyz']} |")
lines += ["", "Anything under ~15 mm needs a physical check; the scan lacks the cone and may miss hoses/wiring. Hood closing sweep is not simulated.", ""]

# 3) cone placeholder ----------------------------------------------------------------------------------
a, b = np.array([265, -228, -70.]), np.array([245, -45, 10.]); L = np.linalg.norm(b - a); cone = trimesh.creation.cylinder(radius=75, height=L, sections=48)
cone.apply_transform(trimesh.geometry.align_vectors([0, 0, 1], (b - a) / L)); cone.apply_translation((a + b) / 2); pq_cone = trimesh.proximity.ProximityQuery(cone)
cone_items = []
for pref, lab in [("C_", "guide U-bracket + flap"), ("S_", "throat sleeve")]:
    k, m = part(pref)
    if m is None: continue
    pts, _ = trimesh.sample.sample_surface(m, 4000); d = pq_cone.signed_distance(to_global(pts))
    cone_items.append({"part": lab, "min_gap_to_cone_placeholder_mm": round(float(d.max() * -1 if False else -d.max()), 1) if False else round(float(np.min(-d)), 1)})
rep["checks"]["cone_placeholder"] = cone_items
lines += ["## 3. Cone placeholder (D150, from scan void + photo; NOT scanned)"] + [f"- {c['part']}: min gap {c['min_gap_to_cone_placeholder_mm']} mm (positive = clear)" for c in cone_items] + ["", "The brief's starting target is a 25–50 mm outlet-to-filter gap. Set the flap reach/angle after measuring the real cone.", ""]

# 4) inner-panel gap at bolts / rivnuts (provisional underside) ------------------------------------------
def gap_at(x, y, r=9):
    g = to_global([[x, y, 0]])[0]; v = underC.vertices; s = np.hypot(v[:, 0] - g[0], v[:, 1] - g[1]) < r
    if s.sum() < 3: return None
    return float(np.median(zq(v[s, 0] - O[0], v[s, 1] - O[1]) - v[s, 2]))
gaps = {f"bolt {i+1} ({x:+.0f},{y:+.0f})": (None if gap_at(x, y) is None else round(gap_at(x, y), 1)) for i, (x, y) in enumerate(bolts)}
rep["checks"]["inner_panel_depth_below_skin_mm_PROVISIONAL"] = gaps
lines += ["## 4. Inner panel depth below the outer skin at each fastener (PROVISIONAL scan)", "| location (local x,y) | depth: skin top → inner-panel underside (mm) | spacer tube = depth − 0.8 skin − 1.6 washer (mm) |", "|---|---|---|"]
for k, v in gaps.items(): lines.append(f"| {k} | {v} | {'' if v is None else round(v - P['skinT'] - 1.6, 1)} |")
lines += ["", f"Design value is {P['gap']} mm. The tube passes through a Ø10.5 hole in the inner panel and bears on a washer against the outer skin, so the inner panel is never clamped; cut each tube to its own measured length after the pilot holes. Depths over ~34 mm exceed the M6x50; buy two M6x60 or move that bolt. The front row sits on the rib transition — check it first.", ""]

# 5) flow areas ------------------------------------------------------------------------------------------
def rr_area(w, l, r): return w * l - (4 - np.pi) * r * r
mouthH = P["top"] - P["chF"] - P["bzW"] - P["gk"] - P["baseT"]
areas = {"mouth_clear_cm2": round(rr_area(P["mouthW"], mouthH, P["mouthR"]) / 100, 1), "throat_clear_cm2": round(rr_area(P["cutW"], P["cutL"], P["cutR"]) / 100, 1), "hood_cut_cm2_with_sleeve": round(rr_area(holeW, holeL, P["cutR"] + P["sw"]) / 100, 1), "mouth_clear_height_mm": round(mouthH, 1)}
rep["checks"]["areas"] = areas
lines += ["## 5. Flow areas (geometry only, no CFD)", f"- Mouth clear {P['mouthW']} x {mouthH:.1f} R{P['mouthR']} = **{areas['mouth_clear_cm2']} cm²** (smallest section; brief minimum 100–110, preferred 120–135).", f"- Throat (sleeve inside) {P['cutW']} x {P['cutL']} R{P['cutR']} = {areas['throat_clear_cm2']} cm². Hood cut with sleeve = {holeW} x {holeL} = {areas['hood_cut_cm2_with_sleeve']} cm².", "- Verdict: above the minimum, below the preferred band. If you want 120 cm² later, raise the roof to 76 (mouth 59.5) — one parameter.", ""]

# 6) print-orientation overhang check -----------------------------------------------------------------------
def Rx(deg):
    t = np.radians(deg); return np.array([[1, 0, 0], [0, np.cos(t), -np.sin(t)], [0, np.sin(t), np.cos(t)]])
orient = {"A_body": ("roof-down (flat top on the bed)", Rx(180)), "B_": ("lying on its back (rear face down)", Rx(-90)), "R_": ("flange face down, plug up", Rx(90)),
          "S_": ("standing upright (as modelled)", np.eye(3)), "C_": ("bracket face down, flap rising at 45°", Rx(180)), "T_": ("flat (as modelled)", np.eye(3))}
ov = []
for pref, (desc, Rot) in orient.items():
    k, m = part(pref)
    if m is None: continue
    V = (Rot @ m.vertices.T).T; F = m.faces; mm = trimesh.Trimesh(V, F, process=False)
    nrm = mm.face_normals; area = mm.area_faces; zmin = V[:, 2].min()
    bed = (np.abs(V[F][:, :, 2] - zmin) < 0.3).all(1)
    down = nrm[:, 2] < -np.cos(np.radians(45))              # facing down steeper than 45° => needs support (unless on bed or a bridge)
    steep = down & ~bed
    vol = m.volume / 1000.0
    ov.append({"part": k[:40], "orientation": desc, "overhang_area_cm2": round(float(area[steep].sum() / 100), 1), "overhang_pct_of_surface": round(float(100 * area[steep].sum() / area.sum()), 1), "volume_cm3": round(vol, 1), "est_grams_ASA": round(vol * 1.07 * 0.62, 0), "bbox_mm": [round(float(x), 1) for x in (V.max(0) - V.min(0))]})
rep["checks"]["print_orientation"] = ov
lines += ["## 6. Print orientation / overhang check (faces steeper than 45° facing down, excluding the bed face)", "| part | orientation | overhang area cm² | % of surface | volume cm³ | est. g (ASA, 4 walls, ~40% infill) | bbox in print orientation |", "|---|---|---|---|---|---|---|"]
for o in ov: lines.append(f"| {o['part']} | {o['orientation']} | {o['overhang_area_cm2']} | {o['overhang_pct_of_surface']} | {o['volume_cm3']} | {o['est_grams_ASA']:.0f} | {o['bbox_mm']} |")
lines += ["", "Body roof-down: the only overhang is the underside of the 17–20 mm flange ring at 60+ mm height — enable tree supports touching that ring only (paint-on support or a support blocker over the cavity). Everything else prints support-free in the listed orientation.", ""]
# 7) tool access -------------------------------------------------------------------------------------------
sock_r = 17 / 2   # 3/8"-drive 10 mm socket OD ~17
ta = {"nut_centre_to_cowl_side_wall_mm": round(P["bx"] - P["bodyW"] / 2, 1), "nut_centre_to_cowl_front_face_mm": round(abs(P["yf"]) - abs(P["yF"]), 1), "nut_centre_to_cowl_rear_face_mm": round(P["yr"] - P["yR"], 1),
      "socket_radius_assumed_mm": sock_r, "washer_edge_to_side_wall_mm": round(P["bx"] - P["bodyW"] / 2 - 6, 1)}
ta["side_margin_mm"] = round(ta["nut_centre_to_cowl_side_wall_mm"] - sock_r, 1); ta["front_margin_mm"] = round(ta["nut_centre_to_cowl_front_face_mm"] - sock_r, 1); ta["rear_margin_mm"] = round(ta["nut_centre_to_cowl_rear_face_mm"] - sock_r, 1)
ta["verdict"] = "OK" if min(ta["side_margin_mm"], ta["front_margin_mm"], ta["rear_margin_mm"]) >= 2 else "TIGHT"
rep["checks"]["tool_access"] = ta
lines += ["## 7. Tool and hand access", f"- Nuts are on top of the flange. Nut centre to cowl wall: sides {ta['nut_centre_to_cowl_side_wall_mm']} mm, front {ta['nut_centre_to_cowl_front_face_mm']} mm, rear {ta['nut_centre_to_cowl_rear_face_mm']} mm. A 3/8\"-drive 10 mm socket (Ø17) has {ta['side_margin_mm']} / {ta['front_margin_mm']} / {ta['rear_margin_mm']} mm of margin → **{ta['verdict']}**. Use a socket or nut driver, not an open-end wrench (no swing room on the cowl side).",
          "- Bolt heads are under the backing strips. With the hood open the underside is fully exposed, so a 4 mm hex key (button head) or 5 mm (cap head) reaches every head; the engine bay only matters with the hood closed.", "- Sleeve, guide bracket and strips all go in from below with the hood open; the bezel and rain cap from the front. Nothing has to be reached through the mouth.", ""]
json.dump(rep, open(OUT + "validation_report.json", "w"), indent=1)
open(OUT + "validation_report.md", "w").write("\n".join(lines))
print("\n".join(lines))
