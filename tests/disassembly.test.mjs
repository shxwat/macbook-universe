import assert from 'node:assert/strict';
import {canRelease,sequence} from '../src/disassembly.ts';
assert.equal(canRelease('bottom',[]),false,'cover must retain its fasteners');
const screws=Array.from({length:8},(_,i)=>'screw-'+i);
assert.equal(canRelease('bottom',screws.slice(1)),false,'one missing release blocks the cover');
assert.equal(canRelease('bottom',screws),true);
assert.equal(canRelease('fan',['bottom','bmu','antenna']),false,'fan cannot precede logic board');
assert.equal(canRelease('board',['bottom','bmu','antenna']),false,'board cannot precede connections');
const removed=[...screws];
for(const stage of sequence){assert.equal(canRelease(stage.id,removed),true,stage.id);removed.push(stage.id);assert.equal(canRelease(stage.id,removed),false,'cannot release twice');}
assert.equal(canRelease('unknown',removed),false);
console.log('PASS: lower-case fasteners, prerequisites, duplicate removal and complete sequence');
