import numpy as np
from PIL import Image as PILImage
from streamlit_drawable_canvas import st_canvas
from datetime import date
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as PDFImage
from reportlab.lib.styles import getSampleStyleSheet
st.set_page_config(page_title='TNG | Control de uniformes',layout='wide',page_icon='👕',initial_sidebar_state='expanded')
st.markdown("""<style>
[data-testid="stAppViewContainer"]{background:#f3f7fc;color:#132a49}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#071c3a,#0a3769)}
[data-testid="stSidebar"] *{color:#f3f8ff!important}
[data-testid="stSidebar"] [role="radiogroup"] label{border-radius:9px;padding:8px 10px;margin:3px 0}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){background:#1673c8}
.block-container{padding-top:1.1rem;max-width:1500px}
h1,h2,h3{color:#0a2b53!important}
[data-testid="stMetric"]{background:white;border:1px solid #dce6f3;border-radius:14px;padding:18px;box-shadow:0 3px 13px #123f7110}
[data-testid="stMetricLabel"]{font-weight:700;color:#37526f}
[data-testid="stMetricValue"]{color:#0a4e91}
[data-testid="stForm"], [data-testid="stExpander"]{background:white;border:1px solid #dce6f3;border-radius:14px}
[data-testid="stDataFrame"]{border:1px solid #dce6f3;border-radius:12px;overflow:hidden}
div.stButton>button[kind="primary"],div.stDownloadButton>button[kind="primary"]{background:#0866b4;color:white;border-radius:9px}
.tng-banner{background:linear-gradient(105deg,#06234b,#07599e);border-radius:16px;color:white;padding:22px 26px;margin-bottom:18px;box-shadow:0 6px 20px #092f5a20}
.tng-banner h2{color:white!important;margin:0;font-size:27px}.tng-banner p{margin:5px 0 0;color:#d8ecff}
.tng-card-title{font-size:18px;font-weight:750;color:#0a2b53;margin:10px 0}
</style>""",unsafe_allow_html=True)
DB=os.getenv('TNG_DB','tng_uniformes.db')
def conn():
    c=sqlite3.connect(DB,timeout=20); c.execute('PRAGMA foreign_keys=ON'); return c
def hashpw(p,s): return hashlib.pbkdf2_hmac('sha256',p.encode(),bytes.fromhex(s),600000).hex()
def adduser(c,u,p,r):
    s=secrets.token_hex(16); c.execute('INSERT INTO users VALUES(?,?,?,?)',(u,s,hashpw(p,s),r))
with conn() as c:
    c.execute('PRAGMA journal_mode=WAL')
    c.executescript('''CREATE TABLE IF NOT EXISTS users(u TEXT PRIMARY KEY,s TEXT,h TEXT,r TEXT);
    CREATE TABLE IF NOT EXISTS workers(id TEXT PRIMARY KEY,name TEXT,puesto TEXT,disciplina TEXT);
    CREATE TABLE IF NOT EXISTS stock(prenda TEXT,talla TEXT,qty INTEGER CHECK(qty>=0),PRIMARY KEY(prenda,talla));
    CREATE TABLE IF NOT EXISTS moves(id INTEGER PRIMARY KEY,fecha TEXT,prenda TEXT,talla TEXT,cantidad INTEGER,tipo TEXT,matricula TEXT,usuario TEXT,recibido TEXT);
    CREATE TABLE IF NOT EXISTS requests(id INTEGER PRIMARY KEY,matricula TEXT REFERENCES workers(id),prenda TEXT,talla TEXT,cantidad INTEGER CHECK(cantidad>0),estado TEXT,usuario TEXT);
    ''')
    columns=[row[1] for row in c.execute('PRAGMA table_info(moves)')]
    if 'firma_png' not in columns: c.execute('ALTER TABLE moves ADD COLUMN firma_png BLOB')
    if not c.execute('SELECT 1 FROM users').fetchone():
        try: a=st.secrets['ADMIN_PASSWORD']; b=st.secrets['ALMACEN_PASSWORD']
        except Exception:
            st.error('Configura ADMIN_PASSWORD y ALMACEN_PASSWORD en Secrets antes del primer inicio.'); st.stop()
        if min(len(a),len(b))<12 or a==b: st.error('Usa dos contraseñas distintas de al menos 12 caracteres.'); st.stop()
        adduser(c,'relaciones_laborales',a,'Admin'); adduser(c,'almacen',b,'Almacén')
