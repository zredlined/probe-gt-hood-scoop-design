"""Figures for the build guide. Usage: python3 cad/make_figures.py stl docs/images"""
import sys, os, json, numpy as np, trimesh, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon, FancyArrowPatch
from PIL import Image, ImageDraw, ImageFont
plt.rcParams['font.family'] = 'DejaVu Sans'
STL, OUT = sys.argv[1].rstrip("/"), sys.argv[2].rstrip("/"); os.makedirs(OUT, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(HERE) + "/reference/"
src = open(os.path.join(HERE, "raster.py")).read(); exec("import numpy as np\n" + src[src.index("def render("):src.index("def scoop_items(")])
PU = json.load(open(STL + "/parameters_used.json")); P = PU["parameters"]; DV = PU["derived"]
fit = json.load(open(os.path.join(HERE, "site_fit.json"))); O = np.array(fit["O_scan_xy_approx"]); cf = fit["outer_quadratic_coef_local"]; zc = fit["z_at_O"]
n = np.array([-cf[1], -cf[2], 1.0]); n /= np.linalg.norm(n); zl = n; xl = np.cross([0, 1, 0], zl); xl /= np.linalg.norm(xl); yl = np.cross(zl, xl); Rm = np.c_[xl, yl, zl]
def to_global(V): return (Rm @ np.asarray(V).T).T + np.array([O[0], O[1], zc])
BLK, PUR, ALU, YEL, HOOD = (0.10, 0.10, 0.11), (0.46, 0.17, 0.58), (0.78, 0.79, 0.81), (0.95, 0.85, 0.2), (0.60, 0.17, 0.42)
parts = {k: trimesh.load(f"{STL}/{k}.stl") for k in ["A_body", "B_bezel", "S_throat_sleeve", "R_rain_cap", "C_guide_flap", "D_backing_strips_reference", "T_fit_check_template"]}
col = {"A_body": BLK, "B_bezel": PUR, "S_throat_sleeve": PUR, "R_rain_cap": PUR, "C_guide_flap": PUR, "D_backing_strips_reference": ALU, "T_fit_check_template": YEL}
def label(img, items, title=None):
    im = Image.fromarray(img); d = ImageDraw.Draw(im)
    try: f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26); ft = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 34)
    except Exception: f = ImageFont.load_default(); ft = f
    for (x, y, txt, tx, ty) in items:
        d.line([(x, y), (tx, ty)], fill=(40, 40, 40), width=2); d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(40, 40, 40))
        d.rectangle([tx - 6, ty - 18, tx + 10 + d.textlength(txt, font=f), ty + 18], fill=(255, 255, 255), outline=(40, 40, 40)); d.text((tx + 2, ty - 15), txt, fill=(20, 20, 20), font=f)
    if title: d.text((20, 16), title, fill=(20, 20, 20), font=ft)
    return im

# 1) exploded view -----------------------------------------------------------------------------------------------
def sh(m, dz=0, dy=0): v = m.vertices.copy(); v[:, 2] += dz; v[:, 1] += dy; return (v, m.faces)
items = [(*sh(parts["A_body"], 0), col["A_body"]), (*sh(parts["B_bezel"], 0, -40), col["B_bezel"]), (*sh(parts["R_rain_cap"], 0, -40), col["R_rain_cap"]),
         (*sh(parts["S_throat_sleeve"], -40), col["S_throat_sleeve"]), (*sh(parts["D_backing_strips_reference"], -70), col["D_backing_strips_reference"]), (*sh(parts["C_guide_flap"], -95), col["C_guide_flap"])]
img = render(items, cam_dir=(0.6, -0.65, 0.45), up=(0, 0, 1), W=1600, H=1000, mmpp=0.33, center=[0, -20, -30])
im = label(img, [(900, 250, "A  body: flange + cowl (black ASA)", 1080, 130), (640, 300, "B  mouth bezel (purple)", 120, 130), (450, 430, "R  rain cap (purple)", 100, 640),
                 (990, 640, "S  throat sleeve (purple)", 1150, 560), (700, 640, "D  4 aluminium strips 25x3", 160, 840), (1160, 820, "C  guide bracket + flap (purple)", 1100, 930)],
           "Exploded view (hood between A and S; strips and guide sit under the hood)")
im.save(f"{OUT}/fig_exploded.png")

