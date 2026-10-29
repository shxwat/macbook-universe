"""R10: correct closed envelope, rebuild display as non-overlapping optical surfaces.
31.26 x 22.12 x 1.55 cm envelope from Apple 121552. Small radii/positions reconstructed.
"""
import bpy, math, json
from pathlib import Path
R=Path(__file__).resolve().parent.parent
bpy.ops.wm.open_mainfile(filepath=str(R/'MacBook-Pro-14-M4-exterior-r09.blend'))
scene=bpy.context.scene
for o in scene.objects:o.hide_render=False
# Original body/keyboard stack was taller than the published closed device.
# Scale all horizontal assemblies together so ports, top case and internals retain registration.
for o in scene.objects:
 if o.parent is None and o.type=='EMPTY' and o.name!='DISPLAY_HINGE':
  o.scale.z*=.55;o.location.z*=.55
lid=bpy.data.objects['DISPLAY_HINGE'];lid.location.z=.077425;lid.rotation_euler.x=0
for o in list(lid.children):
 for c in list(o.children_recursive):bpy.data.objects.remove(c,do_unlink=True)
 bpy.data.objects.remove(o,do_unlink=True)
wrapper=bpy.data.objects.new('R10_DISPLAY_STRUCTURE',None);bpy.context.collection.objects.link(wrapper);wrapper.parent=lid;wrapper.scale.y=.5

def material(name,c,metal=0,rough=.4,emit=0):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*c,1);p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 if emit:p.inputs['Emission Color'].default_value=(*c,1);p.inputs['Emission Strength'].default_value=emit
 return m
body=bpy.data.materials['Space black · anodized aluminum'];p=body.node_tree.nodes.get('Principled BSDF');p.inputs['Metallic'].default_value=.8;p.inputs['Roughness'].default_value=.29
seal=bpy.data.materials['Elastomer seals'];glass=material('R10 · black display border',(.003,.0035,.004),.08,.18)
screen=material('R10 · LCD self luminous',(.005,.008,.012),0,1,.5)

def contour(w,h,r):
 p=[]
 for cx,cz,a in [(w/2-r,h/2-r,0),(-w/2+r,h/2-r,90),(-w/2+r,-h/2+r,180),(w/2-r,-h/2+r,270)]:
  for j in range(25):
   t=math.radians(a+j*90/24);p.append((cx+math.cos(t)*r,cz+math.sin(t)*r))
 return p

def panel(name,w,h,r,y,z,mat,thickness=0):
 ps=contour(w,h,r);n=len(ps);v=[(x,y,zz+z) for x,zz in ps];faces=[tuple(range(n))]
 if thickness:
  v+=[(x,y+thickness,zz+z) for x,zz in ps];faces+=[tuple(reversed(range(n,n*2)))];faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(v,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);o.parent=wrapper;o.data.materials.append(mat)
 if name=='DISPLAY_PIXELS':
  uv=mesh.uv_layers.new(name='Display UV')
  for face in mesh.polygons:
   for li in face.loop_indices:
    co=mesh.vertices[mesh.loops[li].vertex_index].co;uv.data[li].uv=((co.x/w)+.5,(co.z-z)/h+.5)
 if thickness:
  mod=o.modifiers.new('Continuous edge highlight','BEVEL');mod.width=.002;mod.segments=3;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name);o.modifiers.new('Machined surface normals','WEIGHTED_NORMAL')
 return o
# All coordinates use the existing hinge axis. Display face and border are separated in depth.
# Housing is now long enough to cover the palm rest when closed.
panel('R10 display rear housing',3.115,2.135,.091,-.0075,1.0575,body,.047)
panel('R10 perimeter elastomer',3.085,2.105,.080,-.018,1.0575,seal,.008)
panel('R10 display black border',3.055,2.077,.072,-.026,1.0575,glass,.003)
panel('DISPLAY_PIXELS',3.024,1.964,.048,-.032,1.104,screen)
# Notch is opaque black, not glass floating above the image.
panel('R10 camera notch',.288,.058,.012,-.034,2.062,glass,.001)
for x,r in [(0,.009),(-.052,.0038),(.055,.003)]:
 bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=8,radius=r,location=(x,-.0355,2.063));o=bpy.context.object;o.name='R10 camera lens' if x==0 else 'R10 sensor aperture';o.scale.y=.10;o.parent=wrapper;o.data.materials.append(bpy.data.materials['Camera lens coating'])
# Weighted normals prevent broad aluminum faces being shaded like inflated plastic.
for o in scene.objects:
 if o.type=='MESH' and o.data.materials and o.data.materials[0] in [body]:
  for poly in o.data.polygons:poly.use_smooth=False
# Retain a fully editable revision and a compressed local runtime asset.
bpy.ops.wm.save_as_mainfile(filepath=str(R/'MacBook-Pro-14-M4-r10.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in scene.objects:
 if o.type not in ['LIGHT','CAMERA']:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(R/'public/models/macbook-m4-r10.glb'),export_format='GLB',export_extras=True,export_apply=True,use_selection=True,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=18)
json.dump({'revision':10,'width_cm':31.26,'depth_cm':22.12,'closed_height_cm':1.55,'display_aspect':3.024/1.964,'classification':'Published envelope with reconstructed radii, seams, placement and optical layers.','source':'https://support.apple.com/en-us/121552'},open(R/'references/model-report-r10.json','w'),indent=2)
from mathutils import Vector
lid.rotation_euler.x=math.pi/2;bpy.context.view_layer.update()
exterior_roots=['ENCLOSURE','TOP_DECK','KEYBOARD','TRACKPAD','DISPLAY_HINGE','BOTTOM_COVER']
pts=[o.matrix_world@Vector(c) for name in exterior_roots for o in [bpy.data.objects[name]]+list(bpy.data.objects[name].children_recursive) if o.type=='MESH' for c in o.bound_box]
height=max(p.z for p in pts)-min(p.z for p in pts)
assert abs(height-.155)<.0005,('Closed exterior height mismatch',height)
report=json.load(open(R/'references/model-report-r10.json'));report['measured_closed_exterior_cm']=round(height*10,4);report['screen_surface']='Single-sided UV-mapped surface; no shadow reception in viewer';json.dump(report,open(R/'references/model-report-r10.json','w'),indent=2)
print('PASS_CLOSED_ENVELOPE',height,flush=True)
print('R10_COMPLETE',flush=True)
