"""Build the 'Scoop on car' assembly (3 scan meshes + design Part Studio) and export printable parts.
Export uses a second Part Studio with the same feature placed flat (placeOnScan=false) so STLs are bed-ready.
Usage: python assemble_export.py [--no-assembly] [--no-export]"""
from os_api import *
import sys, subprocess
state = json.load(open("onshape_state.json")); fsid = state["fsid"]; PS = EID
API10 = BASE + "/api/v10"; CALLS = 0
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/step"
os.makedirs(OUT, exist_ok=True)

def api(method, path, body=None, raw=False, params=None):
    global CALLS; CALLS += 1
    for attempt in range(5):
        r = requests.request(method, API10 + path, json=body, params=params, auth=auth(), headers={"Accept": "application/json;charset=UTF-8; qs=0.09" if not raw else "*/*"}, timeout=300, allow_redirects=False)
        if r.status_code != 429: break
        time.sleep(20 * (attempt + 1))
    if r.status_code in (301, 302, 303, 307, 308):
        r = requests.get(r.headers["Location"], auth=auth(), timeout=600)
    if r.status_code >= 400: raise SystemExit(f"{method} {path} -> {r.status_code}: {r.text[:800]}")
    if raw: return r.content
    return r.json() if r.content.strip() else {}

def wait_ok(ps):
    for _ in range(30):
        f = api("GET", f"/partstudios/d/{DID}/w/{WID}/e/{ps}/features"); st = {x["name"]: f["featureStates"].get(x["featureId"], {}).get("featureStatus") for x in f["features"]}
        if all(v in ("OK", "WARNING", "ERROR") for v in st.values()): return st
        time.sleep(4)
    return st

def rebuild_assembly():
    old = state.get("asm")
    if old: api("DELETE", f"/elements/d/{DID}/w/{WID}/e/{old}")
    asm = api("POST", f"/assemblies/d/{DID}/w/{WID}", {"name": "Scoop on car (scan, shared origin)"})["id"]
    state["asm"] = asm; json.dump(state, open("onshape_state.json", "w"), indent=1)
    for eid, types in ((PS, ["PARTS"]), (state["mesh"]["hood_outer"], ["PARTS"]), (state["mesh"]["hood_outer"], ["SURFACES"]),
                       (state["mesh"]["hood_underside"], ["PARTS"]), (state["mesh"]["hood_underside"], ["SURFACES"]),
                       (state["mesh"]["engine_bay"], ["PARTS"]), (state["mesh"]["engine_bay"], ["SURFACES"])):
        try: api("POST", f"/assemblies/d/{DID}/w/{WID}/e/{asm}/instances", {"documentId": DID, "elementId": eid, "isWholePartStudio": True, "includePartTypes": types})
        except SystemExit as ex: print("  instance skipped:", str(ex)[:160])
    inst = api("GET", f"/assemblies/d/{DID}/w/{WID}/e/{asm}?includeNonSolids=true")["rootAssembly"]["instances"]
    print(f"assembly rebuilt: {asm} with {len(inst)} instances")
    return asm

def ensure_flat_studio():
    ps = state.get("flat_ps")
    if not ps:
        ps = api("POST", f"/partstudios/d/{DID}/w/{WID}", {"name": "Scoop FLAT (export / printing)"})["id"]; state["flat_ps"] = ps; json.dump(state, open("onshape_state.json", "w"), indent=1)
    # mirror the feature from the design studio, with placeOnScan=false
    src = api("GET", f"/partstudios/d/{DID}/w/{WID}/e/{PS}/features")
    feat = [f for f in src["features"] if f.get("featureType") == "probeHoodScoop"][0]
    for p in feat["parameters"]:
        if p.get("parameterId") in ("placeOnScan", "showToolAccess"): p["value"] = False
    for k in ("featureId", "nodeId"): feat.pop(k, None)
    dst = api("GET", f"/partstudios/d/{DID}/w/{WID}/e/{ps}/features")
    for f in dst["features"]:
        if f.get("featureType") == "probeHoodScoop": api("DELETE", f"/partstudios/d/{DID}/w/{WID}/e/{ps}/features/featureid/{f['featureId']}")
    api("POST", f"/partstudios/d/{DID}/w/{WID}/e/{ps}/features", {"feature": feat})
    print("flat studio feature state:", wait_ok(ps))
    return ps

def export_parts(ps):
    parts = api("GET", f"/parts/d/{DID}/w/{WID}/e/{ps}")
    printable = [p for p in parts if p["name"][:1] in ("A", "B", "C", "R", "S", "T") and not p["name"].startswith("ERR")]
    for p in printable:
        safe = "".join(c if c.isalnum() else "_" for c in p["name"])[:60]
        data = api("GET", f"/partstudios/d/{DID}/w/{WID}/e/{ps}/stl", raw=True, params={"units": "millimeter", "mode": "binary", "angleTolerance": 0.08, "chordTolerance": 0.04, "partIds": p["partId"]})
        open(f"{OUT}/{safe}.stl", "wb").write(data); print(f"  STL {safe}.stl  {len(data)//1024} kB")
    # STEP of everything in the flat studio (CAD exchange)
    js = api("POST", f"/partstudios/d/{DID}/w/{WID}/e/{ps}/translations", {"formatName": "STEP", "storeInDocument": False, "stepVersionString": "AP242"})
    tid = js["id"]; st = js.get("requestState"); t0 = time.time()
    while st == "ACTIVE" and time.time() - t0 < 600: time.sleep(6); js = api("GET", f"/translations/{tid}"); st = js.get("requestState")
    if st == "DONE" and js.get("resultExternalDataIds"):
        data = api("GET", f"/documents/d/{DID}/externaldata/{js['resultExternalDataIds'][0]}", raw=True)
        open(f"{OUT}/probe_hood_scoop_system_flat.step", "wb").write(data); print(f"  STEP probe_hood_scoop_system_flat.step {len(data)//1024} kB")
    else: print("  STEP export:", st, js.get("failureReason"))
    return printable

if __name__ == "__main__":
    if "--no-assembly" not in sys.argv: rebuild_assembly()
    if "--no-export" not in sys.argv:
        ps = ensure_flat_studio(); export_parts(ps)
    print("API calls:", CALLS)
    print(f"open: https://cad.onshape.com/documents/{DID}/w/{WID}/e/{state.get('asm', PS)}")