# 2) on the car ---------------------------------------------------------------------------------------------------
hood = trimesh.load(R + "scan/02_hood_outer_mm.stl", process=False)
v = hood.vertices; k = (np.abs(v[:, 0] - O[0]) < 330) & (np.abs(v[:, 1] - O[1]) < 300); hf = hood.faces[k[hood.faces].all(1)]
it = [(v, hf, HOOD)] + [(to_global(parts[p].vertices), parts[p].faces, col[p]) for p in ("A_body", "B_bezel")]
img = render(it, cam_dir=(0.55, -0.6, 0.5), up=(0, 0, 1), W=1600, H=900, mmpp=0.42, center=[O[0], O[1], zc])
label(img, [], "On the hood scan — viewed from the front-right of the car").save(f"{OUT}/fig_on_car.png")

# 3) template use + hood cut drawing (local frame) -----------------------------------------------------------------
bolts = DV["bolts"]; hw, hl, hr = DV["hood_cut"]; baseW, bF, bR = P["baseW"], -P["baseFront"], P["baseRear"]
fig, ax = plt.subplots(figsize=(13, 10), dpi=120); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(FancyBboxPatch((-baseW / 2 + 10, bF + 10), baseW - 20, (bR - bF) - 20, boxstyle="round,pad=10", fc="#f3e27a", ec="#333", lw=1.5))
ax.add_patch(FancyBboxPatch((-hw / 2 + hr, -hl / 2 + hr), hw - 2 * hr, hl - 2 * hr, boxstyle=f"round,pad={hr}", fc="white", ec="#333", lw=1.5))
for i, (x, y) in enumerate(bolts):
    ax.add_patch(Circle((x, y), 3.25, fc="white", ec="#333", lw=1.2)); ax.text(x + 7, y + 7, str(i + 1), fontsize=12, weight="bold")
ax.plot([-5, 5], [0, 0], "k-", lw=0.8); ax.plot([0, 0], [-5, 5], "k-", lw=0.8); ax.text(4, -14, "O (centre)", fontsize=10)
ax.add_patch(Polygon([(-6, bF), (6, bF), (0, bF + 8)], fc="#333")); ax.text(0, bF - 54, "FRONT (toward bumper)", ha="center", fontsize=13, weight="bold")
ax.plot([-50, 50], [bR - 10, bR - 10], "k:", lw=1); ax.plot([-50, 50], [bR - 10, bR - 10], "ko", ms=4); ax.text(0, bR + 6, "100 mm between the two small holes — check your print scale", ha="center", fontsize=10)
def dim(x0, y0, x1, y1, t, off=(0, 0)):
    ax.annotate("", (x0, y0), (x1, y1), arrowprops=dict(arrowstyle="<->", lw=1)); ax.text((x0 + x1) / 2 + off[0], (y0 + y1) / 2 + off[1], t, ha="center", va="center", fontsize=11, bbox=dict(fc="white", ec="none", pad=1))
dim(-112, -112, 112, -112, "224 between side holes", (0, -7)); dim(-hw / 2, 52, hw / 2, 52, f"cut {hw} x {hl}, R{hr} corners", (0, 8)); dim(140, -80, 140, -4, "76", (12, 0)); dim(140, -4, 140, 72, "76", (12, 0))
dim(-140, bF, -140, bR, f"{bR - bF}", (-14, 0)); dim(-baseW / 2, bF - 36, baseW / 2, bF - 36, f"{baseW} overall", (0, -7))
ax.text(-baseW / 2, bR + 22, "Template as seen from BELOW the open hood (your right = car's right when facing the car). Holes Ø6.5 are for marking; drill 3 mm pilots first.", fontsize=11)
ax.set_xlim(-175, 180); ax.set_ylim(-162, 130); fig.tight_layout(); fig.savefig(f"{OUT}/fig_template_and_cut.png", facecolor="white"); plt.close()

