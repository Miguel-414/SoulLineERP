import { useState, useEffect } from "react";
import { authApi, rolesApi, personasApi } from "../../services/api";
import { useAuth } from "../../contexts/AuthContext";
import { useToast } from "../../contexts/ToastContext";
import {
  Modal,
  ConfirmDialog,
  FloatingInput,
  LoadingState,
  EmptyState,
  SearchBar,
} from "../../components/ui";

export default function UsuariosPage() {
  const toast = useToast();
  const { user: me } = useAuth();
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [personas, setPersonas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [modal, setModal] = useState(false);
  const [saving, setSaving] = useState(false);
  const [delTarget, setDelTarget] = useState(null);
  const [deleting, setDeleting] = useState(false);

  const EMPTY_FORM = {
    // Persona
    primer_nombre: "",
    segundo_nombre: "",
    primer_apellido: "",
    segundo_apellido: "",
    nombre: "",
    email: "",
    direccion: "",
    telefono: "",
    // Usuario
    nombre_usuario: "",
    contrasena: "",
    id_rol: "",
  };
  const [form, setForm] = useState(EMPTY_FORM);
  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));

  const load = () => {
    setLoading(true);
    Promise.all([
      authApi.listarUsuarios(),
      rolesApi.listar(),
      personasApi.listar(),
    ])
      .then(([us, rs, ps]) => {
        setUsers(us);
        setRoles(rs);
        setPersonas(ps);
      })
      .catch(() => toast.error("Error al cargar usuarios"))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const filtered = users.filter((u) =>
    u.nombre_usuario.toLowerCase().includes(search.toLowerCase()),
  );
  const personaNombre = (id) =>
    personas.find((p) => p.id_persona === id)?.nombre ?? `Persona #${id}`;
  const rolNombre = (id) => roles.find((r) => r.id_rol === id)?.nombre ?? "—";

  async function handleCreate() {
    if (
      !form.nombre_usuario ||
      !form.contrasena ||
      !form.id_rol ||
      !form.primer_nombre ||
      !form.primer_apellido ||
      !form.email
    ) {
      toast.warning(
        "Nombre de usuario, contraseña, rol, nombre y email son obligatorios",
      );
      return;
    }
    setSaving(true);
    try {
      await authApi.register({
        persona: {
          primer_nombre: form.primer_nombre,
          segundo_nombre: form.segundo_nombre || null,
          primer_apellido: form.primer_apellido,
          segundo_apellido: form.segundo_apellido || null,
          nombre:
            form.nombre || `${form.primer_nombre} ${form.primer_apellido}`,
          email: form.email,
          direccion: form.direccion,
          telefono: form.telefono,
        },
        usuario: {
          nombre_usuario: form.nombre_usuario,
          contrasena: form.contrasena,
          id_rol: Number(form.id_rol),
        },
      });
      toast.success("Usuario creado exitosamente");
      setModal(false);
      setForm(EMPTY_FORM);
      load();
    } catch (err) {
      toast.error(err.message);
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete() {
    setDeleting(true);
    try {
      await authApi.eliminarUsuario(delTarget.id_usuario);
      toast.success("Usuario eliminado");
      setDelTarget(null);
      load();
    } catch (err) {
      toast.error(err.message);
    } finally {
      setDeleting(false);
    }
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1 className="page-title">Usuarios</h1>
          <p className="page-subtitle">Cuentas de acceso al sistema</p>
        </div>
        <button className="btn btn-primary" onClick={() => setModal(true)}>
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.5"
          >
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
          Nuevo usuario
        </button>
      </div>

      <div className="table-card">
        <div className="table-toolbar">
          <SearchBar
            value={search}
            onChange={setSearch}
            placeholder="Buscar usuario..."
          />
          <span className="text-muted" style={{ fontSize: 13 }}>
            {filtered.length} registros
          </span>
        </div>
        {loading ? (
          <LoadingState />
        ) : (
          <div className="table-wrapper">
            {filtered.length === 0 ? (
              <EmptyState text="No hay usuarios" />
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>Usuario</th>
                    <th>Persona</th>
                    <th>Rol</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((u) => (
                    <tr key={u.id_usuario}>
                      <td className="td-main">
                        <div
                          style={{
                            display: "flex",
                            alignItems: "center",
                            gap: 10,
                          }}
                        >
                          <div
                            style={{
                              width: 30,
                              height: 30,
                              borderRadius: "50%",
                              background:
                                "linear-gradient(135deg,var(--primary-purple),var(--primary-pink))",
                              display: "flex",
                              alignItems: "center",
                              justifyContent: "center",
                              fontSize: 12,
                              fontWeight: 700,
                              flexShrink: 0,
                            }}
                          >
                            {u.nombre_usuario.slice(0, 2).toUpperCase()}
                          </div>
                          {u.nombre_usuario}
                          {u.nombre_usuario === me?.nombre_usuario && (
                            <span
                              className="badge badge-purple"
                              style={{ fontSize: 10 }}
                            >
                              Tú
                            </span>
                          )}
                        </div>
                      </td>
                      <td>{personaNombre(u.id_persona)}</td>
                      <td>
                        <span className="badge badge-purple">
                          {rolNombre(u.id_rol)}
                        </span>
                      </td>
                      <td>
                        {u.nombre_usuario !== "superadmin" &&
                          u.id_usuario !== me?.id_usuario && (
                            <button
                              className="btn btn-danger btn-icon"
                              onClick={() => setDelTarget(u)}
                            >
                              <svg
                                width="15"
                                height="15"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                              >
                                <polyline points="3 6 5 6 21 6" />
                                <path d="M19 6l-1 14H6L5 6" />
                              </svg>
                            </button>
                          )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}
      </div>

      {/* Modal crear usuario + persona */}
      <Modal
        open={modal}
        onClose={() => setModal(false)}
        title="Nuevo usuario"
        size="modal-lg"
        icon={
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
        }
        footer={
          <>
            <button
              className="btn btn-ghost"
              onClick={() => setModal(false)}
              disabled={saving}
            >
              Cancelar
            </button>
            <button
              className="btn btn-primary"
              onClick={handleCreate}
              disabled={saving}
            >
              {saving ? "Creando..." : "Crear usuario"}
            </button>
          </>
        }
      >
        <p
          style={{
            fontSize: 12,
            color: "var(--text-gray)",
            textTransform: "uppercase",
            letterSpacing: 1,
            marginBottom: 4,
          }}
        >
          Datos personales
        </p>
        <div className="form-grid-2">
          <FloatingInput
            id="upn"
            label="Primer nombre *"
            value={form.primer_nombre}
            onChange={set("primer_nombre")}
          />
          <FloatingInput
            id="usn"
            label="Segundo nombre"
            value={form.segundo_nombre}
            onChange={set("segundo_nombre")}
          />
        </div>
        <div className="form-grid-2">
          <FloatingInput
            id="upa"
            label="Primer apellido *"
            value={form.primer_apellido}
            onChange={set("primer_apellido")}
          />
          <FloatingInput
            id="usa"
            label="Segundo apellido"
            value={form.segundo_apellido}
            onChange={set("segundo_apellido")}
          />
        </div>
        <div className="form-grid-2">
          <FloatingInput
            id="uem"
            label="Email *"
            type="email"
            value={form.email}
            onChange={set("email")}
          />
          <FloatingInput
            id="utel"
            label="Teléfono"
            value={form.telefono}
            onChange={set("telefono")}
          />
        </div>
        <FloatingInput
          id="udir"
          label="Dirección"
          value={form.direccion}
          onChange={set("direccion")}
        />

        <div className="divider" style={{ margin: "8px 0" }} />
        <p
          style={{
            fontSize: 12,
            color: "var(--text-gray)",
            textTransform: "uppercase",
            letterSpacing: 1,
            marginBottom: 4,
          }}
        >
          Cuenta de acceso
        </p>

        <div className="form-grid-2">
          <FloatingInput
            id="uusr"
            label="Nombre de usuario *"
            value={form.nombre_usuario}
            onChange={set("nombre_usuario")}
          />
          <FloatingInput
            id="upwd"
            label="Contraseña *"
            type="password"
            value={form.contrasena}
            onChange={set("contrasena")}
          />
        </div>
        <div className="form-group">
          <label className="form-label-top">Rol *</label>
          <select
            className="form-select"
            value={form.id_rol}
            onChange={set("id_rol")}
          >
            <option value="">Seleccionar rol...</option>
            {roles.map((r) => (
              <option key={r.id_rol} value={r.id_rol}>
                {r.nombre}
              </option>
            ))}
          </select>
        </div>
      </Modal>

      <ConfirmDialog
        open={!!delTarget}
        onClose={() => setDelTarget(null)}
        onConfirm={handleDelete}
        loading={deleting}
        title={`¿Eliminar a "${delTarget?.nombre_usuario}"?`}
        message="El usuario perderá acceso inmediatamente."
      />
    </div>
  );
}
