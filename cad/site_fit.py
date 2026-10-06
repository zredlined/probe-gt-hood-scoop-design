import numpy as np, trimesh, json
import os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/reference/scan/"
outer=trimesh.load(R+"02_hood_outer_mm_color.ply",process=False); V=outer.vertices
under=trimesh.load(R+"03_hood_underside_PROVISIONAL_mm_color.ply",process=False); U=under.vertices
bay=trimesh.load(R+"01_engine_bay_mm_color.ply",process=False); B=bay.vertices
Cu=np.asarray(under.visual.vertex_colors)[:,:3].astype(float)

# 1) wide sticker extents from underside colors (bright, low-sat), front region
bright=Cu.mean(1); sat=Cu.max(1)-Cu.min(1)
m=(bright>110)&(sat<70)&(U[:,1]<-250)&(U[:,1]>-420)
S=U[m]
for lo,hi,name in [(-340,-200,"left sticker A"),(-200,-80,"left sticker B"),(-60,220,"wide center sticker"),(240,320,"right small sticker")]:
    p=S[(S[:,0]>lo)&(S[:,0]<hi)]
    if len(p): print(f"{name:22s} n={len(p):4d}  X {np.percentile(p[:,0],2):6.0f}..{np.percentile(p[:,0],98):6.0f}  Y {np.percentile(p[:,1],2):6.0f}..{np.percentile(p[:,1],98):6.0f}  Zmean {p[:,2].mean():6.1f}")

# 2) candidate site O (approximate; right ~70% of wide sticker, rear half) 
O=np.array([110.0,-340.0])
print("\nCandidate O (scan XY, APPROXIMATE from sticker neighborhood):",O)

# 3) local quadratic fit of OUTER skin over 300x260 window
w=(np.abs(V[:,0]-O[0])<150)&(np.abs(V[:,1]-O[1])<130)
P=V[w]; print("outer verts in window:",len(P))
x=P[:,0]-O[0]; y=P[:,1]-O[1]; z=P[:,2]
A=np.c_[np.ones_like(x),x,y,x*x,x*y,y*y]
coef,*_=np.linalg.lstsq(A,z,rcond=None)
res=z-A@coef
print("quadratic fit z = a + b x + c y + d x^2 + e xy + f y^2 (local, mm):")
for n,cf in zip("abcdef",coef): print(f"  {n} = {cf: .6f}")
print(f"  residual RMS {res.std():.2f} mm, p95 |res| {np.percentile(abs(res),95):.2f} mm")
zc=coef[0]; print(f"  outer skin Z at O: {zc:.1f}")
sx,sy=coef[1],coef[2]
print(f"  slope at O: dz/dx={sx:.4f} ({np.degrees(np.arctan(sx)):.1f} deg), dz/dy={sy:.4f} ({np.degrees(np.arctan(sy)):.1f} deg)  -> hood falls toward FRONT by {np.degrees(np.arctan(-sy)):.1f} deg")
print(f"  curvature: d2z/dx2={2*coef[3]:.5f} (R~{1/abs(2*coef[3]) if coef[3] else 0:.0f} mm), d2z/dy2={2*coef[5]:.5f} (R~{1/abs(2*coef[5]) if coef[5] else 0:.0f} mm)")
def zq(xx,yy): return coef[0]+coef[1]*xx+coef[2]*yy+coef[3]*xx*xx+coef[4]*xx*yy+coef[5]*yy*yy
# sag across a 250x200 flange relative to its tangent plane at O
xs=np.linspace(-125,125,51); ys=np.linspace(-100,100,41); XX,YY=np.meshgrid(xs,ys)
dev=zq(XX,YY)-(zc+sx*XX+sy*YY)
print(f"  flange 250x200 deviation from tangent plane at O: min {dev.min():.2f} max {dev.max():.2f} mm")
print(f"  corners rel. plane: FL {dev[0,0]:.2f} FR {dev[0,-1]:.2f} RL {dev[-1,0]:.2f} RR {dev[-1,-1]:.2f}")

# 4) underside skin gap at the sticker region (exposed single skin?)
wu=(np.abs(U[:,0]-O[0])<100)&(np.abs(U[:,1]-O[1])<36)
Q=U[wu]; gap=zq(Q[:,0]-O[0],Q[:,1]-O[1])-Q[:,2]
print(f"\nunderside pts within 200x71 of O: {len(Q)}  outer-minus-underside gap: median {np.median(gap):.1f}  p10 {np.percentile(gap,10):.1f}  p90 {np.percentile(gap,90):.1f} mm (PROVISIONAL registration)")
# wider: flange footprint 250x200 -> where are the ribs (gap>8mm)?
wf=(np.abs(U[:,0]-O[0])<125)&(np.abs(U[:,1]-O[1])<100)
Q=U[wf]; gap=zq(Q[:,0]-O[0],Q[:,1]-O[1])-Q[:,2]
print(f"underside pts within 250x200 flange: {len(Q)} gap median {np.median(gap):.1f} p90 {np.percentile(gap,90):.1f} max {gap.max():.1f}")
# grid of gap over flange footprint 25 mm cells
print("gap map (rows = Y from front -100 to rear +100, cols = X -125..125, 25mm cells; value=median outer-under gap, '.'=no pts)")
for yy in range(-100,100,25):
    row=""
    for xx in range(-125,125,25):
        s=(Q[:,0]-O[0]>=xx)&(Q[:,0]-O[0]<xx+25)&(Q[:,1]-O[1]>=yy)&(Q[:,1]-O[1]<yy+25)
        row+=f"{np.median(gap[s]):5.0f}" if s.sum()>3 else "    ."
    print(f"  Y{yy:+4d}:"+row)

# 5) engine bay below the site: highest bay geometry under the opening region and rearward toward cone
for (x0,x1,y0,y1,name) in [(10,210,-380,-300,"under opening"),(10,210,-300,-200,"just rear of opening"),(10,260,-200,-50,"further rear (cone zone?)"),(200,450,-300,-100,"right-rear")]:
    s=(B[:,0]>x0)&(B[:,0]<x1)&(B[:,1]>y0)&(B[:,1]<y1)
    if s.sum(): print(f"bay {name:26s} n={s.sum():6d}  Z max {B[s,2].max():6.0f}  p95 {np.percentile(B[s,2],95):6.0f}  median {np.median(B[s,2]):6.0f}   (outer skin ~{zq((x0+x1)/2-O[0],(y0+y1)/2-O[1]):.0f})")
json.dump({"O_scan_xy_approx":O.tolist(),"outer_quadratic_coef_local":coef.tolist(),"z_at_O":float(zc)},open("site_fit.json","w"),indent=1)
