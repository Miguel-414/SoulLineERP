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

function get(path) { return request(path, { method: 'GET' }); }
function del(path) { return request(path, { method: 'DELETE' }); }
function post(path, body) { return request(path, { method: 'POST', body: JSON.stringify(body) }); }
function patch(path, body) { return request(path, { method: 'PATCH', body: JSON.stringify(body) }); }

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
                const body = await res.json().catch(() => ({}));
                throw new Error(body.detail ?? 'Credenciales incorrectas');
            }
            return res.json();
        });
    },
    me: () => get('/auth/me'),
    listarUsuarios: (p = 0) => get(`/auth/usuarios?skip=${p * 50}&limit=50`),
    actualizarUsuario: (id, d) => patch(`/auth/usuarios/${id}`, d),
    eliminarUsuario: (id) => del(`/auth/usuarios/${id}`),
    register: (data) => post('/auth/register', data),
};

// ── Roles ─────────────────────────────────────────────────────────────────

export const rolesApi = {
    listar: () => get('/roles/'),
    crear: (data) => post('/roles/', data),
    actualizar: (id, d) => patch(`/roles/${id}`, d),
    eliminar: (id) => del(`/roles/${id}`),
};

// ── Personas ──────────────────────────────────────────────────────────────

export const personasApi = {
    listar: (p = 0) => get(`/personas/?skip=${p * 50}&limit=50`),
    obtener: (id) => get(`/personas/${id}`),
    crear: (data) => post('/personas/', data),
    actualizar: (id, d) => patch(`/personas/${id}`, d),
    eliminar: (id) => del(`/personas/${id}`),
};

// ── Tipos de Activo ───────────────────────────────────────────────────────

export const tiposActivoApi = {
    listar: () => get('/objetos/tipos-activo'),
    crear: (data) => post('/objetos/tipos-activo', data),
    actualizar: (id, d) => patch(`/objetos/tipos-activo/${id}`, d),
    eliminar: (id) => del(`/objetos/tipos-activo/${id}`),
};

// ── Objetos ───────────────────────────────────────────────────────────────

export const objetosApi = {
    listar: (p = 0) => get(`/objetos/?skip=${p * 50}&limit=50`),
    obtener: (id) => get(`/objetos/${id}`),
    crear: (data) => post('/objetos/', data),
    actualizar: (id, d) => patch(`/objetos/${id}`, d),
    eliminar: (id) => del(`/objetos/${id}`),
    listarItems: (idObj, p = 0) => get(`/objetos/${idObj}/items?skip=${p * 50}&limit=50`),
    crearItem: (idObj, data) => post(`/objetos/${idObj}/items`, data),
    actualizarItem: (id, d) => patch(`/objetos/items/${id}`, d),
};

// ── Ubicaciones ───────────────────────────────────────────────────────────

export const ubicacionesApi = {
    listar: (p = 0) => get(`/ubicaciones/?skip=${p * 50}&limit=50`),
    obtener: (id) => get(`/ubicaciones/${id}`),
    crear: (data) => post('/ubicaciones/', data),
    actualizar: (id, d) => patch(`/ubicaciones/${id}`, d),
    eliminar: (id) => del(`/ubicaciones/${id}`),
    inventario: (id, p = 0) => get(`/ubicaciones/${id}/inventario?skip=${p * 50}&limit=50`),
    crearInventario: (id, d) => post(`/ubicaciones/${id}/inventario`, d),
    actualizarInventario: (id, d) => patch(`/ubicaciones/inventario/${id}`, d),
};

// ── Proveedores ───────────────────────────────────────────────────────────

export const proveedoresApi = {
    listar: (p = 0) => get(`/facturas/proveedores?skip=${p * 50}&limit=50`),
    obtener: (id) => get(`/facturas/proveedores/${id}`),
    crear: (data) => post('/facturas/proveedores', data),
    actualizar: (id, d) => patch(`/facturas/proveedores/${id}`, d),
    eliminar: (id) => del(`/facturas/proveedores/${id}`),
};

// ── Facturas ──────────────────────────────────────────────────────────────

export const facturasApi = {
    listar: (p = 0, idProv) => get(`/facturas/?skip=${p * 50}&limit=50${idProv ? `&id_proveedor=${idProv}` : ''}`),
    obtener: (id) => get(`/facturas/${id}`),
    crear: (data) => post('/facturas/', data),
    actualizar: (id, d) => patch(`/facturas/${id}`, d),
    detalles: (id) => get(`/facturas/${id}/detalles`),
    crearDetalle: (id, d) => post(`/facturas/${id}/detalles`, d),
};