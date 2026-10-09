import os
import io
import datetime
import sqlite3
import pandas as pd
import streamlit as st
import bcrypt
from PIL import Image

# Importación de la librería de base de datos Turso / SQLite
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
    page_title="Control de Uniformes - TNG",
    page_icon="👔",
    layout="wide"
)

# --- PROTECCIÓN ANTI-TRADUCTOR EN EL DOM ---
st.markdown("""
    <script>
        document.documentElement.classList.add('notranslate');
        document.documentElement.setAttribute('translate', 'no');
    </script>
    <style>
        .notranslate {
            translate: no !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN A BASE DE DATOS (TURSO / LOCAL) ---
def conectar_bd():
    url = st.secrets.get("TURSO_DATABASE_URL", None)
    token = st.secrets.get("TURSO_AUTH_TOKEN", None)
    
    if url and token:
        return libsql.connect(url, auth_token=token)
    else:
        return sqlite3.connect("almacen_tng.db", check_same_thread=False)

# --- INICIALIZACIÓN DE TABLAS ---
def inicializar_bd():
    conn = conectar_bd()
    cursor = conn.cursor()
    
    # Tabla Empleados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            puesto TEXT NOT NULL,
            disciplina TEXT NOT NULL
        )
    """)
    
    # Tabla Prendas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            talla TEXT NOT NULL,
            stock INTEGER NOT NULL,
            activo INTEGER DEFAULT 1
        )
    """)
    
    # Tabla Entregas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entregas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empleado_id INTEGER,
            prenda_id INTEGER,
            cantidad INTEGER,
            fecha TEXT,
            firma_base64 TEXT,
            FOREIGN KEY (empleado_id) REFERENCES empleados (id),
            FOREIGN KEY (prenda_id) REFERENCES prendas (id)
        )
    """)
    
    # Tabla Matriz de Dotación
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dotaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            puesto TEXT NOT NULL,
            prenda_id INTEGER,
            frecuencia_dias INTEGER DEFAULT 180,
            FOREIGN KEY (prenda_id) REFERENCES prendas (id)
        )
    """)
    
    conn.commit()
    conn.close()

inicializar_bd()

# --- MENÚ LATERAL DE NAVEGACIÓN ---
st.sidebar.title("Hutchison Ports TNG")
st.sidebar.image("https://img.icons8.com/color/96/worker-male.png", width=80)

opcion = st.sidebar.radio(
    "Navegación / Módulos:",
    [
        "👥 Registro de Trabajadores",
        "📦 Control de Almacén",
        "✍️ Entregas y Firma Digital",
        "🔔 Alertas y Notificaciones",
        "📊 Analítica Avanzada"
    ]
)

# ==========================================
# 1. MÓDULO: REGISTRO DE TRABAJADORES
# ==========================================
if opcion == "👥 Registro de Trabajadores":
    st.header("👥 Gestión y Registro de Trabajadores")
    st.caption("Administración de nómina, puestos y disciplinas técnicas.")

    with st.form("form_empleado", clear_on_submit=True):
        col1, col2 = st.columns(2)
        matricula = col1.text_input("Matrícula del Empleado")
        nombre = col2.text_input("Nombre Completo")
        puesto = col1.text_input("Puesto / Cargo")
        disciplina = col2.selectbox(
            "Disciplina Técnica", 
            ["Mecánica y Tubería", "Electricidad e Instrumentación", "Pintura y Maniobras", "Administrativo"]
        )
        guardar = st.form_submit_button("Guardar Empleado")

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
                    st.success(f"Empleado {nombre} registrado correctamente.")
                except Exception as e:
                    st.error(f"Error al registrar: {e}")
                finally:
                    conn.close()
            else:
                st.warning("Por favor complete todos los campos obligatorios.")

    st.subheader("Lista de Trabajadores Registrados")
    conn = conectar_bd()
    df_emp = pd.read_sql_query("SELECT matricula as Matrícula, nombre as Nombre, puesto as Puesto, disciplina as Disciplina FROM empleados", conn)
    conn.close()
    st.dataframe(df_emp, use_container_width=True)

# ==========================================
# 2. MÓDULO: CONTROL DE ALMACÉN
# ==========================================
elif opcion == "📦 Control de Almacén":
    st.header("📦 Control de Inventario de Prendas y EPI")
    
    with st.form("form_prenda", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        nombre_prenda = col1.text_input("Nombre de la Prenda / Equipo")
        categoria = col2.selectbox("Categoría", ["Calzado", "Camisa/Overol", "Casco/Protección", "Pantalón"])
        talla = col3.text_input("Talla / Medida")
        stock = col1.number_input("Existencia Inicial", min_value=0, value=10)
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
                st.success(f"Prenda '{nombre_prenda}' agregada con éxito.")

    st.subheader("Existencias en Almacén")
    conn = conectar_bd()
    df_prendas = pd.read_sql_query("SELECT id, nombre as Prenda, categoria as Categoría, talla as Talla, stock as Stock FROM prendas WHERE activo = 1", conn)
    conn.close()
    st.dataframe(df_prendas, use_container_width=True)

# ==========================================
# 3. MÓDULO: ENTREGAS Y FIRMA DIGITAL
# ==========================================
elif opcion == "✍️ Entregas y Firma Digital":
    st.header("✍️ Entrega de Uniformes y Firma de Conformidad")
    
    conn = conectar_bd()
    df_e = pd.read_sql_query("SELECT id, matricula || ' - ' || nombre as label FROM empleados", conn)
    df_p = pd.read_sql_query("SELECT id, nombre || ' (' || talla || ') - Stock: ' || stock as label, stock FROM prendas WHERE activo = 1", conn)
    conn.close()

    if df_e.empty or df_p.empty:
        st.warning("Debe registrar al menos un empleado y una prenda en el inventario antes de realizar entregas.")
    else:
        emp_sel = st.selectbox("Seleccione al Trabajador", df_e["label"].tolist())
        prenda_sel = st.selectbox("Seleccione la Prenda", df_p["label"].tolist())
        cant = st.number_input("Cantidad a Entregar", min_value=1, value=1)
        
        st.write("### Firma Digital del Empleado")
        if st_canvas:
            canvas_result = st_canvas(
                fill_color="rgba(255, 255, 255, 0)",
                stroke_width=2,
                stroke_color="#000000",
                background_color="#eeeeee",
                height=150,
                key="canvas",
            )
        else:
            st.info("Instale 'streamlit-drawable-canvas' para habilitar el panel táctil de firma.")

        if st.button("Confirmar Entrega y Registrar"):
            emp_id = int(df_e[df_e["label"] == emp_sel]["id"].values[0])
            prenda_id = int(df_p[df_p["label"] == prenda_sel]["id"].values[0])
            stock_actual = int(df_p[df_p["label"] == prenda_sel]["stock"].values[0])

            if cant > stock_actual:
                st.error("No hay suficiente stock en inventario para realizar esta entrega.")
            else:
                conn = conectar_bd()
                cur = conn.cursor()
                # Registrar entrega
                cur.execute(
                    "INSERT INTO entregas (empleado_id, prenda_id, cantidad, fecha) VALUES (?, ?, ?, ?)",
                    (emp_id, prenda_id, cant, datetime.date.today().strftime("%Y-%m-%d"))
                )
                # Descontar inventario
                cur.execute("UPDATE prendas SET stock = stock - ? WHERE id = ?", (cant, prenda_id))
                conn.commit()
                conn.close()
                st.success("¡Entrega registrada y stock actualizado con éxito!")

# ==========================================
# 4. MÓDULO: ALERTAS Y NOTIFICACIONES
# ==========================================
elif opcion == "🔔 Alertas y Notificaciones":
    st.header("🔔 Centro de Alertas y Notificaciones Operativas")
    st.caption("Monitoreo en tiempo real de niveles de stock e inventario crítico.")

    conn = conectar_bd()
    
    # 1. Alerta de Stock Mínimo
    st.subheader("⚠️ Alertas de Stock Crítico (Menos de 5 unidades)")
    df_stock_bajo = pd.read_sql_query("""
        SELECT nombre as Prenda, categoria as Categoría, talla as Talla, stock as Stock_Actual
        FROM prendas 
        WHERE stock <= 5 AND activo = 1
        ORDER BY stock ASC
    """, conn)
    
    if not df_stock_bajo.empty:
        st.error(f"¡Atención! Hay {len(df_stock_bajo)} prendas con stock crítico o agotado.")
        st.dataframe(df_stock_bajo, use_container_width=True)
    else:
        st.success("✅ Todo el inventario se encuentra por encima del nivel mínimo tolerable.")

    st.divider()

    # 2. Alerta de Renovación Pendiente
    st.subheader("📅 Próximas Renovaciones de Uniformes")
    df_renovaciones = pd.read_sql_query("""
        SELECT 
            emp.nombre as Empleado,
            emp.puesto as Puesto,
            p.nombre as Prenda,
            e.fecha as Fecha_Ultima_Entrega
        FROM entregas e
        INNER JOIN empleados emp ON e.empleado_id = emp.id
        INNER JOIN prendas p ON e.prenda_id = p.id
        ORDER BY e.fecha ASC
    """, conn)
    conn.close()

    if not df_renovaciones.empty:
        st.dataframe(df_renovaciones, use_container_width=True)
    else:
        st.info("ℹ️ No hay registros pendientes de renovación.")

# ==========================================
# 5. MÓDULO: ANALÍTICA AVANZADA
# ==========================================
elif opcion == "📊 Analítica Avanzada":
    st.header("📊 Analítica e Inteligencia de Datos")
    st.caption("Visualización interactiva y exportación de métricas clave del proceso de dotación.")

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
        st.info("Aún no existen registros de entregas para generar métricas analíticas.")
    else:
        col_m1, col_m2 = st.columns(2)

        # Gráfico 1: Consumo de Prendas por Categoría
        with col_m1:
            st.subheader("📦 Uniformes Entregados por Categoría")
            if px:
                fig_cat = px.pie(
                    df_entregas_full, 
                    names="Categoria", 
                    values="Cantidad", 
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                st.plotly_chart(fig_cat, use_container_width=True)
            else:
                st.bar_chart(df_entregas_full.groupby("Categoria")["Cantidad"].sum())

        # Gráfico 2: Top Puestos con mayor recepción
        with col_m2:
            st.subheader("👔 Dotación por Disciplina Técnica")
            df_disc = df_entregas_full.groupby("Disciplina")["Cantidad"].sum().reset_index()
            if px:
                fig_disc = px.bar(
                    df_disc,
                    x="Cantidad",
                    y="Disciplina",
                    orientation="h",
                    color="Cantidad",
                    color_continuous_scale="Blues"
                )
                st.plotly_chart(fig_disc, use_container_width=True)
            else:
                st.dataframe(df_disc)

        st.divider()

        # Exportación de Datos a Excel
        st.subheader("📥 Exportación de Reportes Ejecutivos")
        st.write("Genera un reporte consolidado en formato Excel con todo el historial de entregas.")

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_entregas_full.to_excel(writer, index=False, sheet_name='Historial_Entregas')
        
        st.download_button(
            label="📊 Descargar Reporte Completo (Excel)",
            data=buffer.getvalue(),
            file_name="Reporte_Dotacion_Uniformes_TNG.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
