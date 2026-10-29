# Laptop Universe demo

The rendered demo media is not committed. Regenerate it locally from the current (logo-free) model:

1. `blender -b --python demo/render_demo.py` renders the seven studio shots to `demo/renders/`.
2. `blender -b --python demo/rerender_details.py` re-renders the internal shots without unverified board labels.
3. `python3 demo/edit_demo.py` generates the title overlays, an original synthesized score and `Laptop-Universe-Demo.mp4` (30 s, 1080 × 1350, H.264 / AAC). Requires ffmpeg.

Suggested post copy: `POST-CAPTION.txt`. Independent concept, not affiliated with Apple.