CAT={p:[str(n) for n in range(28,53,2)] for p in ['Camisola','Pantalón','Overol']}
CAT.update({p:[str(n) for n in range(22,32)] for p in ['Botas MR','Botas DURAMAX','Botas PETROLERAS']})
def df(q,args=()):
    with conn() as c: return pd.read_sql_query(q,c,params=args)
def prendas(key):
    p=st.selectbox('Prenda',list(CAT),key=key+'p'); t=st.selectbox('Talla',CAT[p],key=key+'t'); return p,t
st.markdown('<div class="tng-banner"><h2>HUTCHISON PORTS TNG  |  Control de Uniformes</h2><p>Optimización del proceso de dotación, control y trazabilidad de uniformes</p></div>',unsafe_allow_html=True)
if 'user' not in st.session_state:
    with st.form('login'):
        u=st.text_input('Usuario'); p=st.text_input('Contraseña',type='password'); go=st.form_submit_button('Iniciar sesión')
    if go:
        with conn() as c: row=c.execute('SELECT s,h,r FROM users WHERE u=?',(u,)).fetchone()
        if row and hmac.compare_digest(hashpw(p,row[0]),row[1]): st.session_state.user=u; st.session_state.role=row[2]; st.rerun()
        else: st.error('Credenciales incorrectas')
    st.stop()
u=st.session_state.user; admin=st.session_state.role=='Admin'
st.sidebar.markdown('### 👕 TNG Uniformes'); st.sidebar.write('👤 Relaciones Laborales' if admin else '📦 Almacén'); st.sidebar.caption(u)
if st.sidebar.button('Cerrar sesión'): st.session_state.clear(); st.rerun()
page=st.sidebar.radio('MENÚ PRINCIPAL',['Panel general','Inventario','Dotación','Solicitudes','Reportes'])
def move(p,t,n,kind,worker='',rec='',request=None,firma=None):
    with conn() as c:
        c.execute('BEGIN IMMEDIATE')
        if request is not None:
            r=c.execute('SELECT matricula,prenda,talla,cantidad,estado FROM requests WHERE id=?',(request,)).fetchone()
            if r!=(worker,p,t,n,'Autorizada'): raise ValueError('Solicitud no disponible')
        c.execute('INSERT OR IGNORE INTO stock VALUES(?,?,0)',(p,t))
        delta=n if kind in ('Entrada','Devolución') else -n
        if not c.execute('UPDATE stock SET qty=qty+? WHERE prenda=? AND talla=? AND qty+?>=0',(delta,p,t,delta)).rowcount: raise ValueError('Existencias insuficientes')
        c.execute('INSERT INTO moves(fecha,prenda,talla,cantidad,tipo,matricula,usuario,recibido,firma_png) VALUES(datetime("now"),?,?,?,?,?,?,?,?)',(p,t,n,kind,worker,u,rec,firma))
        if request is not None: c.execute('UPDATE requests SET estado="Entregada" WHERE id=?',(request,))
def signature_box(key):
    st.write('**Firma del trabajador** (mouse o pantalla táctil)')
    st.caption('El trabajador debe firmar personalmente. Usa el botón de limpiar para repetirla.')
    canvas=st_canvas(fill_color='rgba(0,0,0,0)',stroke_width=3,stroke_color='#142e54',background_color='#FFFFFF',height=150,width=520,drawing_mode='freedraw',key=key,update_streamlit=True)
    if canvas.image_data is None: return None
    rgba=np.asarray(canvas.image_data).astype('uint8')
    if rgba.shape[-1]==4:
        mask=(rgba[:,:,:3]<190).any(axis=2) & (rgba[:,:,3]>0)
    else: mask=(rgba[:,:,:3]<190).any(axis=2)
    if int(mask.sum())<25: return None
    img=PILImage.fromarray(rgba).convert('RGB'); output=io.BytesIO(); img.save(output,format='PNG'); return output.getvalue()

def movement_table(query,args=()):
    return df(query,args).drop(columns=['firma_png'],errors='ignore')

def runmove(*args,**kwargs):
    try: move(*args,**kwargs); st.success('Movimiento registrado')
    except (ValueError,sqlite3.Error) as e: st.error(str(e))
