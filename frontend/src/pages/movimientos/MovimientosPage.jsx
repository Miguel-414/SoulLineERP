import { useState, useEffect } from "react";
import { movimientosApi, objetosApi, ubicacionesApi } from "../../services/api";
import { useToast } from "../../contexts/ToastContext";
import {
  Modal,
  ConfirmDialog,
  FloatingInput,
  LoadingState,
  EmptyState,
  SearchBar,
} from "../../components/ui";

const EMPTY_MOV = {
  fecha_movimiento: new Date().toISOString().slice(0, 10),
  id_tipo_movimiento: "",
};
const EMPTY_DET = {
  id_objeto: "",
  id_item_serializado: "",
  id_inventario_origen: "",
  id_inventario_destino: "",
  id_ubicacion_origen: "",
  id_ubicacion_destino: "",
  cantidad_afectada: 1,
  observaciones: "",
};

export default function MovimientosPage() {
  const toast = useToast();
  const [movs, setMovs] = useState([]);
  const [tipos, setTipos] = useState([]);
  const [objetos, setObjetos] = useState([]);
  const [ubicaciones, setUbicaciones] = useState([]);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [filterTipo, setFilterTipo] = useState("");

  // Modal crear movimiento
  const [modalMov, setModalMov] = useState(false);
  const [formMov, setFormMov] = useState(EMPTY_MOV);
  const [savingMov, setSavingMov] = useState(false);

  // Modal detalles (ver + agregar)
  const [detailMov, setDetailMov] = useState(null);
  const [detalles, setDetalles] = useState([]);
  const [loadingDet, setLoadingDet] = useState(false);
  const [modalDet, setModalDet] = useState(false);
  const [formDet, setFormDet] = useState(EMPTY_DET);
  const [savingDet, setSavingDet] = useState(false);
  const [delDetTarget, setDelDetTarget] = useState(null);
  const [deletingDet, setDeletingDet] = useState(false);

  // Delete movimiento
  const [delTarget, setDelTarget] = useState(null);
  const [deleting, setDeleting] = useState(false);

  // todo aqui hay problema no esta trayendo los tipos de movimientos
  // ? la informacion a los endpoint se esta enviando bien, pero no esta entrando correctamente a la promesa
  // ! otra pagina tampoco esta interactuando correctamente al traer tipos en un formulario
  // ? item serializado
  function load() {
    setLoading(true);
    Promise.all([
      movimientosApi.listar(0, 100, filterTipo || undefined),
      movimientosApi.listarTipos(),
      objetosApi.listar(),
      ubicacionesApi.listar(),
      objetosApi.listarTodosItems(),
    ])
      .then(([ms, ts, obs, ubs, its]) => {
        setMovs(ms);
        setTipos(ts);
        setObjetos(obs);
        setUbicaciones(ubs);
        setItems(its);
      })
      .catch(() => toast.error("Error al cargar movimientos"))
      .finally(() => setLoading(false));
  }
  useEffect(load, [filterTipo]);

  const set = (k) => (e) => setFormDet((f) => ({ ...f, [k]: e.target.value }));
  const nombreTipo = (id) =>
    tipos.find((t) => t.id_tipo_movimiento === id)?.nombre ?? `Tipo #${id}`;
  const nombreObj = (id) =>
    objetos.find((o) => o.id_objeto === id)?.nombre ?? `Obj. #${id}`;
  const nombreUbi = (id) =>
    ubicaciones.find((u) => u.id_ubicacion === id)?.nombre ?? `Ub. #${id}`;

  const filtered = movs.filter((m) => {
    const nt = nombreTipo(m.id_tipo_movimiento).toLowerCase();
    return (
      nt.includes(search.toLowerCase()) ||
      String(m.id_movimiento).includes(search)
    );
  });

  async function handleCreateMov() {
    if (!formMov.id_tipo_movimiento || !formMov.fecha_movimiento) {
      toast.warning("Tipo y fecha son obligatorios");
      return;
    }
    setSavingMov(true);
    try {
      const newMov = await movimientosApi.crear({
        ...formMov,
        id_tipo_movimiento: Number(formMov.id_tipo_movimiento),
      });
      toast.success("Movimiento creado");
      setModalMov(false);
      setFormMov(EMPTY_MOV);
      load();
      // Abrir detalles automáticamente
      setDetailMov(newMov);
      setDetalles([]);
    } catch (err) {
      toast.error(err.message);
    } finally {
      setSavingMov(false);
    }
  }

  async function openDetail(mov) {
    setDetailMov(mov);
    setDetalles([]);
    setLoadingDet(true);
    try {
      const d = await movimientosApi.listarDetalles(mov.id_movimiento);
      setDetalles(d);
    } catch {
      toast.error("Error al cargar detalles");
    } finally {
      setLoadingDet(false);
    }
  }

  async function handleAddDetalle() {
    if (
      !formDet.id_objeto ||
      !formDet.id_ubicacion_destino ||
      !formDet.cantidad_afectada
    ) {
      toast.warning("Objeto, ubicación destino y cantidad son obligatorios");
      return;
    }
    setSavingDet(true);
    try {
      const payload = {
        id_movimiento: detailMov.id_movimiento,
        id_objeto: Number(formDet.id_objeto),
        id_item_serializado: formDet.id_item_serializado
          ? Number(formDet.id_item_serializado)
          : null,
        id_inventario_origen: formDet.id_inventario_origen
          ? Number(formDet.id_inventario_origen)
          : null,
        id_inventario_destino: formDet.id_inventario_destino
          ? Number(formDet.id_inventario_destino)
          : null,
        id_ubicacion_origen: formDet.id_ubicacion_origen
          ? Number(formDet.id_ubicacion_origen)
          : null,
        id_ubicacion_destino: Number(formDet.id_ubicacion_destino),
        cantidad_afectada: Number(formDet.cantidad_afectada),
        observaciones: formDet.observaciones || null,
      };
      const newDet = await movimientosApi.crearDetalle(
        detailMov.id_movimiento,
        payload,
      );
      setDetalles((d) => [...d, newDet]);
      toast.success("Línea de detalle agregada");
      setModalDet(false);
      setFormDet(EMPTY_DET);
    } catch (err) {
      toast.error(err.message);
    } finally {
      setSavingDet(false);
    }
  }

  async function handleDeleteDetalle() {
    setDeletingDet(true);
    try {
      await movimientosApi.eliminarDetalle(delDetTarget.id_detalle_movimiento);
      setDetalles((d) =>
        d.filter(
          (x) => x.id_detalle_movimiento !== delDetTarget.id_detalle_movimiento,
        ),
      );
      toast.success("Detalle eliminado");
      setDelDetTarget(null);
    } catch (err) {
      toast.error(err.message);
    } finally {
      setDeletingDet(false);
    }
  }

  async function handleDeleteMov() {
    setDeleting(true);
    try {
      await movimientosApi.eliminar(delTarget.id_movimiento);
      toast.success("Movimiento eliminado");
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
          <h1 className="page-title">Movimientos</h1>
          <p className="page-subtitle">
            Registro de entradas, salidas y traslados del inventario
          </p>
        </div>
        <button
          className="btn btn-primary"
          onClick={() => {
            setFormMov(EMPTY_MOV);
            setModalMov(true);
          }}
        >
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
          Registrar movimiento
        </button>
      </div>

      <div className="table-card">
        <div className="table-toolbar">
          <SearchBar
            value={search}
            onChange={setSearch}
            placeholder="Buscar por tipo, #ID..."
          />
          <select
            className="form-select"
            style={{ width: "auto", minWidth: 180 }}
            value={filterTipo}
            onChange={(e) => setFilterTipo(e.target.value)}
          >
            <option value="">Todos los tipos</option>
            {tipos.map((t) => (
              <option key={t.id_tipo_movimiento} value={t.id_tipo_movimiento}>
                {t.nombre}
              </option>
            ))}
          </select>
        </div>

        {loading ? (
          <LoadingState />
        ) : (
          <div className="table-wrapper">
            {filtered.length === 0 ? (
              <EmptyState
                text="No hay movimientos registrados"
                action={
                  <button
                    className="btn btn-primary"
                    onClick={() => setModalMov(true)}
                  >
                    Registrar primero
                  </button>
                }
              />
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Fecha</th>
                    <th>Tipo</th>
                    <th>Líneas</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((m) => (
                    <tr key={m.id_movimiento}>
                      <td className="text-muted">#{m.id_movimiento}</td>
                      <td className="td-main">{m.fecha_movimiento}</td>
                      <td>
                        <span className="badge badge-purple">
                          {nombreTipo(m.id_tipo_movimiento)}
                        </span>
                      </td>
                      <td>
                        <button
                          className="btn btn-secondary"
                          style={{ fontSize: 12, padding: "5px 10px" }}
                          onClick={() => openDetail(m)}
                        >
                          Ver detalles
                        </button>
                      </td>
                      <td>
                        <button
                          className="btn btn-danger btn-icon"
                          onClick={() => setDelTarget(m)}
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
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}
      </div>

      {/* Modal crear movimiento */}
      <Modal
        open={modalMov}
        onClose={() => setModalMov(false)}
        title="Registrar movimiento"
        icon={
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M7 16V4m0 0L3 8m4-4l4 4M17 8v12m0 0l4-4m-4 4l-4-4" />
          </svg>
        }
        footer={
          <>
            <button
              className="btn btn-ghost"
              onClick={() => setModalMov(false)}
              disabled={savingMov}
            >
              Cancelar
            </button>
            <button
              className="btn btn-primary"
              onClick={handleCreateMov}
              disabled={savingMov}
            >
              {savingMov ? "Creando..." : "Crear y agregar detalles →"}
            </button>
          </>
        }
      >
        <div className="info-box">
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <circle cx="12" cy="12" r="10" />
            <path d="M12 8v4m0 4h.01" />
          </svg>
          <span>
            Al crear el movimiento, podrás agregar las líneas de detalle (qué
            objetos se movieron, desde dónde y hacia dónde).
          </span>
        </div>
        <div className="form-grid-2">
          <FloatingInput
            id="mfecha"
            label="Fecha del movimiento *"
            type="date"
            value={formMov.fecha_movimiento}
            onChange={(e) =>
              setFormMov((f) => ({ ...f, fecha_movimiento: e.target.value }))
            }
          />
          <div className="form-group">
            <label className="form-label-top">Tipo de movimiento *</label>
            <select
              className="form-select"
              value={formMov.id_tipo_movimiento}
              onChange={(e) =>
                setFormMov((f) => ({
                  ...f,
                  id_tipo_movimiento: e.target.value,
                }))
              }
            >
              {/* todo no esta trayendo bien tipo de movimiento */}
              <option value="">Seleccionar...</option>
              {tipos.map((t) => (
                <option key={t.id_tipo_movimiento} value={t.id_tipo_movimiento}>
                  {t.nombre}
                </option>
              ))}
            </select>
          </div>
        </div>
      </Modal>

      {/* Modal detalles del movimiento */}
      <Modal
        open={!!detailMov}
        onClose={() => setDetailMov(null)}
        size="modal-lg"
        title={`Movimiento #${detailMov?.id_movimiento} · ${detailMov ? nombreTipo(detailMov.id_tipo_movimiento) : ""}`}
        icon={
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        }
        footer={
          <button
            className="btn btn-primary"
            onClick={() => {
              setFormDet(EMPTY_DET);
              setModalDet(true);
            }}
          >
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
            Agregar línea de detalle
          </button>
        }
      >
        {detailMov && (
          <div
            style={{ display: "flex", gap: 24, fontSize: 13, marginBottom: 8 }}
          >
            <div>
              <span className="text-muted">Fecha:</span>{" "}
              <strong>{detailMov.fecha_movimiento}</strong>
            </div>
            <div>
              <span className="text-muted">Tipo:</span>{" "}
              <span className="badge badge-purple">
                {nombreTipo(detailMov.id_tipo_movimiento)}
              </span>
            </div>
          </div>
        )}
        <div className="divider" style={{ marginBottom: 12 }} />

        {loadingDet ? (
          <LoadingState text="Cargando detalles..." />
        ) : detalles.length === 0 ? (
          <EmptyState text="Sin líneas de detalle aún" />
        ) : (
          <table>
            <thead>
              <tr>
                <th>Objeto</th>
                <th>Origen</th>
                <th>Destino</th>
                <th>Cantidad</th>
                <th>Observaciones</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {detalles.map((d) => (
                <tr key={d.id_detalle_movimiento}>
                  <td className="td-main">{nombreObj(d.id_objeto)}</td>
                  <td className="text-muted">
                    {d.id_ubicacion_origen
                      ? nombreUbi(d.id_ubicacion_origen)
                      : "—"}
                  </td>
                  <td>{nombreUbi(d.id_ubicacion_destino)}</td>
                  <td>
                    <span
                      style={{
                        fontWeight: 700,
                        color: "var(--primary-purple)",
                      }}
                    >
                      {d.cantidad_afectada}
                    </span>
                  </td>
                  <td className="text-muted" style={{ fontSize: 12 }}>
                    {d.observaciones ?? "—"}
                  </td>
                  <td>
                    <button
                      className="btn btn-danger btn-icon"
                      onClick={() => setDelDetTarget(d)}
                    >
                      <svg
                        width="14"
                        height="14"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                      >
                        <polyline points="3 6 5 6 21 6" />
                        <path d="M19 6l-1 14H6L5 6" />
                      </svg>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </Modal>

      {/* Modal agregar detalle */}
      <Modal
        open={modalDet}
        onClose={() => setModalDet(false)}
        size="modal-lg"
        title="Nueva línea de detalle"
        icon={
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M12 5v14M5 12h14" />
          </svg>
        }
        footer={
          <>
            <button
              className="btn btn-ghost"
              onClick={() => setModalDet(false)}
              disabled={savingDet}
            >
              Cancelar
            </button>
            <button
              className="btn btn-primary"
              onClick={handleAddDetalle}
              disabled={savingDet}
            >
              {savingDet ? "Guardando..." : "Agregar línea"}
            </button>
          </>
        }
      >
        <div className="form-grid-2">
          <div className="form-group">
            <label className="form-label-top">Objeto *</label>
            <select
              className="form-select"
              value={formDet.id_objeto}
              onChange={set("id_objeto")}
            >
              <option value="">Seleccionar...</option>
              {objetos.map((o) => (
                <option key={o.id_objeto} value={o.id_objeto}>
                  {o.nombre}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label className="form-label-top">Item serializado</label>
            <select
              className="form-select"
              value={formDet.id_item_serializado}
              onChange={set("id_item_serializado")}
            >
              <option value="">Ninguno</option>
              {items
                .filter(
                  (i) =>
                    !formDet.id_objeto ||
                    i.id_objeto === Number(formDet.id_objeto),
                )
                .map((i) => (
                  <option
                    key={i.id_item_serializado}
                    value={i.id_item_serializado}
                  >
                    {i.placa_activo}
                  </option>
                ))}
            </select>
          </div>
        </div>

        <div className="form-grid-2">
          <div className="form-group">
            <label className="form-label-top">Ubicación origen</label>
            <select
              className="form-select"
              value={formDet.id_ubicacion_origen}
              onChange={set("id_ubicacion_origen")}
            >
              <option value="">Sin origen (nueva entrada)</option>
              {ubicaciones.map((u) => (
                <option key={u.id_ubicacion} value={u.id_ubicacion}>
                  {u.nombre}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label className="form-label-top">Ubicación destino *</label>
            <select
              className="form-select"
              value={formDet.id_ubicacion_destino}
              onChange={set("id_ubicacion_destino")}
            >
              <option value="">Seleccionar...</option>
              {ubicaciones.map((u) => (
                <option key={u.id_ubicacion} value={u.id_ubicacion}>
                  {u.nombre}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="form-grid-2">
          <FloatingInput
            id="ddet_cant"
            label="Cantidad afectada *"
            type="number"
            min="1"
            value={formDet.cantidad_afectada}
            onChange={set("cantidad_afectada")}
          />
          <FloatingInput
            id="ddet_obs"
            label="Observaciones"
            value={formDet.observaciones}
            onChange={set("observaciones")}
          />
        </div>
      </Modal>

      {/* Confirm delete detalle */}
      <ConfirmDialog
        open={!!delDetTarget}
        onClose={() => setDelDetTarget(null)}
        onConfirm={handleDeleteDetalle}
        loading={deletingDet}
        title="¿Eliminar esta línea de detalle?"
        message="Se eliminará el movimiento de este objeto de este registro."
      />

      {/* Confirm delete movimiento */}
      <ConfirmDialog
        open={!!delTarget}
        onClose={() => setDelTarget(null)}
        onConfirm={handleDeleteMov}
        loading={deleting}
        title={`¿Eliminar movimiento #${delTarget?.id_movimiento}?`}
        message="Se eliminarán también todas las líneas de detalle de este movimiento."
      />
    </div>
  );
}
