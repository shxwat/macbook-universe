"""Revision 05: visual reconstruction from base-M4 Apple/iFixit service imagery.
Non-labeled package details and positions are visual approximations, not a schematic.
The previous Blender scene and GLB are preserved; this produces new files.
"""
import bpy, math, os, json
from collections import defaultdict
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=R+'/MacBook-Pro-14-M4.blend')
scene=bpy.context.scene
for o in scene.objects:o.hide_render=False
for name in ['BATTERY','COOLING_FAN','LOGIC_BOARD','FLEX_CABLES','THERMAL_ASSEMBLY','SPEAKERS']:
 print('assembly',name,flush=True)

def material(name,color,metal=0,rough=.45):
 m=bpy.data.materials.get(name) or bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
m={
 'board':material('R05 · graphite substrate',(.032,.036,.041),.16,.6),
 'cell':material('R05 · laminated battery',(.025,.027,.031),.12,.52),
 'edge':material('R05 · folded pouch seams',(.075,.077,.080),.38,.48),
 'shield':material('R05 · black RF shields',(.019,.021,.025),.48,.42),
 'thermal':material('R05 · thermal assembly dark coating',(.045,.048,.053),.5,.4),
 'fan':material('R05 · fan shroud',(.018,.021,.026),.18,.5),
 'metal':material('R05 · fastener steel',(.31,.33,.35),.82,.35),
 'matte':material('R05 · polymer',(.012,.014,.018),.06,.6),
 'flex':material('R05 · cable backing',(.026,.029,.032),.22,.52),
 'contact':material('R05 · connector contacts',(.35,.24,.12),.65,.4),
 'print':material('R05 · enclosure marking',(.21,.23,.24),.05,.7),
}

def root(name,component,parent,layer='internal'):
 o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.parent=parent;o['componentId']=component;o['layer']=layer;o['accuracy']='Reconstructed';o['source']='https://support.apple.com/en-us/120769';return o

def box(name,position,dimensions,material,parent,bevel=.004):
 bpy.ops.mesh.primitive_cube_add(size=1,location=position);o=bpy.context.object;o.name=name;o.dimensions=dimensions;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.parent=parent;o.data.materials.append(m[material]);o.hide_render=False
 if bevel:
  b=o.modifiers.new('Small manufacturing radius','BEVEL');b.width=min(bevel,min(dimensions)*.44);b.segments=3;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=b.name);o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return o

def cylinder(name,pos,radius,depth,material,parent,vertices=20):
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=pos);o=bpy.context.object;o.name=name;o.parent=parent;o.data.materials.append(m[material]);o.hide_render=False;return o

def label(name,content,pos,size,material,parent):
 c=bpy.data.curves.new(name,'FONT');c.body=content;c.size=size;c.align_x='CENTER';c.align_y='CENTER';c.resolution_u=3
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.location=pos;o.parent=parent;c.materials.append(m[material]);bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.convert(target='MESH');o.select_set(False);return o

def path(name,points,width,material,parent):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.resolution_u=16;c.bevel_depth=width;c.bevel_resolution=4;s=c.splines.new('BEZIER');s.bezier_points.add(len(points)-1)
 for bp,p in zip(s.bezier_points,points):bp.co=p;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.parent=parent;c.materials.append(m[material]);bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.convert(target='MESH');o.select_set(False);o.hide_render=False;return o

def remove_children(o):
 for c in list(o.children_recursive):bpy.data.objects.remove(c,do_unlink=True)

