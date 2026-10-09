# Decisions

Why the design is the way it is. Newest first. Each entry is the decision, the reason, and what it replaced.

## 2026-10-08 — Rev H

**Two-piece body, joined on the bench.** A flange plate printed top-face-down and a cowl printed roof-down, both with zero supports. Six M4 screws go up through countersunk holes in the plate into bosses inside the cowl skirt, with a tongue-and-groove to locate them. Replaces the one-piece body, which needed a full ring of support under the flange at 60 mm and put support scars on the visible nut face. Also fixes a gap in the earlier two-piece attempt, which had no fastener between cowl and base. Self-tapping M4 is the default; a parameter switches the bosses to captive M4 nyloc pockets.

**Mouth face raked 20°.** The front face leans back instead of standing vertical. Less bluff, throws rain down rather than into the throat, and it is the most recognisable 90s scoop cue (WRX, Evo, GTi-R all had raked boxes). Roof raised 72 → 74 to keep the mouth above 100 cm² (now 186 x 55.5, 103 cm²).

**AMS for the logo, not the bezel.** The 4OGS deboss on the roof becomes a purple inlay with three filament swaps in the first layers, which costs almost nothing. A full-height purple bezel would swap on every layer and purge 150–300 g of filament for a 3 g feature, so the bezel is now an optional separate part, off by default.

**Scan meshes re-registered in Onshape.** The STL import had centred each mesh on the origin; the scoop therefore appeared displaced toward the middle of the hood in the assembly. The unit-fix feature now also moves each mesh back by its original bounding-box centre. The local renders and validation were never affected; they always used the raw scan files.

## 2026-10-06 — Rev F / G

**Bolts head-down, nylocs on top.** With nuts underneath, the bolt ends came within 2 mm of engine-bay structure at the front-right corner, where the scan shows only about 43 mm under the skin. Heads down removes 10 mm of under-hood protrusion.

**Guide clamped by the two middle bolts.** A U-bracket with the flap replaced a hanger ring with rivnuts, bosses and four M6x20. Removes four purchases and a tool; the guide comes off by loosening two nuts.

**Four pieces of 25 x 3 flat bar instead of a sheet frame.** Hardware-store material, hacksaw and drill.

**Cowl narrowed 210 → 196.** A 10 mm socket on the side nuts needed 8.5 mm of radius and had 7. Now 14 mm centre-to-wall.

**Spacer tubes through an oversize hole in the inner panel.** The hood is double-skinned at the site (about 21 mm, varying). The tube bears on a washer against the outer skin and the inner panel is never clamped, so the depth at each hole only changes a tube length.

## 2026-10-05 — Rev A to E

**Location.** The owner's nozzle-tested spot on the exposed label patch, not a position inferred from the scan. The scan was used to find the site (label colours), fit the hood curvature there, and check clearances.

**Hardware M6.** The brief said M5; the owner has M6x50 in quantity.

**Throat sleeve.** The hood cut grows to 199 x 75 so a 2 mm liner can run through both skins, keeping the cavity dry and hiding cut edges.

**Open fresh-air feed, not a sealed intake.** Per the brief. The throat and bolt pattern are sized so a sealed box can be added later on the same opening.

**Teenage Engineering slab, black with purple accents.** Flat roof, small chamfers, uniform radii, exposed fasteners on a regular pitch, debossed wordmark. Colours follow the car's livery.