if page=='Panel general':
    st.header('📊 Panel General')
    st.caption('Resumen de inventario, entregas y movimientos de uniformes')
    s=df('SELECT * FROM stock'); m=df('SELECT * FROM moves')
    trabajadores=int(df('SELECT COUNT(*) AS n FROM workers').iloc[0]['n'])
    entregas=int(m[m.tipo.isin(['Entrega','Reposición'])].cantidad.sum()) if not m.empty else 0
    a,b,d,e=st.columns(4)
    a.metric('📦 Existencias totales',int(s.qty.sum()))
    b.metric('👕 Prendas entregadas',entregas)
    d.metric('⚠️ Tallas con stock bajo',int((s.qty<=5).sum()))
    e.metric('👥 Trabajadores',trabajadores)
    if not s.empty:
        st.subheader('📈 Gráficas de inventario')
        left,right=st.columns(2)
        with left:
            st.write('Existencias por prenda')
            st.bar_chart(s.groupby('prenda').qty.sum())
        with right:
            st.write('Distribución de existencias')
            import matplotlib.pyplot as plt
            fig,ax=plt.subplots(figsize=(5,3.2)); totals=s.groupby('prenda').qty.sum(); totals=totals[totals>0]
            if not totals.empty:
                ax.pie(totals,labels=totals.index,autopct='%1.0f%%',textprops={'fontsize':8}); st.pyplot(fig)
            else: st.info('Todavía no hay existencias para graficar.')
            plt.close(fig)
        st.subheader('🚨 Alertas de existencias bajas')
        st.dataframe(s[s.qty<=5],hide_index=True)
    if s.empty: st.info('Registra entradas de inventario para visualizar las gráficas de existencias.')
    if not m.empty:
        st.subheader('Entradas, entregas, reposiciones y devoluciones')
        st.bar_chart(m.groupby('tipo').cantidad.sum())
        m['dia']=pd.to_datetime(m.fecha,errors='coerce').dt.date
        byday=m.pivot_table(index='dia',columns='tipo',values='cantidad',aggfunc='sum',fill_value=0)
        if not byday.empty:
            st.write('Movimientos por fecha'); st.line_chart(byday)
    if admin:
        with st.expander('⚙️ Administrar usuarios (solo Relaciones Laborales)'):
            with st.form('newuser'):
                nu=st.text_input('Nuevo usuario'); np=st.text_input('Contraseña (mínimo 12 caracteres)',type='password'); nr=st.selectbox('Rol',['Admin','Almacén']); go=st.form_submit_button('Crear cuenta')
            if go:
                if not nu.strip() or len(np)<12: st.error('Datos inválidos')
                else:
                    try:
                        with conn() as c: adduser(c,nu.strip(),np,nr)
                        st.success('Cuenta creada')
                    except sqlite3.IntegrityError: st.error('El usuario ya existe')
elif page=='Inventario':
    st.header('📦 Inventario y movimientos'); p,t=prendas('inv'); n=st.number_input('Cantidad',min_value=1,step=1); k=st.selectbox('Movimiento',['Entrada','Salida de ajuste']); motivo=st.text_input('Referencia o motivo')
    if st.button('Registrar movimiento'):
        if motivo.strip(): runmove(p,t,n,k,rec=motivo)
        else: st.error('Indica el motivo')
    st.dataframe(df('SELECT * FROM stock ORDER BY prenda,talla').rename(columns={'qty':'Existencias'}),hide_index=True)
