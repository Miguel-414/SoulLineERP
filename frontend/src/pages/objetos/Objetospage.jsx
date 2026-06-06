import { useState, useEffect } from "react";
import { objetosApi, tiposActivoApi } from "../../services/api";
import { useToast } from "../../contexts/ToastContext";
import {
  Modal,
  ConfirmDialog,
  FloatingInput,
  LoadingState,
  EmptyState,
  EstadoBadge,
  SearchBar,
} from "../../components/Ui";

const EMPTY = {
  tipo_objeto: "unico",
  nombre: "",
  descripcion: "",
  marca: "",
  modelo: "",
  id_tipo_activo: "",
};

export default function ObjetosPage() {
  const toast = useToast();
  const [items, setItems] = useState([]);
  const [tipos, setTipos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [modal, setModal] = useState(false);
  const [editing, setEditing] = useState(null); // null = crear, obj = editar
  const [form, setForm] = useState(EMPTY);
  const [saving, setSaving] = useState(false);
  const [delTarget, setDelTarget] = useState(null);
  const [deleting, setDeleting] = useState(false);

  const load = () => {
    setLoading(true);
    Promise.all([objetosApi.listar(), tiposActivoApi.listar()])
      .then(([objs, tps]) => {
        setItems(objs);
        setTipos(tps);
      })
      .catch(() => toast.error("Error al cargar los datos"))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  // Filtrado local por nombre / marca
  const filtered = items.filter((i) =>
    [i.nombre, i.marca, i.modelo].some((v) =>
      v?.toLowerCase().includes(search.toLowerCase()),
    ),
  );

  function openCreate() {
    setEditing(null);
    setForm(EMPTY);
    setModal(true);
  }

  function openEdit(obj) {
    setEditing(obj);
    setForm({
      tipo_objeto: obj.tipo_objeto,
      nombre: obj.nombre,
      descripcion: obj.descripcion,
      marca: obj.marca ?? "",
      modelo: obj.modelo ?? "",
      id_tipo_activo: obj.id_tipo_activo,
    });
    setModal(true);
  }

  async function handleSave() {
    if (!form.nombre || !form.descripcion || !form.id_tipo_activo) {
      toast.warning("Nombre, descripción y tipo de activo son obligatorios");
      return;
    }
    setSaving(true);
    try {
      const payload = { ...form, id_tipo_activo: Number(form.id_tipo_activo) };
      if (editing) {
        const { tipo_objeto, id_tipo_activo, ...updatePayload } = payload;
        await objetosApi.actualizar(editing.id_objeto, updatePayload);
        toast.success("Objeto actualizado");
      } else {
        await objetosApi.crear(payload);
        toast.success("Objeto creado");
      }
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
      await objetosApi.eliminar(delTarget.id_objeto);
      toast.success("Objeto eliminado");
      setDelTarget(null);
      load();
    } catch (err) {
      toast.error(err.message);
    } finally {
      setDeleting(false);
    }
  }

  const nombreTipo = (id) =>
    tipos.find((t) => t.id_tipo_activo === id)?.nombre ?? "—";

  return (
    <div className="page-container">
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">Objetos</h1>
          <p className="page-subtitle">
            Catálogo de activos registrados en el sistema
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
          Nuevo objeto
        </button>
      </div>

      {/* Tabla */}
      <div className="table-card">
        <div className="table-toolbar">
          <SearchBar
            value={search}
            onChange={setSearch}
            placeholder="Buscar por nombre, marca..."
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
                text="No hay objetos registrados"
                action={
                  <button className="btn btn-primary" onClick={openCreate}>
                    Crear primero
                  </button>
                }
              />
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>Nombre</th>
                    <th>Tipo</th>
                    <th>Tipo Activo</th>
                    <th>Marca</th>
                    <th>Modelo</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((obj) => (
                    <tr key={obj.id_objeto}>
                      <td className="td-main">{obj.nombre}</td>
                      <td>
                        <EstadoBadge value={obj.tipo_objeto} />
                      </td>
                      <td>{nombreTipo(obj.id_tipo_activo)}</td>
                      <td>{obj.marca ?? "—"}</td>
                      <td>{obj.modelo ?? "—"}</td>
                      <td>
                        <div style={{ display: "flex", gap: 6 }}>
                          <button
                            className="btn btn-ghost btn-icon"
                            onClick={() => openEdit(obj)}
                            title="Editar"
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
                            onClick={() => setDelTarget(obj)}
                            title="Eliminar"
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
                              <path d="M10 11v6M14 11v6" />
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

      {/* Modal crear/editar */}
      <Modal
        open={modal}
        onClose={() => setModal(false)}
        title={editing ? "Editar objeto" : "Nuevo objeto"}
        icon={
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z" />
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
                  : "Crear objeto"}
            </button>
          </>
        }
      >
        <div className="form-grid-2">
          <FloatingInput
            id="nombre"
            label="Nombre *"
            value={form.nombre}
            onChange={(e) => setForm((f) => ({ ...f, nombre: e.target.value }))}
          />
          <div className="form-group">
            <label className="form-label-top">Tipo Activo *</label>
            <select
              className="form-select"
              value={form.id_tipo_activo}
              onChange={(e) =>
                setForm((f) => ({ ...f, id_tipo_activo: e.target.value }))
              }
            >
              <option value="">Seleccionar...</option>
              {tipos.map((t) => (
                <option key={t.id_tipo_activo} value={t.id_tipo_activo}>
                  {t.nombre}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="form-group">
          <label className="form-label-top">Descripción *</label>
          <textarea
            className="form-textarea"
            placeholder="Describe el objeto..."
            value={form.descripcion}
            onChange={(e) =>
              setForm((f) => ({ ...f, descripcion: e.target.value }))
            }
          />
        </div>

        <div className="form-grid-2">
          <FloatingInput
            id="marca"
            label="Marca"
            value={form.marca}
            onChange={(e) => setForm((f) => ({ ...f, marca: e.target.value }))}
          />
          <FloatingInput
            id="modelo"
            label="Modelo"
            value={form.modelo}
            onChange={(e) => setForm((f) => ({ ...f, modelo: e.target.value }))}
          />
        </div>

        {!editing && (
          <div className="form-group">
            <label className="form-label-top">Tipo de objeto</label>
            <select
              className="form-select"
              value={form.tipo_objeto}
              onChange={(e) =>
                setForm((f) => ({ ...f, tipo_objeto: e.target.value }))
              }
            >
              <option value="unico">Único (serializado)</option>
              <option value="acumulable">Acumulable (por cantidad)</option>
            </select>
          </div>
        )}
      </Modal>

      {/* Confirm delete */}
      <ConfirmDialog
        open={!!delTarget}
        onClose={() => setDelTarget(null)}
        onConfirm={handleDelete}
        loading={deleting}
        title={`¿Eliminar "${delTarget?.nombre}"?`}
        message="Se eliminará el objeto y todos sus registros asociados. Esta acción es irreversible."
      />
    </div>
  );
}
