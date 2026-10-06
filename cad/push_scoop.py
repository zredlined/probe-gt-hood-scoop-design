from os_api import *
import sys
state=json.load(open("onshape_state.json")); fsid=state["fsid"]; PS=EID
API10=BASE+"/api/v10"; CALLS=0
def api(method,path,body=None):
    global CALLS; CALLS+=1
    for attempt in range(5):
        r=requests.request(method,API10+path,json=body,auth=auth(),headers={"Accept":"application/json;charset=UTF-8; qs=0.09"},timeout=180)
        if r.status_code!=429: break
        time.sleep(20*(attempt+1))
    if r.status_code>=400: raise SystemExit(f"{method} {path} -> {r.status_code}: {r.text[:1500]}")
    return r.json() if r.content.strip() else {}
scaler=open("mesh_scale.fs").read(); scoop=open("scoop.fs").read()
body_scoop="\n".join(l for l in scoop.splitlines() if not l.startswith("FeatureScript ") and not l.startswith("import(path"))
code=scaler+"\n\n"+body_scoop
api("POST",f"/featurestudios/d/{DID}/w/{WID}/e/{fsid}",{"contents":code})
specs=api("GET",f"/featurestudios/d/{DID}/w/{WID}/e/{fsid}/featurespecs"); names=[s.get("featureType") for s in specs.get("featureSpecs",[])]
print("compiled feature types:",names)
if "probeHoodScoop" not in names:
    # fetch compile diagnostics if available
    try:
        c=api("GET",f"/featurestudios/d/{DID}/w/{WID}/e/{fsid}")
        print("studio keys:",list(c.keys())); 
        for k in ("notices","messages","errors"):
            if k in c: print(k, json.dumps(c[k],indent=1)[:3000])
    except SystemExit as ex: print(ex)
    raise SystemExit("FeatureScript did not compile")
mv=api("GET",f"/documents/d/{DID}/w/{WID}/currentmicroversion")["microversion"]
feats=api("GET",f"/partstudios/d/{DID}/w/{WID}/e/{PS}/features")
for f in feats["features"]:
    if f.get("featureType")=="probeHoodScoop": api("DELETE",f"/partstudios/d/{DID}/w/{WID}/e/{PS}/features/featureid/{f['featureId']}")
DEF_BOOL=dict(buildTemplate=True,buildBase=True,buildCowl=True,buildBezel=True,buildGuide=True,buildBacking=True,buildHardware=True,placeOnScan=True,sleeve=True,buildRainCap=True,onePiece=True,buildSleeve=True,showToolAccess=True)
DEF_LEN=dict(cutW=195,cutL=71,cutR=10,sleeveWall=2,skinT=0.8,innerGap=21,innerT=0.8,gasketT=1.5,baseW=244,baseFront=97,baseRear=84,baseR=10,baseT=6,bodyW=196,bodyFront=65,bodyRear=60,roofTop=72,wall=3,bodyR=4,chamferF=4,chamferR=10,mouthW=186,mouthR=4,lipR=2.5,bezelW=5,boltX=112,boltYF=80,boltYM=-4,boltYR=72,holeD=6.5,boltL=50,backingT=3,guideW=200,guideReach=50,cheekH=55,guideT=3)
DEF_ANG=dict(guideAngle=45)
overrides=json.loads(sys.argv[1]) if len(sys.argv)>1 else {}
params=[]
for k,v in DEF_BOOL.items(): params.append({"btType":"BTMParameterBoolean-144","parameterId":k,"value":bool(overrides.get(k,v))})
for k,v in DEF_LEN.items(): v=overrides.get(k,v); params.append({"btType":"BTMParameterQuantity-147","parameterId":k,"expression":f"{v} mm","units":"millimeter","value":v})
for k,v in DEF_ANG.items(): v=overrides.get(k,v); params.append({"btType":"BTMParameterQuantity-147","parameterId":k,"expression":f"{v} deg","units":"degree","value":v})
feat={"btType":"BTMFeature-134","featureType":"probeHoodScoop","name":"Probe hood scoop system","namespace":f"e{fsid}::m{mv}","parameters":params}
r=api("POST",f"/partstudios/d/{DID}/w/{WID}/e/{PS}/features",{"feature":feat}); print("inserted; immediate state:",r.get("featureState",{}).get("featureStatus"))
st={}
for _ in range(30):
    feats=api("GET",f"/partstudios/d/{DID}/w/{WID}/e/{PS}/features"); st={f["name"]:feats["featureStates"].get(f["featureId"],{}) for f in feats["features"]}
    if all(v.get("featureStatus") in ("OK","WARNING","ERROR") for v in st.values()): break
    time.sleep(4)
for k,v in st.items():
    print(f"  feature {k!r}: {v.get('featureStatus')}"); print('   state:',json.dumps(v)[:1500])
if all(v.get("featureStatus") in ("OK","WARNING") for v in st.values()):
    parts=api("GET",f"/parts/d/{DID}/w/{WID}/e/{PS}")
    for p in parts: print(f"  part {p['name']:<45} id={p['partId']}")
    state["parts"]={p['name']:p['partId'] for p in parts}
json.dump(state,open("onshape_state.json","w"),indent=1)
print("API calls:",CALLS)
