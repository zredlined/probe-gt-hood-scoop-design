# Point-cloud check of the mounting plate site

Request for whoever has the raw hood scan (EXStar project). Goal: replace our provisional inner-panel data at the eight bolt sites with real numbers before the plate is bolted on, and confirm the throat cut is clear.

## Frame
Use the delivered scan frame (the one `reference/scan/*.stl` are in): +Y rearward, +Z up, mm. The hood is the closed-position outer skin; the inner panel is the hood underside cloud, which was only provisionally registered (median lateral error about 4 mm, 95th percentile 12 mm). If the raw project lets you register the underside to the outer skin locally around this site (hood front edge, label-patch edges, headlight notches), do that first and report the residual.

Local plate frame: origin O = (110.0, −340.0, 104.2); x = [0.9997, 0, −0.0248]; y = [0.0038, 0.9883, 0.1522]; z (hood normal) = [0.0245, −0.1523, 0.988].

## Positions (scan X, Y; Z is the outer skin there)
| hole | local x,y | scan X, Y, Z |
|---|---|---|
| 1 | −112, −80 | −2.3, −419.1, 94.8 |
| 2 | +112, −80 | 221.7, −419.1, 89.3 |
| 3 | −112, −4 | −2.0, −344.0, 106.4 |
| 4 | +112, −4 | 222.0, −344.0, 100.8 |
| 5 | −112, +72 | −1.7, −268.8, 118.0 |
| 6 | +112, +72 | 222.2, −268.8, 112.4 |
| 7 | 0, −80 | 109.7, −419.1, 92.0 |
| 8 | 0, +72 | 110.3, −268.8, 115.2 |

Throat cut (199 x 75, R12) corners: (10.4, −377.1), (209.3, −377.1), (209.6, −302.9), (10.7, −302.9).
Plate outline corners: (−12.3, −435.9), (231.6, −435.9), (232.3, −257.0), (−11.6, −257.0).
Backing strips on the inner panel: two 25 x 249 strips centred on rows y = −80 and y = +72 (local), spanning x = −124.5 to +124.5; two 25 x 110 strips centred on holes 3 and 4, spanning local y = −59 to +51.

## Deliverables
1. **Depth at each hole**: distance along the hood normal from the outer skin surface to the inner-panel underside, at each of the 8 positions, with a 12 mm radius footprint around each. Report median and spread. Our provisional values were 38, 15, 20, 16, 20, 18, 30, 12 mm for holes 1–8; the design assumes 21.
2. **Flatness under each strip**: along each of the four strip footprints, the inner-panel underside height profile relative to a best-fit plane. Flag any step over 2 mm, rib edge, bead or hole. A strip needs flat metal across its 25 mm width.
3. **Throat region**: confirm the inner panel exists as a flat sheet across the whole 199 x 75 throat footprint, with no rib, bracket or bonded seam crossing it. Report the inner-panel depth across it (we expect about 21 mm, uniform).
4. **Outer skin**: residual of the outer skin against the quadratic `z = −0.000148 x² − 0.000013 xy − 0.000285 y²` in the local frame over the plate outline. Anything over 1.5 mm, and where.
5. **Anything else within 30 mm of the plate outline** on the underside that stands proud of the inner panel: hinge bolts, weld nuts, wiring clips.

## Output
A short table per deliverable and a top-down image of the underside cloud around the site with the eight holes, the four strips and the throat drawn on it. Numbers in mm in the scan frame. If a hole should move, say by how much and in which direction, in the local x/y frame.
