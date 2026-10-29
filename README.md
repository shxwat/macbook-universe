# Laptop Universe — revision 10

Interactive engineering explorer for a **14-inch M-series laptop with an M4-class chip**, rebuilt as an independent visual study. Live at **https://macbook-universe.vercel.app**; the deployed site matches this repository.

> **Independent concept. Not affiliated with, sponsored by, or endorsed by Apple Inc.** The model carries no manufacturer logo or trademark text. Product and company names mentioned in sources belong to their respective owners and are used only to identify the referenced documentation.

The current revision rebuilds the display and exterior stack and adds eight explorable assembly sections. See `references/REVISION-10.md` for reconstruction limits, primary sources and validation.

## Run

`npm install` then `npm run dev -- --port 5176`. Production: `npm run build`.

## Editable assets

- `MacBook-Pro-14-M4-r10.blend` — current editable Blender scene.
- `public/models/macbook-m4-r10.glb` — current Draco-compressed runtime model; decoder shipped locally in `public/draco/`.
- `modeling/rebuild_exterior_r10.py` — current exterior and display authoring pipeline.
- `modeling/refine_exterior_r09.py` — exterior clean-up; strips any brand mark or trademark text inherited from earlier scenes. The lid back is plain aluminum.
- `modeling/rebuild_internals.py`, `photo_guided_detail_r07.py`, and `structural_finish_r08.py` — successive interior reconstruction scripts. The original scene is preserved in `MacBook-Pro-14-M4.blend`.
- `references/model-report.json` — mesh/triangle inventory and sources. Approximately 328k triangles before the final added detail; see report for updated counts.
- `modeling/build_macbook.py`, `refine_and_render.py`, `final_adjust.py`, `export_web.py` — sequential authoring, refinement and export pipeline. Execute with Blender from this checkout. The first script resets the generated model scene; it does not import Apple CAD.

## Regenerating the runtime model

The app loads only `public/models/macbook-m4-r10.glb`. Object names are significant (the viewer selects parts by name), so regenerate it with the pipeline rather than re-exporting by hand:

```sh
blender -b --factory-startup --python modeling/refine_exterior_r09.py   # r08 scene -> MacBook-Pro-14-M4-exterior-r09.blend
blender -b --factory-startup --python modeling/rebuild_exterior_r10.py  # r09 scene -> MacBook-Pro-14-M4-r10.blend + public/models/macbook-m4-r10.glb
```

The r10 step exports a Draco-compressed GLB (level 6, 18-bit positions, extras on) and asserts the closed exterior height. Earlier scripts (`build_macbook.py` → `structural_finish_r08.py`) rebuild the interior scenes from scratch and also write intermediate GLBs, which are git-ignored and not shipped.

## What changed

The original in-browser proxy boxes have been replaced by Blender-authored geometry: hollow enclosure, separate deck and lower cover, 78 keycaps including split up/down arrows, legends, Touch ID, grille perforations, trackpad and backing, hinge barrels, notch optics, port cavities/rims/tongues/contacts, feet, eight P5 screw representations, PCB substrate and small components, package labels, routing abstractions, connector cowlings, flex ribbons, cell pouches, battery management, speaker diaphragms, heat pipe/fin stack and curved fan vanes.

The viewer provides click selection, double-click focus, six camera presets, orbit/pan/zoom, isolate, wireframe, X-ray, labels, lid articulation, key travel, PNG capture, fullscreen and continuous exploded cutaway control.

The guided sequence gates lower-case release on eight screw releases, then progresses through BMU flex, vent/antenna module, board connections, logic board and fan. Internal fasteners and connectors are grouped service stages. The exploded cutaway is separate from the removal sequence.

Inside M4 shows 4 performance + 6 efficiency CPU cores, 10 GPU cores and 16 Neural Engine cores in an **explicitly conceptual arrangement**, plus a package-layer separation control and memory relationship.

All eleven lessons have a signal-flow diagram and distinct visual mechanism: chain-of-trust stages, charging/BMU path, simplified instruction pipeline, shared memory, triangle-to-pixel rendering, flash-to-buffer transfer, heat pipe/fins/fan, mini-LED/LCD/RGB layers, scissor-key cutaway, speaker/pressure waves and transmission/antenna. Controls support play, pause, speed, reset and stepping. Animation timing and geometry are educational.

Lab presets and sliders drive a visible relative heat overlay, fan animation and transparent illustrative equations. These are not device measurements or predictions. There is no real telemetry. Memory pressure is independent of the thermal equation.

## Accuracy boundaries