# 4) bolt stack section (vertical scale x3 for legibility; dimensions in labels are true) ------------------------------
K = 3.0
fig, ax = plt.subplots(figsize=(13, 8), dpi=120); ax.set_aspect("equal"); ax.axis("off")
gk, skin, gap, inner, strip = P["gasketT"], P["skinT"], P["innerGap"], P["innerT"], P["backingT"]
def rect(x0, z0, w, h, **kw): ax.add_patch(Rectangle((x0, z0 * K), w, h * K, **kw))
layers = [("printed flange, 6 mm, steel limiter tube inside", gk, gk + 6, "#222"), ("gasket tape, 2 mm (1.5 compressed)", 0, gk, "#8a8a8a"), ("outer hood skin, ~0.8 mm", -skin, 0, "#c21f2f"),
          ("gap between the skins: spacer tube Ø10 fills it", -skin - gap, -skin, "#f4f4f4"), ("inner panel, ~0.8 mm: Ø10.5 hole, not clamped", -skin - gap - inner, -skin - gap, "#c21f2f"), ("aluminium strip 25 x 3", -skin - gap - inner - strip, -skin - gap - inner, "#bdbdbd")]
for (name, z0, z1, c) in layers: rect(-70, z0, 140, z1 - z0, fc=c, ec="#333", lw=0.8)
ylab = [gk + 4, gk - 2, -5, -skin - gap / 2, -skin - gap - 2, -skin - gap - inner - strip - 4]
for (name, z0, z1, c), yl in zip(layers, ylab):
    ax.annotate(name, xy=(70, (z0 + z1) / 2 * K), xytext=(95, yl * K), fontsize=11, va="center", arrowprops=dict(arrowstyle="-", lw=0.8, color="#555"))
rect(-5, -skin - gap, 10, gap, fc="#999", ec="#333")                                        # spacer tube
rect(-6.25, -skin - 1.6, 12.5, 1.6, fc="#999", ec="#333")                                   # washer under skin
rect(-5, gk, 10, 6, fc="#999", ec="#333")                                                   # limiter
zhead = -skin - gap - inner - strip - 3.3
rect(-3.2, zhead, 6.4, 3.3 + strip + inner + gap + skin + gk + 6 + 1.6 + 6 + 9, fc="#555", ec="#333")   # bolt
rect(-5.25, zhead, 10.5, 3.3, fc="#333", ec="#111")                                         # head
rect(-6, gk + 6, 12, 1.6, fc="#999", ec="#333"); rect(-5, gk + 7.6, 10, 6, fc="#999", ec="#333")   # washer + nut on top
L = [("M6x50 button head, 4 mm hex key. Goes in from BELOW.", zhead + 1.6, -5.25, True), ("washer Ø12 sits against the outer skin", -skin - 0.8, -6.25, False),
     ("washer + M6 nyloc on TOP, 10 mm socket", gk + 10, -5, True), ("about 9 mm of thread sticks out: trim it, or fit an acorn nut", gk + 19, -3.2, False)]
for txt, z, x, bold in L:
    ax.annotate(txt, xy=(x, z * K), xytext=(-90, z * K), fontsize=11, ha="right", va="center", weight="bold" if bold else "normal", arrowprops=dict(arrowstyle="-", lw=0.8, color="#555"))
ax.annotate("", (-78, 0), (-78, (-skin - gap - inner) * K), arrowprops=dict(arrowstyle="<->", lw=1.2))
ax.text(-82, (-skin - gap - inner) / 2 * K, "MEASURE this at each\npilot hole (Round 1)", fontsize=11, va="center", ha="right", weight="bold")
ax.set_xlim(-330, 330); ax.set_ylim((zhead - 4) * K, (gk + 24) * K); ax.set_title("One of the eight bolts, section through the hood (not to scale vertically)", fontsize=14, loc="left")
fig.tight_layout(); fig.savefig(f"{OUT}/fig_bolt_stack.png", facecolor="white"); plt.close()

# 5) print orientations ---------------------------------------------------------------------------------------------
def Rx(deg):
    t = np.radians(deg); return np.array([[1, 0, 0], [0, np.cos(t), -np.sin(t)], [0, np.sin(t), np.cos(t)]])
orient = [("A_body", "A body — roof DOWN (supports under flange only)", Rx(180)), ("B_bezel", "B bezel — lying on its back", Rx(-90)), ("S_throat_sleeve", "S sleeve — standing", np.eye(3)),
          ("R_rain_cap", "R rain cap — flange down, plug up", Rx(90)), ("C_guide_flap", "C guide — bracket down, flap rising 45°", Rx(180)), ("T_fit_check_template", "T template — flat (PLA)", np.eye(3))]
