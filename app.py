"""TNG - Control y Trazabilidad de Uniformes

Ejecutar:
    pip install -r requirements.txt
    python app.py
Abrir: http://localhost:5000
"""
import os
from flask import Flask, Response

app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>TNG · Control y Trazabilidad de Uniformes</title>
<style>
:root{--bg:#eef2f8;--card:#fff;--tx:#0f172a;--mu:#64748b;--bd:#e2e8f0;--nav:#0b1d3a;--pr:#1d4ed8;--ok:#16a34a;--wa:#f59e0b;--er:#dc2626;--hd:#f1f5f9;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0b1220;--card:#131c2e;--tx:#e8edf6;--mu:#93a1b8;--bd:#25324a;--hd:#1a2540;color-scheme:dark}}
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--tx);font-size:14px}
.app{display:flex;min-height:100vh}
aside{width:200px;background:var(--nav);color:#cbd5e1;padding:18px 12px;display:flex;flex-direction:column;gap:6px;position:sticky;top:0;height:100vh}
aside h1{color:#fff;font-size:24px;margin:0 8px 18px;letter-spacing:1px}
aside button{all:unset;cursor:pointer;padding:11px 12px;border-radius:8px;display:flex;gap:10px;align-items:center;font-size:14px}
aside button:hover{background:#ffffff14}
aside button.on{background:var(--pr);color:#fff}
main{flex:1;padding:20px;min-width:0}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;gap:10px}
.top h2{margin:0;font-size:20px}
.top small{color:var(--mu)}
.card{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:16px;margin-bottom:16px}
.card h3{margin:0 0 12px;font-size:15px}
.grid{display:grid;gap:12px}
.g4{grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}
.g2{grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}
.kpi{border-radius:12px;padding:16px;color:#fff;cursor:pointer}
.kpi b{font-size:30px;display:block}
.k1{background:#2563eb}.k2{background:#16a34a}.k3{background:#f59e0b}.k4{background:#7c3aed}
.ring{width:74px;height:74px;border-radius:50%;display:grid;place-items:center;font-weight:700;margin:auto}
.ring i{background:var(--card);width:56px;height:56px;border-radius:50%;display:grid;place-items:center;font-style:normal}
table{width:100%;border-collapse:collapse}
th,td{text-align:left;padding:9px 8px;border-bottom:1px solid var(--bd)}
th{background:var(--hd);font-size:12px;color:var(--mu)}
.tw{overflow-x:auto}
tr.cl{cursor:pointer}tr.cl:hover{background:var(--hd)}
.b{padding:3px 10px;border-radius:99px;font-size:12px;font-weight:600;display:inline-block}
.b.ok{background:#dcfce7;color:#166534}.b.wa{background:#fef3c7;color:#92400e}.b.er{background:#fee2e2;color:#991b1b}
button.p,button.s{border:0;border-radius:8px;padding:9px 16px;cursor:pointer;font-size:14px;font-weight:600}
button.p{background:var(--pr);color:#fff}
button.s{background:var(--hd);color:var(--tx);border:1px solid var(--bd)}
button.g{background:var(--ok);color:#fff;border:0;border-radius:8px;padding:9px 16px;cursor:pointer;font-weight:600}
input,select,textarea{width:100%;padding:9px;border:1px solid var(--bd);border-radius:8px;background:var(--card);color:var(--tx);font:inherit}
label{display:block;font-size:12px;color:var(--mu);margin:10px 0 4px}
.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.chip{padding:6px 14px;border-radius:99px;border:1px solid var(--bd);cursor:pointer;background:var(--card)}
.chip.on{background:var(--pr);color:#fff;border-color:var(--pr)}
canvas{width:100%;height:130px;border:1px dashed var(--mu);border-radius:8px;background:#fff;touch-action:none}
.ov{position:fixed;inset:0;background:#0009;display:none;align-items:center;justify-content:center;z-index:50;padding:14px}
.ov.on{display:flex}
.md{background:var(--card);border-radius:14px;padding:20px;width:100%;max-width:520px;max-height:90vh;overflow:auto}
.md.w{max-width:760px}
.dr{justify-content:flex-end}
.dr .md{max-width:460px;height:100%;max-height:100%;border-radius:14px 0 0 14px}
.fab{position:fixed;right:18px;bottom:18px;width:54px;height:54px;border-radius:50%;background:var(--pr);color:#fff;border:0;font-size:24px;cursor:pointer;z-index:40}
#chat{position:fixed;right:18px;bottom:84px;width:320px;max-width:calc(100vw - 36px);background:var(--card);border:1px solid var(--bd);border-radius:14px;display:none;flex-direction:column;z-index:40;height:380px}
#chat.on{display:flex}
#msgs{flex:1;overflow:auto;padding:12px;display:flex;flex-direction:column;gap:8px}
.m{padding:8px 11px;border-radius:12px;max-width:85%;background:var(--hd)}
.m.u{background:var(--pr);color:#fff;align-self:flex-end}
.nt{display:flex;gap:10px;padding:10px 0;border-bottom:1px solid var(--bd)}
.nt:last-child{border:0}
#bell{position:relative}
#pop{position:absolute;right:0;top:44px;width:320px;max-width:90vw;display:none;z-index:30}
#pop.on{display:block}
.mob{display:none}
@media(max-width:760px){
 .app{flex-direction:column}
 aside{width:100%;height:auto;flex-direction:row;overflow-x:auto;position:sticky;z-index:20;padding:8px}
 aside h1{display:none}aside button{flex:none;padding:9px 11px}
 main{padding:12px}
}
@media print{aside,.fab,#chat,.top,.noprint{display:none!important}.ov{position:static;background:none}}
</style>
</head>
<body>
<div class="app">
<aside id="nav"></aside>
<main>
 <div class="top">
  <div><h2 id="ttl"></h2><small id="sub"></small></div>
  <div class="row" style="position:relative">
   <button class="s" id="bell" onclick="togglePop()">🔔 <span id="nc" class="b er"></span></button>
   <div id="pop" class="card"></div>
  </div>
 </div>
 <div id="view"></div>
</main>
</div>
<button class="fab" onclick="document.getElementById('chat').classList.toggle('on')" title="Asistente TNG">💬</button>
<div id="chat"><div style="padding:10px 12px;border-bottom:1px solid var(--bd)"><b>Asistente TNG 2.0</b></div>
<div id="msgs"><div class="m">Hola, puedes preguntarme: “¿Cuál es la matrícula de Juan Pérez?” o “¿Cuántas botas talla 27 hay?”</div></div>
<div class="row" style="padding:8px"><input id="q" placeholder="Escribe tu pregunta..." onkeydown="if(event.key==='Enter')ask()" style="flex:1"><button class="p" onclick="ask()">➤</button></div></div>
<div class="ov" id="ov" onclick="if(event.target===this)closeM()"><div class="md" id="md"></div></div>

<script>
const $=id=>document.getElementById(id);
let W=[
{m:'001245',n:'Juan Pérez López',d:'Operaciones',t:'Sindicalizado',ing:'12/03/2020',s:'Activo'},
{m:'001102',n:'Luis Ramírez',d:'Mantenimiento',t:'Sindicalizado',ing:'05/08/2019',s:'Activo'},
{m:'001118',n:'Carlos Ruiz',d:'Almacén',t:'Confianza',ing:'14/02/2021',s:'Activo'},
{m:'001134',n:'Ana Torres',d:'Producción',t:'Sindicalizado',ing:'20/09/2018',s:'Baja'},
{m:'001301',n:'María González',d:'Almacén',t:'Confianza',ing:'03/01/2022',s:'Activo'}];
let INV=[
{n:'Overol',r:'28 - 52',e:320,min:100,c:'overol'},
{n:'Camisola',r:'28 - 52',e:180,min:80,c:'camisola'},
{n:'Pantalón',r:'28 - 52',e:240,min:80,c:'pantalon'},
{n:'Botas MR',r:'22 - 31',e:95,min:50,c:'botas'},
{n:'Botas DURAMAX',r:'22 - 31',e:60,min:60,c:'botas'},
{n:'Botas PETROLERAS',r:'22 - 31',e:45,min:60,c:'botas'}];
let MOV=[
{f:'15/01/2025',t:'Entrada',m:'—',p:'Overol',tl:'42',q:10,u:'Almacén'},
{f:'20/01/2025',t:'Entrega',m:'001245',p:'Overol',tl:'42',q:1,u:'RL'},
{f:'05/03/2025',t:'Devolución',m:'001245',p:'Overol',tl:'42',q:1,u:'Almacén'},
{f:'10/03/2025',t:'Entrega',m:'001245',p:'Overol',tl:'42',q:1,u:'RL'},
{f:'22/03/2025',t:'Cambio de talla',m:'001245',p:'Overol',tl:'44',q:1,u:'Almacén'}];
let SOL=[{id:'SOL-00465',p:'Camisola',tl:'42',q:5,mo:'Desgaste'}];
let NOT=[
{i:'🔴',t:'Nueva solicitud de reposición',d:'SOL-00465 · Camisola talla 42',h:'Hoy 10:24'},
{i:'🟠',t:'Stock bajo',d:'Botas DURAMAX talla 27 · 15 piezas restantes',h:'Ayer 12:45'},
{i:'🟣',t:'Recordatorio de dotación',d:'Próxima dotación: 15/11/2026',h:'Ayer 08:00'}];
const MOT=['Desgaste','Daño','Pérdida','Cambio de talla','Reposición programada'];
let tab='inicio',fil='Todas',sel='';
const T={inicio:['Inicio','Bienvenido, Relaciones Laborales'],inv:['Inventario de uniformes','Existencias y reposición'],ent:['Entregas','Registro, firma digital y acuse'],tra:['Trabajadores','Expediente, historial y bajas'],rep:['Reportes','Consulta y exportación']};
const ICO={inicio:'🏠',inv:'📦',ent:'📝',tra:'👷',rep:'📊'};
function nav(){ $('nav').innerHTML='<h1>TNG</h1>'+Object.keys(T).map(k=>`<button class="${k===tab?'on':''}" onclick="go('${k}')">${ICO[k]} ${T[k][0].split(' ')[0]}</button>`).join('')}
function go(k){tab=k;$('pop').classList.remove('on');render()}
function st(p){return p.e<=p.min?['wa','Stock bajo']:['ok','Normal']}
function render(){nav();$('ttl').textContent=T[tab][0];$('sub').textContent=T[tab][1];$('nc').textContent=NOT.length;$('view').innerHTML=V[tab]();if(tab==='ent')initEnt()}
function togglePop(){ $('pop').innerHTML='<h3>Notificaciones</h3>'+NOT.map(n=>`<div class="nt"><span>${n.i}</span><div><b>${n.t}</b><br><small>${n.d} · ${n.h}</small></div></div>`).join('');$('pop').classList.toggle('on')}
const V={
inicio(){const a=W.filter(w=>w.s==='Activo').length,bajo=INV.filter(p=>p.e<=p.min).length;
return `<div class="card" style="background:linear-gradient(135deg,#0b1d3a,#1d4ed8);color:#fff;border:0"><h2 style="margin:0 0 4px">Sistema de Control y Trazabilidad de Uniformes</h2><span>Controla · Registra · Anticipa</span></div>
<div class="grid g4" style="margin-bottom:16px">
<div class="kpi k1" onclick="go('tra')"><b>${a}</b>Trabajadores activos</div>
<div class="kpi k2" onclick="go('ent')"><b>${MOV.filter(m=>m.t==='Entrega').length}</b>Entregas registradas</div>
<div class="kpi k3" onclick="go('inv')"><b>${SOL.length}</b>Solicitudes en proceso</div>
<div class="kpi k4" onclick="go('inv')"><b>${bajo}</b>Prendas con stock bajo</div></div>
<div class="card"><h3>Indicadores clave (KPI)</h3><div class="grid g4">
${[['92%','Entrega oportuna',92,'#16a34a'],['3.4','Rotación de inventario',68,'#2563eb'],[bajo,'Prendas en stock bajo',40,'#f59e0b'],['2','Próximas dotaciones',25,'#7c3aed']].map(k=>`<div style="text-align:center"><div class="ring" style="background:conic-gradient(${k[3]} ${k[2]}%,var(--bd) 0)"><i>${k[0]}</i></div><small>${k[1]}</small></div>`).join('')}</div></div>
<div class="card"><h3>Movimientos de uniformes (últimos 7 días)</h3>${bars()}</div>`},
inv(){const l=INV.filter(p=>fil==='Todas'||p.c===fil.toLowerCase().replace('ó','o'));
return `<div class="card"><div class="row" style="margin-bottom:12px">${['Todas','Overol','Camisola','Pantalón','Botas'].map(c=>`<span class="chip ${c===fil?'on':''}" onclick="fil='${c}';render()">${c}</span>`).join('')}<span style="flex:1"></span><button class="p" onclick="solM()">+ Solicitar reposición</button></div>
<div class="tw"><table><tr><th>Prenda</th><th>Talla</th><th>Existencia</th><th>Estado</th></tr>${l.map(p=>{const s=st(p);return `<tr><td>${p.n}</td><td>${p.r}</td><td>${p.e}</td><td><span class="b ${s[0]}">${s[1]}</span></td></tr>`}).join('')}</table></div></div>
<div class="card"><h3>Solicitudes de reposición</h3>${SOL.map(s=>`<div class="nt"><div><b>${s.id}</b> · ${s.p} talla ${s.tl} × ${s.q}<br><small>Motivo: ${s.mo}</small></div></div>`).join('')||'Sin solicitudes'}</div>`},
ent(){return `<div class="grid g2"><div class="card"><h3>Nueva entrega</h3>
<label>Matrícula o nombre del trabajador</label><input id="wk" list="wl" placeholder="Buscar trabajador..." oninput="fillW()"><datalist id="wl">${W.filter(w=>w.s==='Activo').map(w=>`<option value="${w.m} - ${w.n}">`).join('')}</datalist>
<div id="wi" style="color:var(--mu);margin-top:6px">Disciplina / tipo: —</div>
<label>Prendas a entregar</label><div id="pr"></div>
<button class="s" onclick="addP()" style="margin-top:6px">+ Agregar prenda</button>
<label>Firma del trabajador</label><canvas id="cv"></canvas>
<div class="row" style="margin-top:8px"><button class="s" onclick="clr()">Limpiar</button><button class="p" onclick="entrega()">Generar acuse</button></div></div>
<div class="card"><h3>Historial de movimientos</h3><div class="tw"><table><tr><th>Fecha</th><th>Tipo</th><th>Matrícula</th><th>Prenda</th><th>Talla</th><th>Cant.</th></tr>${MOV.slice().reverse().map(m=>`<tr><td>${m.f}</td><td>${m.t}</td><td>${m.m}</td><td>${m.p}</td><td>${m.tl}</td><td>${m.q}</td></tr>`).join('')}</table></div></div></div>`},
tra(){return `<div class="card"><div class="tw"><table><tr><th>Matrícula</th><th>Nombre</th><th>Disciplina</th><th>Tipo</th><th>Estatus</th></tr>${W.map(w=>`<tr class="cl" onclick="exp('${w.m}')"><td>${w.m}</td><td>${w.n}</td><td>${w.d}</td><td>${w.t}</td><td><span class="b ${w.s==='Activo'?'ok':'er'}">${w.s}</span></td></tr>`).join('')}</table></div><small style="color:var(--mu)">Toca un trabajador para abrir su expediente.</small></div>`},
rep(){const R=[['Inventario actual'],['Movimientos por prenda'],['Entregas por trabajador'],['Solicitudes pendientes'],['Reporte de bajas']];
return `<div class="card">${R.map((r,i)=>`<div class="nt" style="align-items:center"><span style="flex:1">📄 ${r[0]}</span><button class="s" onclick="repM(${i})">Ver reporte</button></div>`).join('')}</div>`}};
function bars(){const d=[[8,5,30],[12,9,28],[6,11,25],[14,7,32],[9,8,33],[11,12,30],[7,6,31]];return `<div style="display:flex;gap:10px;align-items:flex-end;height:130px">${d.map((x,i)=>`<div style="flex:1;display:flex;gap:2px;align-items:flex-end;height:100%">${x.map((v,j)=>`<div title="${v}" style="flex:1;height:${v*3}px;background:${['#2563eb','#f59e0b','#16a34a'][j]};border-radius:3px 3px 0 0"></div>`).join('')}</div>`).join('')}</div><small>■ Entradas ■ Salidas ■ Existencia</small>`}
function openM(h,c){$('md').className='md '+(c||'');$('md').innerHTML=h;$('ov').className='ov on '+(c==='dr'?'dr':'')}
function closeM(){$('ov').className='ov'}
function sig(c){const x=c.getContext('2d');const r=c.getBoundingClientRect();c.width=r.width;c.height=r.height;x.lineWidth=2;x.lineCap='round';x.strokeStyle='#1e3a8a';let d=false;c.dirty=false;
c.onpointerdown=e=>{d=true;c.dirty=true;x.beginPath();x.moveTo(e.offsetX,e.offsetY)};c.onpointermove=e=>{if(d){x.lineTo(e.offsetX,e.offsetY);x.stroke()}};c.onpointerup=c.onpointerleave=()=>d=false}
function clr(id){const c=$(id||'cv');c.getContext('2d').clearRect(0,0,c.width,c.height);c.dirty=false}
function initEnt(){ $('pr').innerHTML='';addP();sig($('cv'))}
function addP(){const d=document.createElement('div');d.className='row';d.style.marginBottom='6px';d.innerHTML=`<select style="flex:2">${INV.map(p=>`<option>${p.n}</option>`).join('')}</select><input placeholder="Talla" style="flex:1" value="42"><input type="number" min="1" value="1" style="flex:1">`;$('pr').appendChild(d)}
function fillW(){const m=($('wk').value.match(/^\d+/)||[''])[0];const w=W.find(x=>x.m===m);$('wi').textContent=w?`Disciplina: ${w.d} · Tipo: ${w.t}`:'Disciplina / tipo: —'}
function entrega(){const m=($('wk').value.match(/^\d+/)||[''])[0];const w=W.find(x=>x.m===m&&x.s==='Activo');if(!w)return alert('Selecciona un trabajador activo de la lista.');if(!$('cv').dirty)return alert('Falta la firma del trabajador.');
const items=[...$('pr').children].map(r=>({p:r.children[0].value,tl:r.children[1].value,q:+r.children[2].value||1}));const img=$('cv').toDataURL();const f=new Date().toLocaleDateString('es-MX');
items.forEach(i=>{MOV.push({f,t:'Entrega',m:w.m,p:i.p,tl:i.tl,q:i.q,u:'RL'});const p=INV.find(x=>x.n===i.p);if(p)p.e=Math.max(0,p.e-i.q)});
openM(`<h3>Acuse de entrega</h3><p><b>Matrícula:</b> ${w.m}<br><b>Nombre:</b> ${w.n}<br><b>Fecha:</b> ${new Date().toLocaleString('es-MX')}</p><table><tr><th>Prenda</th><th>Talla</th><th>Cant.</th></tr>${items.map(i=>`<tr><td>${i.p}</td><td>${i.tl}</td><td>${i.q}</td></tr>`).join('')}</table><p><b>Firma del trabajador</b></p><img src="${img}" style="width:100%;max-height:120px;object-fit:contain;border:1px solid var(--bd);border-radius:8px;background:#fff"><div class="row noprint" style="margin-top:12px"><button class="p" onclick="window.print()">Imprimir / PDF</button><button class="s" onclick="closeM();render()">Cerrar</button></div>`)}
function solM(){openM(`<h3>Solicitud de reposición</h3><label>Prenda</label><select id="sp">${INV.map(p=>`<option>${p.n}</option>`).join('')}</select><div class="row"><div style="flex:1"><label>Talla</label><input id="st" value="42"></div><div style="flex:1"><label>Cantidad</label><input id="sq" type="number" min="1" value="5"></div></div><label>Motivo</label><select id="sm">${MOT.map(m=>`<option>${m}</option>`).join('')}</select><label>Firma de autorización</label><canvas id="sc"></canvas><div class="row" style="margin-top:10px"><button class="s" onclick="clr('sc')">Limpiar</button><button class="p" onclick="saveSol()">Guardar solicitud</button><button class="s" onclick="closeM()">Cancelar</button></div>`);sig($('sc'))}
function saveSol(){if(!$('sc').dirty)return alert('Falta la firma de autorización.');const id='SOL-'+String(466+SOL.length).padStart(5,'0');SOL.push({id,p:$('sp').value,tl:$('st').value,q:$('sq').value,mo:$('sm').value});NOT.unshift({i:'🔴',t:'Nueva solicitud de reposición',d:id+' · '+$('sp').value,h:'Ahora'});closeM();render()}
function exp(m){const w=W.find(x=>x.m===m);const h=MOV.filter(x=>x.m===m);
openM(`<div class="row" style="justify-content:space-between"><h3 style="margin:0">Expediente digital</h3><button class="s" onclick="closeM()">✕</button></div><p><b style="font-size:17px">${w.n}</b><br>Matrícula ${w.m} · ${w.d} · ${w.t}<br>Ingreso: ${w.ing} · <span class="b ${w.s==='Activo'?'ok':'er'}">${w.s}</span></p>
<h3>Documentos</h3><div class="nt">📕 INE.pdf</div><div class="nt">📕 Comprobante de domicilio.pdf</div><div class="nt">📕 RFC.pdf</div>
<h3 style="margin-top:12px">Historial de movimientos</h3><div class="tw"><table><tr><th>Fecha</th><th>Tipo</th><th>Prenda</th><th>Talla</th></tr>${h.map(x=>`<tr><td>${x.f}</td><td>${x.t}</td><td>${x.p}</td><td>${x.tl}</td></tr>`).join('')||'<tr><td colspan=4>Sin movimientos</td></tr>'}</table></div>
${w.s==='Activo'?`<button class="p" style="margin-top:14px;background:var(--er)" onclick="bajaM('${m}')">Registrar baja</button>`:''}`,'dr')}
function bajaM(m){openM(`<h3>Registrar baja</h3><label>Motivo</label><select id="bm"><option>Renuncia</option><option>Despido</option><option>Invalidez</option></select><div class="row" style="margin-top:14px"><button class="p" onclick="baja('${m}')">Confirmar baja</button><button class="s" onclick="exp('${m}')">Cancelar</button></div>`)}
function baja(m){const w=W.find(x=>x.m===m);w.s='Baja';NOT.unshift({i:'🟣',t:'Baja de trabajador',d:w.m+' · '+w.n+' · '+$('bm').value,h:'Ahora'});closeM();render()}
function repM(i){const D=[
['Inventario actual',['Prenda','Talla','Existencia'],INV.map(p=>[p.n,p.r,p.e])],
['Movimientos por prenda',['Fecha','Tipo','Matrícula','Prenda','Cant.'],MOV.map(m=>[m.f,m.t,m.m,m.p,m.q])],
['Entregas por trabajador',['Matrícula','Entregas'],W.map(w=>[w.m+' '+w.n,MOV.filter(x=>x.m===w.m&&x.t==='Entrega').length])],
['Solicitudes pendientes',['Folio','Prenda','Talla','Cant.','Motivo'],SOL.map(s=>[s.id,s.p,s.tl,s.q,s.mo])],
['Bajas de trabajadores',['Matrícula','Nombre','Estatus'],W.filter(w=>w.s==='Baja').map(w=>[w.m,w.n,w.s])]][i];
openM(`<h3>${D[0]}</h3><div class="tw"><table><tr>${D[1].map(h=>`<th>${h}</th>`).join('')}</tr>${D[2].map(r=>`<tr>${r.map(c=>`<td>${c}</td>`).join('')}</tr>`).join('')||'<tr><td>Sin datos</td></tr>'}</table></div><div class="row noprint" style="margin-top:12px"><button class="p" onclick="window.print()">Imprimir / PDF</button><button class="s" onclick="closeM()">Cerrar</button></div>`,'w')}
function say(t,u){const d=document.createElement('div');d.className='m'+(u?' u':'');d.innerHTML=t;$('msgs').appendChild(d);$('msgs').scrollTop=1e5}
function ask(){const v=$('q').value.trim();if(!v)return;$('q').value='';say(v,1);const l=v.toLowerCase();let r='No encontré eso. Prueba con un nombre, una matrícula o “stock bajo”.';
const w=W.find(x=>l.includes(x.n.toLowerCase().split(' ')[0])&&l.includes(x.n.toLowerCase().split(' ')[1]||'')||l.includes(x.m));
if(w)r=`<b>${w.n}</b><br>Matrícula: ${w.m}<br>${w.d} · ${w.t} · ${w.s}`;
else if(l.includes('stock')||l.includes('existencia')||l.includes('botas')){const b=INV.filter(p=>l.includes('botas')?p.c==='botas':p.e<=p.min);r=b.map(p=>`${p.n}: ${p.e} pzas`).join('<br>')||'Todo en orden.'}
else if(l.includes('solicitud'))r=SOL.map(s=>`${s.id} · ${s.p} × ${s.q}`).join('<br>');
say(r)}
render();
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return Response(HTML, mimetype="text/html")


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