elif page=='Dotación':
    st.header('👕 Dotación y firma del trabajador')
    st.caption('Busca por matrícula, registra la entrega y solicita la firma personal del trabajador.')
    if admin:
        with st.expander('Registrar trabajador'):
            with st.form('worker'):
                i=st.text_input('Matrícula'); name=st.text_input('Nombre'); puesto=st.text_input('Puesto'); disc=st.text_input('Disciplina'); go=st.form_submit_button('Guardar')
            if go:
                if all(x.strip() for x in (i,name,puesto,disc)):
                    with conn() as c: c.execute('INSERT INTO workers VALUES(?,?,?,?) ON CONFLICT(id) DO UPDATE SET name=excluded.name,puesto=excluded.puesto,disciplina=excluded.disciplina',(i.strip(),name,puesto,disc))
                    st.success('Trabajador guardado')
                else: st.error('Completa los campos')
    i=st.text_input('Buscar por matrícula').strip(); w=df('SELECT * FROM workers WHERE id=?',(i,))
    if not w.empty:
        st.dataframe(w,hide_index=True); p,t=prendas('dot'); n=st.number_input('Cantidad',min_value=1,step=1); k=st.selectbox('Tipo',['Entrega','Reposición','Devolución']); rec=st.text_input('Nombre de quien recibe o devuelve (constancia textual)')
        firma=signature_box('firma_dot_'+i)
        if st.button('Registrar dotación'):
            if not rec.strip(): st.error('Indica quién recibe')
            elif k in ('Entrega','Reposición') and firma is None: st.error('Se necesita la firma del trabajador para registrar esta entrega.')
            else: runmove(p,t,n,k,i,rec,firma=firma)
        st.dataframe(movement_table('SELECT * FROM moves WHERE matricula=? ORDER BY id DESC',(i,)),hide_index=True)
    elif i: st.warning('Matrícula no encontrada')
elif page=='Solicitudes':
    st.header('📋 Solicitudes y autorizaciones')
    if admin:
        i=st.text_input('Matrícula').strip(); p,t=prendas('sol'); n=st.number_input('Cantidad',min_value=1,step=1)
        if st.button('Crear solicitud'):
            try:
                with conn() as c: c.execute('INSERT INTO requests(matricula,prenda,talla,cantidad,estado,usuario) VALUES(?,?,?,?,?,?)',(i,p,t,n,'Pendiente',u))
                st.success('Solicitud creada')
            except sqlite3.IntegrityError: st.error('Matrícula no registrada')
    r=df('SELECT * FROM requests ORDER BY id DESC'); st.dataframe(r,hide_index=True)
    eligible=r[r.estado.isin(['Pendiente','Autorizada'] if admin else ['Autorizada'])]
    if not eligible.empty:
        rid=st.selectbox('Folio',eligible.id.tolist()); x=eligible[eligible.id==rid].iloc[0]
        if x.estado=='Pendiente' and admin:
            if st.button('Autorizar'):
                with conn() as c: c.execute('UPDATE requests SET estado="Autorizada" WHERE id=? AND estado="Pendiente"',(int(rid),))
                st.rerun()
        else:
            rec=st.text_input('Nombre de quien recibe')
            firma=signature_box('firma_solicitud_'+str(rid))
            if st.button('Confirmar entrega'):
                if not rec.strip(): st.error('Indica el nombre de quien recibe.')
                elif firma is None: st.error('Solicita la firma del trabajador antes de confirmar.')
                else: runmove(x.prenda,x.talla,int(x.cantidad),'Entrega',x.matricula,rec,int(rid),firma=firma)
else:
    st.header('📑 Reportes y trazabilidad'); m=movement_table('SELECT * FROM moves ORDER BY id DESC'); i=st.text_input('Filtrar matrícula'); m=m[m.matricula==i] if i else m; st.dataframe(m,hide_index=True)
    b=io.BytesIO(); m.to_excel(b,index=False); st.download_button('📥 Exportar Excel',b.getvalue(),'movimientos.xlsx',mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    if not m.empty:
        mid=st.selectbox('Movimiento para constancia PDF',m.id.tolist()); x=m[m.id==mid].iloc[0]; b=io.BytesIO(); styles=getSampleStyleSheet(); from xml.sax.saxutils import escape
        elements=[Paragraph('TNG | Acuse de movimiento',styles['Title']),Spacer(1,18)]
        for k,v in x.items(): elements.append(Paragraph(escape(f'{k}: {v}'),styles['Normal'])); elements.append(Spacer(1,7))
        with conn() as c: sig=c.execute('SELECT firma_png FROM moves WHERE id=?',(int(mid),)).fetchone()[0]
        if sig:
            elements.extend([Spacer(1,18),Paragraph('Firma del trabajador:',styles['Heading3']),PDFImage(io.BytesIO(sig),width=260,height=75)])
        else: elements.append(Paragraph('Sin firma digital registrada para este movimiento.',styles['Italic']))
        SimpleDocTemplate(b).build(elements)
        st.download_button('📄 Descargar acuse PDF con firma',b.getvalue(),f'acuse_{mid}.pdf',mime='application/pdf')
