"""Blender-authored visual reconstruction. Published envelope; approximate internal geometry.
Run: blender -b --python modeling/build_macbook.py
"""
import bpy, math, os, random, json
from mathutils import Vector
from collections import defaultdict
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
random.seed(24)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for d in list(bpy.data.materials):bpy.data.materials.remove(d)
def mat(name,c,metal=0,rough=.4,emission=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 if emission:p.inputs['Emission Color'].default_value=(*c,1);p.inputs['Emission Strength'].default_value=emission
 return m
m={
'body':mat('Space black · anodized aluminum',(.115,.125,.14),.9,.27),
'edge':mat('Diamond-cut edge',(.26,.28,.30),.98,.23),
'key':mat('Keycap · satin black',(.012,.015,.019),.08,.46),
'well':mat('Keyboard recess',(.006,.008,.011),.15,.4),
'white':mat('Key legend · warm white',(.66,.70,.73),0,.5,.25),
'glass':mat('Display cover glass',(.006,.009,.014),.15,.09),
'rubber':mat('Elastomer seals',(.009,.011,.014),0,.83),
'pcb':mat('Soldermask · dark graphite green',(.016,.035,.031),.35,.36),
'copper':mat('Copper heat transfer',(.29,.12,.045),.92,.28),
'gold':mat('Gold contacts',(.47,.31,.09),.85,.26),
'steel':mat('Shielding · brushed stainless',(.3,.32,.35),.95,.32),
'chip':mat('IC package · epoxy',(.015,.018,.022),.12,.38),
'cell':mat('Cell pouch · graphite polymer',(.026,.029,.034),.25,.47),
'foil':mat('Cell pouch seam',(.09,.095,.10),.8,.35),
'flex':mat('Polyimide flex cable',(.16,.07,.018),.45,.43),
'cap':mat('MLCC ceramic',(.29,.23,.17),.25,.52),
'ink':mat('PCB silkscreen',(.38,.43,.4),.05,.6),
'blue':mat('Camera lens coating',(.014,.043,.08),.6,.1),
'screen':mat('Screen placeholder',(.015,.045,.07),.1,.25,1),
}
roots={}
def root(name,part,layer='internal',parent=None):
 o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o['componentId']=part;o['layer']=layer;o['accuracy']='Reconstructed' if layer=='exterior' else 'Approximate';o['source']='https://support.apple.com/en-us/120927';o.parent=parent;roots[name]=o;return o
base=root('ENCLOSURE','chassis','exterior');deck=root('TOP_DECK','chassis','deck');keys=root('KEYBOARD','keyboard','deck');track=root('TRACKPAD','trackpad','deck');lid=root('DISPLAY_HINGE','display','lid');lid.location=(0,1.035,.075)
bottom=root('BOTTOM_COVER','bottom','bottom');board=root('LOGIC_BOARD','board');battery=root('BATTERY','battery');fan=root('COOLING_FAN','fan');heat=root('THERMAL_ASSEMBLY','thermal');speaker=root('SPEAKERS','speakers');ports=root('IO_BOARDS','ports');cables=root('FLEX_CABLES','cables');fast=root('LOWER_CASE_FASTENERS','bottom','fasteners');antenna=root('ANTENNA_VENT','antenna');
all_mesh=[]
def finish(o,name,material,parent,part=None):
 o.name=name;o.data.materials.append(m[material]);o.parent=parent
 if part:o['componentId']=part
 all_mesh.append(o);return o

def box(name,loc,size,material,parent,bevel=.005,part=None):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  b=o.modifiers.new('Machined radii','BEVEL');b.width=min(bevel,min(size)*.44);b.segments=3
  bpy.ops.object.modifier_apply(modifier=b.name)
  n=o.modifiers.new('Surface normals','WEIGHTED_NORMAL');n.keep_sharp=True
 return finish(o,name,material,parent,part)
def plate(name,loc,w,d,h,r,material,parent):
 verts=[]
 for z in [-h/2,h/2]:
  for cx,cy,a in [(w/2-r,d/2-r,0),(-w/2+r,d/2-r,90),(-w/2+r,-d/2+r,180),(w/2-r,-d/2+r,270)]:
   for j in range(13):
    t=math.radians(a+j*90/12);verts.append((cx+math.cos(t)*r,cy+math.sin(t)*r,z))
 n=52;faces=[tuple(reversed(range(n))),tuple(range(n,n*2))]
 for i in range(n):j=(i+1)%n;faces.append((i,j,j+n,i+n))
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);o.location=loc;finish(o,name,material,parent)
 b=o.modifiers.new('Micro edge break','BEVEL');b.width=min(.003,h*.2);b.segments=2
 bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=b.name)
 o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');return o

