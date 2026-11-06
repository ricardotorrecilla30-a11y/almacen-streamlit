<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TNG - Control y Trazabilidad de Uniformes</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Chart.js for Dashboards -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Google Fonts Inter -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        tng: {
                            sidebar: '#0f172a',
                            sidebarHover: '#1e293b',
                            primary: '#2563eb',
                            primaryHover: '#1d4ed8',
                            accent: '#f59e0b',
                            bg: '#f8fafc',
                            card: '#ffffff'
                        }
                    },
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    }
                }
            }
        }
    </script>
    <style>
        body { font-family: 'Inter', sans-serif; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        /* Custom scrollbars */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #f1f5f9; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
    </style>
</head>
<body class="bg-tng-bg text-slate-800 antialiased flex h-screen overflow-hidden">

    <!-- SIDEBAR DE NAVEGACIÓN SIMPLIFICADO -->
    <aside class="w-64 bg-tng-sidebar text-white flex flex-col justify-between flex-shrink-0 z-20 shadow-lg">
        <div>
            <!-- Header Marca TNG -->
            <div class="p-5 border-b border-slate-700/60 flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-xl shadow-md">
                    TNG
                </div>
                <div>
                    <h1 class="font-bold text-lg leading-tight tracking-wide">SISTEMA TNG</h1>
                    <p class="text-xs text-slate-400">Uniformes & Trazabilidad</p>
                </div>
            </div>

            <!-- Menú Consolidado (Sin saturación de pestañas) -->
            <nav class="mt-4 px-3 space-y-1">
                <button onclick="switchTab('dashboard')" id="nav-dashboard" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-colors bg-blue-600 text-white">
                    <i class="fa-solid fa-chart-pie w-5 text-center"></i>
                    <span>Inicio / Dashboard</span>
                </button>

                <button onclick="switchTab('inventario')" id="nav-inventario" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-slate-300 hover:bg-tng-sidebarHover hover:text-white transition-colors">
                    <i class="fa-solid fa-boxes-stacked w-5 text-center"></i>
                    <span>Inventario de Prendas</span>
                </button>

                <button onclick="switchTab('entregas')" id="nav-entregas" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-slate-300 hover:bg-tng-sidebarHover hover:text-white transition-colors">
                    <i class="fa-solid fa-signature w-5 text-center"></i>
                    <span>Registro & Firma Digital</span>
                </button>

                <button onclick="switchTab('trabajadores')" id="nav-trabajadores" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-slate-300 hover:bg-tng-sidebarHover hover:text-white transition-colors">
                    <i class="fa-solid fa-id-card-clip w-5 text-center"></i>
                    <span>Trabajadores & Expediente</span>
                </button>

                <button onclick="switchTab('reportes')" id="nav-reportes" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-slate-300 hover:bg-tng-sidebarHover hover:text-white transition-colors">
                    <i class="fa-solid fa-file-invoice-dollar w-5 text-center"></i>
                    <span>Reportes & KPI</span>
                </button>
            </nav>
        </div>

        <!-- Perfil Usuario Bottom -->
        <div class="p-4 border-t border-slate-700/60 flex items-center justify-between text-xs text-slate-400">
            <div class="flex items-center gap-2">
                <div class="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center font-semibold text-white">
                    RL
                </div>
                <div>
                    <p class="font-medium text-slate-200">Relaciones Laborales</p>
                    <p class="text-[10px] text-green-400 flex items-center gap-1">
                        <span class="w-1.5 h-1.5 rounded-full bg-green-400 inline-block"></span> En línea
                    </p>
                </div>
            </div>
            <button onclick="showNotification('Sesión finalizada')" class="hover:text-white p-1" title="Cerrar sesión">
                <i class="fa-solid fa-right-from-bracket"></i>
            </button>
        </div>
    </aside>

    <!-- ÁREA PRINCIPAL DE CONTENIDO -->
    <div class="flex-1 flex flex-col h-screen overflow-hidden">
        
        <!-- Header Superior -->
        <header class="bg-white border-b border-slate-200 px-8 py-4 flex items-center justify-between flex-shrink-0">
            <div>
                <h2 id="page-title" class="text-xl font-bold text-slate-800">Bienvenido, Relaciones Laborales</h2>
                <p class="text-xs text-slate-500">Sistema Integral de Control, Registro y Trazabilidad de EPP y Uniformes</p>
            </div>
            <div class="flex items-center gap-4">
                <button onclick="toggleChatbot()" class="relative bg-slate-100 hover:bg-slate-200 text-slate-600 p-2.5 rounded-lg text-sm transition-colors" title="Chatbot TNG">
                    <i class="fa-solid fa-robot text-blue-600"></i>
                </button>
                <div class="relative">
                    <button onclick="showNotification('Tiene 3 solicitudes pendientes de autorización')" class="bg-slate-100 hover:bg-slate-200 text-slate-600 p-2.5 rounded-lg text-sm transition-colors relative">
                        <i class="fa-regular fa-bell"></i>
                        <span class="absolute top-1 right-1 w-2 h-2 rounded-full bg-red-500"></span>
                    </button>
                </div>
                <div class="text-right text-xs border-l border-slate-200 pl-4">
                    <p class="font-semibold text-slate-700">Fecha del Sistema</p>
                    <p class="text-slate-500" id="current-date">06 de Noviembre, 2026</p>
                </div>
            </div>
        </header>

        <!-- Pestañas de Contenido Dinámico -->
        <main class="flex-1 overflow-y-auto p-8 bg-slate-50">

            <!-- 1. DASHBOARD PRINCIPAL -->
            <section id="tab-dashboard" class="tab-content active space-y-6">
                
                <!-- Card Bienvenida / Hero Banner -->
                <div class="bg-gradient-to-r from-slate-900 via-blue-950 to-slate-900 rounded-2xl p-6 text-white shadow-md relative overflow-hidden">
                    <div class="relative z-10 max-w-2xl">
                        <span class="bg-blue-600/80 text-blue-100 text-xs px-3 py-1 rounded-full uppercase tracking-wider font-semibold">Módulo de Control TNG</span>
                        <h3 class="text-2xl font-bold mt-2">Sistema de Control y Trazabilidad de Uniformes</h3>
                        <p class="text-sm text-slate-300 mt-1">Gestione entregas, controle el inventario en tiempo real y consulte los expedientes digitales de los trabajadores de forma ágil.</p>
                    </div>
                    <i class="fa-solid fa-vest-patches absolute -right-4 -bottom-6 text-9xl text-white/5 transform -rotate-12 pointer-events-none"></i>
                </div>

                <!-- KPI Metric Cards Grid -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                        <div>
                            <p class="text-xs font-semibold text-slate-500 uppercase">Trabajadores Activos</p>
                            <h4 class="text-3xl font-extrabold text-slate-800 mt-1">245</h4>
                            <span class="text-xs text-emerald-600 font-medium flex items-center gap-1 mt-1">
                                <i class="fa-solid fa-arrow-up"></i> 100% Personal Registrado
                            </span>
                        </div>
                        <div class="w-12 h-12 bg-blue-50 text-blue-600 rounded-xl flex items-center justify-center text-xl">
                            <i class="fa-solid fa-users"></i>
                        </div>
                    </div>

                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                        <div>
                            <p class="text-xs font-semibold text-slate-500 uppercase">Entregas Pendientes</p>
                            <h4 class="text-3xl font-extrabold text-slate-800 mt-1">1,245</h4>
                            <span class="text-xs text-amber-600 font-medium flex items-center gap-1 mt-1">
                                <i class="fa-solid fa-clock"></i> Por programar este mes
                            </span>
                        </div>
                        <div class="w-12 h-12 bg-amber-50 text-amber-600 rounded-xl flex items-center justify-center text-xl">
                            <i class="fa-solid fa-truck-ramp-box"></i>
                        </div>
                    </div>

                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                        <div>
                            <p class="text-xs font-semibold text-slate-500 uppercase">Solicitudes en Proceso</p>
                            <h4 class="text-3xl font-extrabold text-slate-800 mt-1">12</h4>
                            <span class="text-xs text-blue-600 font-medium flex items-center gap-1 mt-1">
                                <i class="fa-solid fa-rotate"></i> Cambios por desgaste
                            </span>
                        </div>
                        <div class="w-12 h-12 bg-orange-50 text-orange-600 rounded-xl flex items-center justify-center text-xl">
                            <i class="fa-solid fa-clipboard-list"></i>
                        </div>
                    </div>

                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                        <div>
                            <p class="text-xs font-semibold text-slate-500 uppercase">Entregas Hoy</p>
                            <h4 class="text-3xl font-extrabold text-slate-800 mt-1">38</h4>
                            <span class="text-xs text-purple-600 font-medium flex items-center gap-1 mt-1">
                                <i class="fa-solid fa-circle-check"></i> Con Firma Digital
                            </span>
                        </div>
                        <div class="w-12 h-12 bg-purple-50 text-purple-600 rounded-xl flex items-center justify-center text-xl">
                            <i class="fa-solid fa-file-signature"></i>
                        </div>
                    </div>
                </div>

                <!-- Gráficas & Secciones de Estado -->
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <!-- Gauge / Indicadores de Desempeño -->
                    <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                        <h4 class="font-bold text-slate-800 mb-4 flex items-center gap-2">
                            <i class="fa-solid fa-gauge-high text-blue-600"></i> Indicadores Clave (KPI)
                        </h4>
                        <div class="flex flex-col items-center justify-center my-4">
                            <!-- Circular Progress Simple simulation -->
                            <div class="relative w-36 h-36 flex items-center justify-center">
                                <svg class="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                                    <path class="text-slate-100" stroke-width="3.5" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                                    <path class="text-blue-600" stroke-dasharray="92, 100" stroke-width="3.5" stroke-linecap="round" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                                </svg>
                                <div class="absolute text-center">
                                    <span class="text-3xl font-extrabold text-slate-800">92%</span>
                                    <p class="text-[10px] text-slate-400 uppercase font-semibold">Entrega Oportuna</p>
                                </div>
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-3 pt-4 border-t border-slate-100 text-center">
                            <div class="bg-slate-50 p-2 rounded-lg">
                                <p class="text-xs text-slate-500">Rotación de Inventario</p>
                                <p class="text-lg font-bold text-slate-700">3.4</p>
                            </div>
                            <div class="bg-slate-50 p-2 rounded-lg">
                                <p class="text-xs text-slate-500">Prendas en stock bajo</p>
                                <p class="text-lg font-bold text-amber-600">8 ítems</p>
                            </div>
                        </div>
                    </div>

                    <!-- Notificaciones & Avisos -->
                    <div class="lg:col-span-2 bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between mb-4">
                                <h4 class="font-bold text-slate-800 flex items-center gap-2">
                                    <i class="fa-regular fa-bell text-blue-600"></i> Últimas Notificaciones del Sistema
                                </h4>
                                <span class="text-xs text-slate-400">Hoy</span>
                            </div>
                            <div class="space-y-3">
                                <div class="flex items-start gap-3 p-3 rounded-lg bg-amber-50/60 border border-amber-100 text-xs">
                                    <i class="fa-solid fa-triangle-exclamation text-amber-600 text-base mt-0.5"></i>
                                    <div class="flex-1">
                                        <p class="font-semibold text-slate-800">Hay 3 solicitudes pendientes de autorización</p>
                                        <p class="text-slate-500">Revisión requerida por departamento de Almacén.</p>
                                    </div>
                                    <span class="text-[10px] text-slate-400">Hace 10 min</span>
                                </div>
                                <div class="flex items-start gap-3 p-3 rounded-lg bg-blue-50/60 border border-blue-100 text-xs">
                                    <i class="fa-solid fa-boxes-packing text-blue-600 text-base mt-0.5"></i>
                                    <div class="flex-1">
                                        <p class="font-semibold text-slate-800">Se requiere compra de overoles Talla 40</p>
                                        <p class="text-slate-500">El stock ha disminuido por debajo del punto mínimo.</p>
                                    </div>
                                    <span class="text-[10px] text-slate-400">Ayer 17:20</span>
                                </div>
                                <div class="flex items-start gap-3 p-3 rounded-lg bg-emerald-50/60 border border-emerald-100 text-xs">
                                    <i class="fa-solid fa-calendar-check text-emerald-600 text-base mt-0.5"></i>
                                    <div class="flex-1">
                                        <p class="font-semibold text-slate-800">Próxima dotación masiva programada</p>
                                        <p class="text-slate-500">Programada para el 15 de Octubre en Planta Principal.</p>
                                    </div>
                                    <span class="text-[10px] text-slate-400">Ayer 11:00</span>
                                </div>
                            </div>
                        </div>
                        <div class="mt-4 pt-4 border-t border-slate-100 flex justify-end">
                            <button onclick="switchTab('entregas')" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold transition-colors flex items-center gap-2">
                                <i class="fa-solid fa-plus"></i> Registrar Nueva Entrega
                            </button>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 2. INVENTARIO DE UNIFORMES -->
            <section id="tab-inventario" class="tab-content space-y-6">
                <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
                        <div>
                            <h3 class="text-lg font-bold text-slate-800">Inventario de Uniformes</h3>
                            <p class="text-xs text-slate-500">Consulta de existencias, tallas y alertas de reabastecimiento</p>
                        </div>
                        <div class="flex items-center gap-3">
                            <div class="relative">
                                <i class="fa-solid fa-magnifying-glass absolute left-3 top-3 text-slate-400 text-xs"></i>
                                <input type="text" id="inventory-search" onkeyup="filterInventory()" placeholder="Buscar prenda, talla o código..." class="pl-9 pr-4 py-2 border border-slate-200 rounded-lg text-xs w-64 focus:outline-none focus:ring-2 focus:ring-blue-500">
                            </div>
                            <button onclick="showNotification('Exportando inventario a Excel...')" class="bg-emerald-600 hover:bg-emerald-700 text-white px-3 py-2 rounded-lg text-xs font-medium flex items-center gap-2">
                                <i class="fa-solid fa-file-excel"></i> Exportar
                            </button>
                        </div>
                    </div>

                    <!-- Tabla de prendas -->
                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-xs text-slate-600">
                            <thead class="bg-slate-50 text-slate-700 font-semibold uppercase border-b border-slate-200">
                                <tr>
                                    <th class="py-3 px-4">Prenda</th>
                                    <th class="py-3 px-4">Talla</th>
                                    <th class="py-3 px-4">Existencia</th>
                                    <th class="py-3 px-4">Estado</th>
                                    <th class="py-3 px-4 text-center">Acciones</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y border-b border-slate-200" id="inventory-table-body">
                                <tr class="hover:bg-slate-50/80">
                                    <td class="py-3 px-4 font-semibold text-slate-800 flex items-center gap-2">
                                        <i class="fa-solid fa-shirt text-slate-400"></i> Overol Industrial
                                    </td>
                                    <td class="py-3 px-4">38 - 52</td>
                                    <td class="py-3 px-4 font-bold text-slate-800">330</td>
                                    <td class="py-3 px-4">
                                        <span class="bg-emerald-100 text-emerald-700 px-2.5 py-1 rounded-full text-[10px] font-semibold">Normal</span>
                                    </td>
                                    <td class="py-3 px-4 text-center">
                                        <button class="text-blue-600 hover:underline font-semibold" onclick="showNotification('Detalle de overol') font-medium">Ver Tallas</button>
                                    </td>
                                </tr>
                                <tr class="hover:bg-slate-50/80">
                                    <td class="py-3 px-4 font-semibold text-slate-800 flex items-center gap-2">
                                        <i class="fa-solid fa-user-tie text-slate-400"></i> Camisola de Trabajo
                                    </td>
                                    <td class="py-3 px-4">38 - 52</td>
                                    <td class="py-3 px-4 font-bold text-slate-800">180</td>
                                    <td class="py-3 px-4">
                                        <span class="bg-emerald-100 text-emerald-700 px-2.5 py-1 rounded-full text-[10px] font-semibold">Normal</span>
                                    </td>
                                    <td class="py-3 px-4 text-center">
                                        <button class="text-blue-600 hover:underline font-semibold" onclick="showNotification('Detalle de camisola') font-medium">Ver Tallas</button>
                                    </td>
                                </tr>
                                <tr class="hover:bg-slate-50/80">
                                    <td class="py-3 px-4 font-semibold text-slate-800 flex items-center gap-2">
                                        <i class="fa-solid fa-socks text-slate-400"></i> Pantalón de Trabajo
                                    </td>
                                    <td class="py-3 px-4">28 - 52</td>
                                    <td class="py-3 px-4 font-bold text-slate-800">240</td>
                                    <td class="py-3 px-4">
                                        <span class="bg-emerald-100 text-emerald-700 px-2.5 py-1 rounded-full text-[10px] font-semibold">Normal</span>
                                    </td>
                                    <td class="py-3 px-4 text-center">
                                        <button class="text-blue-600 hover:underline font-semibold">Ver Tallas</button>
                                    </td>
                                </tr>
                                <tr class="hover:bg-slate-50/80 bg-amber-50/30">
                                    <td class="py-3 px-4 font-semibold text-slate-800 flex items-center gap-2">
                                        <i class="fa-solid fa-shoe-prints text-slate-400"></i> Botas Dielectricas HR
                                    </td>
                                    <td class="py-3 px-4">22 - 31</td>
                                    <td class="py-3 px-4 font-bold text-amber-700">95</td>
                                    <td class="py-3 px-4">
                                        <span class="bg-amber-100 text-amber-800 px-2.5 py-1 rounded-full text-[10px] font-semibold">Stock Bajo</span>
                                    </td>
                                    <td class="py-3 px-4 text-center">
                                        <button class="text-blue-600 hover:underline font-semibold">Solicitar</button>
                                    </td>
                                </tr>
                                <tr class="hover:bg-slate-50/80 bg-amber-50/30">
                                    <td class="py-3 px-4 font-semibold text-slate-800 flex items-center gap-2">
                                        <i class="fa-solid fa-shoe-prints text-slate-400"></i> Botas de Seguridad Estándar
                                    </td>
                                    <td class="py-3 px-4">22 - 31</td>
                                    <td class="py-3 px-4 font-bold text-amber-700">60</td>
                                    <td class="py-3 px-4">
                                        <span class="bg-amber-100 text-amber-800 px-2.5 py-1 rounded-full text-[10px] font-semibold">Stock Bajo</span>
                                    </td>
                                    <td class="py-3 px-4 text-center">
                                        <button class="text-blue-600 hover:underline font-semibold">Solicitar</button>
                                    </td>
                                </tr>
                                <tr class="hover:bg-slate-50/80 bg-amber-50/30">
                                    <td class="py-3 px-4 font-semibold text-slate-800 flex items-center gap-2">
                                        <i class="fa-solid fa-shoe-prints text-slate-400"></i> Botas Petroleras
                                    </td>
                                    <td class="py-3 px-4">22 - 31</td>
                                    <td class="py-3 px-4 font-bold text-amber-700">45</td>
                                    <td class="py-3 px-4">
                                        <span class="bg-amber-100 text-amber-800 px-2.5 py-1 rounded-full text-[10px] font-semibold">Stock Bajo</span>
                                    </td>
                                    <td class="py-3 px-4 text-center">
                                        <button class="text-blue-600 hover:underline font-semibold">Solicitar</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>

            <!-- 3. REGISTRO DE ENTREGA & FIRMA DIGITAL -->
            <section id="tab-entregas" class="tab-content space-y-6">
                <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                    
                    <!-- Formulario Registro de Entrega -->
                    <div class="lg:col-span-7 bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
                        <div class="border-b border-slate-100 pb-3">
                            <h3 class="text-lg font-bold text-slate-800">Nueva Entrega de Uniforme</h3>
                            <p class="text-xs text-slate-500">Ingrese la matrícula del trabajador y seleccione las prendas a entregar</p>
                        </div>

                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Matrícula *</label>
                                <div class="relative">
                                    <input type="text" id="worker-id" value="001245" class="w-full pl-3 pr-8 py-2 border border-slate-200 rounded-lg text-xs focus:ring-2 focus:ring-blue-500 font-semibold">
                                    <i class="fa-solid fa-magnifying-glass absolute right-3 top-3 text-slate-400 text-xs cursor-pointer" onclick="loadWorkerData()"></i>
                                </div>
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Nombre Completo</label>
                                <input type="text" id="worker-name" value="Juan Pérez López" readonly class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs font-medium text-slate-700">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Disciplina / Área</label>
                                <input type="text" value="Operaciones" readonly class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-700">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Tipo de Trabajador</label>
                                <input type="text" value="Sindicalizado" readonly class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-700">
                            </div>
                        </div>

                        <!-- Prendas a Entregar Selector -->
                        <div class="pt-4 border-t border-slate-100">
                            <h4 class="text-xs font-bold text-slate-700 uppercase tracking-wider mb-3">Prendas a Entregar</h4>
                            <div class="space-y-2">
                                <div class="flex items-center justify-between p-2.5 bg-slate-50 rounded-lg border border-slate-200 text-xs">
                                    <span class="font-medium text-slate-700">Overol Industrial</span>
                                    <div class="flex items-center gap-3">
                                        <span class="text-slate-500">Talla: <strong class="text-slate-800">40</strong></span>
                                        <input type="number" value="1" min="1" class="w-14 px-2 py-1 border border-slate-300 rounded text-center">
                                    </div>
                                </div>
                                <div class="flex items-center justify-between p-2.5 bg-slate-50 rounded-lg border border-slate-200 text-xs">
                                    <span class="font-medium text-slate-700">Camisola de Trabajo</span>
                                    <div class="flex items-center gap-3">
                                        <span class="text-slate-500">Talla: <strong class="text-slate-800">42</strong></span>
                                        <input type="number" value="1" min="1" class="w-14 px-2 py-1 border border-slate-300 rounded text-center">
                                    </div>
                                </div>
                                <div class="flex items-center justify-between p-2.5 bg-slate-50 rounded-lg border border-slate-200 text-xs">
                                    <span class="font-medium text-slate-700">Pantalón de Trabajo</span>
                                    <div class="flex items-center gap-3">
                                        <span class="text-slate-500">Talla: <strong class="text-slate-800">40</strong></span>
                                        <input type="number" value="1" min="1" class="w-14 px-2 py-1 border border-slate-300 rounded text-center">
                                    </div>
                                </div>
                                <div class="flex items-center justify-between p-2.5 bg-slate-50 rounded-lg border border-slate-200 text-xs">
                                    <span class="font-medium text-slate-700">Botas Dielectricas</span>
                                    <div class="flex items-center gap-3">
                                        <span class="text-slate-500">Talla: <strong class="text-slate-800">27</strong></span>
                                        <input type="number" value="1" min="1" class="w-14 px-2 py-1 border border-slate-300 rounded text-center">
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="flex justify-end gap-2 pt-2">
                            <button onclick="showNotification('Formulario cancelado')" class="px-4 py-2 border border-slate-300 hover:bg-slate-100 rounded-lg text-xs font-semibold text-slate-600">Cancelar</button>
                            <button onclick="showNotification('Continúe a la firma del acuse')" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold">Siguiente</button>
                        </div>
                    </div>

                    <!-- Acuse de Entrega y Firma Digital Canvas -->
                    <div class="lg:col-span-5 bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
                        <div>
                            <div class="border-b border-slate-100 pb-3 mb-4 flex items-center justify-between">
                                <div>
                                    <h3 class="text-lg font-bold text-slate-800">Acuse de Entrega</h3>
                                    <p class="text-xs text-slate-500">Firma digital de conformidad</p>
                                </div>
                                <span class="bg-blue-50 text-blue-700 text-[10px] px-2 py-1 rounded font-mono">ID: ACU-8842</span>
                            </div>

                            <div class="space-y-2 text-xs bg-slate-50 p-3 rounded-lg border border-slate-100 mb-4">
                                <p><strong class="text-slate-700">Matrícula:</strong> 001245</p>
                                <p><strong class="text-slate-700">Nombre:</strong> Juan Pérez López</p>
                                <p><strong class="text-slate-700">Fecha:</strong> 06/11/2026 10:30 hrs</p>
                            </div>

                            <!-- Canvas de Firma Digital -->
                            <div>
                                <label class="block text-xs font-bold text-slate-700 mb-2">Firma del trabajador (Dibuje en la casilla):</label>
                                <div class="border-2 border-dashed border-slate-300 rounded-xl bg-slate-50 overflow-hidden relative">
                                    <canvas id="signature-pad" class="w-full h-36 cursor-crosshair"></canvas>
                                    <span class="absolute bottom-2 right-2 text-[10px] text-slate-400 select-none">Firma aquí</span>
                                </div>
                                <div class="flex justify-end mt-2">
                                    <button onclick="clearSignature()" class="text-xs text-slate-500 hover:text-red-600 font-medium flex items-center gap-1">
                                        <i class="fa-solid fa-eraser"></i> Limpiar Firma
                                    </button>
                                </div>
                            </div>
                        </div>

                        <div class="pt-4 border-t border-slate-100 space-y-2">
                            <button onclick="generatePDF()" class="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-bold shadow-sm transition-colors flex items-center justify-center gap-2">
                                <i class="fa-solid fa-file-pdf"></i> Generar Acuse PDF & Guardar
                            </button>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 4. TRABAJADORES Y EXPEDIENTES -->
            <section id="tab-trabajadores" class="tab-content space-y-6">
                <!-- Solicitudes & Control de Bajas Toolbar -->
                <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                    
                    <!-- Expediente del Trabajador -->
                    <div class="lg:col-span-8 bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-6">
                        <div class="flex items-center justify-between border-b border-slate-100 pb-4">
                            <div class="flex items-center gap-4">
                                <div class="w-14 h-14 rounded-full bg-blue-100 border-2 border-blue-500 flex items-center justify-center text-blue-700 font-bold text-xl">
                                    JP
                                </div>
                                <div>
                                    <h3 class="text-lg font-bold text-slate-800">Juan Pérez López</h3>
                                    <p class="text-xs text-slate-500">Matrícula: <strong class="text-slate-700">001245</strong> | Operaciones / Sindicalizado</p>
                                </div>
                            </div>
                            <span class="bg-emerald-100 text-emerald-800 text-xs px-3 py-1 rounded-full font-bold">Activo</span>
                        </div>

                        <!-- Sub-pestanas de expediente -->
                        <div class="border-b border-slate-200 flex gap-4 text-xs font-semibold text-slate-500">
                            <button class="pb-2 border-b-2 border-blue-600 text-blue-600">Datos Generales</button>
                            <button class="pb-2 hover:text-slate-800" onclick="showNotification('Cargando documentos...')">Documentos PDF</button>
                            <button class="pb-2 hover:text-slate-800" onclick="showNotification('Cargando historial...')">Historial de Movimientos</button>
                            <button class="pb-2 hover:text-slate-800" onclick="showNotification('Cargando cambios de talla...')">Cambios de Talla</button>
                        </div>

                        <!-- Detalle expediente -->
                        <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 text-xs">
                            <div class="bg-slate-50 p-3 rounded-lg border border-slate-100">
                                <span class="text-slate-400 block">Fecha de Ingreso</span>
                                <strong class="text-slate-700">15/03/2020</strong>
                            </div>
                            <div class="bg-slate-50 p-3 rounded-lg border border-slate-100">
                                <span class="text-slate-400 block">Cargo</span>
                                <strong class="text-slate-700">Jefe de Almacén</strong>
                            </div>
                            <div class="bg-slate-50 p-3 rounded-lg border border-slate-100">
                                <span class="text-slate-400 block">Talla Actual</span>
                                <strong class="text-slate-700">Overol 42 / Botas 27</strong>
                            </div>
                        </div>

                        <!-- Documentos digitalizados -->
                        <div>
                            <h4 class="text-xs font-bold text-slate-700 mb-3 uppercase tracking-wider">Archivos Adjuntos</h4>
                            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                                <div class="p-3 border border-slate-200 rounded-lg text-center hover:border-blue-500 transition-colors cursor-pointer" onclick="showNotification('Abriendo INE.pdf')">
                                    <i class="fa-solid fa-file-pdf text-red-500 text-2xl mb-1"></i>
                                    <p class="text-[11px] font-medium text-slate-700 truncate">INE.pdf</p>
                                </div>
                                <div class="p-3 border border-slate-200 rounded-lg text-center hover:border-blue-500 transition-colors cursor-pointer" onclick="showNotification('Abriendo Comprobante.pdf')">
                                    <i class="fa-solid fa-file-pdf text-red-500 text-2xl mb-1"></i>
                                    <p class="text-[11px] font-medium text-slate-700 truncate">Comprobante.pdf</p>
                                </div>
                                <div class="p-3 border border-slate-200 rounded-lg text-center hover:border-blue-500 transition-colors cursor-pointer" onclick="showNotification('Abriendo RFC.pdf')">
                                    <i class="fa-solid fa-file-pdf text-red-500 text-2xl mb-1"></i>
                                    <p class="text-[11px] font-medium text-slate-700 truncate">RFC.pdf</p>
                                </div>
                                <div class="p-3 border border-slate-200 rounded-lg text-center hover:border-blue-500 transition-colors cursor-pointer" onclick="showNotification('Abriendo Fotografia.jpg')">
                                    <i class="fa-solid fa-image text-blue-500 text-2xl mb-1"></i>
                                    <p class="text-[11px] font-medium text-slate-700 truncate">Fotografia.jpg</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Control de bajas rápidas -->
                    <div class="lg:col-span-4 bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
                        <div>
                            <div class="border-b border-slate-100 pb-3 mb-4">
                                <h3 class="text-base font-bold text-slate-800">Control de Bajas</h3>
                                <p class="text-xs text-slate-500">Registro de bajas y devolución de prendas</p>
                            </div>

                            <div class="space-y-3 text-xs">
                                <div class="p-3 bg-red-50/50 border border-red-100 rounded-lg flex justify-between items-center">
                                    <div>
                                        <p class="font-bold text-slate-800">Luis Fuentes (001102)</p>
                                        <p class="text-slate-500 text-[10px]">Renuncia - 15/08/2025</p>
                                    </div>
                                    <span class="bg-red-100 text-red-700 px-2 py-0.5 rounded text-[10px] font-bold">Baja</span>
                                </div>
                                <div class="p-3 bg-red-50/50 border border-red-100 rounded-lg flex justify-between items-center">
                                    <div>
                                        <p class="font-bold text-slate-800">Carlos Ruiz (001116)</p>
                                        <p class="text-slate-500 text-[10px]">Despido - 12/09/2025</p>
                                    </div>
                                    <span class="bg-red-100 text-red-700 px-2 py-0.5 rounded text-[10px] font-bold">Baja</span>
                                </div>
                                <div class="p-3 bg-red-50/50 border border-red-100 rounded-lg flex justify-between items-center">
                                    <div>
                                        <p class="font-bold text-slate-800">Ana Torres (001504)</p>
                                        <p class="text-slate-500 text-[10px]">Invalidez - 03/10/2025</p>
                                    </div>
                                    <span class="bg-red-100 text-red-700 px-2 py-0.5 rounded text-[10px] font-bold">Inactivo</span>
                                </div>
                            </div>
                        </div>

                        <button onclick="showNotification('Módulo para registrar nueva baja')" class="mt-4 w-full py-2 bg-slate-800 hover:bg-slate-900 text-white rounded-lg text-xs font-semibold">
                            + Registrar Nueva Baja
                        </button>
                    </div>

                </div>
            </section>

            <!-- 5. REPORTES & EXPORTACIÓN -->
            <section id="tab-reportes" class="tab-content space-y-6">
                <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                    
                    <!-- Botones de Generación de Reportes -->
                    <div class="lg:col-span-5 bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
                        <h3 class="text-lg font-bold text-slate-800 border-b border-slate-100 pb-3">Reportes y Exportaciones</h3>
                        
                        <div class="space-y-3">
                            <div class="flex items-center justify-between p-3 border border-slate-200 rounded-xl hover:bg-slate-50">
                                <div>
                                    <p class="text-xs font-bold text-slate-800">Inventario Actual Completo</p>
                                    <p class="text-[10px] text-slate-500">Resumen general con stock de tallas</p>
                                </div>
                                <button onclick="showNotification('Generando PDF de inventario...')" class="bg-red-600 hover:bg-red-700 text-white px-3 py-1.5 rounded-lg text-xs font-semibold">Generar PDF</button>
                            </div>

                            <div class="flex items-center justify-between p-3 border border-slate-200 rounded-xl hover:bg-slate-50">
                                <div>
                                    <p class="text-xs font-bold text-slate-800">Movimientos por Prenda</p>
                                    <p class="text-[10px] text-slate-500">Histórico de entradas y salidas</p>
                                </div>
                                <button onclick="showNotification('Exportando a Excel...')" class="bg-emerald-600 hover:bg-emerald-700 text-white px-3 py-1.5 rounded-lg text-xs font-semibold">Generar Excel</button>
                            </div>

                            <div class="flex items-center justify-between p-3 border border-slate-200 rounded-xl hover:bg-slate-50">
                                <div>
                                    <p class="text-xs font-bold text-slate-800">Entregas por Trabajador</p>
                                    <p class="text-[10px] text-slate-500">Relación detallada por matrícula</p>
                                </div>
                                <button onclick="showNotification('Generando PDF de entregas...')" class="bg-red-600 hover:bg-red-700 text-white px-3 py-1.5 rounded-lg text-xs font-semibold">Generar PDF</button>
                            </div>

                            <div class="flex items-center justify-between p-3 border border-slate-200 rounded-xl hover:bg-slate-50">
                                <div>
                                    <p class="text-xs font-bold text-slate-800">Solicitudes Pendientes</p>
                                    <p class="text-[10px] text-slate-500">Cambios de talla y desgate acumulado</p>
                                </div>
                                <button onclick="showNotification('Exportando a Excel...')" class="bg-emerald-600 hover:bg-emerald-700 text-white px-3 py-1.5 rounded-lg text-xs font-semibold">Generar Excel</button>
                            </div>
                        </div>
                    </div>

                    <!-- Gráfica de Barras KPI -->
                    <div class="lg:col-span-7 bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                        <h3 class="text-lg font-bold text-slate-800 mb-2">Movimientos de Uniformes (Últimos 7 Días)</h3>
                        <p class="text-xs text-slate-500 mb-4">Comparativa de Entradas vs Salidas vs Existencia general</p>
                        <div class="h-64">
                            <canvas id="kpiChart"></canvas>
                        </div>
                    </div>

                </div>
            </section>

        </main>
    </div>

    <!-- 6. CHATBOT FLOTANTE TNG 2.0 -->
    <div id="chatbot-widget" class="fixed bottom-6 right-6 w-80 sm:w-96 bg-white rounded-2xl shadow-2xl border border-slate-200 hidden flex-col z-50 overflow-hidden">
        <!-- Header Bot -->
        <div class="bg-tng-sidebar text-white p-4 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white">
                    <i class="fa-solid fa-robot"></i>
                </div>
                <div>
                    <h4 class="font-bold text-sm">Asistente TNG 2.0</h4>
                    <p class="text-[10px] text-green-400">En línea - Consultas Rápidas</p>
                </div>
            </div>
            <button onclick="toggleChatbot()" class="text-slate-400 hover:text-white">
                <i class="fa-solid fa-xmark text-lg"></i>
            </button>
        </div>
        <!-- Chat Body -->
        <div id="chat-messages" class="p-4 h-72 overflow-y-auto space-y-3 text-xs bg-slate-50">
            <div class="bg-blue-100 text-blue-900 p-3 rounded-xl rounded-tl-none max-w-[85%]">
                ¡Hola! Soy tu asistente TNG. ¿En qué puedo ayudarte? Puedes preguntarme sobre stock, matrículas o folios.
            </div>
            <div class="space-y-1">
                <p class="text-[10px] text-slate-400 font-semibold uppercase">Sugerencias:</p>
                <button onclick="sendQuickChat('¿Cuál es la matrícula de Juan Pérez?')" class="block w-full text-left bg-white hover:bg-slate-100 border border-slate-200 p-2 rounded-lg text-slate-700 text-[11px]">
                    ¿Cuál es la matrícula de Juan Pérez?
                </button>
                <button onclick="sendQuickChat('¿Cuántas botas talla 27 hay en existencia?')" class="block w-full text-left bg-white hover:bg-slate-100 border border-slate-200 p-2 rounded-lg text-slate-700 text-[11px]">
                    ¿Cuántas botas talla 27 hay en existencia?
                </button>
            </div>
        </div>
        <!-- Input Chat -->
        <div class="p-3 bg-white border-t border-slate-200 flex gap-2">
            <input type="text" id="chat-input" placeholder="Escribe tu pregunta..." class="flex-1 px-3 py-2 border border-slate-200 rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-blue-500">
            <button onclick="sendChatMessage()" class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-lg text-xs">
                <i class="fa-solid fa-paper-plane"></i>
            </button>
        </div>
    </div>

    <!-- NOTIFICACIÓN TOAST SIMULADA -->
    <div id="toast" class="fixed top-5 right-5 bg-slate-900 text-white px-4 py-3 rounded-xl shadow-xl text-xs flex items-center gap-3 transition-opacity duration-300 opacity-0 pointer-events-none z-50">
        <i class="fa-solid fa-circle-check text-emerald-400 text-base"></i>
        <span id="toast-message">Operación realizada exitosamente</span>
    </div>

    <!-- JAVASCRIPT PRINCIPAL -->
    <script>
        // Cambiar entre Pestañas Consolidadas
        function switchTab(tabId) {
            // Ocultar todas las pestañas
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });

            // Desmarcar botones de navegación
            document.querySelectorAll('.nav-btn').forEach(btn => {
                btn.classList.remove('bg-blue-600', 'text-white');
                btn.classList.add('text-slate-300', 'hover:bg-tng-sidebarHover');
            });

            // Activar la pestaña elegida
            document.getElementById('tab-' + tabId).classList.add('active');

            // Resaltar botón activo
            const activeBtn = document.getElementById('nav-' + tabId);
            if (activeBtn) {
                activeBtn.classList.remove('text-slate-300', 'hover:bg-tng-sidebarHover');
                activeBtn.classList.add('bg-blue-600', 'text-white');
            }

            // Cambiar título de encabezado
            const titleMap = {
                'dashboard': 'Bienvenido, Relaciones Laborales',
                'inventario': 'Inventario General de Uniformes',
                'entregas': 'Registro de Entrega & Firma Digital',
                'trabajadores': 'Expedientes Digitales de Trabajadores',
                'reportes': 'Centro de Reportes & Indicadores KPI'
            };
            document.getElementById('page-title').innerText = titleMap[tabId] || 'Sistema TNG';
        }

        // Mostrar Notificación Toast
        function showNotification(msg) {
            const toast = document.getElementById('toast');
            document.getElementById('toast-message').innerText = msg;
            toast.classList.remove('opacity-0', 'pointer-events-none');
            setTimeout(() => {
                toast.classList.add('opacity-0', 'pointer-events-none');
            }, 3000);
        }

        // Búsqueda en Inventario
        function filterInventory() {
            const query = document.getElementById('inventory-search').value.toLowerCase();
            const rows = document.querySelectorAll('#inventory-table-body tr');
            rows.forEach(row => {
                const text = row.innerText.toLowerCase();
                row.style.display = text.includes(query) ? '' : 'none';
            });
        }

        // Simulación de Búsqueda de Trabajador por Matrícula
        function loadWorkerData() {
            const id = document.getElementById('worker-id').value;
            if(id === '001245') {
                document.getElementById('worker-name').value = "Juan Pérez López";
                showNotification("Trabajador encontrado: Juan Pérez López");
            } else {
                document.getElementById('worker-name').value = "Trabajador Desconocido";
                showNotification("Matrícula no registrada");
            }
        }

        // Toggle Widget del Chatbot
        function toggleChatbot() {
            const widget = document.getElementById('chatbot-widget');
            if (widget.classList.contains('hidden')) {
                widget.classList.remove('hidden');
                widget.classList.add('flex');
            } else {
                widget.classList.add('hidden');
                widget.classList.remove('flex');
            }
        }

        // Enviar Mensajes en el Chatbot
        function sendChatMessage() {
            const input = document.getElementById('chat-input');
            if(!input.value.trim()) return;
            sendQuickChat(input.value);
            input.value = '';
        }

        function sendQuickChat(text) {
            const container = document.getElementById('chat-messages');
            
            // Mensaje usuario
            const userMsg = document.createElement('div');
            userMsg.className = 'bg-blue-600 text-white p-3 rounded-xl rounded-tr-none max-w-[85%] ml-auto text-right';
            userMsg.innerText = text;
            container.appendChild(userMsg);

            // Respuesta bot simulada
            setTimeout(() => {
                const botMsg = document.createElement('div');
                botMsg.className = 'bg-blue-100 text-blue-900 p-3 rounded-xl rounded-tl-none max-w-[85%]';
                
                if(text.includes('Juan')) {
                    botMsg.innerText = "La matrícula de Juan Pérez López es 001245. Su puesto actual es Jefe de Almacén en Operaciones.";
                } else if(text.includes('botas') || text.includes('existencia')) {
                    botMsg.innerText = "Actualmente quedan 95 pares de Botas Dieléctricas Talla 27 en stock de Almacén.";
                } else {
                    botMsg.innerText = "He recibido tu consulta. Puedes revisar más detalles en la pestaña de Inventario o Expedientes.";
                }
                
                container.appendChild(botMsg);
                container.scrollTop = container.scrollHeight;
            }, 600);
        }

        // --- CANVAS DE FIRMA DIGITAL ---
        const canvas = document.getElementById('signature-pad');
        const ctx = canvas.getContext('2d');
        let drawing = false;

        function resizeCanvas() {
            const rect = canvas.getBoundingClientRect();
            canvas.width = rect.width;
            canvas.height = rect.height;
            ctx.lineWidth = 2;
            ctx.lineCap = 'round';
            ctx.strokeStyle = '#1e293b';
        }

        window.addEventListener('resize', resizeCanvas);
        setTimeout(resizeCanvas, 200);

        function startDrawing(e) {
            drawing = true;
            ctx.beginPath();
            const pos = getPos(e);
            ctx.moveTo(pos.x, pos.y);
        }

        function draw(e) {
            if (!drawing) return;
            const pos = getPos(e);
            ctx.lineTo(pos.x, pos.y);
            ctx.stroke();
        }

        function stopDrawing() {
            drawing = false;
        }

        function getPos(e) {
            const rect = canvas.getBoundingClientRect();
            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;
            return {
                x: clientX - rect.left,
                y: clientY - rect.top
            };
        }

        canvas.addEventListener('mousedown', startDrawing);
        canvas.addEventListener('mousemove', draw);
        canvas.addEventListener('mouseup', stopDrawing);
        canvas.addEventListener('mouseleave', stopDrawing);

        canvas.addEventListener('touchstart', startDrawing);
        canvas.addEventListener('touchmove', draw);
        canvas.addEventListener('touchend', stopDrawing);

        function clearSignature() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            showNotification('Lienzo de firma limpiado');
        }

        function generatePDF() {
            showNotification('Generando Acuse de Entrega PDF con firma digital...');
        }

        // --- INICIALIZAR GRÁFICA KPI (CHART.JS) ---
        window.onload = function() {
            const ctxChart = document.getElementById('kpiChart').getContext('2d');
            new Chart(ctxChart, {
                type: 'bar',
                data: {
                    labels: ['10/Sep', '01/Oct', '02/Oct', '03/Oct', '04/Oct', '05/Oct', '06/Oct'],
                    datasets: [
                        {
                            label: 'Entradas',
                            data: [65, 59, 80, 81, 56, 55, 40],
                            backgroundColor: '#2563eb'
                        },
                        {
                            label: 'Salidas',
                            data: [45, 48, 40, 69, 86, 27, 90],
                            backgroundColor: '#f59e0b'
                        },
                        {
                            label: 'Existencia Total',
                            data: [90, 85, 70, 75, 60, 80, 95],
                            backgroundColor: '#10b981'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'bottom' }
                    },
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        };
    </script>
</body>
</html>