Published outer dimensions and base-M4 specifications are sourced. Local geometry, exact key dimensions, cell count/shape, PCB component identity/placement, traces, connector positions and the smallest manufacturing details are reconstructed. Copper routing is visual explanation, not a proprietary netlist. Service diagrams guide the assembly relationships but do not provide factory CAD or tolerances. The thermal assembly can be separated for education; Apple instructs servicing the heat sink with the logic board. Camera optics, speaker driver internals, the keyboard scissor mechanism, chip package layers and semiconductor floorplan are educational approximations.

The current interior uses Apple service imagery for assembly relationships and repair imagery for visual guidance. The iFixit M4 battery guide states that some of its photos depict the previous model, so the six-pouch layout is a visual reconstruction rather than a verified M4 cell map. Small board components are anonymous approximations. Startup lines show functional relationships, not measured current paths or a verified netlist.

This revision is substantially more detailed, but it is **not an exact digital twin, complete service simulator, or manufacturing model**. Full accuracy requires measured scan/CAD, licensed production assets, validated screw-position maps, connector-by-connector mechanisms, detailed display laminates and external validation.

## Sources

- https://support.apple.com/en-us/121552 — exact base M4 specifications and outer envelope
- https://support.apple.com/en-us/120927 — model-specific exploded view and orderable assemblies
- https://support.apple.com/en-us/120769 — logic board, cowlings and connections
- https://support.apple.com/en-us/120750 — fan and prerequisites
- https://support.apple.com/en-us/120760 — BMU flex procedure
- https://support.apple.com/en-us/120764 — vent/antenna procedure
- https://support.apple.com/en-us/120762 — trackpad procedure
- https://support.apple.com/en-us/120929 — speaker procedure
- https://support.apple.com/en-us/120759 — bottom case
- https://support.apple.com/guide/security/secac71d5623/web — Apple silicon boot chain

The sources above are linked, not redistributed: no manufacturer or repair-guide images are stored in this repository or shipped by the app. No third-party laptop mesh is used. The studio HDR was reused from the existing M5 project. Three.js decoder files retain the upstream Three.js/Draco licensing.

## Verification

`node tests/disassembly.test.mjs` tests cover screw gating, internal prerequisites, duplicate releases and full sequence progression. `npm run build` checks TypeScript and produces the runtime bundle. Browser QA covers rendering, component selection, mode switching, lesson stepping, thermal mechanism, assembly list and camera presets. Browser pixel-perfect realism, exact physical measurements and real device thermal accuracy are not established by these checks.

## Revision 03 — power-button startup trace

Click the physical power-button callout or **Press power · trace startup**. The same Blender model becomes a ghosted cutaway with colored, selectable functional paths. A ten-stage timeline connects the power request, general supply relationship, Boot ROM, LLB, firmware, LocalPolicy, Secure Enclave, iBoot, boot objects in unified memory, SSV checks, kernel handoff and a login boundary. Playback supports pause, stepping, speed, replay and optional camera follow. Battery/adapter variants change the functional source. A rejected iBoot-signature case stops the state machine before kernel execution and shows a recovery boundary.

The app does **not** claim exact current paths. Power, control, data and verification have separate colors and descriptions. Every stage states its sources and unknowns. Exact base-M4 net names, PMIC identity, rail values and memory-routing locations were not verified, and are not invented. Unknown memory/storage positions use off-model functional terminals. Unidentified PCB decoration is hidden by default in startup evidence mode. See `references/STARTUP-RESEARCH.md` and `references/ACCURACY-REQUIREMENTS.md`.


Run `node tests/boot.test.mjs` for startup sequencing, pause, completion, signature-failure gating, graph consistency and source/unknown metadata checks. The evidence graph is also available at `/references/startup-evidence.json`.

## Revision 04 — cinematic navigation

The default view follows the user's local `goroutine-industrial-18s.mp4` reference: a full-screen industrial scene, slow director camera, on-object callouts, one stage caption and a thin progress rail. Choose chapters from the rail or **Stages**, use play/pause and speed, and open the inspector for sourced explanations. Dragging takes over the camera; **Director on / Free camera** returns control to the automatic motion. Arrow keys step the startup sequence and Space toggles playback when focus is outside a control. **Workbench** opens the full assembly interface.

The reference video was used for interaction and visual direction. It does not establish hardware facts. Startup paths remain explicitly functional overlays, with physical traces and unlabeled chip identities left unverified.

## Contributors

- [Shashwat](https://github.com/shxwat) — project creator and direction.
- Codex (OpenAI) — AI coding assistance, implementation, testing, and demo production.
