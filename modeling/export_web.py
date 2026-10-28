import bpy,os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=R+'/MacBook-Pro-14-M4.blend')
bpy.data.objects['DISPLAY_HINGE'].rotation_euler.x=0
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.context.scene.objects:
 if o.type not in ['CAMERA','LIGHT']:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=R+'/public/models/macbook-m4-detailed.glb',export_format='GLB',export_extras=True,export_apply=True,use_selection=True,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=16)
