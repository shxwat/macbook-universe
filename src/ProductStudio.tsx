import{Environment,Lightformer,ContactShadows}from'@react-three/drei';
/** Neutral photographic softboxes. Reflections describe the metal without painting it. */
export default function ProductStudio({grounded=false}:{grounded?:boolean}){return <>
<ambientLight intensity={.12}/><directionalLight position={[2,6,4]} intensity={.75} color="#ffffff"/>
<Environment resolution={512} frames={1} background={false}>
 <color attach="background" args={['#111111']}/>
 <Lightformer form="rect" intensity={4.0} color="#ffffff" scale={[6,3,1]} position={[-3,5,1]} rotation={[Math.PI/2,0,-.35]}/>
 <Lightformer form="rect" intensity={3.5} color="#ffffff" scale={[1,5,1]} position={[4,2,0]} rotation={[0,-Math.PI/2,0]}/>
 <Lightformer form="rect" intensity={2} color="#ffffff" scale={[6,.65,1]} position={[0,2,-4]} rotation={[0,0,0]}/>
 <Lightformer form="rect" intensity={.8} color="#ffffff" scale={[5,2,1]} position={[0,1,5]} rotation={[0,Math.PI,0]}/>
</Environment>
{grounded&&<ContactShadows position={[0,-.059,0]} opacity={.4} scale={8} blur={2.8} far={1.2} resolution={512} frames={Infinity} color="#000000"/>}
</>}