def ring(name,r_outer,r_inner,z,thickness,parent,material):
 N=96;v=[]
 for zz in [z-thickness/2,z+thickness/2]:
  for radius in [r_outer,r_inner]:
   for i in range(N):a=math.tau*i/N;v.append((radius*math.cos(a),radius*math.sin(a),zz))
 f=[]
 for i in range(N):
  j=(i+1)%N;f.extend([(i,j,2*N+j,2*N+i),(N+j,N+i,3*N+i,3*N+j),(2*N+i,2*N+j,3*N+j,3*N+i),(j,i,N+i,N+j)])
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(v,[],f);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);o.parent=parent;o.data.materials.append(m[material]);o.hide_render=False
 b=o.modifiers.new('Shroud edge','BEVEL');b.width=.003;b.segments=2;bpy.context.view_layer.objects.active=o;bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.ops.object.modifier_apply(modifier=b.name);o.select_set(False);o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');return o

# The six-cell arrangement follows the photographed service assembly: four outer cells,
# two central cells. Sizes and contours are hand-reconstructed from photos.
battery=bpy.data.objects['BATTERY'];
for o in list(battery.children):
 if o.name.startswith('CELL_BANK_'):remove_children(o);bpy.data.objects.remove(o,do_unlink=True)
cells=[(-.92,.00,.58,.43),(-.92,-.52,.58,.43),(-.30,-.27,.56,.95),(.30,-.27,.56,.95),(.92,.00,.58,.43),(.92,-.52,.58,.43)]
for i,(x,y,w,d) in enumerate(cells):
 group=root('R05_CELL_%02d'%i,'battery',battery,'cell');group['source']='https://www.ifixit.com/Guide/MacBook+Pro+14-Inch+Late+2024+(M4)+Battery+Replacement/217910'
 box('Laminated pouch edge',(x,y,-.006),(w+.018,d+.018,.034),'edge',group,.012)
 box('Battery pouch',(x,y,.014),(w,d,.040),'cell',group,.015)
 # Only the centre pouches bear reconstructed generic safety markings.
 if i in [2,3]:
  label('Generic cell chemistry','Li-ion',(x,y+.17,.035),.036,'print',group)
  for k in range(8):box('Fine safety marking',(x,y+.06-k*.037,.035),(w*(.43+(k%3)*.035),.0014,.0009),'print',group,0)
 # Perimeter seam and pull-tab shape are approximations from the guide photographs.
 for side in [-1,1]:box('Pouch edge seal',(x+side*(w/2-.012),y,.035),(.006,d*.88,.001),'edge',group,.0002)

# Replace the exaggerated battery board with a low profile central bridge.
bmu=bpy.data.objects['BATTERY_MANAGEMENT'];remove_children(bmu)
box('Battery management bridge',(0,.27,.012),(.35,.115,.026),'board',bmu,.005)
box('Battery connector housing',(0,.30,.031),(.17,.052,.018),'matte',bmu,.003)
for i in range(10):box('Connector contact',(-.07+i*.015,.274,.041),(.004,.013,.002),'contact',bmu,.0001)
cylinder('Bridge retaining fastener',(.11,.29,.037),.009,.007,'metal',bmu)

# Darken the substrate and replace saturated metallic material assignments.
board=bpy.data.objects['LOGIC_BOARD']
for obj in board.children:
 if obj.type=='MESH' and obj.data.materials and 'Soldermask' in obj.data.materials[0].name:obj.data.materials.clear();obj.data.materials.append(m['board'])
# Major shield outlines follow service photos; individual package identity is intentionally unassigned.
shields=root('R05_BOARD_SHIELDS','board',board)
shield_specs=[(-1.09,.77,.27,.27),(-.78,.82,.31,.18),(-.80,.58,.59,.18),(-.39,.85,.29,.19),(-.37,.59,.38,.22),(.13,.47,.24,.25),(.32,.82,.16,.19),(-1.25,.46,.16,.16)]
for i,(x,y,w,d) in enumerate(shield_specs):
 box('EMI shield %02d'%i,(x,y,.036),(w,d,.035),'shield',shields,.007)
 for side in [-1,1]:box('Shield seam',(x+side*(w/2-.004),y,.054),(.002,d*.9,.0014),'metal',shields,0)
 for xx in [-1,1]:
  for yy in [-1,1]:cylinder('Shield corner pin',(x+xx*(w/2-.012),y+yy*(d/2-.012),.056),.003,.003,'metal',shields,12)
