# Startup research — 28 October 2026

Reference scope: base M4, 14-inch MacBook Pro, November 2024. Normal press-and-release startup, Full Security path. Authentication/FileVault are explicit scope boundaries.

## Primary evidence consulted

1. Apple model repair manual: https://support.apple.com/en-us/120922
2. Base-M4 board/connector documentation: https://support.apple.com/en-us/120769
3. Touch ID board procedure: https://support.apple.com/en-us/120776
4. Base-M4 assembly catalogue: https://support.apple.com/en-us/120927
5. Model specifications: https://support.apple.com/en-us/121552
6. Boot modes: https://support.apple.com/guide/security/sec10869885b/web
7. Boot process: https://support.apple.com/guide/security/secac71d5623/web
8. Secure Enclave: https://support.apple.com/guide/security/sec59b0b31ff/web
9. Startup diagnostics: https://support.apple.com/en-us/117313
10. Startup display: https://support.apple.com/en-us/102535
11. Startup screens/login: https://support.apple.com/en-us/102675
12. FileVault: https://support.apple.com/guide/mac-help/mh11785/mac
13. Apple developer architecture session: https://developer.apple.com/videos/play/wwdc2020/10686/
14. Independent platform research (kernel handoff only): https://asahilinux.org/docs/platform/introduction/

## Electrical blueprint search

Queries included base M4 + A3112 + 820-03129 + schematic/boardview/power sequence, as well as model-specific teardown and package-identification searches. Broad results included listings for M4 Pro board 820-03400, older-generation schematics and forum requests reporting unavailable files. None supplied an independently verifiable base-M4 netlist or boardview during this research. This is a bounded search result, not a claim that no such file exists anywhere.

The board/model mapping was cross-checked against the repair community's model index, https://repair.wiki/w/Macbook_Board_and_Model_numbers. It is a community index, not an Apple electrical blueprint. Marketplace and unverified blueprint listings were not used to assign any electrical net or voltage.

## What is deliberately not asserted

- Exact PMIC device, rail values, enable order, reset waveforms, switching behavior or current measurements.
- A physical Boot ROM, LLB or Secure Enclave floorplan.
- Actual DRAM/NAND package locations or channel routing on this reconstructed mesh.
- A physical conductor following a glowing overlay.
- Real startup performance, an observed live boot, firmware verification performed by this app, or a universal order for the login/FileVault UI.

## Visual contract

The glowing lines are functional overlays elevated above the model. Amber encodes energy transfer (including a conceptual return). Green encodes control. Cyan encodes data. Violet encodes trust/policy relationships. Animated pulses express explanatory direction/progression, not electrons, signal propagation speed or measured current.

Unknown memory/storage placements are shown as off-model functional terminals in evidence-first startup mode. Unidentified PCB populations and decorative routes are hidden by default in that mode. Existing authored geometry remains classified as reconstructed/approximate.

The logical inset has no physical die boundaries. Its arrows encode documented responsibilities and relationships, not exact chip interconnects. The ten stages unpack responsibilities for readability; they are not measured, exclusive hardware phases.

Every stage and route has a machine-readable explanation and evidence boundary in `src/bootModel.ts`, also exported as `public/references/startup-evidence.json`. All reference images retain Apple's provenance and are shown as source plates, visibly separate from the generated 3D scene.
