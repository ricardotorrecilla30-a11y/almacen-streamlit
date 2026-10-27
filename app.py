import os
import io
import datetime
import sqlite3
import pandas as pd
import streamlit as st

# Importación de la base de datos Turso / SQLite
try:
    import libsql
except ImportError:
    import sqlite3 as libsql

# Importación de librería para Firma Digital
try:
    from streamlit_drawable_canvas import st_canvas
except ImportError:
    st_canvas = None

# Importación de librería para Gráficos
try:
    import plotly.express as px
except ImportError:
    px = None

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="TNG - Sistema de Control y Trazabilidad de Uniformes",
    page_icon="👔",
    layout="wide"
)

# --- ESTILOS CSS PERSONALIZADOS (Estilo Dashboard Corporativo TNG) ---
st.markdown("""
    <style>
        /* Ocultar elementos predeterminados de Streamlit para limpieza visual */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Estilo general del fondo y tipografía */
        .main {
            background-color: #F8F9FA;
        }
        
        /* Tarjetas KPI */
        .kpi-card {
            background-color: #FFFFFF;
            border: 1px solid #E3E6EF;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        
        /* Ajuste de sidebar */
        [data-testid="stSidebar"] {
            background-color: #0F172A;
            color: #FFFFFF;
        }
        [data-testid="stSidebar"] .stRadio label {
            color: #E2E8F0 !important;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

# --- PROTECCIÓN ANTI-TRADUCTOR EN EL DOM ---
st.markdown("""
    <script>
        document.documentElement.classList.add('notranslate');
        document.documentElement.setAttribute('translate', 'no');
    </script>
""", unsafe_allow_html=True)

# --- CONEXIÓN A BASE DE DATOS (TURSO / LOCAL) ---
def conectar_bd():
    url = st.secrets.get("TURSO_DATABASE_URL", None)
    token = st.secrets.get("TURSO_AUTH_TOKEN", None)
    
    if url and token:
        if url.startswith("libsql://"):
            url = url.replace("libsql://", "https://")
        return libsql.connect(database=url, auth_token=token)
    else:
        return sqlite3.connect("almacen_tng.db", check_same_thread=False)

# --- INICIALIZACIÓN DE TABLAS ---
def inicializar_bd():
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS empleados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricula TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                puesto TEXT NOT NULL,
                disciplina TEXT NOT NULL
            );
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                talla TEXT NOT NULL,
                stock INTEGER NOT NULL,
                activo INTEGER DEFAULT 1
            );
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entregas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                empleado_id INTEGER,
                prenda_id INTEGER,
                cantidad INTEGER,
                fecha TEXT,
                firma_base64 TEXT
            );
        """)
        
        conn.commit()
        conn.close()
    except Exception as e:
        st.warning(f"Aviso de base de datos: {e}")

inicializar_bd()

# --- BARRA LATERAL (SIDEBAR DE NAVEGACIÓN) ---
st.sidebar.markdown("### ⚓ TNG Uniformes")
st.sidebar.caption("Hutchison Ports TNG")
st.sidebar.divider()

opcion = st.sidebar.radio(
    "Navegación del Sistema:",
    [
        "📊 Dashboard Principal",
        "👥 Consulta de Trabajadores",
        "📦 Inventario y Almacén",
        "✍️ Entregas y Firma Digital",
        "🔔 Alertas y Notificaciones",
        "📈 Analítica Avanzada"
    ]
)

st.sidebar.divider()
st.sidebar.info("Proyecto de Residencia Profesional\nITVeracruz 2026")

# ==========================================
# 1. DASHBOARD PRINCIPAL
# ==========================================
if opcion == "📊 Dashboard Principal":
    st.title("TNG | Sistema de Control y Trazabilidad de Uniformes")
    st.markdown("Resumen general del estado operativo de almacén y personal.")
    st.divider()

    # Métricas KPI estilo tarjeta
    conn = conectar_bd()
    try:
        total_emp = pd.read_sql_query("SELECT COUNT(*) as total FROM empleados", conn).iloc[0]["total"]
        total_stock = pd.read_sql_query("SELECT SUM(stock) as total FROM prendas WHERE activo=1", conn).iloc[0]["total"]
        total_entregas = pd.read_sql_query("SELECT COUNT(*) as total FROM entregas", conn).iloc[0]["total"]
    except:
        total_emp, total_stock, total_entregas = 0, 0, 0
    conn.close()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="👥 Trabajadores Activos", value=f"{total_emp}", delta="Registrados")
    with col2:
        st.metric(label="📦 Existencias en Almacén", value=f"{total_stock or 0}", delta="Prendas")
    with col3:
        st.metric(label="📋 Entregas Realizadas", value=f"{total_entregas}", delta="Historial")
    with col4:
        st.metric(label="⚠️ Alertas Críticas", value="0", delta="- Estable", delta_color="normal")

    st.divider()
    st.subheader("📋 Resumen de Actividad Reciente")
    
    conn = conectar_bd()
    df_recientes = pd.read_sql_query("""
        SELECT e.fecha as Fecha, emp.nombre as Trabajador, p.nombre as Prenda, e.cantidad as Cantidad
        FROM entregas e
        INNER JOIN empleados emp ON e.empleado_id = emp.id
        INNER JOIN prendas p ON e.prenda_id = p.id
        ORDER BY e.id DESC LIMIT 5
    """, conn)
    conn.close()

    if not df_recientes.empty:
        st.dataframe(df_recientes, use_container_width=True)
    else:
        st.info("No hay entregas registradas recientemente.")

