# Revision 10 — display, exterior envelope and assembly sections

The screen now has a single image surface with exported UVs and no shadow reception. Its border and camera notch are separate opaque surfaces. Runtime selection and boot highlighting no longer tint the entire display enclosure. The display uses an illustrative wallpaper, startup logo/progress and login boundary; it is not a macOS capture or operating system.

`modeling/rebuild_exterior_r10.py` reconstructs the longer display housing and corrects the vertical enclosure stack. A closed-pose bounding-box assertion measures the modeled exterior including the feet against 1.55 cm. Width and depth of the unibody remain 31.26 × 22.12 cm. The image surface is 30.24 × 19.64 cm, consistent with Apple's published resolution and 254 ppi. Corner radii, exact bezel thickness, seams, the hinge mechanics and coatings are reconstructed, not measured production CAD.

The cinematic explorer now contains eight assembly sections. The camera focuses the selected assembly; surrounding enclosure geometry provides context. The separation slider lifts or separates the selected parts. Keyboard study also includes a magnified scissor-key section with an independent press control. These are explanatory sections, not instructions for opening bonded or non-serviceable components.

- Cooling: existing shroud and impeller are separated, with a representative motor/bearing section.
- Logic board: cowlings, shielding, a representative solder interface and a PCB laminate study. Unverified NAND/DRAM location labels are hidden in this study.
- Keyboard: caps, scissor frames, domes and backing, plus the magnified key mechanism.
- Trackpad: touch surface, illustrative electrode grid, haptic section and existing mounting frame.
- Display: housing, an illustrative mini-LED field, optical films and the image/cover surface. Display layers and the LED field are not a factory stack or LED map.
- Ports: enlarged USB Type-C shell, tongue and 24-contact interface; original port boards remain in context. This is standard-interface anatomy, not an identified Apple supplier component.
- Battery: a representative pouch laminate, electrodes, separator and current collectors above the reconstructed pack.
- Speakers: representative diaphragm, voice-coil and magnet section. This does not locate the six actual drivers inside Apple's enclosures.

Each section shows the documented relationship and its reconstruction limits, with source links. All exact microgeometry, counts not explicitly sourced, component placements, materials and optical/PCB/cell stack thicknesses remain illustrative. No new exact netlist, PCB route, PMIC identity or proprietary boardview is claimed.

## Primary references

- [Apple base-M4 specifications](https://support.apple.com/en-us/121552)
- [Apple base-M4 fan](https://support.apple.com/en-us/120750)
- [Apple base-M4 logic board](https://support.apple.com/en-us/120769)
- [Apple keys anatomy](https://support.apple.com/en-us/101268)
- [Apple trackpad and flex](https://support.apple.com/en-us/120762)
- [Apple display assembly](https://support.apple.com/en-us/120767)
- [Apple USB-C boards](https://support.apple.com/en-us/120778)
- [USB-IF Type-C release 2.0, receptacle contact interface](https://www.usb.org/sites/default/files/USB%20Type-C%20Spec%20R2.0%20-%20August%202019.pdf)
- [US EPA lithium-ion cell construction](https://www.epa.gov/hw/lithium-ion-battery-recycling)

## Verification

- Blender closed-envelope assertion: 1.5500 cm including the modeled rubber feet.
- TypeScript and production Vite build.
- Existing deterministic startup/source-graph tests and guided-disassembly prerequisite tests.
- Browser review of the exterior, final startup screen and the eight assembly sections, including slider interaction.

## Clean material rendering

Automatic transparency fades, selection/boot emission tints, procedural roughness grain and product self-shadow maps have been removed. The cutaway lifts opaque assemblies before hiding them. Screen state is controlled by its texture alone, with a plain gradient background and no competing opacity/brightness updates. The camera depth range is tightened to reduce conflicts between small nearby surfaces. Explicit X-ray remains an opt-in inspection control. Browser checks covered the internal power view and final screen with no runtime errors.

## Neutral product studio revision

The viewer now uses neutral rectangular softbox reflections instead of the former HDR colour cast. The dark aluminum, satin keycaps and reflective screen have distinct materials. Decorative page gradients are removed, the camera holds a product framing at rest, and a contact shadow anchors the feet. This is a presentation correction; it does not certify hand-reconstructed manufacturing geometry.

The idle display shows a procedural wallpaper drawn on the canvas; no third-party artwork is used. It is not an OS session. Startup and login remain illustrative states.

The full-screen generic block scenes for non-startup lessons have been replaced by the corresponding laptop assemblies. Step changes separate the hardware study, with explanatory responsibilities remaining in the lesson panel. Chip floorplan mode remains explicitly conceptual.
