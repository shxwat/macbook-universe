"""R06: surface finish and anonymous, photo-guided board detail.
Coordinates and component identities remain approximate; no netlist is implied.
"""
import bpy, math, os, json
from collections import defaultdict
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=R+'/MacBook-Pro-14-M4-internals-r05.blend')
scene=bpy.context.scene;board=bpy.data.objects['LOGIC_BOARD']
def material(name,color,metal,rough):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;m.diffuse_color=(*color,1);return m
mat={
 'ceramic':material('R06 · ceramic passive study',(.20,.19,.17),.18,.60),
 'dark':material('R06 · unmarked packages',(.026,.029,.033),.15,.58),
 'solder':material('R06 · solder terminations',(.19,.20,.20),.58,.46),
 'via':material('R06 · reference contact dots',(.31,.23,.12),.70,.42),
 'white':material('R06 · muted silkscreen',(.24,.25,.25),.0,.76)
}
grp=bpy.data.objects.new('R06_PHOTO_GUIDED_DETAILS',None);bpy.context.collection.objects.link(grp);grp.parent=board;grp['componentId']='board';grp['layer']='internal';grp['accuracy']='Approximate';grp['description']='Anonymous component shapes patterned after the reference photographs. Exact identities, counts and positions are not verified.';grp['source']='https://support.apple.com/en-us/120769'
# Build thousands of tiny bevel-free cuboids in five meshes to keep draw calls small.
buckets=defaultdict(lambda:[[],[]])
def cube(kind,x,y,z,w,d,h):
 v,f=buckets[kind];n=len(v);v.extend([(x+sx*w/2,y+sy*d/2,z+sz*h/2) for sz in [-1,1] for sy in [-1,1] for sx in [-1,1]])
 f.extend([(n+0,n+1,n+3,n+2),(n+4,n+6,n+7,n+5),(n+0,n+4,n+5,n+1),(n+2,n+3,n+7,n+6),(n+0,n+2,n+6,n+4),(n+1,n+5,n+7,n+3)])
# Manually bounded strips are the exposed regions visible between shields and edge connectors.
zones=[(-1.28,.22,44,3,.036,.027),(-1.24,.39,40,2,.039,.029),(-1.18,.94,38,2,.041,.025),(-1.34,.49,4,17,.030,.025),(1.27,.40,4,18,.028,.027)]
count=0
for zi,(x0,y0,cols,rows,dx,dy) in enumerate(zones):
 for row in range(rows):
  for col in range(cols):
   if (col*7+row*11+zi)%9==0 or (col//5+row*2+zi)%7==0:continue
   x=x0+col*dx+(((col*17+row*19+zi*3)%11)-5)*.0008;y=y0+row*dy+(((col*13+row*23+zi*7)%9)-4)*.0007;w=[.012,.016,.020][(col+row*2)%3];d=[.009,.012][(col+zi)%2];z=.026
   if (col+row+zi)%4==0:
    cube('dark',x,y,z,.025,.021,.014)
    for side in [-1,1]:cube('solder',x+side*.013,y,z,.004,.018,.011)
   else:
    cube('ceramic',x,y,z,w,d,.008)
    for side in [-1,1]:cube('solder',x+side*w*.46,y,z,.003,d,.009)
   if (col+row)%3==0:cube('via',x+.013,y+.009,.021,.004,.004,.001)
   count+=1
# Additional grouped rectangular, unidentified silhouettes reflect larger packages visible in photos.
for x,y,w,d in [(-1.19,.45,.06,.042),(-1.07,.43,.07,.04),(-.73,.40,.09,.04),(-.43,.42,.08,.05),(-.14,.39,.06,.04),(.07,.39,.07,.04),(.33,.4,.055,.038),(1.33,.50,.07,.055),(1.32,.72,.07,.04)]:
 cube('dark',x,y,.032,w,d,.02)
 for side in [-1,1]:cube('solder',x+side*(w*.48),y,.026,.006,d*.7,.008)
for key,(verts,faces) in buckets.items():
 mesh=bpy.data.meshes.new('R06_'+key);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('Photo-guided micro geometry · '+key,mesh);bpy.context.collection.objects.link(o);o.parent=grp;o.data.materials.append(mat[key]);o.hide_render=False
# Pouch faces are slightly crowned; the deformation is a material study, not a measured shape.
for o in list(scene.objects):
 if o.name=='Battery pouch' or o.name.startswith('Battery pouch.'):
  bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
  sub=o.modifiers.new('Gentle pouch surface','SUBSURF');sub.subdivision_type='SIMPLE';sub.levels=3;bpy.ops.object.modifier_apply(modifier=sub.name)
  coords=[v.co for v in o.data.vertices];mx=max(abs(v.x) for v in coords);my=max(abs(v.y) for v in coords);mz=max(v.z for v in coords)
  for v in o.data.vertices:
   if v.co.z>mz*.8:
    ax=min(1,abs(v.co.x)/max(mx,1e-5));ay=min(1,abs(v.co.y)/max(my,1e-5));v.co.z+=.003*(1-ax*ax)*(1-ay*ay)
  for poly in o.data.polygons:poly.use_smooth=True
  o.select_set(False)
# Preserve a separate editable scene and export a new revision; retain earlier models.
bpy.ops.wm.save_as_mainfile(filepath=R+'/MacBook-Pro-14-M4-internals-r06.blend')
bpy.data.objects['DISPLAY_HINGE'].rotation_euler.x=0
bpy.ops.object.select_all(action='DESELECT')
for o in scene.objects:
 if o.type not in ['CAMERA','LIGHT']:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=R+'/public/models/macbook-m4-internals-r06.glb',export_format='GLB',export_extras=True,export_apply=True,use_selection=True,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=16)
meshes=[o for o in scene.objects if o.type=='MESH'];data={'revision':6,'meshes':len(meshes),'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in meshes),'visualMicrocomponentClusters':count,'classification':'Reference-guided visual reconstruction. Silhouettes and mechanical features are approximate; component identities, exact counts, electrical nets and locations are not established.','sources':['https://support.apple.com/en-us/120769','https://support.apple.com/en-us/120750','https://www.ifixit.com/Guide/MacBook+Pro+14-Inch+Late+2024+(M4)+Battery+Replacement/217910']}
json.dump(data,open(R+'/references/model-report-r06.json','w'),indent=2);print('REBUILD_COMPLETE',json.dumps(data),flush=True)
