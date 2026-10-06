# Bill of materials

Depths marked **measure** are confirmed in Round 1 of the build guide before anything is cut to length.

## Printed parts

| Part | File | Material | Orientation | Supports | Walls / infill | Filament |
|---|---|---|---|---|---|---|
| T  template | `stl/T_fit_check_template.stl` | PLA | flat | none | 2 / 15 % | ~40 g |
| A  body | `stl/A_body.stl` | ASA, black | roof down | tree supports under the flange ring only | 4 / 40 % gyroid | ~255 g |
| B  bezel | `stl/B_bezel.stl` | ASA, purple | on its back | none | 3 / 100 % | ~3 g |
| S  throat sleeve | `stl/S_throat_sleeve.stl` | ASA, purple | standing | none | 3 / any | ~21 g |
| R  rain cap | `stl/R_rain_cap.stl` | ASA, purple | flange down | none | 3 / 20 % | ~55 g |
| C  guide | `stl/C_guide_flap.stl` | ASA, purple | bracket down | none (45° flap) | 4 / 30 % | ~41 g |

Totals: black ASA about 260 g, purple ASA about 120 g, PLA about 40 g. Estimates, allow 25 %.

The body is 244 x 181 x 75 mm and fits the P1S bed with 6 mm to spare each side. Use a 5 mm brim. Pausing at layer 3 and swapping to purple turns the 0.6 mm logo deboss into an inlay.

### Why these materials
- **ASA** for every part on or under the hood. The hood skin reaches 70 to 90 °C in sun with a hot engine. ASA stays stiff to about 95 °C and does not chalk in UV. Print with the door closed, nozzle 260 to 270 °C, bed 90 to 100 °C, aux fan off, part fan low, dry filament, glue stick on the textured plate.
- **PLA** for the template only. It softens above about 55 °C.
- **PETG** is not recommended for anything on the hood; it softens around 75 to 80 °C. Fine for a throwaway first-fit guide.
- If the guide ever droops after a hot run, print it again in PC or PA-CF from the same file.

## Hardware

| Item | Qty | Spec | Notes |
|---|---|---|---|
| M6 x 50 button head (ISO 7380) | 8 | 8.8 or stainless | On hand. Button heads keep the most clearance under the hood; socket caps also work. |
| M6 nyloc nut | 8 | DIN 985 | On top of the flange. |
| M6 flat washer Ø12 | 16 | DIN 125 | 8 under the nuts, 8 between spacer tube and outer skin. |
| Aluminium flat bar 25 x 3 mm | 1 m | 6061 or 6082 | 2 x 249 mm with three Ø6.5 holes, 2 x 110 mm with one hole. |
| Tube Ø10 outside, 1.5 wall | 1 m | aluminium or steel | 8 limiters at 6.0 mm, 8 spacers at the **measured** depth minus 2.4 mm. |
| Closed-cell foam tape 2 mm x 20 to 25 mm | 1.5 m | EPDM or neoprene, adhesive backed | Gasket loop under the flange and around the throat. |
| RTV silicone or seam sealer | 1 tube | black | Sleeve to inner panel. |
| CA glue | 1 | medium | Bezel. |
| Rust primer or touch-up paint | 1 | | Cut edges and holes. |
| M6 acorn nut | 8 | DIN 1587 | Optional. Covers the thread above the nyloc; otherwise trim the bolts. |

New purchases: the flat bar, the tube, the foam tape and nylocs if there are none in the bin.

## Tools
Drills 3, 6.5 and 10.5 mm (or a step drill), Ø24 hole saw or step drill for the corners, jigsaw with a fine metal blade or a nibbler, files, deburring tool, hacksaw or cut-off wheel, depth gauge or hooked wire plus ruler, masking tape, torque wrench to 6 N·m, 10 mm socket, 4 mm hex key.

## Bolt stack
Head below the strip, nut on top. From the bottom: button head 3.3 → strip 3 → spacer tube (measured, inside a Ø10.5 hole in the inner panel) → washer 1.6 → outer skin 0.8 → gasket 1.5 compressed → flange 6 with a steel limiter tube inside → washer 1.6 → nyloc 6. At the scan's 21 mm gap that is 40.7 mm head-to-nut, leaving about 9 mm of M6x50 above the nut. If a measured depth exceeds about 34 mm, that hole needs an M6x60.