def cyl(name,loc,r,h,material,parent,vertices=32,rotation=None,part=None):
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=h,location=loc);o=bpy.context.object
 if rotation:o.rotation_euler=rotation
 for p in o.data.polygons:p.use_smooth=abs(p.normal.z)<.5
 return finish(o,name,material,parent,part)
def text(name,body,loc,size,material,parent,rot=(0,0,0)):
 c=bpy.data.curves.new(name,'FONT');c.body=body;c.size=size;c.align_x='CENTER';c.align_y='CENTER';c.resolution_u=3
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=rot;o.parent=parent;o.data.materials.append(m[material]);bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o.select_set(False);all_mesh.append(o);return o

def curve(name,points,r,material,parent):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.resolution_u=12;c.bevel_depth=r;c.bevel_resolution=3;s=c.splines.new('BEZIER');s.bezier_points.add(len(points)-1)
 for bp,p in zip(s.bezier_points,points):bp.co=p;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.parent=parent;o.data.materials.append(m[material]);bpy.context.view_layer.objects.active=o;bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.ops.object.convert(target='MESH');o.select_set(False);all_mesh.append(o);return o

def cut(o,cutter):
 bpy.context.view_layer.objects.active=o;b=o.modifiers.new('Precision opening','BOOLEAN');b.operation='DIFFERENCE';b.object=cutter
 bpy.ops.object.modifier_apply(modifier=b.name);all_mesh.remove(cutter);bpy.data.objects.remove(cutter,do_unlink=True)
# Hollow milled shell, with a continuous perimeter. Top deck is a separate revealable mesh.
shell=plate('Milled unibody frame',(0,0,0),3.126,2.212,.132,.115,'body',base)
cutter=plate('Internal pocket',(0,0,.035),2.998,2.085,.16,.09,'body',base);cut(shell,cutter)
top=plate('Palm rest and keyboard deck',(0,0,.068),3.112,2.198,.026,.11,'body',deck)
cut(top,plate('Keyboard pocket',(0,.30,.075),2.56,1.19,.08,.055,'well',deck))
cut(top,plate('Trackpad opening',(0,-.665,.075),1.32,.715,.08,.045,'well',deck))
plate('Keyboard recessed backplate',(0,.30,.057),2.56,1.19,.016,.055,'well',keys)
# 78-key US-inspired layout; exact key widths and legends are reconstructed.
rows=[ [('esc',1.55)]+[(f'F{i}',1) for i in range(1,13)]+[('◎',1)],
[(s,1) for s in ['`','1','2','3','4','5','6','7','8','9','0','−','=']]+[('delete',1.55)],
[('tab',1.5)]+[(s,1) for s in ['Q','W','E','R','T','Y','U','I','O','P','[',']']]+[('\\',1.05)],
[('caps lock',1.8)]+[(s,1) for s in ['A','S','D','F','G','H','J','K','L',';',"'"]]+[('return',1.8)],
[('shift',2.35)]+[(s,1) for s in ['Z','X','C','V','B','N','M',',','.','/']]+[('shift',2.35)],
[('fn',1),('control',1),('option',1),('command',1.25),(' ',5.6),('command',1.25),('option',1),('◀',1),('▲',1),('▶',1)]]
for ri,row in enumerate(rows):
 unit=2.43/sum(w for _,w in row);x=-1.215;yy=.80-ri*.194
 for ci,(label,w) in enumerate(row):
  width=unit*w-.024;cx=x+unit*w/2;x+=unit*w
  kr=root(f'KEY_{ri:02}_{ci:02}','keyboard','key',keys)
  plate(f'Keycap_{ri}_{ci}',(cx,yy,.087),width,.166,.025,.021,'key',kr)
  if ri==0 and ci==13:
   cyl('Touch ID sensor',(cx,yy,.103),.058,.006,'glass',kr)
   cyl('Touch ID ring',(cx,yy,.101),.063,.004,'edge',kr)
  elif label.strip():text('Legend_'+label,label,(cx,yy,.101),.034 if len(label)>2 else .049,'white',kr)
  if ri==1 and ci in range(1,11):text('Secondary legend','!@#$%^&*()'[ci-1],(cx,yy+.045,.101),.024,'white',kr)
  if label=='caps lock':cyl('Caps indicator',(cx-.09,yy,.103),.005,.002,'white',kr,12)
