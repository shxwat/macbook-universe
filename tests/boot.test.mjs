import assert from 'node:assert/strict';
import {advanceBoot,inspectBootStage,bootStages,bootPaths,bootSources} from '../src/bootModel.ts';
const init={stage:0,elapsed:0,playing:true,complete:false,failed:false};
const paused={...init,playing:false};assert.deepEqual(advanceBoot(paused,10,'none'),paused);
assert.deepEqual(advanceBoot(init,NaN,'none'),init);
let b=advanceBoot(init,bootStages[0].duration-.1,'none');assert.equal(b.stage,0);
b=advanceBoot(b,.2,'none');assert.equal(b.stage,1);assert.ok(Math.abs(b.elapsed-.1)<1e-8);
const complete=advanceBoot(init,1000,'none');assert.equal(complete.complete,true);assert.equal(complete.stage,9);assert.equal(complete.failed,false);assert.equal(complete.playing,false);
const failed=advanceBoot(init,1000,'iboot-signature');assert.equal(failed.failed,true);assert.equal(failed.stage,5);assert.equal(failed.complete,false);assert.equal(failed.playing,false);
assert.deepEqual(advanceBoot(failed,1000,'iboot-signature'),failed,'verification failure cannot execute next stage');
assert.equal(inspectBootStage(9,'iboot-signature').stage,5,'inspection cannot bypass failure scenario');
assert.equal(inspectBootStage(100,'none').stage,9);assert.equal(inspectBootStage(-3,'none').stage,0);
for(const stage of bootStages){for(const id of stage.sources)assert.ok(bootSources[id]);for(const id of stage.paths)assert.ok(bootPaths.some(p=>p.id===id));assert.ok(stage.unknown.length>20,'each stage declares its evidence boundary');}
for(const path of bootPaths){assert.ok(path.note.length>15);assert.ok(path.points.length>=3);for(const n of path.stages)assert.ok(bootStages[n].paths.includes(path.id));}
assert.equal(new Set(bootPaths.map(p=>p.id)).size,bootPaths.length);
console.log('PASS: deterministic startup, pause, boundaries, completion, signature rejection, source graph and route evidence');
