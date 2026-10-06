# Validation report — Probe hood scoop

Site: scan X 110, Y -340, skin Z 104.2 (label-neighbourhood estimate). All clearances come from the scan meshes; the cone is a placeholder; the hood underside registration is PROVISIONAL.

## 1. Flange underside vs outer skin (scan)
- 5723 sampled points on the flange underside. Distance to the scanned skin: min 0.03, median 1.59, p95 3.45, max 6.41 mm. Design gasket gap is 1.5 mm, so a median near 1.5 with p95 under ~3 means the lofted underside tracks the real hood within scan noise.

## 2. Under-hood clearance to the engine-bay scan
| item | min clearance (mm) | where (scan XYZ) |
|---|---|---|
| throat sleeve | 12.2 | [201.0, -372.0, 70.0] |
| guide U-bracket + flap | 11.8 | [214.0, -355.0, 68.0] |
| bolt heads (head-down, under strips) | 10.6 | [218.0, -343.0, 67.0] |
| backing strips | 11.1 | [209.0, -383.0, 68.0] |

Anything under ~15 mm needs a physical check; the scan lacks the cone and may miss hoses/wiring. Hood closing sweep is not simulated.

## 3. Cone placeholder (D150, from scan void + photo; NOT scanned)
- guide U-bracket + flap: min gap 53.6 mm (positive = clear)
- throat sleeve: min gap 103.2 mm (positive = clear)

The brief's starting target is a 25–50 mm outlet-to-filter gap. Set the flap reach/angle after measuring the real cone.

## 4. Inner panel depth below the outer skin at each fastener (PROVISIONAL scan)
| location (local x,y) | depth: skin top → inner-panel underside (mm) | spacer tube = depth − 0.8 skin − 1.6 washer (mm) |
|---|---|---|
| bolt 1 (-112,-80) | 38.5 | 36.1 |
| bolt 2 (+112,-80) | 14.9 | 12.5 |
| bolt 3 (-112,-4) | 20.3 | 17.9 |
| bolt 4 (+112,-4) | 15.7 | 13.3 |
| bolt 5 (-112,+72) | 20.2 | 17.8 |
| bolt 6 (+112,+72) | 18.3 | 15.9 |
| bolt 7 (+0,-80) | 29.8 | 27.4 |
| bolt 8 (+0,+72) | 12.3 | 9.9 |

Design value is 21 mm. The tube passes through a Ø10.5 hole in the inner panel and bears on a washer against the outer skin, so the inner panel is never clamped; cut each tube to its own measured length after the pilot holes. Depths over ~34 mm exceed the M6x50; buy two M6x60 or move that bolt. The front row sits on the rib transition — check it first.

## 5. Flow areas (geometry only, no CFD)
- Mouth clear 186 x 55.5 R4 = **103.1 cm²** (smallest section; brief minimum 100–110, preferred 120–135).
- Throat (sleeve inside) 195 x 71 R10 = 137.6 cm². Hood cut with sleeve = 199 x 75 = 148.0 cm².
- Verdict: above the minimum, below the preferred band. If you want 120 cm² later, raise the roof to 76 (mouth 59.5) — one parameter.

## 6. Print orientation / overhang check (faces steeper than 45° facing down, excluding the bed face)
| part | orientation | overhang area cm² | % of surface | volume cm³ | est. g (ASA, 4 walls, ~40% infill) | bbox in print orientation |
|---|---|---|---|---|---|---|
| A_body.stl | roof-down (flat top on the bed) | 314.6 | 18.1 | 384.0 | 255 | [244.0, 181.0, 75.3] |
| B_bezel.stl | lying on its back (rear face down) | 0.0 | 0.0 | 4.4 | 3 | [196.0, 59.9, 3.0] |
| R_rain_cap.stl | flange face down, plug up | 1.3 | 0.4 | 82.2 | 55 | [196.0, 60.5, 18.0] |
| S_throat_sleeve.stl | standing upright (as modelled) | 0.0 | 0.0 | 31.2 | 21 | [199.0, 75.0, 29.9] |
| C_guide_flap.stl | bracket face down, flap rising at 45° | 136.3 | 30.7 | 62.3 | 41 | [250.0, 121.0, 59.2] |
| T_fit_check_template.stl | flat (as modelled) | 0.0 | 0.0 | 57.6 | 38 | [244.0, 181.0, 2.0] |

Body roof-down: the only overhang is the underside of the 17–20 mm flange ring at 60+ mm height — enable tree supports touching that ring only (paint-on support or a support blocker over the cavity). Everything else prints support-free in the listed orientation.

## 7. Tool and hand access
- Nuts are on top of the flange. Nut centre to cowl wall: sides 14.0 mm, front 15 mm, rear 12 mm. A 3/8"-drive 10 mm socket (Ø17) has 5.5 / 6.5 / 3.5 mm of margin → **OK**. Use a socket or nut driver, not an open-end wrench (no swing room on the cowl side).
- Bolt heads are under the backing strips. With the hood open the underside is fully exposed, so a 4 mm hex key (button head) or 5 mm (cap head) reaches every head; the engine bay only matters with the hood closed.
- Sleeve, guide bracket and strips all go in from below with the hood open; the bezel and rain cap from the front. Nothing has to be reached through the mouth.
