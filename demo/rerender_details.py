import bpy, math, os
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent.parent
bpy.ops.wm.open_mainfile(filepath=str(R/'MacBook-Pro-14-M4-r10.blend'))
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=True
s.render.resolution_x=1440;s.render.resolution_y=1800;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.film_transparent=False
s.view_settings.view_transform='AgX'
for o in list(s.objects):
 if o.type in ['LIGHT','CAMERA']:bpy.data.objects.remove(o,do_unlink=True)
world=bpy.data.worlds.new('Demo charcoal studio');world.use_nodes=True;s.world=world;world.node_tree.nodes['Background'].inputs[0].default_value=(.018,.024,.031,1);world.node_tree.nodes['Background'].inputs[1].default_value=.35
for name,power,size,loc,color in [('Key',550,5,(1,-3,5),(0.83,.91,1)),('Rim',750,3,(-3,2,4),(.7,.84,1)),('Strip',350,2,(3,2,2),(1,.9,.76))]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=color;o.rotation_euler=(Vector((0,0,.5))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;s.camera=cam;cam.data.lens=55
roots=[o for o in s.objects if o.parent is None and o.type=='EMPTY'];saved={o.name:o.location.copy() for o in roots};lid=bpy.data.objects['DISPLAY_HINGE']
for m in bpy.data.materials:
 if not m.use_nodes:continue
 p=m.node_tree.nodes.get('Principled BSDF')
 if p and 'Emission Strength' in p.inputs:p.inputs['Emission Strength'].default_value=0
 if p and 'Space black' in m.name:p.inputs['Base Color'].default_value=(.035,.04,.047,1);p.inputs['Roughness'].default_value=.31
# Clean luminous display, with a subdued studio-blue background.
m=bpy.data.objects['DISPLAY_PIXELS'].data.materials[0];p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.006,.012,.019,1);p.inputs['Emission Color'].default_value=(.018,.055,.085,1);p.inputs['Emission Strength'].default_value=.8

def visible(o,v):
 o.hide_render=not v
 for c in o.children_recursive:c.hide_render=not v

def setup(names,lidangle=108):
 for o in roots:o.location=saved[o.name].copy();visible(o,o.name in names)
 lid.rotation_euler.x=math.radians(90-lidangle)
 for o in s.objects:
  if o.type=='MESH':
   if o.parent and o.parent.name=='LOGIC_BOARD' and o.data.materials and not o.data.materials[0].name.startswith(('Soldermask','R05 · graphite substrate')):o.hide_render=True
   if any(m.name=='PCB silkscreen' for m in o.data.materials):o.hide_render=True
   parent=o.parent
   while parent:
    if parent.name.startswith(('NAND_','DRAM_')):o.hide_render=True
    parent=parent.parent
   for mod in o.modifiers:
    if mod.type=='WEIGHTED_NORMAL':mod.show_render=True

def render(i,pos,target,lens=55):
 if i not in [2,3,5]:return
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens;s.render.filepath=str(R/f'demo/renders/{i:02}.png');bpy.ops.render.render(write_still=True);print('SHOT_COMPLETE',i,flush=True)
exterior=['ENCLOSURE','TOP_DECK','KEYBOARD','TRACKPAD','DISPLAY_HINGE','BOTTOM_COVER','IO_BOARDS','LOWER_CASE_FASTENERS','ANTENNA_VENT']
setup(exterior,0);render(0,(3.6,-4.8,3.8),(0,0,.05),53)
setup(exterior);render(1,(3.9,-5.3,3.0),(0,0,.8),52)
inside=[o.name for o in roots if o.name not in ['TOP_DECK','KEYBOARD','TRACKPAD','DISPLAY_HINGE']]
setup(inside);render(2,(1.0,-2.6,4.4),(0,.13,0),52)
setup(['ENCLOSURE','LOGIC_BOARD','COOLING_FAN','THERMAL_ASSEMBLY','FLEX_CABLES']);
for n,z in [('THERMAL_ASSEMBLY',.44),('FLEX_CABLES',.26)]:bpy.data.objects[n].location.z+=z
bpy.data.objects['R05_BOARD_SHIELDS'].location.z+=.7
render(3,(1.1,-2.3,2.6),(-.3,.65,.22),62)
# Fan shroud and rotor separate visibly; source fan geometry remains unchanged.
setup(['COOLING_FAN','THERMAL_ASSEMBLY']);fan=bpy.data.objects['COOLING_FAN'];rot=bpy.data.objects['FAN_ROTOR'];rot.location.z+=.32
sh=[]
for o in fan.children:
 if o.type=='MESH' and o.data.materials and o.data.materials[0].name=='R05 · fan shroud':o.location.z+=.9;sh.append(o)
render(4,(2.1,-1.1,1.9),(.90,.65,.25),65)
rot.location.z-=.32
for o in sh:o.location.z-=.9
# Full layered machine, showing separation without transparent metal.
setup([o.name for o in roots],90)
for n,z in [('BOTTOM_COVER',-.55),('LOGIC_BOARD',.38),('THERMAL_ASSEMBLY',.65),('FLEX_CABLES',.55),('TOP_DECK',1.00),('KEYBOARD',1.01),('TRACKPAD',1.00),('DISPLAY_HINGE',1.03)]:bpy.data.objects[n].location.z+=z
render(5,(4.5,-6.4,4.3),(0,0,.8),49)
setup(exterior);render(6,(-3.6,-5.1,2.5),(0,0,.65),52)
print('DEMO_RENDERS_COMPLETE',flush=True)
