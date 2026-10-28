import {create} from 'zustand';
export type Mode='Discover'|'Disassemble'|'Inside M4'|'How it works'|'Lab';
type State={mode:Mode;selected:string;explode:number;lid:number;removed:string[];resetKey:number;set:(v:Partial<State>)=>void;reset:()=>void};
export const useLab=create<State>((set)=>({mode:'Discover',selected:'chassis',explode:0,lid:108,removed:[],resetKey:0,set,reset:()=>set(s=>({selected:'chassis',explode:0,lid:108,removed:[],resetKey:s.resetKey+1}))}));
