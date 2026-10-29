from pathlib import Path
import numpy as np, wave, subprocess, json
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent; W,H=1080,1350;fps=30
font='/System/Library/Fonts/Supplemental/Arial.ttf';bold='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
shots=[('01 / THE OBJECT','You know the outside.','LAPTOP UNIVERSE',4.0),('02 / LOOK CLOSER','Now go beneath it.','A MACHINE, OPENED UP.',4.0),('03 / THE SYSTEM','Every assembly. Connected.','POWER · COMPUTE · COOLING',4.5),('04 / BELOW THE SHIELDS','There is another layer.','EXPLORE THE LOGIC BOARD',4.0),('05 / HEAT → AIR','Follow the mechanism.','OPEN THE COOLING ASSEMBLY',4.0),('06 / TAKE IT APART','Understand the whole.','LAYER BY LAYER',4.5),('INTERACTIVE HARDWARE EXPLORER','MacBook Universe.','BUILT TO BE EXPLORED.',5.0)]
clips=[]
for i,(label,title,sub,dur) in enumerate(shots):
 im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
 # soft editorial gradients, preserving the studio product in the centre.
 a=np.zeros((H,W,4),dtype=np.uint8)
 for y in range(H):
  alpha=int(240*max(0,(260-y)/260)) if y<260 else int(235*min(1,max(0,(y-870)/240)))
  a[y,:,0:3]=[7,12,17];a[y,:,3]=alpha
 im=Image.fromarray(a);d=ImageDraw.Draw(im)
 d.text((64,64),'M / U',font=ImageFont.truetype(bold,25),fill=(224,233,233,255))
 d.text((W-120,70),f'{i+1:02}',font=ImageFont.truetype(font,18),fill=(143,163,169,255))
 d.line((64,112,W-64,112),fill=(103,127,133,100),width=1)
 d.text((64,1038),label,font=ImageFont.truetype(font,18),fill=(154,183,179,255))
 size=52 if len(title)<28 else 44
 d.text((62,1081),title,font=ImageFont.truetype(bold,size),fill=(232,238,238,255))
 d.text((64,1165),sub,font=ImageFont.truetype(font,18),fill=(161,176,181,255))
 d.line((64,1230,W-64,1230),fill=(103,127,133,100),width=1)
 d.text((64,1255),'INDEPENDENT VISUAL STUDY · RECONSTRUCTED GEOMETRY',font=ImageFont.truetype(font,12),fill=(116,136,145,255))
 im.save(R/f'overlay-{i}.png')
 frames=round(dur*fps);z="1.02+0.075*on/%d"%frames if i%2==0 else "1.095-0.075*on/%d"%frames
 vf=f"[0:v]scale=1440:1800,zoompan=z='{z}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={frames}:s={W}x{H}:fps={fps},setsar=1[bg];[bg][1:v]overlay=0:0,fade=t=in:st=0:d=0.22,fade=t=out:st={dur-.22}:d=0.22,format=yuv420p[v]"
 out=R/f'clip-{i}.mp4'
 subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(R/f'renders/{i:02}.png'),'-i',str(R/f'overlay-{i}.png'),'-filter_complex',vf,'-map','[v]','-t',str(dur),'-c:v','libx264','-preset','medium','-crf','17','-profile:v','high',str(out)],check=True);clips.append(out)
(R/'clips.txt').write_text(''.join("file '%s'\n"%p for p in clips))
# Original, locally synthesised sound design; no licensed recording or samples.
duration=sum(s[3] for s in shots);sr=48000;t=np.arange(int(sr*duration))/sr;audio=np.zeros_like(t)
for f in [55,82.4069,110,164.8138]:audio+=.025*np.sin(2*np.pi*f*t+1.5*np.sin(2*np.pi*.08*t))*np.minimum(t/2,1)*np.minimum((duration-t)/2,1)
rng=np.random.default_rng(2026)
for beat in np.arange(0,duration,.5):
 start=int(beat*sr);n=min(int(.32*sr),len(t)-start);u=np.arange(n)/sr
 audio[start:start+n]+=.20*np.sin(2*np.pi*(44*u+3.3*(1-np.exp(-u*24))))*np.exp(-u*15)
 if round(beat*2)%2==1:audio[start:start+n]+=.014*rng.normal(size=n)*np.exp(-u*40)
for j,at in enumerate(np.cumsum([0]+[s[3] for s in shots[:-1]])):
 start=int(at*sr);n=min(sr,len(t)-start);u=np.arange(n)/sr
 audio[start:start+n]+=.034*rng.normal(size=n)*np.sin(np.pi*u)**2*np.exp(-u*3)
 for k,f in enumerate([220,329.6276,440]):audio[start:start+n]+=.025*np.sin(2*np.pi*f*u)*np.exp(-u*5)
audio=np.tanh(audio*1.3)*.75;audio*=np.minimum(t/.08,1)*np.clip((duration-t)/1.4,0,1)
left=audio;right=np.roll(audio,240)*.97;stereo=np.stack([left,right],axis=1)
with wave.open(str(R/'original-score.wav'),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes((stereo*32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(R/'clips.txt'),'-i',str(R/'original-score.wav'),'-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=8','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-shortest',str(R/'Laptop-Universe-Demo.mp4')],check=True)
print('DEMO_EXPORT_COMPLETE',duration,flush=True)