# Inverted T arrow cluster, split up/down on its middle key.
plate('Trackpad precision gap',(0,-.665,.064),1.32,.715,.018,.045,'well',track)
plate('Force Touch glass',(0,-.665,.075),1.305,.70,.013,.042,'body',track)
# Lip recess for fingertip.
notch=plate('Opening lip',(0,-1.099,.060),.42,.07,.06,.025,'body',base);cut(shell,notch)
# Speaker grille perforations consolidated later into two material batches.
for side in [-1,1]:
 for ix in range(8):
  for iy in range(61):
   x=side*(1.337+ix*.019);y=-.30+iy*.018
   cyl('Speaker perforation',(x,y,.083),.0045,.0012,'well',deck,8)
# Bottom cover, feet, case fasteners.
plate('Lower case',(0,0,-.071),3.115,2.20,.018,.115,'body',bottom)
for x in [-1.20,1.20]:
 for y in [-.83,.82]:
  cyl('Rubber foot',(x,y,-.089),.107,.023,'rubber',bottom,48)
  cyl('Foot center',(x,y,-.103),.077,.003,'rubber',bottom,48)
screw_pos=[(-1.36,.94),(-.49,1.00),(.49,1.00),(1.36,.94),(-1.46,-.07),(1.46,-.07),(-1.35,-.96),(1.35,-.96)]
for i,(x,y) in enumerate(screw_pos):
 sr=root('CASE_SCREW_'+str(i),'screw-'+str(i),'screw',fast);cyl('Pentalobe head',(x,y,-.085),.022,.006,'steel',sr,24);cyl('Screw shaft',(x,y,-.064),.009,.04,'steel',sr,12)
 for j in range(5):
  a=j*math.tau/5;box('P5 recess',(x+.006*math.cos(a),y+.006*math.sin(a),-.089),(.006,.006,.001),'well',sr,0)
# Ports: actual cutouts in shell, metal surrounds, contact tongues.
# Model left: MagSafe, two TB4, headphone. Right: HDMI, TB4, SDXC.
for side,entries in [(-1,[('MagSafe 3',.79,.19,.045),('Thunderbolt 4 A',.42,.115,.046),('Thunderbolt 4 B',.19,.115,.046),('Headphone',-.08,.058,.058)]),(1,[('HDMI',.73,.19,.06),('Thunderbolt 4 C',.40,.115,.046),('SDXC',.07,.27,.018)])]:
 for name,y,w,h in entries:
  cutter=box('Port cutter',(side*1.56,y,-.007),(.15,w,h),'well',base,.014);cut(shell,cutter)
  pg=root(name.replace(' ','_'),'ports','io',ports)
  box(name+' cavity',(side*1.525,y,-.007),(.028,w*.98,h*.97),'well',pg,.008)
  if 'Headphone' in name:
   cyl('Audio jack ring',(side*1.567,y,-.007),.029,.004,'steel',pg,32,rotation=(0,math.pi/2,0))
   cyl('Audio jack opening',(side*1.57,y,-.007),.022,.005,'well',pg,24,rotation=(0,math.pi/2,0))
  else:
   for sy in [-1,1]:box(name+' rim',(side*1.565,y+sy*w*.49,-.007),(.005,.004,h),'edge',pg,.001)
   for sz in [-1,1]:box(name+' rim',(side*1.565,y,-.007+sz*h*.49),(.005,w,.003),'edge',pg,.001)
   if 'Thunderbolt' in name:
    box('USB-C center tongue',(side*1.555,y,-.007),(.014,w*.73,.011),'chip',pg,.003)
    for j in range(10):box('USB-C contact',(side*1.564,y-w*.32+j*w*.071,-.001),(.005,.003,.002),'gold',pg,0)
   elif 'MagSafe' in name:
    for j in range(5):cyl('MagSafe contact',(side*1.565,y-.058+j*.029,-.007),.006,.003,'gold',pg,12,rotation=(0,math.pi/2,0))
   elif 'HDMI' in name:box('HDMI contact insert',(side*1.555,y,-.002),(.014,.13,.012),'chip',pg,.002)
  # Internal I/O daughterboard and ribbon.
  box(name+' PCB',(side*1.40,y,.001),(.20,w+.05,.016),'pcb',pg,.005)
