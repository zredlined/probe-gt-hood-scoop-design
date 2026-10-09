"""One Feature Studio write for scaler + scoop, then re-insert the mesh fix (with centre restore) in the three scan studios
and the scoop feature in the design studio. Minimal calls; prints a running count."""
from os_api import *
import sys
state = json.load(open("onshape_state.json")); fsid = state["fsid"]; PS = EID
API10 = BASE + "/api/v10"; CALLS = 0
def api(method, path, body=None):
    global CALLS; CALLS += 1
    for attempt in range(5):
        r = requests.request(method, API10 + path, json=body, auth=auth(), headers={"Accept": "application/json;charset=UTF-8; qs=0.09"}, timeout=180)
        if r.status_code != 429: break
        time.sleep(20 * (attempt + 1))
    if r.status_code >= 400: raise SystemExit(f"{method} {path} -> {r.status_code}: {r.text[:1200]}")
    return r.json() if r.content.strip() else {}
scaler = open("mesh_scale.fs").read(); scoop = open("scoop.fs").read()
code = scaler + "\n\n" + "\n".join(l for l in scoop.splitlines() if not l.startswith("FeatureScript ") and not l.startswith("import(path"))
api("POST", f"/featurestudios/d/{DID}/w/{WID}/e/{fsid}", {"contents": code})
names = [s.get("featureType") for s in api("GET", f"/featurestudios/d/{DID}/w/{WID}/e/{fsid}/featurespecs").get("featureSpecs", [])]
print("compiled:", names)
if not {"meshUnitFix", "probeHoodScoop"} <= set(names): raise SystemExit("compile failed")
mv = api("GET", f"/documents/d/{DID}/w/{WID}/currentmicroversion")["microversion"]
# --- mesh studios: delete old fix, insert new with the original bbox centre (from reference STL bounds) ---
centres = {"hood_outer": (76.35, 123.88, 71.86), "hood_underside": (83.61, 90.92, 19.42), "engine_bay": (42.2, 29.8, -162.42)}
for key, eid in state["mesh"].items():
    feats = api("GET", f"/partstudios/d/{DID}/w/{WID}/e/{eid}/features")
    for f in feats["features"]:
        if f.get("featureType") == "meshUnitFix": api("DELETE", f"/partstudios/d/{DID}/w/{WID}/e/{eid}/features/featureid/{f['featureId']}")
    cx, cy, cz = centres[key]
    params = [{"btType": "BTMParameterQuantity-147", "parameterId": "scaleFactor", "expression": "0.001", "value": 0.001}]
    for pid, v in (("cx", cx), ("cy", cy), ("cz", cz)): params.append({"btType": "BTMParameterQuantity-147", "parameterId": pid, "expression": f"{v} mm", "units": "millimeter", "value": v})
    api("POST", f"/partstudios/d/{DID}/w/{WID}/e/{eid}/features", {"feature": {"btType": "BTMFeature-134", "featureType": "meshUnitFix", "name": "Mesh unit fix (mm, scan frame)", "namespace": f"e{fsid}::m{mv}", "parameters": params}})
    print("mesh fixed:", key)
# --- scoop feature: delete + insert with all parameters ---
DEF_BOOL = dict(buildTemplate=True, buildBase=True, buildCowl=True, buildBezel=False, buildGuide=True, buildBacking=True, buildHardware=True, placeOnScan=True, sleeve=True, buildRainCap=True, buildSleeve=True, showToolAccess=True, captiveNuts=False)
DEF_LEN = dict(cutW=195, cutL=71, cutR=10, sleeveWall=2, skinT=0.8, innerGap=21, innerT=0.8, gasketT=1.5, baseW=244, baseFront=97, baseRear=84, baseR=10, baseT=8, bodyW=196, bodyFront=65, bodyRear=60, roofTop=74, wall=3, bodyR=4, chamferF=4, chamferR=10, mouthW=186, mouthR=4, lipR=2.5, bezelW=5, boltX=112, boltYF=80, boltYM=-4, boltYR=72, holeD=6.5, boltL=50, backingT=3, guideW=200, guideReach=50, cheekH=55, guideT=3, bossD=10, bossH=9, screwPilot=3.4, screwClear=4.3, nutAF=7.2, nutH=5.2)
DEF_ANG = dict(guideAngle=45, rakeDeg=20)
overrides = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
params = [{"btType": "BTMParameterBoolean-144", "parameterId": k, "value": bool(overrides.get(k, v))} for k, v in DEF_BOOL.items()]
for k, v in DEF_LEN.items(): v = overrides.get(k, v); params.append({"btType": "BTMParameterQuantity-147", "parameterId": k, "expression": f"{v} mm", "units": "millimeter", "value": v})
for k, v in DEF_ANG.items(): v = overrides.get(k, v); params.append({"btType": "BTMParameterQuantity-147", "parameterId": k, "expression": f"{v} deg", "units": "degree", "value": v})
feats = api("GET", f"/partstudios/d/{DID}/w/{WID}/e/{PS}/features")
for f in feats["features"]:
    if f.get("featureType") == "probeHoodScoop": api("DELETE", f"/partstudios/d/{DID}/w/{WID}/e/{PS}/features/featureid/{f['featureId']}")
api("POST", f"/partstudios/d/{DID}/w/{WID}/e/{PS}/features", {"feature": {"btType": "BTMFeature-134", "featureType": "probeHoodScoop", "name": "Probe hood scoop system", "namespace": f"e{fsid}::m{mv}", "parameters": params}})
time.sleep(6)
parts = api("GET", f"/parts/d/{DID}/w/{WID}/e/{PS}")
for p in parts:
    if p["name"][:1] in ("A", "B", "S", "R", "C", "T") or p["name"].startswith("ERR"): print("  part", p["name"][:95])
bb = api("GET", f"/partstudios/d/{DID}/w/{WID}/e/{state['mesh']['hood_outer']}/boundingboxes")
print("hood mesh bbox (mm): lo", [round(bb[k] * 1000) for k in ("lowX", "lowY", "lowZ")], "hi", [round(bb[k] * 1000) for k in ("highX", "highY", "highZ")], "(scan: -667..820, -570..818, 15..129)")
state["scoop_defaults"] = {**DEF_BOOL, **DEF_LEN, **DEF_ANG}; json.dump(state, open("onshape_state.json", "w"), indent=1)
print("API calls:", CALLS)
