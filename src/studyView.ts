import type{AssemblyStudy,Mode}from'./store';
type ViewState={study:AssemblyStudy;mode:Mode;bootActive:boolean;lesson:number;step:number;studySpread:number};
const lessons:AssemblyStudy[]=['none','battery','board','board','board','board','cooling','display','keyboard','speakers','ports'];
export function visibleStudy(s:ViewState):AssemblyStudy{return s.study!=='none'?s.study:s.mode==='How it works'&&!s.bootActive?lessons[s.lesson]||'none':'none'}
export function visibleSpread(s:ViewState):number{return s.study==='none'&&s.mode==='How it works'&&!s.bootActive?.15+Math.min(3,s.step)/3*.7:s.studySpread}
