import * as THREE from 'three';
const cache=new Map();const material=c=>{if(!cache.has(c))cache.set(c,new THREE.MeshStandardMaterial({color:c,roughness:.77}));return cache.get(c);};
export function createAnimeCharacter(index=0,owner=false){
 const g=new THREE.Group();g.userData.characterStyle='anime-chibi';const skin=['#ffe0c1','#d6a178','#f2c5a3','#b78060'][index%4],shirt=['#eaa6b1','#9ac9df','#dbc286','#bea5df','#a5cbb8','#edbedb'][index%6],hair=owner?'#dc8740':['#4b3c4c','#8b624d','#343e60','#b48b63','#67627e'][index%5],iris=['#607eaa','#64836b','#8c69a0','#90684d'][index%4];
 const mesh=(p,geo,c,x=0,y=0,z=0)=>{const m=new THREE.Mesh(geo,material(c));m.position.set(x,y,z);m.castShadow=true;p.add(m);return m;};
 const ball=(p,r,c,x,y,z)=>mesh(p,new THREE.SphereGeometry(r,12,10),c,x,y,z);const legs=[],arms=[];
 for(const side of [-1,1]){const leg=new THREE.Group();leg.position.set(side*.105,.30,0);g.add(leg);mesh(leg,new THREE.CylinderGeometry(.065,.07,.24,8),'#fff4e8',0,-.10);mesh(leg,new THREE.BoxGeometry(.13,.10,.23),'#4d4b66',0,-.25,.04);legs.push(leg);const arm=new THREE.Group();arm.position.set(side*.225,.77,0);g.add(arm);mesh(arm,new THREE.CylinderGeometry(.075,.065,.26,8),shirt,0,-.11);ball(arm,.077,skin,0,-.27,0);arms.push(arm);}
 mesh(g,new THREE.CylinderGeometry(.18,.22,.42,10),owner?'#8fc5b8':shirt,0,.62);if(owner||index%2===0)mesh(g,new THREE.BoxGeometry(.36,.19,.26),'#545978',0,.37);if(!owner&&index%2)mesh(g,new THREE.CylinderGeometry(.20,.29,.20,12),shirt,0,.43);
 mesh(g,new THREE.BoxGeometry(.21,.19,.035),'#fff8ef',0,.76,.17);for(const side of [-1,1]){const collar=mesh(g,new THREE.BoxGeometry(.13,.045,.04),'#535b80',side*.065,.83,.20);collar.rotation.z=side*.38;}mesh(g,new THREE.BoxGeometry(.055,.13,.045),owner?'#efa753':'#a56583',0,.70,.20);
 const head=ball(g,.335,skin,0,1.075,0);head.name='anime-face';ball(g,.072,skin,-.33,1.06,0);ball(g,.072,skin,.33,1.06,0);
 const cap=mesh(g,new THREE.SphereGeometry(.35,16,10,0,Math.PI*2,0,Math.PI*.48),hair,0,1.095,0);cap.name='anime-hair';for(const side of [-1,1]){const bang=ball(g,.15,hair,side*.18,1.28,.20);bang.scale.set(.85,1.15,.45);if(!owner&&index%3===1){const tail=ball(g,.17,hair,side*.34,1.10,-.07);tail.scale.set(.8,1.4,.8);}}
 for(const side of [-1,1]){const x=side*.125;const outline=ball(g,.087,'#41354f',x,1.09,.297);outline.scale.set(.80,1.22,.28);const eye=ball(g,.069,iris,x,1.085,.316);eye.scale.set(.76,1.18,.28);const pupil=ball(g,.037,'#293247',x,1.085,.333);pupil.scale.set(.70,1.30,.25);ball(g,.024,'#ffffff',x-.018,1.122,.346);ball(g,.011,'#fffdf4',x+.020,1.066,.347);const cheek=ball(g,.049,'#edacb1',side*.235,1.00,.257);cheek.scale.set(1,.45,.20);}
 const smile=mesh(g,new THREE.TorusGeometry(.055,.009,5,12,Math.PI),'#a9696c',0,.97,.317);smile.rotation.z=Math.PI;
 if(owner){for(const [x,y,r,h]of [[0,1.59,.24,.65],[-.20,1.43,.13,.36],[.19,1.46,.13,.39]]){const flame=mesh(g,new THREE.ConeGeometry(r,h,8),'#e59445',x,y,0);flame.rotation.z=-x*.8;}mesh(g,new THREE.ConeGeometry(.12,.35,8),'#ffe3a1',.015,1.61,.11);}
 else if(index%3===0){mesh(g,new THREE.CylinderGeometry(.36,.36,.07,14),shirt,0,1.39);mesh(g,new THREE.SphereGeometry(.28,12,6,0,Math.PI*2,0,Math.PI/2),shirt,0,1.40);}
 return {g,legs,arms};
}