# Hinge barrels and rear black antenna/vent strip.
for x in [-1.04,1.04]:
 cyl('Display hinge barrel',(x,1.025,.085),.055,.40,'edge',base,48,rotation=(0,math.pi/2,0))
 box('Hinge mounting bracket',(x,.96,.017),(.30,.14,.03),'steel',antenna,.015)
 for xx in [-.09,.09]:cyl('Hinge bracket fastener',(x+xx,.96,.04),.014,.009,'steel',antenna,16)
box('Rear vent and antenna',(0,1.04,.015),(1.68,.11,.09),'well',antenna,.01)
for i in range(70):box('Exhaust grille',( -.80+i*.023,1.102,.02),(.009,.012,.05),'body',antenna,.002)
# Lid local coordinates: upright, front toward -Y. Physical aspect follows 14.2 display.
plate_obj=plate('Display aluminum rear',(0,.016,1.0),3.115,2.018,.047,.09,'body',lid)
# Plate initially XY, rotate into XZ and use local offset.
plate_obj.rotation_euler=(math.pi/2,0,0)
bezel=plate('Display perimeter seal',(0,-.015,1.0),3.07,1.97,.014,.075,'rubber',lid);bezel.rotation_euler=(math.pi/2,0,0)
glass=plate('Display black glass',(0,-.024,1.0),3.035,1.935,.009,.065,'glass',lid);glass.rotation_euler=(math.pi/2,0,0)
# Screen surface is replaced with a local canvas texture in the web viewer.
screen=plate('DISPLAY_PIXELS',(0,-.030,1.004),2.965,1.845,.001,.047,'screen',lid);screen.rotation_euler=(math.pi/2,0,0)
box('Camera notch',(0,-.034,1.912),(.37,.012,.073),'glass',lid,.012)
for x,r in [(0,.013),(-.067,.007),(.067,.005)]:
 cyl('Camera optics',(x,-.042,1.918),r,.004,'blue',lid,24,rotation=(math.pi/2,0,0))
# Internals based on the service locator. One fan at right when seen through deck.
# PCB outline excludes the fan pocket; small packages are educational visual reconstruction.
pcb=plate('Logic board substrate',(-.38,.69,.005),1.79,.62,.025,.055,'pcb',board)
plate('Logic board left extension',(-1.13,.40,.005),.28,.38,.025,.035,'pcb',board)
# Main package, DRAM relationship and storage: positions are reconstructed, not exact traces.
chiproot=root('M4_PACKAGE','m4','package',board)
plate('M4 package substrate',(-.35,.67,.045),.48,.46,.027,.025,'pcb',chiproot)
plate('M4 heat spreader',(-.35,.67,.068),.39,.37,.025,.024,'steel',chiproot)
text('M4 marking','M4',(-.35,.67,.082),.12,'well',chiproot)
for x in [-.73,.06]:
 pg=root('DRAM_'+str(x),'memory','package',board);box('Unified memory package',(x,.66,.048),(.25,.30,.045),'chip',pg,.009);text('DRAM marking','MEMORY',(x,.66,.073),.026,'ink',pg)
for i,x in enumerate([-.87,-.62]):
 pg=root('NAND_'+str(i),'storage','package',board);box('NAND package',(x,.91,.044),(.18,.14,.035),'chip',pg,.004);text('NAND marking','NAND',(x,.91,.063),.026,'ink',pg)
