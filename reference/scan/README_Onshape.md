# Probe engine bay and hood — Onshape reference, first pass

Import the STL files as **millimeters**. All share one coordinate system. Z points approximately up, Y approximately rearward and X across the car. The frame comes from the bay scan, not a surveyed vehicle centerline or ground plane. Keep the supplied origin and orientation; do not center or rotate individual meshes independently.

## Start with these files

- **01_engine_bay_mm.stl** — 250,000 triangles, about 12.5 MB. Engine bay with its captured surrounding panels.
- **02_hood_outer_mm.stl** — about 100,000 triangles, 5 MB. Isolated outer hood, positioned from the closed-hood exterior scan through overlapping bodywork.
- **03_hood_underside_PROVISIONAL_mm.stl** — about 150,000 triangles, 7.5 MB. Approximate closed-position underside. This placement has unresolved local conflicts and is not approved for tight clearance decisions.
- **04_combined_LAYOUT_ONLY_PROVISIONAL_mm.stl** — all three, about 500,000 triangles, 25 MB. One-file convenience reference. Includes the provisional underside. It is a concatenation of open mesh surfaces, not a welded or watertight solid; separate component names and convenient visibility controls are not guaranteed in an STL import.
- Matching **color PLY** files — for color inspection in CloudCompare or other mesh tools; use STL for this Onshape workflow.

These are reference meshes, not printable parts. Use them to locate and shape new parametric CAD parts. Scanned openings and missing coverage remain open. A missing surface does not establish free space.

## Onshape setup

1. Unzip the package. Create an Onshape document and import the three numbered individual STL files, choosing **millimeter** units. Leave any Y-up to Z-up reorientation off: these files are already approximately Z-up.
2. Keep the imports as separate references so the outer hood and underside can be hidden independently. If imports appear in separate Part Studios, use a design Part Studio with Derived references at **Base origin**, without additional placement. If the mesh selection is inconvenient in your import, the combined STL provides a one-file layout alternative.
3. Check scale against these approximate envelopes: engine-bay mesh 1630 × 1439 × 539 mm; isolated hood outer 1487 × 1389 × 114 mm. These are bounding boxes of the captured geometry, not nominal factory part dimensions.
4. Begin with the engine bay and outer hood. Enable the provisional underside only when reviewing its uncertainty. Model the vent and duct as normal CAD features, using local sections/reference sketches where needed. Avoid converting every mesh triangle into an individual CAD face.
5. Before fixing a close-fitting duct, validate the underside position with physical measurements or an additional scan that provides a stronger geometric connection. Check the front headlight notches, both rear corners, and several inner-reinforcement heights.

The exports were read back locally and checked. They have **not** been imported into the user's Onshape account during this task.

## What is established

The saved EXStar clouds were extracted with their normals and captured colors. Original EXStar projects were not changed. The hood-closed exterior and hood-open engine bay were aligned by a rigid, unit-scale geometry fit using common painted bodywork. No matching marker constellation was found between those projects; the underside has no saved marker set.

Five overlapping body regions were checked after fitting. Median nearest-point differences were about **0.54–1.05 mm**, with 95th-percentile differences **1.04–1.64 mm** among accepted local correspondences. These are agreement between scans, not certified physical accuracy. Checks use geometric correspondence and normal agreement; unmatched/uncaptured regions are excluded and counts are in the JSON report.

The outer hood was separated by identifying exterior surfaces absent from the hood-open scan and selecting the connected hood footprint. This is a scan-derived segmentation, not an exact factory trim boundary. Shared-body subtraction can trim a few millimeters near the panel gaps; small segmentation imperfections remain.

## What remains provisional

The underside was rigidly fitted using painted perimeter strips and the isolated outer-hood silhouette, including the headlight notches and curved rear edge. No scaling, nonrigid warping, or forced surface fusion was used. A folded underside edge is not the same physical surface as the top skin.

The final fit used 1,691 perimeter samples after excluding 247 likely background/nonmatching samples from the fit. Median lateral edge disagreement is **4.41 mm**, and the 95th percentile is **12.32 mm**. Median absolute vertical edge disagreement is **1.27 mm**, with a 95th percentile of **3.98 mm**. These fitted-edge statistics do not establish interior accuracy.

A separate raw-point height check found unresolved intersections: among interior underside samples with nearby outer-skin support, about **6.8% lie more than 2 mm above the outer skin**, and **2.9% more than 5 mm above**. This diagnostic includes all captured underside geometry in the tested footprint; it does not establish the cause. The underside is therefore useful for reviewing the rough layout, but **do not trust it as a collision envelope yet**. The cross-section image shows the mismatch. A tight duct design should wait for these conflicts to be reconciled.

Three disconnected wiper/background fragments were removed from the Onshape underside mesh after component inspection. The full extracted cloud and detailed meshes preserve them for review. Other small captured parts were retained where possible.

## Mesh processing and validation

CloudCompare performed spatial subsampling at 2 mm for the bay/exterior and 1.5 mm for the underside. Open3D performed ball-pivoting reconstruction and quadratic simplification. No global watertight reconstruction, blanket hole filling, or surface smoothing was used.

The final CAD copies total about 500,000 triangles. Bidirectional sampled comparisons against the detailed reconstructed meshes give 95th-percentile simplification differences below **0.30 mm** for all three. This isolates the extra change caused by simplification: it does not include scan error, alignment error, missing coverage, or reconstruction error. Larger local maxima are recorded in the report.

The full native-color clouds, aligned clouds, detailed meshes, transform matrices, scripts and logs remain in the parent work folder. The separate Blender review file preserves three named objects at the supplied positions. The exploded illustration temporarily offsets the hood layers for visibility; the STL files and saved Blender objects have no exploded offset.

## Official Onshape references

- [Importing files and STL units](https://cad.onshape.com/help/Content/Document/importing_files.htm)
- [Mixed modeling with mesh references](https://cad.onshape.com/help/Content/PartStudio/mixed_modeling.htm)
- [Derived and base-origin placement](https://cad.onshape.com/help/Content/PartStudio/derived.htm)
