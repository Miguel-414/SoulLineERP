import { useState, useEffect } from "react";
import { personasApi } from "../../services/api";
import { useToast } from "../../contexts/ToastContext";
import {
  Modal,
  ConfirmDialog,
  FloatingInput,
  LoadingState,
  EmptyState,
  SearchBar,
} from "../../components/ui";

const EMPTY = {
  primer_nombre: "",
  segundo_nombre: "",
  primer_apellido: "",
  segundo_apellido: "",
  nombre: "",
  email: "",
  direccion: "",
  telefono: "",
};

export default function PersonasPage() {
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
    personasApi
      .listar()
      .then(setItems)
      .catch(() => toast.error("Error al cargar personas"))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const filtered = items.filter((i) =>
    [i.nombre, i.email, i.primer_apellido].some((v) =>
      v?.toLowerCase().includes(search.toLowerCase()),
    ),
  );

  const set = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }));

  function openCreate() {
    setEditing(null);
    setForm(EMPTY);
    setModal(true);
  }
  function openEdit(p) {
    setEditing(p);
    setForm({
      primer_nombre: p.primer_nombre,
      segundo_nombre: p.segundo_nombre ?? "",
      primer_apellido: p.primer_apellido,
      segundo_apellido: p.segundo_apellido ?? "",
      nombre: p.nombre,
      email: p.email,
      direccion: p.direccion,
      telefono: p.telefono,
    });
    setModal(true);
  }

  async function handleSave() {
    if (!form.primer_nombre || !form.primer_apellido || !form.email) {
      toast.warning("Primer nombre, primer apellido y email son obligatorios");
      return;
    }
    setSaving(true);
    try {
      const payload = {
        ...form,
        segundo_nombre: form.segundo_nombre || null,
        segundo_apellido: form.segundo_apellido || null,
      };
      editing
        ? await personasApi.actualizar(editing.id_persona, payload)
        : await personasApi.crear(payload);
      toast.success(editing ? "Persona actualizada" : "Persona creada");
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
      await personasApi.eliminar(delTarget.id_persona);
      toast.success("Persona eliminada");
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
          <h1 className="page-title">Personas</h1>
          <p className="page-subtitle">
            Directorio de contactos y personal del sistema
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
          Nueva persona
        </button>
      </div>

      <div className="table-card">
        <div className="table-toolbar">
          <SearchBar
            value={search}
            onChange={setSearch}
            placeholder="Buscar por nombre, email..."
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
                text="No hay personas registradas"
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
                    <th>Nombre completo</th>
                    <th>Email</th>
                    <th>Teléfono</th>
                    <th>Dirección</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((p) => (
                    <tr key={p.id_persona}>
                      <td className="td-main">{p.nombre}</td>
                      <td>{p.email}</td>
                      <td>{p.telefono}</td>
                      <td>{p.direccion}</td>
                      <td>
                        <div style={{ display: "flex", gap: 6 }}>
                          <button
                            className="btn btn-ghost btn-icon"
                            onClick={() => openEdit(p)}
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
                            onClick={() => setDelTarget(p)}
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
        title={editing ? "Editar persona" : "Nueva persona"}
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
              onClick={handleSave}
              disabled={saving}
            >
              {saving
                ? "Guardando..."
                : editing
                  ? "Guardar cambios"
                  : "Crear persona"}
            </button>
          </>
        }
      >
        <div className="form-grid-2">
          <FloatingInput
            id="ppn"
            label="Primer nombre *"
            value={form.primer_nombre}
            onChange={set("primer_nombre")}
          />
          <FloatingInput
            id="psn"
            label="Segundo nombre"
            value={form.segundo_nombre}
            onChange={set("segundo_nombre")}
          />
        </div>
        <div className="form-grid-2">
          <FloatingInput
            id="ppa"
            label="Primer apellido *"
            value={form.primer_apellido}
            onChange={set("primer_apellido")}
          />
          <FloatingInput
            id="psa"
            label="Segundo apellido"
            value={form.segundo_apellido}
            onChange={set("segundo_apellido")}
          />
        </div>
        <FloatingInput
          id="pnom"
          label="Nombre para mostrar"
          value={form.nombre}
          onChange={set("nombre")}
        />
        <div className="form-grid-2">
          <FloatingInput
            id="pem"
            label="Email *"
            type="email"
            value={form.email}
            onChange={set("email")}
          />
          <FloatingInput
            id="ptel"
            label="Teléfono"
            value={form.telefono}
            onChange={set("telefono")}
          />
        </div>
        <FloatingInput
          id="pdir"
          label="Dirección"
          value={form.direccion}
          onChange={set("direccion")}
        />
      </Modal>

      <ConfirmDialog
        open={!!delTarget}
        onClose={() => setDelTarget(null)}
        onConfirm={handleDelete}
        loading={deleting}
        title={`¿Eliminar a "${delTarget?.nombre}"?`}
        message="Si la persona tiene un usuario asociado, este también será eliminado."
      />
    </div>
  );
}
