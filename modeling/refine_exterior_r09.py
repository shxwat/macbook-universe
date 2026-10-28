"""Improve the exterior emblem on the existing editable revision 08 scene.
Logo silhouette based on the Simple Icons Apple SVG (CC0); placement and finish are visual approximations.
"""
import bpy, math, re
from pathlib import Path
R=Path(__file__).resolve().parent.parent
bpy.ops.wm.open_mainfile(filepath=str(R/'MacBook-Pro-14-M4-internals-r08.blend'))
old=bpy.data.objects.get('DISPLAY_HINGE__Keyboard recess')
if old: bpy.data.objects.remove(old,do_unlink=True)
lid=bpy.data.objects['DISPLAY_HINGE']
svg=(R/'references/apple-mark-simple-icons.svg').read_text()
d=re.search(r'<path d="([^"]+)',svg).group(1)
tokens=re.findall(r'[A-Za-z]|[-+]?(?:\d*\.\d+|\d+\.?\d*)',d)
paths=[]; points=[]; x=y=0.; i=0; command=''
while i<len(tokens):
 if tokens[i].isalpha(): command=tokens[i]; i+=1
 if command in ('M','m'):
  a,b=map(float,tokens[i:i+2]);i+=2
  x,y=(a,b) if command=='M' else (x+a,y+b)
  points=[(x,y)];paths.append(points);command='l'
 elif command=='c':
  vals=list(map(float,tokens[i:i+6]));i+=6
  p0=(x,y); p1=(x+vals[0],y+vals[1]);p2=(x+vals[2],y+vals[3]);p3=(x+vals[4],y+vals[5])
  for j in range(1,13):
   t=j/12; u=1-t
   points.append((u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0],u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]))
  x,y=p3
 elif command in ('z','Z'):
  command=''
 else: raise ValueError('Unsupported SVG command '+command)
mat=bpy.data.materials.new('R09 · polished dark lid emblem');mat.diffuse_color=(.028,.030,.033,1);mat.use_nodes=True
p=mat.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.028,.030,.033,1);p.inputs['Metallic'].default_value=.9;p.inputs['Roughness'].default_value=.19
for n,poly in enumerate(paths):
 verts=[((12-x)*.0155,.0402,1.015+(12-y)*.0155) for x,y in reversed(poly)]
 mesh=bpy.data.meshes.new('Lid emblem contour');mesh.from_pydata(verts,[],[list(range(len(verts)))]);mesh.update()
 obj=bpy.data.objects.new('R09 lid emblem '+str(n),mesh);bpy.context.collection.objects.link(obj);obj.parent=lid;obj.data.materials.append(mat);obj['accuracy']='Approximate silhouette and placement';obj['source']='Simple Icons Apple icon, CC0'
# Preserve the exported zero-angle pivot used by the viewer.
bpy.ops.wm.save_as_mainfile(filepath=str(R/'MacBook-Pro-14-M4-exterior-r09.blend'))
lid.rotation_euler.x=0
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.context.scene.objects:
 if o.type not in ['CAMERA','LIGHT']:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(R/'public/models/macbook-m4-exterior-r09.glb'),export_format='GLB',export_extras=True,export_apply=True,use_selection=True,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=16)
print('EXTERIOR_R09_COMPLETE',flush=True)