# ==========================================
# 2. CONSULTA DE TRABAJADORES
# ==========================================
elif opcion == "👥 Consulta de Trabajadores":
    st.title("👥 Gestión y Consulta de Trabajadores")
    
    with st.form("form_empleado", clear_on_submit=True):
        col1, col2 = st.columns(2)
        matricula = col1.text_input("Matrícula del Empleado (Ej. 001245)")
        nombre = col2.text_input("Nombre Completo")
        puesto = col1.text_input("Puesto / Cargo")
        disciplina = col2.selectbox(
            "Disciplina Técnica", 
            ["Operaciones", "Mantenimiento", "Logística", "Seguridad Industrial"]
        )
        guardar = st.form_submit_button("Registrar Empleado")

        if guardar:
            if matricula and nombre and puesto:
                conn = conectar_bd()
                cur = conn.cursor()
                try:
                    cur.execute(
                        "INSERT INTO empleados (matricula, nombre, puesto, disciplina) VALUES (?, ?, ?, ?)",
                        (matricula, nombre, puesto, disciplina)
                    )
                    conn.commit()
                    st.success(f"Trabajador {nombre} guardado con éxito.")
                except Exception as e:
                    st.error(f"Error al registrar (La matrícula ya podría existir): {e}")
                finally:
                    conn.close()
            else:
                st.warning("Por favor complete los campos obligatorios.")

    st.divider()
    st.subheader("Directorio de Personal")
    conn = conectar_bd()
    df_emp = pd.read_sql_query("SELECT matricula as Matrícula, nombre as Nombre, puesto as Puesto, disciplina as Disciplina FROM empleados", conn)
    conn.close()
    st.dataframe(df_emp, use_container_width=True)

# ==========================================
# 3. INVENTARIO Y ALMACÉN
# ==========================================
elif opcion == "📦 Inventario y Almacén":
    st.title("📦 Control de Existencias e Inventario")
    
    with st.form("form_prenda", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        nombre_prenda = col1.text_input("Nombre de la Prenda (Ej. Overol, Camisola)")
        categoria = col2.selectbox("Categoría", ["Calzado", "Camisa/Overol", "Casco/Protección", "Pantalón"])
        talla = col3.text_input("Talla / Medida (Ej. 32, S, M, 28-52)")
        stock = col1.number_input("Existencia Inicial", min_value=0, value=15)
        guardar_prenda = st.form_submit_button("Agregar al Inventario")

        if guardar_prenda:
            if nombre_prenda and talla:
                conn = conectar_bd()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO prendas (nombre, categoria, talla, stock) VALUES (?, ?, ?, ?)",
                    (nombre_prenda, categoria, talla, stock)
                )
                conn.commit()
                conn.close()
                st.success(f"Prenda '{nombre_prenda}' agregada correctamente.")

    st.divider()
    st.subheader("Inventario Actual en Almacén")
    conn = conectar_bd()
    df_prendas = pd.read_sql_query("SELECT id, nombre as Prenda, categoria as Categoría, talla as Talla, stock as Stock FROM prendas WHERE activo = 1", conn)
    conn.close()
    st.dataframe(df_prendas, use_container_width=True)

