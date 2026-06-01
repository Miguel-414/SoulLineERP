import { useState, useEffect } from "react";
import { ubicacionesApi, objetosApi } from "../../services/api";
import { useToast } from "../../contexts/ToastContext";
import {
  Modal,
  FloatingInput,
  LoadingState,
  EmptyState,
  EstadoBadge,
  SearchBar,
  ConfirmDialog,
} from "../../components/ui";

const EMPTY = {
  id_objeto: "",
  id_item_serializado: "",
  cantidad_actual: 1,
  id_ubicacion: "",
  estado_actual: "OPERATIVO",
  fecha_ultima_actualizacion: "",
};

export default function InventarioPage() {
  const toast = useToast();
  const [ubicaciones, setUbicaciones] = useState([]);
  const [objetos, setObjetos] = useState([]);
  const [items, setItems] = useState([]);
  const [selected, setSelected] = useState(""); // id_ubicacion filter
  const [inventario, setInventario] = useState([]);
  const [loadingInv, setLoadingInv] = useState(false);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [modal, setModal] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(EMPTY);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    Promise.all([
      ubicacionesApi.listar(),
      objetosApi.listar(),
      objetosApi.listarTodosItems(),
    ])
      .then(([ubs, obs, its]) => {
        setUbicaciones(ubs);
        setObjetos(obs);
        setItems(its);
        setLoading(false);
      })
      .catch(() => {
        toast.error("Error al cargar datos");
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    if (!selected) {
      setInventario([]);
      return;
    }
    setLoadingInv(true);
    ubicacionesApi
      .inventario(selected)
      .then(setInventario)
      .catch(() => toast.error("Error al cargar inventario"))
      .finally(() => setLoadingInv(false));
  }, [selected]);

  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));
  const nombreObjeto = (id) =>
    objetos.find((o) => o.id_objeto === id)?.nombre ?? `Obj. #${id}`;
  const nombreUbi = (id) =>
    ubicaciones.find((u) => u.id_ubicacion === id)?.nombre ?? `Ub. #${id}`;

  const filtered = inventario.filter((i) =>
    nombreObjeto(i.id_objeto).toLowerCase().includes(search.toLowerCase()),
  );

  function openCreate() {
    setEditing(null);
    setForm({
      ...EMPTY,
      id_ubicacion: selected,
      fecha_ultima_actualizacion: new Date().toISOString().slice(0, 16),
    });
    setModal(true);
  }
  function openEdit(inv) {
    setEditing(inv);
    setForm({
      id_objeto: inv.id_objeto,
      id_item_serializado: inv.id_item_serializado ?? "",
      cantidad_actual: inv.cantidad_actual,
      id_ubicacion: inv.id_ubicacion,
      estado_actual: inv.estado_actual,
      fecha_ultima_actualizacion:
        inv.fecha_ultima_actualizacion?.slice(0, 16) ?? "",
    });
    setModal(true);
  }

  async function handleSave() {
    if (!form.id_objeto || !form.id_ubicacion) {
      toast.warning("Objeto y ubicación son obligatorios");
      return;
    }
    setSaving(true);
    try {
      const payload = {
        ...form,
        id_objeto: Number(form.id_objeto),
        id_ubicacion: Number(form.id_ubicacion),
        cantidad_actual: Number(form.cantidad_actual),
        id_item_serializado: form.id_item_serializado
          ? Number(form.id_item_serializado)
          : null,
      };
      if (editing) {
        const { id_objeto, id_ubicacion_create, ...upd } = payload;
        await ubicacionesApi.actualizarInventario(editing.id_inventario, {
          cantidad_actual: upd.cantidad_actual,
          estado_actual: upd.estado_actual,
          fecha_ultima_actualizacion: upd.fecha_ultima_actualizacion,
        });
        toast.success("Inventario actualizado");
      } else {
        await ubicacionesApi.crearInventario(
          Number(form.id_ubicacion),
          payload,
        );
        toast.success("Registro creado");
      }
      setModal(false);
      setLoadingInv(true);
      ubicacionesApi
        .inventario(selected)
        .then(setInventario)
        .finally(() => setLoadingInv(false));
    } catch (err) {
      toast.error(err.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1 className="page-title">Inventario</h1>
          <p className="page-subtitle">Stock actual de objetos por ubicación</p>
        </div>
        {selected && (
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
            Agregar al inventario
          </button>
        )}
      </div>

      {/* Selector de ubicación */}
      <div className="table-card" style={{ padding: "16px 20px" }}>
        <p className="form-label-top" style={{ marginBottom: 8 }}>
          Selecciona una ubicación para ver su inventario
        </p>
        <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          {loading ? (
            <span className="text-muted">Cargando...</span>
          ) : (
            ubicaciones.map((u) => (
              <button
                key={u.id_ubicacion}
                className={`btn ${selected == u.id_ubicacion ? "btn-primary" : "btn-ghost"}`}
                onClick={() => setSelected(u.id_ubicacion)}
                style={{ fontSize: 13 }}
              >
                {u.id_zona_padre && "↳ "}
                {u.nombre}
              </button>
            ))
          )}
        </div>
      </div>

      {/* Tabla de inventario */}
      {selected && (
        <div className="table-card">
          <div className="table-toolbar">
            <SearchBar
              value={search}
              onChange={setSearch}
              placeholder="Buscar objeto..."
            />
            <span className="text-muted" style={{ fontSize: 13 }}>
              {nombreUbi(Number(selected))} · {filtered.length} registros
            </span>
          </div>

          {loadingInv ? (
            <LoadingState />
          ) : (
            <div className="table-wrapper">
              {filtered.length === 0 ? (
                <EmptyState
                  text="Sin registros en esta ubicación"
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
                      <th>Objeto</th>
                      <th>Item Serializado</th>
                      <th>Cantidad</th>
                      <th>Estado</th>
                      <th>Última actualización</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filtered.map((inv) => (
                      <tr key={inv.id_inventario}>
                        <td className="td-main">
                          {nombreObjeto(inv.id_objeto)}
                        </td>
                        <td className="text-muted">
                          {inv.id_item_serializado
                            ? `#${inv.id_item_serializado}`
                            : "—"}
                        </td>
                        <td>
                          <span
                            style={{
                              fontWeight: 700,
                              fontSize: 16,
                              color: "var(--primary-purple)",
                            }}
                          >
                            {inv.cantidad_actual}
                          </span>
                        </td>
                        <td>
                          <EstadoBadge value={inv.estado_actual} />
                        </td>
                        <td className="text-muted" style={{ fontSize: 12 }}>
                          {new Date(
                            inv.fecha_ultima_actualizacion,
                          ).toLocaleString("es-CO")}
                        </td>
                        <td>
                          <button
                            className="btn btn-ghost btn-icon"
                            onClick={() => openEdit(inv)}
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
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}
        </div>
      )}

      <Modal
        open={modal}
        onClose={() => setModal(false)}
        title={
          editing
            ? "Editar registro de inventario"
            : "Nuevo registro de inventario"
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
                  ? "Actualizar"
                  : "Crear registro"}
            </button>
          </>
        }
      >
        {!editing && (
          <div className="form-grid-2">
            <div className="form-group">
              <label className="form-label-top">Objeto *</label>
              <select
                className="form-select"
                value={form.id_objeto}
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
              <label className="form-label-top">Item Serializado</label>
              <select
                className="form-select"
                value={form.id_item_serializado}
                onChange={set("id_item_serializado")}
              >
                <option value="">Ninguno</option>
                {items
                  .filter(
                    (i) =>
                      !form.id_objeto || i.id_objeto === Number(form.id_objeto),
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
        )}

        <div className="form-grid-2">
          <FloatingInput
            id="invCant"
            label="Cantidad *"
            type="number"
            min="0"
            value={form.cantidad_actual}
            onChange={set("cantidad_actual")}
          />
          <div className="form-group">
            <label className="form-label-top">Estado</label>
            <select
              className="form-select"
              value={form.estado_actual}
              onChange={set("estado_actual")}
            >
              <option value="OPERATIVO">Operativo</option>
              <option value="FALLANDO">Fallando</option>
              <option value="RETIRADO">Retirado</option>
            </select>
          </div>
        </div>
        <FloatingInput
          id="invFecha"
          label="Fecha de actualización *"
          type="datetime-local"
          value={form.fecha_ultima_actualizacion}
          onChange={set("fecha_ultima_actualizacion")}
        />
      </Modal>
    </div>
  );
}
