import numpy as np, trimesh, json, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from PIL import Image
import os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/reference/scan/"
fit=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"site_fit.json"))); O=np.array(fit["O_scan_xy_approx"]); cf=fit["outer_quadratic_coef_local"]; zc=fit["z_at_O"]
def zq(x,y): return cf[0]+cf[1]*x+cf[2]*y+cf[3]*x*x+cf[4]*x*y+cf[5]*y*y
n=np.array([-cf[1],-cf[2],1.0]); n/=np.linalg.norm(n); zl=n; xl=np.cross([0,1,0],zl); xl/=np.linalg.norm(xl); yl=np.cross(zl,xl); Rm=np.c_[xl,yl,zl]
def to_global(V, sag_bottom=False):
    V=V.copy()
    if sag_bottom:
        b=np.abs(V[:,2])<=0.01; V[b,2]=zq(V[b,0],V[b,1])-(zc+cf[1]*V[b,0]+cf[2]*V[b,1])
    return (Rm@V.T).T+np.array([O[0],O[1],zc])
def crop(m, dx, dy, dz=None):
    v=m.vertices; k=(np.abs(v[:,0]-O[0])<dx)&(np.abs(v[:,1]-O[1])<dy)
    if dz is not None: k&=(v[:,2]>dz[0])&(v[:,2]<dz[1])
    f=m.faces[k[m.faces].all(1)]; return v, f
hood=trimesh.load(R+"02_hood_outer_mm.stl",process=False)
under=trimesh.load(R+"03_hood_underside_PROVISIONAL_mm.stl",process=False)
bay=trimesh.load(R+"01_engine_bay_mm.stl",process=False)
cone_axis=(np.array([265,-228,-70.]),np.array([245,-45,10.]))
def cone_mesh():
    a,b=cone_axis; L=np.linalg.norm(b-a); c=trimesh.creation.cylinder(radius=75,height=L,sections=48)
    T=trimesh.geometry.align_vectors([0,0,1],(b-a)/L); c.apply_transform(T); c.apply_translation((a+b)/2); return c
CONE=cone_mesh(); CONE.export("cone_placeholder.stl")
names=["A_base_frame","B_cowl","bezel","bolt_heads","C_lower_guide_PROVISIONAL"]
parts={k:trimesh.load(f"concept_{k}.stl") for k in names}
col={"cone":(0.25,0.45,0.75),"A_base_frame":(1.0,0.42,0.07),"B_cowl":(0.16,0.16,0.17),"bezel":(1.0,0.42,0.07),"bolt_heads":(0.62,0.62,0.64),"C_lower_guide_PROVISIONAL":(0.45,0.45,0.47),
     "hood":(0.78,0.12,0.18),"under":(0.55,0.10,0.14),"bay":(0.60,0.62,0.66)}
def render(items, cam_dir, up, W=1400, H=900, mmpp=0.5, center=None, light=(0.35,-0.45,0.82), bg=(0.93,0.93,0.92)):
    d=np.array(cam_dir,float); d/=np.linalg.norm(d)   # direction from scene to camera
    r=np.cross(up,d); r/=np.linalg.norm(r); u=np.cross(d,r)
    L=np.array(light,float); L/=np.linalg.norm(L)
    img=np.ones((H,W,3))*np.array(bg); zb=np.full((H,W),-1e9)
    c0=np.array(center if center is not None else [O[0],O[1],zc])
    for V,F,rgb in items:
        P=(V-c0); px=(P@r)/mmpp+W/2; py=H/2-(P@u)/mmpp; pz=P@d
        tri=V[F]; nr=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]); nn=np.linalg.norm(nr,axis=1); ok=nn>1e-6; nr=nr[ok]/nn[ok,None]; F=F[ok]
        lam=np.abs(nr@L)*0.7+0.3; facing=np.sign(nr@d)  # two-sided
        cols=np.clip(np.array(rgb)[None,:]*lam[:,None],0,1)
        X=px[F]; Y=py[F]; Z=pz[F]
        order=np.argsort(Z.mean(1))  # back to front; z-test still applied
        for i in order:
            x=X[i]; y=Y[i]; z=Z[i]
            x0,x1=int(max(np.floor(x.min()),0)),int(min(np.ceil(x.max()),W-1)); y0,y1=int(max(np.floor(y.min()),0)),int(min(np.ceil(y.max()),H-1))
            if x1<x0 or y1<y0: continue
            gx,gy=np.meshgrid(np.arange(x0,x1+1)+0.5,np.arange(y0,y1+1)+0.5)
            det=(x[1]-x[0])*(y[2]-y[0])-(x[2]-x[0])*(y[1]-y[0])
            if abs(det)<1e-9: continue
            l1=((gx-x[0])*(y[2]-y[0])-(x[2]-x[0])*(gy-y[0]))/det; l2=((x[1]-x[0])*(gy-y[0])-(gx-x[0])*(y[1]-y[0]))/det; l0=1-l1-l2
            m=(l0>=-1e-3)&(l1>=-1e-3)&(l2>=-1e-3)
            if not m.any(): continue
            zz=l0*z[0]+l1*z[1]+l2*z[2]; sub=zb[y0:y1+1,x0:x1+1]; w=m&(zz>sub)
            sub[w]=zz[w]; img[y0:y1+1,x0:x1+1][w]=cols[i]
    return (img*255).astype(np.uint8)
def scoop_items(with_guide=True):
    it=[(CONE.vertices,CONE.faces,col["cone"])]
    for k in names:
        if k.startswith("C_") and not with_guide: continue
        m=parts[k]; it.append((to_global(m.vertices,sag_bottom=(k=="A_base_frame")),m.faces,col[k]))
    return it
# View 1: iso from front-right-above (viewer in front of car => camera at -Y, +X, +Z)
hv,hf=crop(hood,330,300)
img1=render([(hv,hf,col["hood"])]+scoop_items(False), cam_dir=(0.55,-0.6,0.58), up=(0,0,1), mmpp=0.42)
Image.fromarray(img1).save("v1_iso_front_right.png")
# View 2: from below-rear, hood underside provisional + scoop + guide
uv,uf=crop(under,260,220); hv2,hf2=crop(hood,260,220)
img2=render([(uv,uf,col["under"]),(hv2,hf2,col["hood"])]+scoop_items(True), cam_dir=(0.45,0.55,-0.7), up=(0,0,1), mmpp=0.42, light=(0.3,0.4,-0.85))
Image.fromarray(img2).save("v2_from_below.png")
# View 3: side elevation from +X, hood as thin slab |X-O|<25 (shows slope), plus engine bay below in same slab (what's under the opening)
hv3,hf3=crop(hood,25,320); uv3,uf3=crop(under,25,320); bv,bf=crop(bay,60,320,dz=(-200,200))
img3=render([(hv3,hf3,col["hood"]),(uv3,uf3,col["under"]),(bv,bf,col["bay"])]+scoop_items(True), cam_dir=(1,0,0), up=(0,0,1), mmpp=0.45, center=[O[0],O[1]+40,zc-80])
Image.fromarray(img3).save("v3_side_section.png")
# View 4: plan from above with engine bay context (hood hidden), guide + opening footprint
bv4,bf4=crop(bay,330,330,dz=(-300,200))
img4=render([(bv4,bf4,col["bay"])]+scoop_items(True), cam_dir=(0,0,1), up=(0,1,0), mmpp=0.5)
Image.fromarray(img4).save("v4_plan_bay.png")
print("ok")
