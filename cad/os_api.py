import os, sys, json, time, requests
# fallback: load .env from the project root (values are only placed in this process environment, never printed)
BASE="https://cad.onshape.com"
AK=os.environ.get("ONSHAPE_ACCESS_KEY"); SK=os.environ.get("ONSHAPE_SECRET_KEY") or os.environ.get("ONSHAPE_SECRET") or os.environ.get("ONSHAPE_SECRET_ACCESS_KEY")
DID="b03b5bf08a93c5df66f722d9"; WID="0932d1534808bff872171f8f"; EID="62cfbbcc4293db63dd347bb5"
def auth(): 
    if not (AK and SK): sys.exit(f"missing keys: access={bool(AK)} secret={bool(SK)}")
    return (AK,SK)
def get(path,**kw): r=requests.get(BASE+path,auth=auth(),headers={"Accept":"application/json;charset=UTF-8; qs=0.09"},**kw); r.raise_for_status(); return r.json()
def post(path,js=None,**kw): r=requests.post(BASE+path,auth=auth(),headers={"Accept":"application/json;charset=UTF-8; qs=0.09","Content-Type":"application/json"},json=js,**kw); 
def post(path,js=None,files=None,data=None,params=None):
    h={"Accept":"application/json;charset=UTF-8; qs=0.09"}
    if files is None: h["Content-Type"]="application/json"
    r=requests.post(BASE+path,auth=auth(),headers=h,json=js,files=files,data=data,params=params)
    if r.status_code>=400: print("ERR",r.status_code,r.text[:800]); r.raise_for_status()
    return r.json() if r.text else {}
if __name__=="__main__":
    print("keys present: access",bool(AK),"secret",bool(SK))
    me=get("/api/v6/users/sessioninfo"); print("auth OK as:",me.get("name"),"| id",me.get("id"))
    doc=get(f"/api/v6/documents/{DID}"); print("document:",doc.get("name"),"| owner",doc.get("owner",{}).get("name"))
    els=get(f"/api/v6/documents/d/{DID}/w/{WID}/elements")
    for e in els: print(f"  element {e['id']}  {e['elementType']:12s} {e.get('dataType','')!s:28s} {e['name']}")
