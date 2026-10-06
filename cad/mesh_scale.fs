FeatureScript 2716;
import(path : "onshape/std/common.fs", version : "2716.0");

// Fix an STL imported without unit specification (file was millimetres, Onshape read metres): scale all bodies about the ORIGIN.
annotation { "Feature Type Name" : "Mesh unit fix (scale about origin)" }
export const meshUnitFix = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "Scale factor (1 unit -> mm = 0.001)" }
        isReal(definition.scaleFactor, { (unitless) : [0.0000001, 0.001, 1000] } as RealBoundSpec);
    }
    {
        const bodies = qEverything(EntityType.BODY);
        opTransform(context, id + "scale", { "bodies" : bodies, "transform" : scaleUniformly(definition.scaleFactor, vector(0, 0, 0) * meter) });
    });
