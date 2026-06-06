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
  id_objeto: "",
  serie: "",
  placa_activo: "",
  estado_funcional: "OPERATIVO",
  estado_fisico: "BUENO",
  fecha_adquisicion: "",
  fecha_puesto_servicio: "",
  n_garantia: "",
  fecha_inicio_garantia: "",
  fecha_fin_garantia: "",
};

export default function ItemsPage() {
  const toast = useToast();
  const [items, setItems] = useState([]);
  const [objetos, setObjetos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [filterEst, setFilterEst] = useState("");
  const [modal, setModal] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(EMPTY);
  const [saving, setSaving] = useState(false);
  const [delTarget, setDelTarget] = useState(null);
  const [deleting, setDeleting] = useState(false);

  // todo no esta pudiendo leer los datos de la api para listar los objetos o tipos de objetos
  const load = () => {
    setLoading(true);
    Promise.all([objetosApi.listarTodosItems(), objetosApi.listar()])
      .then(([its, obs]) => {
        setItems(its);
        setObjetos(obs);
      })
      .catch((err) => toast.error(`Error al cargar items ${err}`))
      .finally(() => setLoading(false));
  };
  useEffect(load, []);

  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));
  const nombreObjeto = (id) =>
    objetos.find((o) => o.id_objeto === id)?.nombre ?? `Objeto #${id}`;

  const filtered = items.filter((i) => {
    const matchSearch = [
      i.placa_activo,
      i.serie,
      nombreObjeto(i.id_objeto),
    ].some((v) => v?.toLowerCase().includes(search.toLowerCase()));
    const matchEst = !filterEst || i.estado_funcional === filterEst;
    return matchSearch && matchEst;
  });

  function openCreate() {
    setEditing(null);
    setForm(EMPTY);
    setModal(true);
  }
  function openEdit(item) {
    setEditing(item);
    setForm({
      id_objeto: item.id_objeto,
      serie: item.serie ?? "",
      placa_activo: item.placa_activo,
      estado_funcional: item.estado_funcional,
      estado_fisico: item.estado_fisico,
      fecha_adquisicion: item.fecha_adquisicion ?? "",
      fecha_puesto_servicio: item.fecha_puesto_servicio ?? "",
      n_garantia: item.n_garantia ?? "",
      fecha_inicio_garantia: item.fecha_inicio_garantia ?? "",
      fecha_fin_garantia: item.fecha_fin_garantia ?? "",
    });
    setModal(true);
  }

  async function handleSave() {
    if (!form.id_objeto || !form.placa_activo || !form.fecha_adquisicion) {
      toast.warning("Objeto, placa y fecha de adquisición son obligatorios");
      return;
    }
    setSaving(true);
    try {
      const payload = {
        ...form,
        id_objeto: Number(form.id_objeto),
        serie: form.serie || null,
        fecha_puesto_servicio: form.fecha_puesto_servicio || null,
        n_garantia: form.n_garantia || null,
        fecha_inicio_garantia: form.fecha_inicio_garantia || null,
        fecha_fin_garantia: form.fecha_fin_garantia || null,
      };
      if (editing) {
        const {
          id_objeto,
          serie,
          placa_activo,
          fecha_adquisicion,
          ...updatePayload
        } = payload;
        await objetosApi.actualizarItem(
          editing.id_item_serializado,
          updatePayload,
        );
        toast.success("Item actualizado");
      } else {
        await objetosApi.crearItem(Number(form.id_objeto), payload);
        toast.success("Item creado");
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
      await objetosApi.eliminarItem(delTarget.id_item_serializado);
      toast.success("Item eliminado");
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
          <h1 className="page-title">Items Serializados</h1>
          <p className="page-subtitle">
            Activos únicos con placa, serie y garantía individual
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
          Nuevo item
        </button>
      </div>

      <div className="table-card">
        <div className="table-toolbar">
          <SearchBar
            value={search}
            onChange={setSearch}
            placeholder="Buscar por placa, serie, objeto..."
          />
          <div style={{ display: "flex", gap: 8 }}>
            <select
              className="form-select"
              style={{ width: "auto" }}
              value={filterEst}
              onChange={(e) => setFilterEst(e.target.value)}
            >
              <option value="">Todos los estados</option>
              <option value="OPERATIVO">Operativo</option>
              <option value="FALLANDO">Fallando</option>
              <option value="RETIRADO">Retirado</option>
            </select>
            <span
              className="text-muted"
              style={{ fontSize: 13, alignSelf: "center" }}
            >
              {filtered.length} items
            </span>
          </div>
        </div>

        {loading ? (
          <LoadingState />
        ) : (
          <div className="table-wrapper">
            {filtered.length === 0 ? (
              <EmptyState
                text="No hay items serializados"
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
                    <th>Placa Activo</th>
                    <th>Objeto</th>
                    <th>Serie</th>
                    <th>Est. Funcional</th>
                    <th>Est. Físico</th>
                    <th>Adquisición</th>
                    <th>Garantía hasta</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((item) => (
                    <tr key={item.id_item_serializado}>
                      <td className="td-main">{item.placa_activo}</td>
                      <td>{nombreObjeto(item.id_objeto)}</td>
                      <td className="text-muted">{item.serie ?? "—"}</td>
                      <td>
                        <EstadoBadge value={item.estado_funcional} />
                      </td>
                      <td>
                        <EstadoBadge value={item.estado_fisico} />
                      </td>
                      <td>{item.fecha_adquisicion ?? "—"}</td>
                      <td>
                        {item.fecha_fin_garantia ?? (
                          <span className="text-muted">—</span>
                        )}
                      </td>
                      <td>
                        <div style={{ display: "flex", gap: 6 }}>
                          <button
                            className="btn btn-ghost btn-icon"
                            onClick={() => openEdit(item)}
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
                            onClick={() => setDelTarget(item)}
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
        size="modal-lg"
        title={
          editing
            ? `Editar item: ${editing.placa_activo}`
            : "Nuevo item serializado"
        }
        icon={
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <rect x="2" y="7" width="20" height="14" rx="2" />
            <path d="M16 3l-4-1-4 1" />
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
                  : "Crear item"}
            </button>
          </>
        }
      >
        {!editing && (
          <div className="form-group">
            <label className="form-label-top">Objeto *</label>
            <select
              className="form-select"
              value={form.id_objeto}
              onChange={set("id_objeto")}
            >
              <option value="">Seleccionar objeto...</option>
              {objetos
                .filter((o) => o.tipo_objeto === "unico")
                .map((o) => (
                  <option key={o.id_objeto} value={o.id_objeto}>
                    {o.nombre}
                  </option>
                ))}
            </select>
          </div>
        )}

        <div className="form-grid-2">
          <FloatingInput
            id="iplaca"
            label="Placa activo *"
            value={form.placa_activo}
            readOnly={!!editing}
            onChange={set("placa_activo")}
          />
          <FloatingInput
            id="iserie"
            label="Número de serie"
            value={form.serie}
            onChange={set("serie")}
          />
        </div>

        <div className="form-grid-2">
          <div className="form-group">
            <label className="form-label-top">Estado funcional</label>
            <select
              className="form-select"
              value={form.estado_funcional}
              onChange={set("estado_funcional")}
            >
              <option value="OPERATIVO">Operativo</option>
              <option value="FALLANDO">Fallando</option>
              <option value="RETIRADO">Retirado</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label-top">Estado físico</label>
            <select
              className="form-select"
              value={form.estado_fisico}
              onChange={set("estado_fisico")}
            >
              <option value="BUENO">Bueno</option>
              <option value="REGULAR">Regular</option>
              <option value="MALO">Malo</option>
            </select>
          </div>
        </div>

        <div className="form-grid-2">
          {!editing && (
            <FloatingInput
              id="ifechaAdq"
              label="Fecha adquisición *"
              type="date"
              value={form.fecha_adquisicion}
              onChange={set("fecha_adquisicion")}
            />
          )}
          <FloatingInput
            id="ifechaServ"
            label="Puesto en servicio"
            type="date"
            value={form.fecha_puesto_servicio}
            onChange={set("fecha_puesto_servicio")}
          />
        </div>

        <div className="divider" style={{ margin: "4px 0" }} />
        <p
          style={{
            fontSize: 11,
            color: "var(--text-gray)",
            textTransform: "uppercase",
            letterSpacing: 1,
          }}
        >
          Garantía (opcional)
        </p>

        <div className="form-grid-3">
          <FloatingInput
            id="igarNro"
            label="N° garantía"
            value={form.n_garantia}
            onChange={set("n_garantia")}
          />
          <FloatingInput
            id="igarIni"
            label="Inicio garantía"
            type="date"
            value={form.fecha_inicio_garantia}
            onChange={set("fecha_inicio_garantia")}
          />
          <FloatingInput
            id="igarFin"
            label="Fin garantía"
            type="date"
            value={form.fecha_fin_garantia}
            onChange={set("fecha_fin_garantia")}
          />
        </div>
      </Modal>

      <ConfirmDialog
        open={!!delTarget}
        onClose={() => setDelTarget(null)}
        onConfirm={handleDelete}
        loading={deleting}
        title={`¿Eliminar item "${delTarget?.placa_activo}"?`}
        message="Se eliminarán también los registros de inventario y movimientos asociados a este item."
      />
    </div>
  );
}
