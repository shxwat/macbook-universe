"""R08: add service-photo-guided structural rails and fasteners.
The precise locations and dimensions are reconstructed; screw counts can be sourced.
"""
import bpy, math, os, json
from collections import defaultdict
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=R+'/MacBook-Pro-14-M4-internals-r07.blend')
scene=bpy.context.scene
for o in scene.objects:o.hide_render=False

def mat(name,color,metal=.0,rough=.45):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
M={'rail':mat('R08 · structural graphite',(.065,.068,.071),.68,.42),'metal':mat('R08 · fasteners',(.24,.25,.26),.82,.38),'dark':mat('R08 · fastener recess',(.009,.010,.012),.1,.68),'contact':mat('R08 · metal contact',(.24,.135,.075),.72,.38),'adhesive':mat('R08 · adhesive tape',(.020,.022,.025),.12,.62)}
def root(name,part,parent,source):
 o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.parent=parent;o['componentId']=part;o['layer']='internal';o['accuracy']='Reconstructed';o['source']=source;return o

def box(name,loc,size,material,parent,bevel=.003):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.parent=parent;o.data.materials.append(M[material]);o.hide_render=False
 if bevel:
  mod=o.modifiers.new('Edge fillet','BEVEL');mod.width=min(bevel,min(size)*.4);mod.segments=2;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name);o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return o

def screw(name,x,y,z,parent):
 bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=.011,depth=.007,location=(x,y,z));o=bpy.context.object;o.name=name;o.parent=parent;o.data.materials.append(M['metal']);o.hide_render=False
 bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=.0053,depth=.001,location=(x,y,z+.004));c=bpy.context.object;c.name='Screw drive recess';c.parent=parent;c.data.materials.append(M['dark']);c.hide_render=False
 # An actual Torx Plus outline is not inferred from a small image; the drive is a generic recess.
 return o

track=bpy.data.objects['TRACKPAD_UNDERSIDE'];rail=root('R08_TRACKPAD_FRAME','trackpad',track,'https://support.apple.com/en-us/120762')
for side in [-1,1]:
 x=side*.61
 box('Trackpad mounting rail',(x,-.36,.055),(.045,.91,.018),'rail',rail,.004)
 for j in range(5):screw('Trackpad mounting screw',x,-.73+j*.18,.070,rail)
 for y in [-.80,-.20]:box('Frame retention clip',(x,y,.068),(.072,.073,.015),'adhesive',rail,.006)
box('Lower trackpad cross brace',(0,-.84,.052),(1.20,.05,.024),'rail',rail,.004)
for x in [-.49,.49]:screw('Cross brace fastener',x,-.84,.068,rail)
# Four visible copper-colored contacts and black insulation at the front edge are shape-only visual reconstructions.
bridge=root('R08_FRONT_CONTACTS','bmu',bpy.data.objects['BATTERY'],'https://support.apple.com/en-us/120760')
box('Contact carrier',(0,-.91,.020),(.74,.115,.025),'dark',bridge,.008)
for x in [-.27,-.09,.09,.27]:box('Unidentified contact pad',(x,-.91,.036),(.12,.065,.009),'contact',bridge,.002)
for x in [-.37,.37]:screw('Carrier fastener',x,-.91,.038,bridge)
# Connector adhesive retainers and insulating films seen in service photographs.
cables=bpy.data.objects['FLEX_CABLES'];ribbon=root('R08_FLEX_FINISH','cables',cables,'https://support.apple.com/en-us/120769')
for x,y,w,d in [(-1.12,.92,.22,.08),(-.57,.95,.20,.065),(-.15,.95,.24,.07),(.28,.94,.19,.065),(1.30,.76,.10,.15)]:
 box('Insulating connector tape',(x,y,.08),(w,d,.003),'adhesive',ribbon,.001)
# Batch same-material hardware per assembly for responsive WebGL rendering.
groups=defaultdict(list)
for o in scene.objects:
 if o.type=='MESH' and o.parent and o.parent.name.startswith('R08_') and o.data.materials:groups[(o.parent.name,o.data.materials[0].name)].append(o)
for key,objects in groups.items():
 if len(objects)<2:continue
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.join();bpy.context.object.name='__'.join(key)
bpy.ops.wm.save_as_mainfile(filepath=R+'/MacBook-Pro-14-M4-internals-r08.blend')
bpy.data.objects['DISPLAY_HINGE'].rotation_euler.x=0
bpy.ops.object.select_all(action='DESELECT')
for o in scene.objects:
 if o.type not in ['CAMERA','LIGHT']:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=R+'/public/models/macbook-m4-internals-r08.glb',export_format='GLB',export_extras=True,export_apply=True,use_selection=True,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=16)
meshes=[o for o in scene.objects if o.type=='MESH'];data={'revision':8,'meshes':len(meshes),'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in meshes),'classification':'Photo-guided visual reconstruction; dimensions, component locations and electrical relationships remain approximate.','note':'The iFixit guide warns that some photographs show a previous model. No exact M4 cell dimensions or circuit nets are inferred from them.','sources':['https://support.apple.com/en-us/120769','https://support.apple.com/en-us/120750','https://support.apple.com/en-us/120762','https://www.ifixit.com/Guide/MacBook+Pro+14-Inch+Late+2024+(M4)+Battery+Replacement/217910']}
json.dump(data,open(R+'/references/model-report-r08.json','w'),indent=2);print('REBUILD_COMPLETE',json.dumps(data),flush=True)