# Dense component population, non-electrical placement; deterministic & clearly approximate.
for i in range(370):
 x=random.uniform(-1.21,.43);y=random.uniform(.40,.97)
 if -.91<x<.23 and .48<y<.84:continue
 w=random.choice([.015,.021,.03,.044]);d=random.choice([.012,.019,.026]);typ='cap' if i%3 else 'chip'
 box('SMT component',(x,y,.026),(w,d,.012 if typ=='cap' else .018),typ,board,.001)
 if typ=='cap':
  for s in [-1,1]:box('Solder termination',(x+s*w*.44,y,.026),(w*.15,d,.013),'steel',board,0)
# Copper routing is a visual abstraction, not a proprietary schematic.
for i in range(48):
 y=.414+i*.011;x=-1.19+(i%7)*.045
 curve('PCB illustrative routing',[(x,y,.019),(x+.1,y,.019),(x+.15,y+.035,.019),(x+.23,y+.035,.019)],.0011,'gold',board)
for i in range(65):
 x=random.uniform(-1.20,.42);y=random.uniform(.42,.96)
 cyl('PCB via',(x,y,.019),.003,.001,'gold',board,8)
# Shield cowlings, connectors and actual visual fasteners grouped by assembly.
for i,(x,y,w) in enumerate([(-1.0,.48,.13),(-1.12,.85,.14),(.28,.87,.18),(.29,.48,.19),(-.45,.41,.20)]):
 box('Connector housing',(x,y,.037),(w,.055,.025),'chip',cables,.003)
 for j in range(10):box('Connector pin',(x-w*.42+j*w*.09,y-.025,.046),(.004,.012,.003),'gold',cables,0)
 box('Connector retaining cowling',(x,y,.065),(w+.045,.07,.009),'steel',cables,.005)
 for xx in [-1,1]:cyl('Cowling screw',(x+xx*(w/2+.013),y,.073),.008,.008,'steel',cables,12)
# Fan housing, rotor, 59 curved vanes and outlet fins.
fan.location=(.94,.64,.008)
cyl('Fan lower housing',(0,0,0),.446,.055,'well',fan,96)
# Open circular rim, built from concentric rings.
for r in [.421,.438]:
 bpy.ops.mesh.primitive_torus_add(major_radius=r,minor_radius=.007,major_segments=96,minor_segments=8,location=(0,0,.045));finish(bpy.context.object,'Fan housing rim','steel',fan)
rotor=root('FAN_ROTOR','fan','rotor',fan)
cyl('Fan motor',(0,0,.047),.112,.043,'steel',rotor,48)
cyl('Motor label',(0,0,.071),.086,.003,'chip',rotor,48)
text('Fan label','FAN',(0,0,.074),.035,'ink',rotor)
for i in range(59):
 a=i*math.tau/59;pts=[]
 for j in range(7):
  r=.12+j*.046;t=a+j*.045;pts.append((math.cos(t)*r,math.sin(t)*r,.05))
 curve('Curved impeller vane',pts,.006,'body',rotor)
for i in range(48):box('Heatsink fin',(.49+i*.018,.985,.052),(.006,.13,.075),'edge',heat,.001)
curve('Heat pipe',[(-.35,.67,.108),(-.24,.84,.108),(.0,.92,.108),(.52,.92,.108)],.036,'copper',heat)
box('Thermal contact plate',(-.35,.67,.099),(.44,.40,.016),'copper',heat,.02)
# Battery: six pouch volumes grouped into three approximate banks, seams and labels.
for i,(x,y,w,d) in enumerate([(-.91,-.36,.55,1.0),(-.29,-.36,.55,1.0),(.32,-.36,.55,1.0),(.94,-.36,.55,1.0)]):
 cell=root('CELL_BANK_'+str(i),'battery','cell',battery)
 plate('Battery pouch',(x,y,-.005),w,d,.067,.045,'cell',cell)
 plate('Pouch folded edge',(x,y,-.038),w+.018,d+.018,.008,.04,'foil',cell)
 for k in range(4):box('Battery fine print',(x,y-.05-k*.037,.031),(w*.64,.003,.001),'ink',cell,0)
 text('Battery identification','Li-ion',(x,y+.20,.032),.045,'ink',cell)
 text('Battery rating','72.4 Wh SYSTEM',(x,y+.12,.032),.026,'ink',cell)
 text('Battery warning','RECONSTRUCTED CELL GEOMETRY',(x,y-.30,.032),.014,'ink',cell)
 box('Battery tab',(x,y+d/2+.025,.005),(.16,.07,.01),'gold',cell,.004)
