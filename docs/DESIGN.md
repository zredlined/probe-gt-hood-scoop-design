# Design notes

## Intent
A supplemental fresh-air feed, not a sealed cold-air intake. The mouth faces forward on the hood's downslope, 74 mm up, well clear of the boundary layer. It captures far more air than the engine draws, so most of it spills into the bay and keeps the area around the cone filter slightly pressurised with outside air. A sealed airbox can bolt to the same opening and hole pattern later; the throat and bolt pattern were sized for that.

## Coordinate frame
Everything in the STLs is in a local frame on the hood at the opening centre O:
- **x** across the car, positive toward your right when standing at the bumper facing the car,
- **y** rearward toward the windshield,
- **z** out of the hood, zero at the outer skin surface at O. The plate underside follows the measured hood curvature (a quadratic fitted to the scan: 8.8° downslope toward the front, about 5 mm of sag at the plate corners).

In the scan's frame O is at about X 110, Y −340, Z 104. That came from the emissions-label neighbourhood the owner tested with a vacuum nozzle, not from a measurement, which is why the template exists.

## Parts and how they go together
![Exploded](images/fig_exploded.png)

- **A1 flange plate**: 244 x 181 x 8, hood-matched underside, flat top. Eight Ø6.5 bolt holes with 0.6 mm debossed rings, a 1.5 mm seat for the sleeve, a 3 x 1.5 mm groove for the cowl tongue, six Ø4.3 countersunk holes for the cowl screws. Prints top-face-down with no supports.
- **A2 cowl**: 196 x 125 slab, roof at 74, mouth face raked back 20°, 4 mm brow chamfer, 10 mm tail chamfer, 4 mm corner radii. Mouth 186 x 55.5 (103 cm²) with a 2.5 mm inner lip radius. A 2.6 mm tongue on the skirt drops into the plate groove; six Ø10 bosses inside the skirt take M4 self-tapping screws (or captive M4 nylocs with `captiveNuts`). 4OGS wordmark debossed 0.6 mm on the roof for an AMS inlay. Prints roof-down with no supports.
- **S throat sleeve**: 199 x 75 outside, 2 mm wall, lines the cut through both skins so the cavity stays dry and the edges are hidden. Pushed up from below into the plate seat, sealed with RTV.
- **R rain cap**: flange matching the raked face, hollow 15 mm plug with 0.3 mm clearance, two 0.6 mm snap bumps, finger notch that doubles as a drain.
- **C guide**: U-bracket (two arms plus a rear bar) clamped under the side strips by the two middle bolts, with a 200 wide flap at 45° reaching 50 mm and a 55 mm inboard cheek that pushes air outboard toward the cone. Provisional until the clay test; reach, angle and cheek are parameters.
- **B bezel (optional)**: 5 mm purple frame flush in a recess on the raked face. Off by default; the AMS logo is the accent instead.
- **D strips**: four pieces of 25 x 3 aluminium flat bar under the inner panel. Two across (front and rear rows, 3 holes) and two short (middle bolts).
- **Fasteners**: 8 x M6x50 head-down, steel limiter tubes through the plate, steel spacer tubes across the inter-skin gap passing through Ø10.5 holes in the inner panel. The clamp path is head → strip → tube → outer skin → gasket → plate → nut, so no plastic carries preload and the inner panel is not pulled toward the outer skin. 6 x M4 join the cowl to the plate on the bench.

## Parameters
All in the Onshape feature and in `cad/local_build.py` (same names, mm).

| Group | Parameter | Default | Meaning |
|---|---|---|---|
| Opening | cutW, cutL, cutR | 195, 71, 10 | clear throat; hood cut = this + 2 x sleeveWall |
| | sleeveWall | 2 | |
| Hood stack | skinT, innerGap, innerT, gasketT | 0.8, 21, 0.8, 1.5 | **measure** innerGap at the pilot holes |
| Plate | baseW, baseFront, baseRear, baseR, baseT | 244, 97, 84, 10, 8 | |
| Cowl | bodyW, bodyFront, bodyRear, roofTop, wall, bodyR | 196, 65, 60, 74, 3, 4 | |
| | chamferF, chamferR, rakeDeg | 4, 10, 20 | |
| Mouth | mouthW, mouthR, lipR, bezelW | 186, 4, 2.5, 5 | mouth height = roofTop − chamferF − bezelW − gasketT − baseT (bezelW is the lintel band whether or not the bezel is built) |
| Cowl screws | bossD, bossH, screwPilot, screwClear, captiveNuts, nutAF, nutH | 10, 9, 3.4, 4.3, off, 7.2, 5.2 | six bosses at x ±91 y ±45 and x ±50 y 53 |
| Bolts | boltX, boltYF, boltYM, boltYR | 112, 80, −4, 72 | rows at y = −80, −4, +72; x = ±112 plus centre front/rear |
| | holeD, boltL, backingT | 6.5, 50, 3 | |
| Guide | guideW, guideReach, guideAngle, cheekH, guideT | 200, 50, 45, 55, 3 | physical-fit parameters |

## Design language
Teenage Engineering slab with a 90s scoop stance: flat top, crisp small chamfers, uniform radii, a raked mouth, exposed fasteners on a regular pitch, black body with a purple inlaid wordmark and purple functional parts. The car's livery is light blue and black with purple panels, hence purple.

## What is not proven
No CFD, no load test, no hood-closing sweep simulation. The scan's hood-underside registration is provisional (median 4 mm lateral, local conflicts) and the cone is not in the scan. The build guide's Round 1 exists to replace those assumptions with measurements. See [DECISIONS.md](DECISIONS.md) for why things are the way they are.
