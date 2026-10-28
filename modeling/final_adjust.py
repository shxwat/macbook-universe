import bpy,os,json
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=R+'/MacBook-Pro-14-M4.blend')
for o in bpy.context.scene.objects:
 if o.parent is None and o.get('layer')=='internal':o.scale.z=.5;o.location.z=o.location.z*.5-.015
# Export only model objects, with no studio cameras/lights and no render-only visibility flags.
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.context.scene.objects:
 if o.type not in ['CAMERA','LIGHT']:o.select_set(True)
bpy.data.objects['DISPLAY_HINGE'].rotation_euler.x=0
bpy.ops.export_scene.gltf(filepath=R+'/public/models/macbook-m4-detailed.glb',export_format='GLB',export_extras=True,export_apply=True,use_selection=True)
bpy.data.objects['DISPLAY_HINGE'].rotation_euler.x=-.314159
# Hide all internal descendants from the exterior render.
for o in bpy.context.scene.objects:
 if o.parent is None and o.get('layer')=='internal':
  o.hide_render=True
  for child in o.children_recursive:child.hide_render=True
nodes=bpy.context.scene.world.node_tree.nodes;links=bpy.context.scene.world.node_tree.links
lp=nodes.new('ShaderNodeLightPath');mix=nodes.new('ShaderNodeMixShader');dark=nodes.new('ShaderNodeBackground');dark.inputs[0].default_value=(.008,.011,.016,1)
links.new(nodes['Background'].outputs[0],mix.inputs[1]);links.new(dark.outputs[0],mix.inputs[2]);links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);links.new(mix.outputs[0],nodes['World Output'].inputs[0])
bpy.ops.wm.save_as_mainfile(filepath=R+'/MacBook-Pro-14-M4.blend')
bpy.context.scene.render.filepath=R+'/references/blender-exterior.png';bpy.ops.render.render(write_still=True)
