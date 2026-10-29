"""Revision 09: exterior clean-up on the editable revision 08 scene.
The lid back is left as plain anodized aluminum; no brand mark is modelled.
"""
import bpy
from pathlib import Path
R=Path(__file__).resolve().parent.parent
bpy.ops.wm.open_mainfile(filepath=str(R/'MacBook-Pro-14-M4-internals-r08.blend'))
old=bpy.data.objects.get('DISPLAY_HINGE__Keyboard recess')
if old: bpy.data.objects.remove(old,do_unlink=True)
# Remove any brand marks or trademark text inherited from earlier scenes.
for o in list(bpy.data.objects):
 if o.name.startswith(('R09 lid emblem','Lid insignia','Insignia leaf','Regulatory engraving')):
  bpy.data.objects.remove(o,do_unlink=True)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'MacBook-Pro-14-M4-exterior-r09.blend'))
print('EXTERIOR_R09_COMPLETE',flush=True)