# BMU, power connector and copper-ended ribbon.
bmu=root('BATTERY_MANAGEMENT','bmu','internal',battery)
box('BMU substrate',(0,.24,.022),(.53,.10,.022),'pcb',bmu,.005)
for i in range(6):box('BMU IC',(-.20+i*.08,.24,.043),(.05,.055,.02),'chip',bmu,.002)
for i in range(4):
 x=-.12+i*.065;curve('Battery power lead',[(x,.24,.035),(x,.31,.045),(x+.1,.39,.045)],.005,'flex',cables)
# Speakers, diaphragm rings, magnets, enclosures at either side of battery.
for side in [-1,1]:
 x=side*1.365
 plate('Speaker acoustic enclosure',(x,-.27,-.006),.245,1.20,.09,.08,'well',speaker)
 for y in [-.62,-.17]:
  plate('Woofer diaphragm',(x,y,.045),.18,.26,.012,.07,'rubber',speaker)
  plate('Driver surround',(x,y,.054),.145,.22,.008,.06,'cell',speaker)
  box('Voice coil',(x,y,.06),(.03,.10,.004),'copper',speaker,.005)
 cyl('Tweeter',(x,.20,.048),.071,.016,'chip',speaker,48)
# Ribbon cables: broad folded strips plus gold conductors, no invented netlist.
for i,(x,y,dx,dy) in enumerate([(-1.22,.55,-.12,.22),(.41,.55,.14,.12),(-.5,.42,.25,-.2),(.4,.45,.10,-.13),(0,-.20,0,-.3),(-.8,.43,-.3,-.12)]):
 ribbon=box('Flex ribbon',(x+dx/2,y+dy/2,.054),(.065,math.hypot(dx,dy),.007),'flex',cables,.001);ribbon.rotation_euler.z=-math.atan2(dx,dy)
 for j in range(5):
  offset=(j-2)*.009;curve('Flex copper conductor',[(x+offset,y,.059),(x+dx+offset,y+dy,.059)],.001,'gold',cables)
# Trackpad underside: bridge, sensing corners and haptic actuator.
tpu=root('TRACKPAD_UNDERSIDE','trackpad','internal')
plate('Trackpad backing',(0,-.68,-.037),1.28,.66,.015,.035,'steel',tpu)
box('Haptic actuator',(0,-.83,-.015),(.54,.13,.038),'chip',tpu,.012)
for x in [-.52,.52]:
 for y in [-.91,-.45]:box('Force sensor',(x,y,-.018),(.11,.08,.02),'pcb',tpu,.006)
# Batch only repeated fixed details by parent and material. Keys, assemblies, screws retain IDs.
buckets=defaultdict(list)
for o in all_mesh:
 if o.type=='MESH' and o.name!='DISPLAY_PIXELS':buckets[(o.parent.name if o.parent else '',o.data.materials[0].name)].append(o)
for (pn,mn),obs in buckets.items():
 if len(obs)<2:continue
 bpy.ops.object.select_all(action='DESELECT')
 for o in obs:o.select_set(True)
 bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();bpy.context.object.name=pn+'__'+mn
# Export clean model with extras, editable source and mesh statistics.
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=R+'/public/models/macbook-m4-detailed.glb',export_format='GLB',export_extras=True,export_apply=True,export_yup=True)
scene=bpy.context.scene;scene.world.color=(.15,.15,.15)
scene['accuracy']='Reference-guided visual reconstruction, not Apple CAD. Outer envelope sourced; internal geometry and semiconductor placements approximate.'
bpy.ops.wm.save_as_mainfile(filepath=R+'/MacBook-Pro-14-M4.blend')
meshes=[o for o in scene.objects if o.type=='MESH']
json.dump({'meshes':len(meshes),'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in meshes),'roots':list(roots),'sources':['https://support.apple.com/en-us/121552','https://support.apple.com/en-us/120927','https://support.apple.com/en-us/120769','https://support.apple.com/en-us/120750'],'accuracy':scene['accuracy']},open(R+'/references/model-report.json','w'),indent=2)
print('MODEL COMPLETE',len(meshes))
