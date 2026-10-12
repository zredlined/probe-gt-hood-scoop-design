# Bill of materials

Depths marked **measure** are confirmed in Round 1 of the build guide before anything is cut to length.

## Printed parts

| Part | File | Material | Orientation | Supports | Walls / infill | Filament |
|---|---|---|---|---|---|---|
| T  template | `stl/T_fit_check_template.stl` | PLA | flat | none | 2 / 15 % | ~40 g |
| A1 flange plate | `stl/A1_flange_plate.stl` | ASA, black | top face down (curved side up) | none | 4 / 15 % | ~150 g |
| A2 cowl | `stl/A2_cowl.stl` | ASA, black (+ purple for the logo, see below) | roof down | none | 4 / 30 % | ~100 g |
| S  throat sleeve | `stl/S_throat_sleeve.stl` | ASA, purple | standing | none | 3 / any | ~21 g |
| R  rain cap | `stl/R_rain_cap.stl` | ASA, purple | flange down, plug up | none | 3 / 20 % | ~55 g |
| C  guide | `stl/C_guide_flap.stl` | ASA, purple | bracket down | none (45° flap) | 4 / 30 % | ~41 g |
| B  bezel (optional) | build with `--set buildBezel=1` | ASA, purple | on its back | none | 3 / 100 % | ~3 g |

Totals: black ASA about 245 g, purple ASA about 120 g, PLA about 40 g. Estimates, allow 25 %. Nothing needs supports.

**Logo inlay with the AMS:** the roof has a 0.6 mm recess in the shape of the wordmark, and `stl/A2_logo_inlay.stl` is the matching 0.6 mm plug. In Bambu Studio import `A2_cowl.stl` and `A2_logo_inlay.stl` together and answer **yes** to loading them as one object with multiple parts, then assign the inlay part to purple. The cowl prints roof-down, so the inlay is layers 1–3 and costs three filament swaps. Without purple, print the cowl alone and the logo stays a crisp recess. Do not multi-colour anything taller; a full-height purple bezel would purge more filament than the whole part weighs.

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

## Shopping checklist (US sources)

Already on hand: 8 x M6x50 button head, 6 x M4 self-tapping, black ASA.

- [ ] **Aluminium flat bar 1" x 1/8"** (25.4 x 3.2 mm), one 3 ft length. Any hardware store carries it; online: [LED Supply](https://www.ledsupply.com/led-heatsinks/aluminum-flat-bar) or [Remington Industries](https://www.remingtonindustries.com/raw-metals/aluminum-flat-bar-1-8-x-1-6061-general-purpose-plate-10-lengths-available-t6511-mill-stock-extruded-0-125-thick/).
- [ ] **Aluminium tube 3/8" OD x 0.049" wall** (ID 0.277" = 7.0 mm, clears M6), 1 to 2 ft. Hobby-shop K&S tube is this size; online: [Speedy Metals](https://speedymetals.com/p-4554-38-od-x-0049-wall-tube-6061-t6-aluminum.aspx) or [Online Metals](https://www.onlinemetals.com/en/buy/aluminum-round-tube-6061). Steel brake-line stock of the same OD also works.
- [ ] **Closed-cell foam weatherstrip tape, 1/16" or 3/32" thick x 1" wide**, adhesive backed, 10 ft roll. Hardware-store EPDM/neoprene weatherstrip is fine; McMaster's [EPDM-blend foam strips](https://www.mcmaster.com/products/strips/material~epdm-neoprene-sbr-foam) if ordering there.
- [ ] **M6 nylon-insert lock nuts, 8** (DIN 985 / ISO 10511), zinc: [Fastener Superstore](https://www.fastenersuperstore.com/products/627689/nylon-insert-locknuts) or [McMaster](https://www.mcmaster.com/products/locknuts/specifications-met~iso-10511/). Skip if you have a bin of them.
- [ ] **M6 flat washers, 16.**
- [ ] **M6 acorn nuts, 8** (optional, covers the proud thread).
- [ ] **Purple ASA, 1 kg** (optional, for cap, guide and the logo inlay): Polymaker PolyLite ASA Purple or SUNLU ASA Purple; both are AMS-compatible. Search the exact names on Amazon; reference listings: [Polymaker](https://www.3djake.ch/en-CH/polymaker/polylite-asa-purple), [SUNLU](https://www.3djake.com/sunlu/asa-purple). Bambu does not sell a purple ASA.
- [ ] **Black RTV silicone** (sleeve seal), **rust primer or touch-up paint**, **masking tape**, **modelling clay** (clearance test).
- [ ] Tools to check: a **step drill to 1/2"** (for the 10.5 mm inner-panel holes and the 6.5 mm skin holes), a **15/16" or 1" hole saw** or step drill to 1" for the R12 corners, a fine metal jigsaw blade, a 10 mm socket, a torque wrench that reads 6 N·m.
