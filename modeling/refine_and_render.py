import bpy,os,math,json
from mathutils import Vector
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=R+'/MacBook-Pro-14-M4.blend')
board=bpy.data.objects['LOGIC_BOARD'];pcb=bpy.data.materials['Soldermask · dark graphite green'];steel=bpy.data.materials['Shielding · brushed stainless'];chip=bpy.data.materials['IC package · epoxy'];ink=bpy.data.materials['PCB silkscreen'];keymat=bpy.data.materials['Keycap · satin black'];white=bpy.data.materials['Key legend · warm white']
def box(name,loc,size,mat,parent,bevel=.004):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.parent=parent;o.data.materials.append(mat)
 b=o.modifiers.new('Edge radii','BEVEL');b.width=min(bevel,min(size)*.3);b.segments=3;bpy.ops.object.modifier_apply(modifier=b.name);o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');return o
def txt(name,body,loc,size,parent,mat=white):
 c=bpy.data.curves.new(name,'FONT');c.body=body;c.size=size;c.align_x='CENTER';c.align_y='CENTER';c.resolution_u=3;o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.parent=parent;o.location=loc;c.materials.append(mat);bpy.context.view_layer.objects.active=o;bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.ops.object.convert(target='MESH');return o
box('PCB_lower_bridge',(0,.295,.005),(2.82,.18,.025),pcb,board,.014)
box('PCB_rear_bridge',(.15,1.005,.005),(2.56,.05,.025),pcb,board)
box('PCB_right_perimeter',(1.425,.66,.005),(.09,.65,.025),pcb,board)
# Populate the reconstructed bridge with grouped controller packages and passive arrays.
for i in range(12):
 x=-1.17+i*.21
 box('Bridge controller',(x,.30,.029),(.11,.09,.025),chip,board,.003)
 for j in [-1,1]:box('Controller termination',(x+j*.061,.30,.026),(.01,.073,.015),steel,board,.001)
for i in range(42):box('Bridge passive',(-1.3+i*.063,.37,.026),(.025,.017,.012),steel if i%3 else chip,board,.001)
# Complete the inverted-T arrow cluster with separately modelled up/down keycaps.
kr=bpy.data.objects['KEY_05_08'];kids=list(kr.children);b=next(o for o in kids if o.data.materials[0]==keymat);cx,cy,cz=b.location;w=b.dimensions.x
for o in kids:bpy.data.objects.remove(o,do_unlink=True)
for label,sgn in [('▲',1),('▼',-1)]:
 box('Arrow_'+label,(cx,cy+sgn*.043,cz),(w,.073,.025),keymat,kr,.01);txt('Arrow legend',label,(cx,cy+sgn*.043,.101),.034,kr)
# Consolidate newly generated board details into fixed material batches.
for mat in [pcb,steel,chip]:
 obs=[o for o in board.children if o.type=='MESH' and len(o.data.materials)==1 and o.data.materials[0]==mat]
 if len(obs)>1:
  bpy.ops.object.select_all(action='DESELECT')
  for o in obs:o.select_set(True)
  bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join()
bpy.ops.object.select_all(action='SELECT');bpy.ops.export_scene.gltf(filepath=R+'/public/models/macbook-m4-detailed.glb',export_format='GLB',export_extras=True,export_apply=True)
# Retain an editable Blender scene with studio lights and an exterior camera.
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24
scene.render.resolution_x=1440;scene.render.resolution_y=1080;scene.render.resolution_percentage=100
world=bpy.data.worlds.new('Studio HDR');world.use_nodes=True;scene.world=world
nodes=world.node_tree.nodes;env=nodes.new('ShaderNodeTexEnvironment');env.image=bpy.data.images.load(R+'/public/textures/studio.hdr');world.node_tree.links.new(env.outputs['Color'],nodes['Background'].inputs['Color']);nodes['Background'].inputs['Strength'].default_value=.5
for name,loc,power,size in [('Key',(1,-3,5),180,5),('Rim',(-4,1,3),200,3),('Top',(0,1,5),160,4)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,.5))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(4.0,-5.8,3.5));camera=bpy.context.object;camera.rotation_euler=(Vector((0,0,.7))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.lens=49;scene.camera=camera
# Match the local viewer's space-black finish.
mat=bpy.data.materials['Space black · anodized aluminum'];p=mat.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.04,.044,.05,1);p.inputs['Roughness'].default_value=.34
# Render exterior. Internals remain authored in the .blend; hide from this render only.
for o in scene.objects:
 if o.parent is None and o.get('layer') in ['internal']:o.hide_render=True
lid=bpy.data.objects['DISPLAY_HINGE'];lid.rotation_euler.x=math.radians(-18)
scene.render.image_settings.file_format='PNG';scene.render.filepath=R+'/references/blender-exterior.png'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=R+'/MacBook-Pro-14-M4.blend')
meshes=[o for o in scene.objects if o.type=='MESH'];report=json.load(open(R+'/references/model-report.json'));report['meshes']=len(meshes);report['triangles']=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in meshes);report['keycaps']=78;report['revision']=2;json.dump(report,open(R+'/references/model-report.json','w'),indent=2)
bpy.ops.render.render(write_still=True)
