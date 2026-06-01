// services/api.js
// Capa de comunicación con la API REST.
// Todas las peticiones pasan por aquí — los componentes nunca usan fetch directamente.

const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api/v1';

// ── helpers ───────────────────────────────────────────────────────────────

function getToken() {
    return localStorage.getItem('token');
}

async function request(path, options = {}) {
    const token = getToken();

    const headers = {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...options.headers,
    };

    const res = await fetch(`${BASE_URL}${path}`, { ...options, headers });

    // Si el token expiró o es inválido, forzar logout
    if (res.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        throw new Error('Sesión expirada');
    }

    if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        const msg = body.detail ?? `Error ${res.status}`;
        throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg));
    }

    // 204 No Content
    if (res.status === 204) return null;

    return res.json();
}

const get = (p) => request(p, { method: 'GET' });
const del = (p) => request(p, { method: 'DELETE' });
const post = (p, b) => request(p, { method: 'POST', body: JSON.stringify(b) });
const patch = (p, b) => request(p, { method: 'PATCH', body: JSON.stringify(b) });

// ── Auth ──────────────────────────────────────────────────────────────────

export const authApi = {
    login(nombre_usuario, contrasena) {
        // El endpoint usa form-data (OAuth2), no JSON
        return fetch(`${BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ username: nombre_usuario, password: contrasena }),
        }).then(async res => {
            if (!res.ok) {
                const b = await res.json().catch(() => ({}));
                throw new Error(b.detail ?? 'Credenciales incorrectas');
            }
            return res.json();
        });
    },
    me: () => get('/auth/me'),
    listarUsuarios: (s = 0, l = 100) => get(`/auth/usuarios?skip=${s}&limit=${l}`),
    actualizarUsuario: (id, d) => patch(`/auth/usuarios/${id}`, d),
    eliminarUsuario: (id) => del(`/auth/usuarios/${id}`),
    register: (data) => post('/auth/register', data),
};

// ── Roles ─────────────────────────────────────────────────────────────────
export const rolesApi = {
    listar: () => get('/roles/'),
    crear: (d) => post('/roles/', d),
    actualizar: (id, d) => patch(`/roles/${id}`, d),
    eliminar: (id) => del(`/roles/${id}`),
};

// ── Personas ──────────────────────────────────────────────────────────────
export const personasApi = {
    listar: (s = 0, l = 100) => get(`/personas/?skip=${s}&limit=${l}`),
    obtener: (id) => get(`/personas/${id}`),
    crear: (d) => post('/personas/', d),
    actualizar: (id, d) => patch(`/personas/${id}`, d),
    eliminar: (id) => del(`/personas/${id}`),
    // Responsables de objeto
    listarRespObj: (idP, s = 0, l = 100) => get(`/personas/${idP}/responsabilidades-objeto?skip=${s}&limit=${l}`),
    crearRespObj: (idP, d) => post(`/personas/${idP}/responsabilidades-objeto`, d),
    actualizarRespObj: (id, d) => patch(`/personas/responsables-objeto/${id}`, d),
    eliminarRespObj: (id) => del(`/personas/responsables-objeto/${id}`),
    // Responsables de ubicación
    listarRespUbi: (idP, s = 0, l = 100) => get(`/personas/${idP}/responsabilidades-ubicacion?skip=${s}&limit=${l}`),
    crearRespUbi: (idP, d) => post(`/personas/${idP}/responsabilidades-ubicacion`, d),
    actualizarRespUbi: (id, d) => patch(`/personas/responsables-ubicacion/${id}`, d),
    eliminarRespUbi: (id) => del(`/personas/responsables-ubicacion/${id}`),
};

// ── Tipos de Activo ───────────────────────────────────────────────────────
export const tiposActivoApi = {
    listar: () => get('/objetos/tipos-activo'),
    crear: (d) => post('/objetos/tipos-activo', d),
    actualizar: (id, d) => patch(`/objetos/tipos-activo/${id}`, d),
    eliminar: (id) => del(`/objetos/tipos-activo/${id}`),
};

// ── Objetos ───────────────────────────────────────────────────────────────
export const objetosApi = {
    listar: (s = 0, l = 100) => get(`/objetos/?skip=${s}&limit=${l}`),
    obtener: (id) => get(`/objetos/${id}`),
    crear: (d) => post('/objetos/', d),
    actualizar: (id, d) => patch(`/objetos/${id}`, d),
    eliminar: (id) => del(`/objetos/${id}`),
    // Items serializados
    listarTodosItems: (s = 0, l = 100) => get(`/objetos/items?skip=${s}&limit=${l}`),
    listarItems: (idObj) => get(`/objetos/${idObj}/items`),
    crearItem: (idObj, d) => post(`/objetos/${idObj}/items`, d),
    actualizarItem: (id, d) => patch(`/objetos/items/${id}`, d),
    eliminarItem: (id) => del(`/objetos/items/${id}`),
    // Objetos acumulables
    listarAcumulables: (idObj, s = 0, l = 100) => get(`/objetos/${idObj}/acumulables?skip=${s}&limit=${l}`),
    obtenerAcumulable: (id) => get(`/objetos/acumulables/${id}`),
    crearAcumulable: (idObj, d) => post(`/objetos/${idObj}/acumulables`, d),
    actualizarAcumulable: (id, d) => patch(`/objetos/acumulables/${id}`, d),
    eliminarAcumulable: (id) => del(`/objetos/acumulables/${id}`),
};

// ── Ubicaciones ───────────────────────────────────────────────────────────
export const ubicacionesApi = {
    listar: (s = 0, l = 100) => get(`/ubicaciones/?skip=${s}&limit=${l}`),
    obtener: (id) => get(`/ubicaciones/${id}`),
    crear: (d) => post('/ubicaciones/', d),
    actualizar: (id, d) => patch(`/ubicaciones/${id}`, d),
    eliminar: (id) => del(`/ubicaciones/${id}`),
    inventario: (id, s = 0, l = 100) => get(`/ubicaciones/${id}/inventario?skip=${s}&limit=${l}`),
    crearInventario: (id, d) => post(`/ubicaciones/${id}/inventario`, d),
    actualizarInventario: (id, d) => patch(`/ubicaciones/inventario/${id}`, d),
};

// ── Proveedores ───────────────────────────────────────────────────────────
export const proveedoresApi = {
    listar: (s = 0, l = 100) => get(`/facturas/proveedores?skip=${s}&limit=${l}`),
    obtener: (id) => get(`/facturas/proveedores/${id}`),
    crear: (d) => post('/facturas/proveedores', d),
    actualizar: (id, d) => patch(`/facturas/proveedores/${id}`, d),
    eliminar: (id) => del(`/facturas/proveedores/${id}`),
};

// ── Facturas ──────────────────────────────────────────────────────────────
export const facturasApi = {
    listar: (s = 0, l = 100, idProv) => get(`/facturas/?skip=${s}&limit=${l}${idProv ? `&id_proveedor=${idProv}` : ''}`),
    obtener: (id) => get(`/facturas/${id}`),
    crear: (d) => post('/facturas/', d),
    actualizar: (id, d) => patch(`/facturas/${id}`, d),
    detalles: (id) => get(`/facturas/${id}/detalles`),
    crearDetalle: (id, d) => post(`/facturas/${id}/detalles`, d),
};

// ── Movimientos ───────────────────────────────────────────────────────────
export const movimientosApi = {
    // Tipos de movimiento
    listarTipos: (s = 0, l = 100) => get(`/movimientos/tipos?skip=${s}&limit=${l}`),
    crearTipo: (d) => post('/movimientos/tipos', d),
    actualizarTipo: (id, d) => patch(`/movimientos/tipos/${id}`, d),
    eliminarTipo: (id) => del(`/movimientos/tipos/${id}`),
    // Movimientos
    listar: (s = 0, l = 100, idTipo) => get(`/movimientos/?skip=${s}&limit=${l}${idTipo ? `&id_tipo_movimiento=${idTipo}` : ''}`),
    obtener: (id) => get(`/movimientos/${id}`),
    crear: (d) => post('/movimientos/', d),
    actualizar: (id, d) => patch(`/movimientos/${id}`, d),
    eliminar: (id) => del(`/movimientos/${id}`),
    // Detalles de movimiento
    listarDetalles: (id, s = 0, l = 100) => get(`/movimientos/${id}/detalles?skip=${s}&limit=${l}`),
    crearDetalle: (id, d) => post(`/movimientos/${id}/detalles`, d),
    actualizarDetalle: (id, d) => patch(`/movimientos/detalles/${id}`, d),
    eliminarDetalle: (id) => del(`/movimientos/detalles/${id}`),
};