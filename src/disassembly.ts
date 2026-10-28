export const sequence=[
{id:'bottom',title:'Lower case',task:'Release 8 P5 fasteners, then clips and sliding hooks.',requires:[],source:'https://support.apple.com/en-us/120759'},
{id:'bmu',title:'BMU flex connection',task:'Fold back the trackpad flex, release the lock and slide the BMU flex free.',requires:['bottom'],source:'https://support.apple.com/en-us/120760'},
{id:'antenna',title:'Vent / antenna module',task:'Release grounding and cowling screws, 3 coaxial connectors, 9 1IPR screws and 6 5IP screws. Actions are grouped in this visual study.',requires:['bottom','bmu'],source:'https://support.apple.com/en-us/120764'},
{id:'cables',title:'Logic-board connections',task:'Release the connector cowlings and disconnect the flex cables. The full connector inventory is in the linked service procedure. Grouped action, not individual connector simulation.',requires:['antenna'],source:'https://support.apple.com/en-us/120769'},
{id:'board',title:'Logic-board assembly',task:'Release the board fasteners and lift / slide the assembly free, retaining the heat sink with it. Positions and motion are reconstructed.',requires:['cables'],source:'https://support.apple.com/en-us/120769'},
{id:'fan',title:'Fan assembly',task:'With the board out, release three 3IP screws and one 5IP screw, then lift out the fan.',requires:['board'],source:'https://support.apple.com/en-us/120750'}
];
export function canRelease(id:string,removed:string[]){const stage=sequence.find(s=>s.id===id);if(!stage||removed.includes(id))return false;if(!stage.requires.every(r=>removed.includes(r)))return false;return id!=="bottom"||Array.from({length:8},(_,i)=>"screw-"+i).every(id=>removed.includes(id));}
