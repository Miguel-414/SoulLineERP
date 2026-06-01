import { useState, useEffect } from "react";
import { personasApi, ubicacionesApi } from "../../services/api";
import { useToast } from "../../contexts/ToastContext";
import {
  Modal,
  ConfirmDialog,
  FloatingInput,
  LoadingState,
  EmptyState,
  SearchBar,
} from "../../components/ui";

const EMPTY_P = {
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
  const [ubicaciones, setUbicaciones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [modal, setModal] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(EMPTY_P);
  const [saving, setSaving] = useState(false);
  const [delTarget, setDelTarget] = useState(null);
  const [deleting, setDeleting] = useState(false);
  const [respModal, setRespModal] = useState(null);
  const [respTab, setRespTab] = useState("objeto");
  const [respObjetos, setRespObjetos] = useState([]);
  const [respUbics, setRespUbics] = useState([]);
  const [loadingResp, setLoadingResp] = useState(false);
  const [modalAddResp, setModalAddResp] = useState(false);
  const [formResp, setFormResp] = useState({
    id_inventario: "",
    id_ubicacion: "",
    fecha_inicio: "",
    fecha_fin: "",
  });
  const [savingResp, setSavingResp] = useState(false);
  const [delRespTarget, setDelRespTarget] = useState(null);
  const [deletingResp, setDeletingResp] = useState(false);

  const load = () => {
    setLoading(true);
    Promise.all([personasApi.listar(), ubicacionesApi.listar()])
      .then(([ps, ubs]) => {
        setItems(ps);
        setUbicaciones(ubs);
      })
      .catch(() => toast.error("Error al cargar personas"))
      .finally(() => setLoading(false));
  };
  useEffect(load, []);

  const filtered = items.filter((i) =>
    [i.nombre, i.email, i.primer_apellido].some((v) =>
      v?.toLowerCase().includes(search.toLowerCase()),
    ),
  );
  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));

  function openCreate() {
    setEditing(null);
    setForm(EMPTY_P);
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

  async function openResp(p) {
    setRespModal(p);
    setRespTab("objeto");
    setLoadingResp(true);
    try {
      const [ro, ru] = await Promise.all([
        personasApi.listarRespObj(p.id_persona),
        personasApi.listarRespUbi(p.id_persona),
      ]);
      setRespObjetos(ro);
      setRespUbics(ru);
    } catch {
      toast.error("Error al cargar responsabilidades");
    } finally {
      setLoadingResp(false);
    }
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

  async function handleAddResp() {
    if (!formResp.fecha_inicio) {
      toast.warning("La fecha de inicio es obligatoria");
      return;
    }
    if (respTab === "objeto" && !formResp.id_inventario) {
      toast.warning("Indica el ID del inventario");
      return;
    }
    if (respTab === "ubicacion" && !formResp.id_ubicacion) {
      toast.warning("Selecciona una ubicación");
      return;
    }
    setSavingResp(true);
    try {
      if (respTab === "objeto") {
        const r = await personasApi.crearRespObj(respModal.id_persona, {
          id_inventario: Number(formResp.id_inventario),
          id_persona: respModal.id_persona,
          fecha_inicio: formResp.fecha_inicio,
          fecha_fin: formResp.fecha_fin || null,
        });
        setRespObjetos((rs) => [...rs, r]);
      } else {
        const r = await personasApi.crearRespUbi(respModal.id_persona, {
          id_ubicacion: Number(formResp.id_ubicacion),
          id_persona: respModal.id_persona,
          fecha_inicio: formResp.fecha_inicio,
          fecha_fin: formResp.fecha_fin || null,
        });
        setRespUbics((rs) => [...rs, r]);
      }
      toast.success("Responsabilidad asignada");
      setModalAddResp(false);
      setFormResp({
        id_inventario: "",
        id_ubicacion: "",
        fecha_inicio: "",
        fecha_fin: "",
      });
    } catch (err) {
      toast.error(err.message);
    } finally {
      setSavingResp(false);
    }
  }

  async function handleDeleteResp() {
    setDeletingResp(true);
    try {
      if (respTab === "objeto") {
        await personasApi.eliminarRespObj(delRespTarget.id_responsable_objeto);
        setRespObjetos((rs) =>
          rs.filter(
            (r) =>
              r.id_responsable_objeto !== delRespTarget.id_responsable_objeto,
          ),
        );
      } else {
        await personasApi.eliminarRespUbi(
          delRespTarget.id_responsable_ubicacion,
        );
        setRespUbics((rs) =>
          rs.filter(
            (r) =>
              r.id_responsable_ubicacion !==
              delRespTarget.id_responsable_ubicacion,
          ),
        );
      }
      toast.success("Responsabilidad eliminada");
      setDelRespTarget(null);
    } catch (err) {
      toast.error(err.message);
    } finally {
      setDeletingResp(false);
    }
  }

  const nombreUbi = (id) =>
    ubicaciones.find((u) => u.id_ubicacion === id)?.nombre ?? `Ub. #${id}`;

  const TabBtn = ({ tab, label, count }) => (
    <button
      onClick={() => setRespTab(tab)}
      style={{
        padding: "8px 16px",
        background: "none",
        border: "none",
        cursor: "pointer",
        fontSize: 14,
        fontWeight: 600,
        color: respTab === tab ? "var(--primary-purple)" : "var(--text-gray)",
        borderBottom:
          respTab === tab
            ? "2px solid var(--primary-purple)"
            : "2px solid transparent",
        transition: "all 0.2s",
      }}
    >
      {label} ({count})
    </button>
  );

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
                    <th>Nombre</th>
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
                      <td className="text-muted" style={{ fontSize: 13 }}>
                        {p.direccion}
                      </td>
                      <td>
                        <div style={{ display: "flex", gap: 6 }}>
                          <button
                            className="btn btn-secondary btn-icon"
                            onClick={() => openResp(p)}
                            title="Responsabilidades"
                          >
                            <svg
                              width="15"
                              height="15"
                              viewBox="0 0 24 24"
                              fill="none"
                              stroke="currentColor"
                              strokeWidth="2"
                            >
                              <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" />
                              <circle cx="9" cy="7" r="4" />
                              <path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75" />
                            </svg>
                          </button>
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
        size="modal-lg"
        title={editing ? "Editar persona" : "Nueva persona"}
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

      <Modal
        open={!!respModal}
        onClose={() => setRespModal(null)}
        size="modal-lg"
        title={`Responsabilidades — ${respModal?.nombre}`}
        icon={
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" />
            <circle cx="9" cy="7" r="4" />
            <path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75" />
          </svg>
        }
        footer={
          <button
            className="btn btn-primary"
            onClick={() => {
              setFormResp({
                id_inventario: "",
                id_ubicacion: "",
                fecha_inicio: "",
                fecha_fin: "",
              });
              setModalAddResp(true);
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
            </svg>{" "}
            Asignar responsabilidad
          </button>
        }
      >
        <div
          style={{
            display: "flex",
            gap: 0,
            borderBottom: "1px solid var(--border-color)",
            marginBottom: 16,
          }}
        >
          <TabBtn tab="objeto" label="Objetos" count={respObjetos.length} />
          <TabBtn
            tab="ubicacion"
            label="Ubicaciones"
            count={respUbics.length}
          />
        </div>
        {loadingResp ? (
          <LoadingState />
        ) : respTab === "objeto" ? (
          respObjetos.length === 0 ? (
            <EmptyState text="Sin responsabilidades de objetos" />
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Inventario #</th>
                  <th>Inicio</th>
                  <th>Fin</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {respObjetos.map((r) => (
                  <tr key={r.id_responsable_objeto}>
                    <td className="td-main">#{r.id_inventario}</td>
                    <td>{r.fecha_inicio}</td>
                    <td>
                      {r.fecha_fin ?? (
                        <span
                          className="badge badge-green"
                          style={{ fontSize: 11 }}
                        >
                          Activo
                        </span>
                      )}
                    </td>
                    <td>
                      <button
                        className="btn btn-danger btn-icon"
                        onClick={() => {
                          setRespTab("objeto");
                          setDelRespTarget(r);
                        }}
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
          )
        ) : respUbics.length === 0 ? (
          <EmptyState text="Sin responsabilidades de ubicaciones" />
        ) : (
          <table>
            <thead>
              <tr>
                <th>Ubicación</th>
                <th>Inicio</th>
                <th>Fin</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {respUbics.map((r) => (
                <tr key={r.id_responsable_ubicacion}>
                  <td className="td-main">{nombreUbi(r.id_ubicacion)}</td>
                  <td>{r.fecha_inicio}</td>
                  <td>
                    {r.fecha_fin ?? (
                      <span
                        className="badge badge-green"
                        style={{ fontSize: 11 }}
                      >
                        Activo
                      </span>
                    )}
                  </td>
                  <td>
                    <button
                      className="btn btn-danger btn-icon"
                      onClick={() => {
                        setRespTab("ubicacion");
                        setDelRespTarget(r);
                      }}
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

      <Modal
        open={modalAddResp}
        onClose={() => setModalAddResp(false)}
        title="Asignar responsabilidad"
        footer={
          <>
            <button
              className="btn btn-ghost"
              onClick={() => setModalAddResp(false)}
              disabled={savingResp}
            >
              Cancelar
            </button>
            <button
              className="btn btn-primary"
              onClick={handleAddResp}
              disabled={savingResp}
            >
              {savingResp ? "Asignando..." : "Asignar"}
            </button>
          </>
        }
      >
        <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
          {["objeto", "ubicacion"].map((tab) => (
            <button
              key={tab}
              onClick={() => setRespTab(tab)}
              className={`btn ${respTab === tab ? "btn-primary" : "btn-ghost"}`}
              style={{ fontSize: 13 }}
            >
              {tab === "objeto"
                ? "Responsable de objeto"
                : "Responsable de ubicación"}
            </button>
          ))}
        </div>
        {respTab === "objeto" ? (
          <div className="form-group">
            <label className="form-label-top">
              ID del registro de inventario *
            </label>
            <input
              className="floating-input"
              type="number"
              placeholder="Ej: 1"
              value={formResp.id_inventario}
              onChange={(e) =>
                setFormResp((f) => ({ ...f, id_inventario: e.target.value }))
              }
            />
            <p
              style={{ fontSize: 12, color: "var(--text-gray)", marginTop: 6 }}
            >
              Consulta los IDs en el módulo Inventario
            </p>
          </div>
        ) : (
          <div className="form-group">
            <label className="form-label-top">Ubicación *</label>
            <select
              className="form-select"
              value={formResp.id_ubicacion}
              onChange={(e) =>
                setFormResp((f) => ({ ...f, id_ubicacion: e.target.value }))
              }
            >
              <option value="">Seleccionar...</option>
              {ubicaciones.map((u) => (
                <option key={u.id_ubicacion} value={u.id_ubicacion}>
                  {u.nombre}
                </option>
              ))}
            </select>
          </div>
        )}
        <div className="form-grid-2" style={{ marginTop: 8 }}>
          <FloatingInput
            id="rfin"
            label="Fecha inicio *"
            type="date"
            value={formResp.fecha_inicio}
            onChange={(e) =>
              setFormResp((f) => ({ ...f, fecha_inicio: e.target.value }))
            }
          />
          <FloatingInput
            id="rfin2"
            label="Fecha fin (opcional)"
            type="date"
            value={formResp.fecha_fin}
            onChange={(e) =>
              setFormResp((f) => ({ ...f, fecha_fin: e.target.value }))
            }
          />
        </div>
      </Modal>

      <ConfirmDialog
        open={!!delTarget}
        onClose={() => setDelTarget(null)}
        onConfirm={handleDelete}
        loading={deleting}
        title={`¿Eliminar a "${delTarget?.nombre}"?`}
        message="Si la persona tiene un usuario asociado, este también será eliminado."
      />
      <ConfirmDialog
        open={!!delRespTarget}
        onClose={() => setDelRespTarget(null)}
        onConfirm={handleDeleteResp}
        loading={deletingResp}
        title="¿Eliminar esta responsabilidad?"
        message="Se quitará la asignación de esta persona."
      />
    </div>
  );
}
