FeatureScript 2716;
import(path : "onshape/std/common.fs", version : "2716.0");

// Fix an STL that Onshape imported in metres and centred on the origin: scale all bodies about the origin, then move the
// bounding-box centre back to where it was in the original file so every scan shares the scan frame.
annotation { "Feature Type Name" : "Mesh unit fix (scale about origin + restore centre)" }
export const meshUnitFix = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "Scale factor (1 unit -> mm = 0.001)" }
        isReal(definition.scaleFactor, { (unitless) : [0.0000001, 0.001, 1000] } as RealBoundSpec);
        annotation { "Name" : "Original centre X" } isLength(definition.cx, { (millimeter) : [-100000, 0, 100000] } as LengthBoundSpec);
        annotation { "Name" : "Original centre Y" } isLength(definition.cy, { (millimeter) : [-100000, 0, 100000] } as LengthBoundSpec);
        annotation { "Name" : "Original centre Z" } isLength(definition.cz, { (millimeter) : [-100000, 0, 100000] } as LengthBoundSpec);
    }
    {
        const bodies = qEverything(EntityType.BODY);
        opTransform(context, id + "scale", { "bodies" : bodies, "transform" : scaleUniformly(definition.scaleFactor, vector(0, 0, 0) * meter) });
        opTransform(context, id + "move", { "bodies" : bodies, "transform" : transform(vector(definition.cx, definition.cy, definition.cz)) });
    });