tiles = []
for k, title, Rot in orient:
    m = parts[k]; V = (Rot @ m.vertices.T).T; V[:, 2] -= V[:, 2].min(); c = V.mean(0); c[2] = V[:, 2].max() / 2
    bed = (np.array([[-140, -110, -0.5], [140, -110, -0.5], [140, 110, -0.5], [-140, 110, -0.5]]) + np.array([c[0], c[1], 0]), np.array([[0, 1, 2], [0, 2, 3]]), (0.85, 0.85, 0.88))
    img = render([bed, (V, m.faces, col[k])], cam_dir=(0.5, -0.7, 0.5), up=(0, 0, 1), W=800, H=520, mmpp=0.45, center=c)
    tiles.append(np.array(label(img, [], title)))
grid = np.vstack([np.hstack(tiles[0:3]), np.hstack(tiles[3:6])]); Image.fromarray(grid).save(f"{OUT}/fig_print_orientation.png")

# 6) tool access plan --------------------------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 8), dpi=120); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(FancyBboxPatch((-baseW / 2 + 10, bF + 10), baseW - 20, (bR - bF) - 20, boxstyle="round,pad=10", fc="#333", ec="#111"))
yF, yR, bodyW = -P["bodyFront"], P["bodyRear"], P["bodyW"]
ax.add_patch(FancyBboxPatch((-bodyW / 2 + 4, yF + 4), bodyW - 8, (yR - yF) - 8, boxstyle="round,pad=4", fc="#111", ec="#000"))
for i, (x, y) in enumerate(bolts):
    ax.add_patch(Circle((x, y), 8.5, fc="#5ad17a", ec="#1b7f3a", alpha=0.55)); ax.add_patch(Circle((x, y), 5, fc="#bbb", ec="#333"))
ax.text(0, (yF + yR) / 2, "cowl", color="white", ha="center", fontsize=14)
ax.annotate("", (bodyW / 2, 30), (P["boltX"], 30), arrowprops=dict(arrowstyle="<->", color="w")); ax.text((bodyW / 2 + P["boltX"]) / 2, 36, f"{P['boltX'] - bodyW / 2:.0f} mm", color="w", ha="center", fontsize=11)
ax.text(-baseW / 2, bR + 34, "Green = Ø17 socket footprint (3/8\"-drive 10 mm socket). All eight clear the cowl.", fontsize=11); ax.text(-baseW / 2, bR + 20, "Use a socket or nut driver on top; an open-end wrench has no swing room next to the cowl.", fontsize=11)
ax.set_xlim(-135, 135); ax.set_ylim(-125, 130); fig.tight_layout(); fig.savefig(f"{OUT}/fig_tool_access.png", facecolor="white"); plt.close()

# 7) location photos ---------------------------------------------------------------------------------------------------
a = Image.open(R + "photos/01_user_marked_hood_underside.png").convert("RGB"); b = Image.open(R + "photos/02_engine_bay_with_cone_filter.png").convert("RGB")
a = a.resize((1200, int(a.height * 1200 / a.width))); b = b.resize((1200, int(b.height * 1200 / b.width)))
try: FL = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
except Exception: FL = ImageFont.load_default()
da = ImageDraw.Draw(a); da.rectangle([(540, 150), (740, 230)], outline=(255, 255, 0), width=5)
da.rectangle([(0, a.height - 90), (1200, a.height)], fill=(0, 0, 0)); da.text((20, a.height - 82), "Scoop goes here (yellow). Hood underside seen from the front of the car;", fill=(255, 255, 0), font=FL); da.text((20, a.height - 46), "the small white box is the spot that was tested with the vacuum nozzle.", fill=(255, 255, 0), font=FL)
db = ImageDraw.Draw(b); db.rectangle([(655, 275), (775, 440)], outline=(255, 60, 60), width=5)
db.rectangle([(0, b.height - 50), (1200, b.height)], fill=(0, 0, 0)); db.text((20, b.height - 42), "Cone filter (red box). The guide flap under the scoop aims air at it.", fill=(255, 90, 90), font=FL)
canvas = Image.new("RGB", (1200, a.height + b.height + 10), (255, 255, 255)); canvas.paste(a, (0, 0)); canvas.paste(b, (0, a.height + 10)); canvas.save(f"{OUT}/fig_location.png")
print("figures written to", OUT)
