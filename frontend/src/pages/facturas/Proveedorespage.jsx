import { useState, useEffect } from "react";
import { proveedoresApi } from "../../services/api";
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
  nit: "",
  razon_social: "",
  email: "",
  telefono: "",
  direccion: "",
};

export default function ProveedoresPage() {
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
    proveedoresApi
      .listar()
      .then(setItems)
      .catch(() => toast.error("Error al cargar proveedores"))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const filtered = items.filter((i) =>
    [i.razon_social, i.nit, i.email].some((v) =>
      v?.toLowerCase().includes(search.toLowerCase()),
    ),
  );

  function openCreate() {
    setEditing(null);
    setForm(EMPTY);
    setModal(true);
  }
  function openEdit(p) {
    setEditing(p);
    setForm({
      nit: p.nit,
      razon_social: p.razon_social,
      email: p.email,
      telefono: p.telefono,
      direccion: p.direccion,
    });
    setModal(true);
  }

  async function handleSave() {
    if (!form.nit || !form.razon_social || !form.email) {
      toast.warning("NIT, razón social y email son obligatorios");
      return;
    }
    setSaving(true);
    try {
      if (editing) {
        const { nit, ...rest } = form;
        await proveedoresApi.actualizar(editing.id_proveedor, rest);
      } else {
        await proveedoresApi.crear(form);
      }
      toast.success(editing ? "Proveedor actualizado" : "Proveedor creado");
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
      await proveedoresApi.eliminar(delTarget.id_proveedor);
      toast.success("Proveedor eliminado");
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
          <h1 className="page-title">Proveedores</h1>
          <p className="page-subtitle">
            Empresas y personas que suministran los activos
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
          Nuevo proveedor
        </button>
      </div>

      <div className="table-card">
        <div className="table-toolbar">
          <SearchBar
            value={search}
            onChange={setSearch}
            placeholder="Buscar por nombre, NIT..."
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
                text="No hay proveedores registrados"
                action={
                  <button className="btn btn-primary" onClick={openCreate}>
                    Agregar primero
                  </button>
                }
              />
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>Razón Social</th>
                    <th>NIT</th>
                    <th>Email</th>
                    <th>Teléfono</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((p) => (
                    <tr key={p.id_proveedor}>
                      <td className="td-main">{p.razon_social}</td>
                      <td>{p.nit}</td>
                      <td>{p.email}</td>
                      <td>{p.telefono}</td>
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
        title={editing ? "Editar proveedor" : "Nuevo proveedor"}
        icon={
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <rect x="1" y="3" width="15" height="13" />
            <polygon points="16 8 20 8 23 11 23 16 16 16 16 8" />
            <circle cx="5.5" cy="18.5" r="2.5" />
            <circle cx="18.5" cy="18.5" r="2.5" />
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
                  : "Crear proveedor"}
            </button>
          </>
        }
      >
        <div className="form-grid-2">
          <FloatingInput
            id="pnit"
            label="NIT *"
            value={form.nit}
            readOnly={!!editing}
            onChange={(e) => setForm((f) => ({ ...f, nit: e.target.value }))}
          />
          <FloatingInput
            id="prs"
            label="Razón Social *"
            value={form.razon_social}
            onChange={(e) =>
              setForm((f) => ({ ...f, razon_social: e.target.value }))
            }
          />
        </div>
        <div className="form-grid-2">
          <FloatingInput
            id="pem"
            label="Email *"
            type="email"
            value={form.email}
            onChange={(e) => setForm((f) => ({ ...f, email: e.target.value }))}
          />
          <FloatingInput
            id="ptel"
            label="Teléfono"
            value={form.telefono}
            onChange={(e) =>
              setForm((f) => ({ ...f, telefono: e.target.value }))
            }
          />
        </div>
        <FloatingInput
          id="pdir"
          label="Dirección"
          value={form.direccion}
          onChange={(e) =>
            setForm((f) => ({ ...f, direccion: e.target.value }))
          }
        />
      </Modal>

      <ConfirmDialog
        open={!!delTarget}
        onClose={() => setDelTarget(null)}
        onConfirm={handleDelete}
        loading={deleting}
        title={`¿Eliminar a "${delTarget?.razon_social}"?`}
        message="Las facturas asociadas a este proveedor también serán afectadas."
      />
    </div>
  );
}