# Fine mechanical points, not identified ICs or simulated electrical traces.
for x,y in [(-1.32,.38),(-1.19,.97),(-.93,.39),(-.6,.38),(-.28,.37),(.03,.39),(.34,.39),(.44,.95)]:
 cylinder('Board screw boss',(x,y,.026),.026,.014,'metal',shields,24);cylinder('Board screw well',(x,y,.034),.009,.004,'matte',shields,16)
 for a in range(4):
  r=math.tau*a/4;box('Fastener recess',(x+.004*math.cos(r),y+.004*math.sin(r),.037),(.006,.002,.001),'matte',shields,0)

# Matte black heat spreader and a pair of dark-coated flattened heat pipes.
thermal=bpy.data.objects['THERMAL_ASSEMBLY'];remove_children(thermal)
box('Thermal contact shield',(-.27,.69,.071),(.54,.31,.028),'thermal',thermal,.02)
for offset in [-.034,.034]:
 o=path('Coated heat pipe',[(-.15,.69+offset,.088),(.05,.72+offset,.090),(.37,.84+offset,.09),(.59,.92+offset,.088)],.022,'thermal',thermal);o.scale.z=.36
box('Finned radiator casing',(.84,1.00,.067),(.62,.10,.088),'fan',thermal,.01)
for i in range(48):box('Heatsink fin',(.56+i*.012,1.006,.071),(.004,.085,.06),'metal',thermal,.0003)

# The real fan is under a broad dark volute housing; only the centre intake is exposed.
fan=bpy.data.objects['COOLING_FAN']
for o in list(fan.children):
 if o.type=='MESH' and 'Shielding' in o.name:bpy.data.objects.remove(o,do_unlink=True)
ring('Fan shroud',.438,.155,.088,.025,fan,'fan')
box('Fan exhaust duct',(0,.405,.080),(.48,.12,.05),'fan',fan,.01)
for angle in [math.radians(35),math.radians(150),math.radians(240),math.radians(320)]:
 x=.405*math.cos(angle);y=.405*math.sin(angle)
 cylinder('Fan mounting boss',(x,y,.091),.022,.017,'fan',fan);cylinder('Fan mounting screw',(x,y,.102),.010,.007,'metal',fan,20)
# Existing radial rotor remains separate and spins under the shroud.
rotor=bpy.data.objects['FAN_ROTOR']
for obj in rotor.children:
 if obj.type=='MESH' and ('label' in obj.name.lower() or 'motor' in obj.name.lower()):obj.hide_render=False
cylinder('Fan motor centre',(0,0,.116),.074,.009,'metal',rotor,48)

# Replace generic speaker holes/visible copper with enclosed side speaker geometry.
speakers=bpy.data.objects['SPEAKERS'];remove_children(speakers)
for side in [-1,1]:
 x=side*1.35
 box('Speaker enclosure',(x,-.30,.0),(.25,1.16,.07),'matte',speakers,.055)
 box('Speaker driver gasket',(x,-.73,.04),(.18,.24,.014),'fan',speakers,.05)
 box('Oval driver diaphragm',(x,-.73,.049),(.145,.20,.01),'cell',speakers,.05)
 for y in [-.96,.19]:cylinder('Speaker mount',(x,y,.038),.012,.008,'metal',speakers,16)

# Ten model-specific flex connectors and eight cowlings are documented by Apple.
# Exact placement here is photo-guided; the shape is not an electrical netlist.
cables=bpy.data.objects['FLEX_CABLES'];remove_children(cables)
for i,(x,y,w) in enumerate([(-1.28,.92,.13),(-1.06,.97,.14),(-.73,1.0,.26),(-.35,1.0,.17),(-.14,1.0,.19),(.22,1.0,.15),(1.35,.98,.15),(1.37,.78,.15),(1.37,.56,.15),(1.37,.37,.15)]):
 box('Flex connector %02d'%i,(x,y,.042),(w,.058,.022),'matte',cables,.003)
 for j in range(9):box('Fine connector contact',(x-w*.39+j*w*.097,y-.025,.054),(.003,.012,.002),'contact',cables,0)
