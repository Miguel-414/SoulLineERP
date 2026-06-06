import { useState, useEffect } from "react";
import { facturasApi, proveedoresApi } from "../../services/api";
import { useToast } from "../../contexts/ToastContext";
import {
  Modal,
  ConfirmDialog,
  FloatingInput,
  LoadingState,
  EmptyState,
  SearchBar,
} from "../../components/Ui";

const EMPTY_FACTURA = {
  id_proveedor: "",
  fecha_generacion: "",
  total_bruto: "",
  iva: "0",
  valor_iva: "0",
  retencion_fuente: "0",
  descuento: "0",
  valor_total: "",
};

export default function FacturasPage() {
  const toast = useToast();
  const [facturas, setFacturas] = useState([]);
  const [provs, setProvs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [filterProv, setFilterProv] = useState("");
  const [modal, setModal] = useState(false);
  const [detailModal, setDetailModal] = useState(null); // factura seleccionada
  const [detalles, setDetalles] = useState([]);
  const [form, setForm] = useState(EMPTY_FACTURA);
  const [saving, setSaving] = useState(false);

  const load = () => {
    setLoading(true);
    Promise.all([
      facturasApi.listar(0, filterProv || undefined),
      proveedoresApi.listar(),
    ])
      .then(([fs, ps]) => {
        setFacturas(fs);
        setProvs(ps);
      })
      .catch(() => toast.error("Error al cargar facturas"))
      .finally(() => setLoading(false));
  };

  useEffect(load, [filterProv]);

  const nombreProv = (id) =>
    provs.find((p) => p.id_proveedor === id)?.razon_social ?? "—";

  const filtered = facturas.filter((f) => {
    const pn = nombreProv(f.id_proveedor).toLowerCase();
    return (
      pn.includes(search.toLowerCase()) || String(f.id_factura).includes(search)
    );
  });

  async function openDetail(f) {
    setDetailModal(f);
    try {
      const d = await facturasApi.detalles(f.id_factura);
      setDetalles(d);
    } catch {
      setDetalles([]);
    }
  }

  async function handleSave() {
    if (
      !form.id_proveedor ||
      !form.fecha_generacion ||
      !form.total_bruto ||
      !form.valor_total
    ) {
      toast.warning("Proveedor, fecha, total bruto y total son obligatorios");
      return;
    }
    setSaving(true);
    try {
      await facturasApi.crear({
        ...form,
        id_proveedor: Number(form.id_proveedor),
        total_bruto: parseFloat(form.total_bruto),
        iva: parseFloat(form.iva) || 0,
        valor_iva: parseFloat(form.valor_iva) || 0,
        retencion_fuente: parseFloat(form.retencion_fuente) || 0,
        descuento: parseFloat(form.descuento) || 0,
        valor_total: parseFloat(form.valor_total),
      });
      toast.success("Factura registrada");
      setModal(false);
      load();
    } catch (err) {
      toast.error(err.message);
    } finally {
      setSaving(false);
    }
  }

  const fmt = (v) =>
    Number(v ?? 0).toLocaleString("es-CO", {
      style: "currency",
      currency: "COP",
      maximumFractionDigits: 0,
    });

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1 className="page-title">Facturas</h1>
          <p className="page-subtitle">
            Registro de compras y documentos financieros
          </p>
        </div>
        <button
          className="btn btn-primary"
          onClick={() => {
            setForm(EMPTY_FACTURA);
            setModal(true);
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
          Nueva factura
        </button>
      </div>

      <div className="table-card">
        <div className="table-toolbar">
          <SearchBar
            value={search}
            onChange={setSearch}
            placeholder="Buscar por proveedor, #..."
          />
          <select
            className="form-select"
            style={{ width: "auto", minWidth: 180 }}
            value={filterProv}
            onChange={(e) => setFilterProv(e.target.value)}
          >
            <option value="">Todos los proveedores</option>
            {provs.map((p) => (
              <option key={p.id_proveedor} value={p.id_proveedor}>
                {p.razon_social}
              </option>
            ))}
          </select>
        </div>
        {loading ? (
          <LoadingState />
        ) : (
          <div className="table-wrapper">
            {filtered.length === 0 ? (
              <EmptyState text="No hay facturas registradas" />
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Proveedor</th>
                    <th>Fecha</th>
                    <th>Total Bruto</th>
                    <th>IVA</th>
                    <th>Valor Total</th>
                    <th>Ver</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((f) => (
                    <tr key={f.id_factura}>
                      <td className="text-muted">#{f.id_factura}</td>
                      <td className="td-main">{nombreProv(f.id_proveedor)}</td>
                      <td>
                        {new Date(f.fecha_generacion).toLocaleDateString(
                          "es-CO",
                        )}
                      </td>
                      <td>{fmt(f.total_bruto)}</td>
                      <td>{f.iva ?? 0}%</td>
                      <td style={{ color: "var(--success)", fontWeight: 600 }}>
                        {fmt(f.valor_total)}
                      </td>
                      <td>
                        <button
                          className="btn btn-secondary btn-icon"
                          onClick={() => openDetail(f)}
                          title="Ver detalles"
                        >
                          <svg
                            width="15"
                            height="15"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                          >
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                            <circle cx="12" cy="12" r="3" />
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

      {/* Modal crear */}
      <Modal
        open={modal}
        onClose={() => setModal(false)}
        title="Nueva factura"
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
            <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
            <polyline points="14 2 14 8 20 8" />
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
              {saving ? "Guardando..." : "Registrar factura"}
            </button>
          </>
        }
      >
        <div className="form-grid-2">
          <div className="form-group">
            <label className="form-label-top">Proveedor *</label>
            <select
              className="form-select"
              value={form.id_proveedor}
              onChange={(e) =>
                setForm((f) => ({ ...f, id_proveedor: e.target.value }))
              }
            >
              <option value="">Seleccionar...</option>
              {provs.map((p) => (
                <option key={p.id_proveedor} value={p.id_proveedor}>
                  {p.razon_social}
                </option>
              ))}
            </select>
          </div>
          <FloatingInput
            id="ffech"
            label="Fecha de generación *"
            type="datetime-local"
            value={form.fecha_generacion}
            onChange={(e) =>
              setForm((f) => ({ ...f, fecha_generacion: e.target.value }))
            }
          />
        </div>
        <div className="form-grid-3">
          <FloatingInput
            id="ftb"
            label="Total bruto *"
            type="number"
            value={form.total_bruto}
            onChange={(e) =>
              setForm((f) => ({ ...f, total_bruto: e.target.value }))
            }
          />
          <FloatingInput
            id="fiva"
            label="IVA %"
            type="number"
            value={form.iva}
            onChange={(e) => setForm((f) => ({ ...f, iva: e.target.value }))}
          />
          <FloatingInput
            id="fviva"
            label="Valor IVA"
            type="number"
            value={form.valor_iva}
            onChange={(e) =>
              setForm((f) => ({ ...f, valor_iva: e.target.value }))
            }
          />
        </div>
        <div className="form-grid-3">
          <FloatingInput
            id="fret"
            label="Retención fuente"
            type="number"
            value={form.retencion_fuente}
            onChange={(e) =>
              setForm((f) => ({ ...f, retencion_fuente: e.target.value }))
            }
          />
          <FloatingInput
            id="fdesc"
            label="Descuento"
            type="number"
            value={form.descuento}
            onChange={(e) =>
              setForm((f) => ({ ...f, descuento: e.target.value }))
            }
          />
          <FloatingInput
            id="fvt"
            label="Valor total *"
            type="number"
            value={form.valor_total}
            onChange={(e) =>
              setForm((f) => ({ ...f, valor_total: e.target.value }))
            }
          />
        </div>
      </Modal>

      {/* Modal detalles */}
      <Modal
        open={!!detailModal}
        onClose={() => setDetailModal(null)}
        title={`Factura #${detailModal?.id_factura}`}
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
            <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
            <polyline points="14 2 14 8 20 8" />
            <line x1="16" y1="13" x2="8" y2="13" />
            <line x1="16" y1="17" x2="8" y2="17" />
          </svg>
        }
      >
        {detailModal && (
          <>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 1fr",
                gap: 12,
                padding: "0 0 8px",
              }}
            >
              <div>
                <p className="text-muted" style={{ fontSize: 12 }}>
                  Proveedor
                </p>
                <p className="td-main">
                  {nombreProv(detailModal.id_proveedor)}
                </p>
              </div>
              <div>
                <p className="text-muted" style={{ fontSize: 12 }}>
                  Fecha
                </p>
                <p>
                  {new Date(detailModal.fecha_generacion).toLocaleDateString(
                    "es-CO",
                  )}
                </p>
              </div>
              <div>
                <p className="text-muted" style={{ fontSize: 12 }}>
                  Total Bruto
                </p>
                <p>{fmt(detailModal.total_bruto)}</p>
              </div>
              <div>
                <p className="text-muted" style={{ fontSize: 12 }}>
                  Valor Total
                </p>
                <p style={{ color: "var(--success)", fontWeight: 600 }}>
                  {fmt(detailModal.valor_total)}
                </p>
              </div>
            </div>
            <div className="divider" />
            <p
              style={{
                fontSize: 12,
                color: "var(--text-gray)",
                marginBottom: 10,
                textTransform: "uppercase",
                letterSpacing: 1,
              }}
            >
              Líneas de detalle
            </p>
            {detalles.length === 0 ? (
              <p className="text-muted" style={{ fontSize: 14 }}>
                Esta factura no tiene líneas de detalle registradas.
              </p>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>Descripción</th>
                    <th>Cant.</th>
                    <th>P. Unitario</th>
                    <th>Total</th>
                  </tr>
                </thead>
                <tbody>
                  {detalles.map((d) => (
                    <tr key={d.id_detalle_factura}>
                      <td>{d.descripcion_factura}</td>
                      <td>{d.cantidad}</td>
                      <td>{fmt(d.precio_unitario)}</td>
                      <td style={{ color: "var(--success)" }}>
                        {fmt(d.valor_total)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </>
        )}
      </Modal>
    </div>
  );
}
