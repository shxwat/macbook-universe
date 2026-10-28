# MacBook Universe

Runnable first milestone for a base M4, 14-inch November 2024 MacBook Pro explorer.

## Run

`npm install` then `npm run dev`. Production: `npm run build`.

## Implemented

React/TypeScript/Vite, React Three Fiber, Drei and Zustand. Five modes; orbit/pan/zoom; lid movement; selectable procedural geometry; source-linked metadata; component search; assembly separation; eight independently released lower-case fasteners with cover release gated on their state; conceptual M4 architecture; eleven sequential lessons with play/pause/speed/reset/step controls; illustrative power and thermal calculations with adjustable CPU/GPU/fan inputs.

## Accuracy and remaining work

This is not a production digital twin. Chassis proportions use published dimensions. All small geometry and internal placement are approximate. M4 architecture is conceptual, not a die floorplan. Internal components are inspectable but are not individually removable. Clip/hook release is a single explained action. Screw positions are proxies and lengths are not assigned without a verified position map. The keyboard is illustrative rather than a complete accurate US layout. Ports are recess proxies. Board traces, connectors, shields, antennas and camera internals are not reconstructed. Lessons provide sequential text, not detailed mechanism animations. Lab scenarios are simplified presets; no real sensors, benchmarks or charging model. Memory pressure is independent of the thermal equation.

Production work requires model-specific photo registration, screw mappings from Apple service pages, documented connector dependencies, licensed CAD/Blender assets, compressed GLB delivery, LOD, mechanism-specific animations and measured thermal validation. Asset replacement can occur within Scene.tsx while preserving IDs in hardware.ts and store state.

## Sources

- https://support.apple.com/en-us/121552 — exact model specifications
- https://support.apple.com/en-us/120922 — exact model repair manual and assembly inventory
- https://www.ifixit.com/Guide/MacBook+Pro+14-Inch+Late+2024+(M4)+Lower+Case+Replacement/217918 — eight P5 lower case fasteners; note the guide's warning that some photographs show the preceding model
- https://support.apple.com/guide/security/secac71d5623/web — Apple silicon secure boot

`src/hardware.ts` is the structured research manifest, with source, accuracy class, materials, purpose and prerequisites per component. No manufacturer floorplan or exact board reconstruction is asserted.

## Verification

TypeScript and Vite production build pass. Browser checked rendering and eight-fastener state progression. Cover release cannot start at zero fasteners. Visual QA corrected thin mesh bevels and narrow-screen control overlap. Further desktop/mobile, keyboard and WebGL fallback testing remains.
