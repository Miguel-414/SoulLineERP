import { useState, useEffect } from "react";
import { ubicacionesApi } from "../../services/api";
import { useToast } from "../../contexts/ToastContext";
import {
  Modal,
  ConfirmDialog,
  FloatingInput,
  LoadingState,
  EmptyState,
  SearchBar,
} from "../../components/ui";

const EMPTY = { nombre: "", descripcion: "", id_zona_padre: "" };

export default function UbicacionesPage() {
  const toast = useToast();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [modal, setModal] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(EMPTY);
  const [saving, setSaving] = useState(false);
  const [delTarget, setDelTarget] = useState(null);
  const [deleting, setDeleting] = useState(false);

  const load = () => {
    setLoading(true);
    ubicacionesApi
      .listar()
      .then(setItems)
      .catch(() => toast.error("Error al cargar ubicaciones"))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const filtered = items.filter((i) =>
    i.nombre.toLowerCase().includes(search.toLowerCase()),
  );

  function openCreate() {
    setEditing(null);
    setForm(EMPTY);
    setModal(true);
  }
  function openEdit(u) {
    setEditing(u);
    setForm({
      nombre: u.nombre,
      descripcion: u.descripcion ?? "",
      id_zona_padre: u.id_zona_padre ?? "",
    });
    setModal(true);
  }

  async function handleSave() {
    if (!form.nombre) {
      toast.warning("El nombre es obligatorio");
      return;
    }
    setSaving(true);
    try {
      const payload = {
        nombre: form.nombre,
        descripcion: form.descripcion || null,
        id_zona_padre: form.id_zona_padre ? Number(form.id_zona_padre) : null,
      };
      editing
        ? await ubicacionesApi.actualizar(editing.id_ubicacion, {
            nombre: form.nombre,
            descripcion: form.descripcion || null,
          })
        : await ubicacionesApi.crear(payload);
      toast.success(editing ? "Ubicación actualizada" : "Ubicación creada");
      setModal(false);
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
      await ubicacionesApi.eliminar(delTarget.id_ubicacion);
      toast.success("Ubicación eliminada");
      setDelTarget(null);
      load();
    } catch (err) {
      toast.error(err.message);
    } finally {
      setDeleting(false);
    }
  }

  const nombrePadre = (id) =>
    items.find((i) => i.id_ubicacion === id)?.nombre ?? "—";

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1 className="page-title">Ubicaciones</h1>
          <p className="page-subtitle">
            Zonas y espacios físicos donde se almacena el inventario
          </p>
        </div>
        <button className="btn btn-primary" onClick={openCreate}>
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
          Nueva ubicación
        </button>
      </div>

      <div className="table-card">
        <div className="table-toolbar">
          <SearchBar
            value={search}
            onChange={setSearch}
            placeholder="Buscar ubicación..."
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
              <EmptyState
                text="No hay ubicaciones registradas"
                action={
                  <button className="btn btn-primary" onClick={openCreate}>
                    Crear primera
                  </button>
                }
              />
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>Nombre</th>
                    <th>Descripción</th>
                    <th>Zona padre</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((u) => (
                    <tr key={u.id_ubicacion}>
                      <td className="td-main">
                        {u.id_zona_padre && (
                          <span
                            style={{
                              color: "var(--primary-purple)",
                              marginRight: 6,
                            }}
                          >
                            ↳
                          </span>
                        )}
                        {u.nombre}
                      </td>
                      <td>{u.descripcion ?? "—"}</td>
                      <td>
                        {u.id_zona_padre ? (
                          nombrePadre(u.id_zona_padre)
                        ) : (
                          <span className="text-muted">Raíz</span>
                        )}
                      </td>
                      <td>
                        <div style={{ display: "flex", gap: 6 }}>
                          <button
                            className="btn btn-ghost btn-icon"
                            onClick={() => openEdit(u)}
                          >
                            <svg
                              width="15"
                              height="15"
                              viewBox="0 0 24 24"
                              fill="none"
                              stroke="currentColor"
                              strokeWidth="2"
                            >
                              <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" />
                              <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" />
                            </svg>
                          </button>
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
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}
      </div>

      <Modal
        open={modal}
        onClose={() => setModal(false)}
        title={editing ? "Editar ubicación" : "Nueva ubicación"}
        icon={
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z" />
            <circle cx="12" cy="10" r="3" />
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
              onClick={handleSave}
              disabled={saving}
            >
              {saving
                ? "Guardando..."
                : editing
                  ? "Guardar cambios"
                  : "Crear ubicación"}
            </button>
          </>
        }
      >
        <FloatingInput
          id="un"
          label="Nombre *"
          value={form.nombre}
          onChange={(e) => setForm((f) => ({ ...f, nombre: e.target.value }))}
        />
        <FloatingInput
          id="ud"
          label="Descripción"
          value={form.descripcion}
          onChange={(e) =>
            setForm((f) => ({ ...f, descripcion: e.target.value }))
          }
        />
        {!editing && (
          <div className="form-group">
            <label className="form-label-top">Zona padre (opcional)</label>
            <select
              className="form-select"
              value={form.id_zona_padre}
              onChange={(e) =>
                setForm((f) => ({ ...f, id_zona_padre: e.target.value }))
              }
            >
              <option value="">Ninguna (ubicación raíz)</option>
              {items.map((u) => (
                <option key={u.id_ubicacion} value={u.id_ubicacion}>
                  {u.nombre}
                </option>
              ))}
            </select>
          </div>
        )}
      </Modal>

      <ConfirmDialog
        open={!!delTarget}
        onClose={() => setDelTarget(null)}
        onConfirm={handleDelete}
        loading={deleting}
        title={`¿Eliminar "${delTarget?.nombre}"?`}
        message="Se eliminarán también las sub-zonas asociadas a esta ubicación."
      />
    </div>
  );
}