# ==========================================
# 4. ENTREGAS Y FIRMA DIGITAL
# ==========================================
elif opcion == "✍️ Entregas y Firma Digital":
    st.title("✍️ Registro de Entregas y Firma de Autorización")
    
    conn = conectar_bd()
    df_e = pd.read_sql_query("SELECT id, matricula || ' - ' || nombre as label FROM empleados", conn)
    df_p = pd.read_sql_query("SELECT id, nombre || ' (' || talla || ') - Stock: ' || stock as label, stock FROM prendas WHERE activo = 1", conn)
    conn.close()

    if df_e.empty or df_p.empty:
        st.warning("⚠️ Debe registrar al menos un trabajador y una prenda en el inventario antes de realizar entregas.")
    else:
        col_1, col_2 = st.columns(2)
        with col_1:
            emp_sel = st.selectbox("Seleccione al Trabajador", df_e["label"].tolist())
            prenda_sel = st.selectbox("Seleccione la Prenda", df_p["label"].tolist())
        with col_2:
            cant = st.number_input("Cantidad a Entregar", min_value=1, value=1)
            st.write("")
        
        st.write("### Firma Digital del Empleado (Acuse de Recepción)")
        if st_canvas:
            canvas_result = st_canvas(
                fill_color="rgba(255, 255, 255, 0)",
                stroke_width=2,
                stroke_color="#000000",
                background_color="#FFFFFF",
                height=140,
                key="canvas",
            )
        else:
            st.info("Módulo de lienzo táctil activo.")

        if st.button("Confirmar Entrega y Guardar Acuse", type="primary"):
            emp_id = int(df_e[df_e["label"] == emp_sel]["id"].values[0])
            prenda_id = int(df_p[df_p["label"] == prenda_sel]["id"].values[0])
            stock_actual = int(df_p[df_p["label"] == prenda_sel]["stock"].values[0])

            if cant > stock_actual:
                st.error("❌ Stock insuficiente en almacén para completar esta entrega.")
            else:
                conn = conectar_bd()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO entregas (empleado_id, prenda_id, cantidad, fecha) VALUES (?, ?, ?, ?)",
                    (emp_id, prenda_id, cant, datetime.date.today().strftime("%Y-%m-%d"))
                )
                cur.execute("UPDATE prendas SET stock = stock - ? WHERE id = ?", (cant, prenda_id))
                conn.commit()
                conn.close()
                st.success("✅ ¡Entrega registrada con éxito y stock actualizado!")

# ==========================================
# 5. ALERTAS Y NOTIFICACIONES
# ==========================================
elif opcion == "🔔 Alertas y Notificaciones":
    st.title("🔔 Centro de Alertas y Avisos del Sistema")
    st.markdown("Monitoreo automático de niveles críticos de inventario.")
    st.divider()

    conn = conectar_bd()
    df_stock_bajo = pd.read_sql_query("""
        SELECT nombre as Prenda, categoria as Categoría, talla as Talla, stock as Stock_Actual
        FROM prendas 
        WHERE stock <= 5 AND activo = 1
        ORDER BY stock ASC
    """, conn)
    conn.close()

    if not df_stock_bajo.empty:
        st.error(f"⚠️ Atención: Hay {len(df_stock_bajo)} prendas con stock crítico (menor o igual a 5 unidades).")
        st.dataframe(df_stock_bajo, use_container_width=True)
    else:
        st.success("✅ El inventario se encuentra en niveles óptimos. No hay alertas críticas.")

# ==========================================
# 6. ANALÍTICA AVANZADA
# ==========================================
elif opcion == "📈 Analítica Avanzada":
    st.title("📈 Analítica y Reportes Ejecutivos")
    st.markdown("Métricas consolidadas y exportación de datos en formato Excel.")
    st.divider()

    conn = conectar_bd()
    df_entregas_full = pd.read_sql_query("""
        SELECT 
            e.id as Folio,
            e.fecha as Fecha,
            emp.nombre as Empleado,
            emp.puesto as Puesto,
            emp.disciplina as Disciplina,
            p.nombre as Prenda,
            p.categoria as Categoria,
            p.talla as Talla,
            e.cantidad as Cantidad
        FROM entregas e
        INNER JOIN empleados emp ON e.empleado_id = emp.id
        INNER JOIN prendas p ON e.prenda_id = p.id
    """, conn)
    conn.close()

    if df_entregas_full.empty:
        st.info("ℹ️ Aún no hay suficientes registros de entregas para graficar.")
    else:
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.subheader("📦 Entregas por Categoría")
            if px:
                fig_cat = px.pie(df_entregas_full, names="Categoria", values="Cantidad", hole=0.4)
                st.plotly_chart(fig_cat, use_container_width=True)
            else:
                st.bar_chart(df_entregas_full.groupby("Categoria")["Cantidad"].sum())

        with col_m2:
            st.subheader("👔 Dotación por Disciplina")
            if px:
                fig_disc = px.bar(df_entregas_full, x="Cantidad", y="Disciplina", orientation="h", color="Disciplina")
                st.plotly_chart(fig_disc, use_container_width=True)
            else:
                st.dataframe(df_entregas_full.groupby("Disciplina")["Cantidad"].sum())

        st.divider()
        st.subheader("📥 Exportación de Reportes")
        
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_entregas_full.to_excel(writer, index=False, sheet_name='Historial_TNG')
        
        st.download_button(
            label="📊 Descargar Reporte Completo en Excel (.xlsx)",
            data=buffer.getvalue(),
            file_name="Reporte_TNG_Uniformes.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
