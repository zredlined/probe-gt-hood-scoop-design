# Bill of materials

Depths marked **measure** are confirmed in Round 1 of the build guide before anything is cut to length.

## Printed parts

| Part | File | Material | Orientation | Supports | Walls / infill | Filament |
|---|---|---|---|---|---|---|
| T  template | `stl/T_fit_check_template.stl` | PLA | flat | none | 2 / 15 % | ~40 g |
| A1 flange plate | `stl/A1_flange_plate.stl` | ASA, black | top face down (curved side up) | none | 4 / 15 % | ~150 g |
| A2 cowl | `stl/A2_cowl.stl` | ASA, black (+ purple for the logo, see below) | roof down | none | 4 / 30 % | ~95 g |
| S  throat sleeve | `stl/S_throat_sleeve.stl` | ASA, purple | standing | none | 3 / any | ~21 g |
| R  rain cap | `stl/R_rain_cap.stl` | ASA, purple | flange down, plug up | none | 3 / 20 % | ~55 g |
| C  guide | `stl/C_guide_flap.stl` | ASA, purple | bracket down | none (45° flap) | 4 / 30 % | ~41 g |
| B  bezel (optional) | build with `--set buildBezel=1` | ASA, purple | on its back | none | 3 / 100 % | ~3 g |

Totals: black ASA about 245 g, purple ASA about 120 g, PLA about 40 g. Estimates, allow 25 %. Nothing needs supports.

**Logo inlay with the AMS:** the cowl prints roof-down, so the 0.6 mm 4OGS deboss is in layers 1–3. Assign those layers (or a modifier on the deboss) to purple. Three swaps total. Do not multi-colour anything taller; a full-height purple bezel would purge more filament than the whole part weighs.

### Why these materials
- **ASA** for every part on or under the hood. The skin reaches 70–90 °C in sun with a hot engine; ASA stays stiff to about 95 °C and does not chalk in UV. Door closed, nozzle 260–270 °C, bed 90–100 °C, aux fan off, part fan low, dry filament, glue stick on the textured plate, 5 mm brim on the plate.
- **PLA** for the template only (softens above ~55 °C).
- **PETG** is not recommended on the hood (softens 75–80 °C). Fine for a throwaway first-fit guide.
- If the guide droops after a hot run, print it again in PC or PA-CF from the same file.

## Hardware

| Item | Qty | Spec | Notes |
|---|---|---|---|
| M6 x 50 button head (ISO 7380) | 8 | 8.8 or stainless | On hand. Head goes under the strip, nyloc on top. |
| M6 nyloc nut | 8 | DIN 985 | On top of the plate. |
| M6 flat washer Ø12 | 16 | DIN 125 | 8 under the nuts, 8 between spacer tube and outer skin. |
| M4 x 16–20 self-tapping screw, countersunk | 6 | for plastic | On hand. Cowl to plate, fitted on the bench. (Or M4 x 16 machine screws with M4 nylocs in the bosses: build with `--set captiveNuts=1`.) |
| Aluminium flat bar 25 x 3 mm | 1 m | 6061 or 6082 | 2 x 249 mm with three Ø6.5 holes, 2 x 110 mm with one hole. |
| Tube Ø10 outside, 1.5 wall | 1 m | aluminium or steel | 8 limiters at **8.0 mm** (plate thickness), 8 spacers at the **measured** depth minus 2.4 mm. |
| Closed-cell foam tape 2 mm x 20–25 mm | 1.5 m | EPDM or neoprene, adhesive | Gasket loop under the plate and around the throat. |
| RTV silicone or seam sealer | 1 tube | black | Sleeve to inner panel. |
| Rust primer or touch-up paint | 1 | | Cut edges and holes. |
| M6 acorn nut | 8 | DIN 1587 | Optional. Covers the ~7 mm of thread above the nyloc; otherwise trim. |

New purchases: the flat bar, the tube, the foam tape, and nylocs if there are none in the bin.

## Tools
Drills 3, 6.5 and 10.5 mm (or a step drill), Ø24 hole saw or step drill for the corners, jigsaw with a fine metal blade or a nibbler, files, deburring tool, hacksaw or cut-off wheel, depth gauge or hooked wire plus ruler, masking tape, torque wrench to 6 N·m, 10 mm socket, 4 mm hex key, PH2 or T20 driver for the M4s.

## Bolt stack
Head below the strip, nut on top. From the bottom: button head 3.3 → strip 3 → spacer tube (measured, through a Ø10.5 hole in the inner panel) → washer 1.6 → outer skin 0.8 → gasket 1.5 compressed → plate 8 with a steel limiter tube inside → washer 1.6 → nyloc 6. At the scan's 21 mm gap that is 42.7 mm head-to-nut, leaving about 7 mm of M6x50 above the nut. If a measured depth exceeds about 32 mm, that hole needs an M6x60.