# 8 service cowlings with screw counts matching the Apple removal list: 2+2+2+2+2+2+3+2.
for i,(x,y,w,count) in enumerate([(-1.28,.92,.13,2),(-1.06,.97,.14,2),(-.73,1.0,.18,2),(-.47,1.0,.18,2),(-.14,1.0,.15,2),(.22,1.0,.15,2),(1.35,.79,.24,3),(1.37,.38,.15,2)]):
 box('Connector cowling %02d'%i,(x,y,.062),(w+.035,.075,.011),'metal',cables,.004)
 for j in range(count):
  xx=x-(w*.43)+j*(w*.86/max(1,count-1));cylinder('Cowling fastener',(xx,y,.071),.006,.006,'matte',cables,16)
# Trackpad flex is visually prominent in the reference and crosses the battery cover.
box('Trackpad flex backing',(0,-.29,.062),(.145,1.02,.009),'flex',cables,.006)
box('Trackpad flex connector',(0,.24,.072),(.20,.09,.016),'matte',cables,.004)
for y in [-.74,-.08]:box('Adhesive retainer',(0,y,.069),(.16,.08,.005),'shield',cables,.002)
# Additional hinge frame rails and machined standoffs; positions are reconstructed.
frame=root('R05_INTERNAL_FRAME','chassis',bpy.data.objects['ENCLOSURE'],'exterior')
for side in [-1,1]:
 box('Internal structural rail',(side*1.485,0,.022),(.035,1.95,.050),'thermal',frame,.005)
 for y in [-.91,-.55,0,.42,.86]:
  cylinder('Frame fastener boss',(side*1.46,y,.050),.018,.014,'metal',frame,20);cylinder('Frame screw recess',(side*1.46,y,.058),.007,.004,'matte',frame,16)

# GLB batches: join repeated new objects only within same parent/material.
groups=defaultdict(list)
for o in list(scene.objects):
 if o.type=='MESH' and o.parent and (o.parent.name.startswith('R05_') or o.parent in [cables,speakers,bmu,thermal,fan]):
  if o.name=='Fan lower housing':continue
  if o.data.materials:groups[(o.parent.name,o.data.materials[0].name)].append(o)
for key,objects in groups.items():
 if len(objects)<2:continue
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.join();bpy.context.object.name='__'.join(key)
# Save an editable scene with all internals visible in viewport. Keep previous files intact.
bpy.ops.wm.save_as_mainfile(filepath=R+'/MacBook-Pro-14-M4-internals-r05.blend')
bpy.data.objects['DISPLAY_HINGE'].rotation_euler.x=0
bpy.ops.object.select_all(action='DESELECT')
for o in scene.objects:
 if o.type not in ['CAMERA','LIGHT']:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=R+'/public/models/macbook-m4-internals-r05.glb',export_format='GLB',export_extras=True,export_apply=True,use_selection=True,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=16)
meshes=[o for o in scene.objects if o.type=='MESH'];data={'revision':5,'meshCount':len(meshes),'triangleCount':sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in meshes),'batteryCells':6,'classification':'Photo-guided geometric reconstruction; exact positions and physical dimensions are not verified.','sources':['https://support.apple.com/en-us/120769','https://support.apple.com/en-us/120750','https://www.ifixit.com/Guide/MacBook+Pro+14-Inch+Late+2024+(M4)+Battery+Replacement/217910']}
json.dump(data,open(R+'/references/model-report-r05.json','w'),indent=2)
print('REBUILD_COMPLETE',json.dumps(data),flush=True)
