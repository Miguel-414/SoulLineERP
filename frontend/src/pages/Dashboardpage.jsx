import { useEffect, useState } from "react";
import { useAuth } from "../contexts/AuthContext";
import {
  objetosApi,
  ubicacionesApi,
  personasApi,
  proveedoresApi,
} from "../services/api";
import { LoadingState } from "../components/Ui";

export default function DashboardPage() {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.allSettled([
      objetosApi.listar(0),
      ubicacionesApi.listar(0),
      personasApi.listar(0),
      proveedoresApi.listar(0),
    ]).then(([obj, ub, per, prov]) => {
      setStats({
        objetos: obj.status === "fulfilled" ? (obj.value?.length ?? 0) : "—",
        ubicaciones: ub.status === "fulfilled" ? (ub.value?.length ?? 0) : "—",
        personas: per.status === "fulfilled" ? (per.value?.length ?? 0) : "—",
        proveedores:
          prov.status === "fulfilled" ? (prov.value?.length ?? 0) : "—",
      });
      setLoading(false);
    });
  }, []);

  const hour = new Date().getHours();
  const greeting =
    hour < 12 ? "Buenos días" : hour < 19 ? "Buenas tardes" : "Buenas noches";

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1 className="page-title">
            {greeting}, {user?.nombre_usuario} 👋
          </h1>
          <p className="page-subtitle">
            Bienvenido al panel de control de Soul Line ERP
          </p>
        </div>
      </div>

      {loading ? (
        <LoadingState />
      ) : (
        <div className="stats-grid">
          <StatCard
            label="Objetos registrados"
            value={stats.objetos}
            color="#a855f7"
            icon={<IconBox />}
          />
          <StatCard
            label="Ubicaciones"
            value={stats.ubicaciones}
            color="#ec4899"
            icon={<IconMapPin />}
          />
          <StatCard
            label="Personas"
            value={stats.personas}
            color="#06b6d4"
            icon={<IconUser />}
          />
          <StatCard
            label="Proveedores"
            value={stats.proveedores}
            color="#22c55e"
            icon={<IconTruck />}
          />
        </div>
      )}

      <div className="info-box" style={{ marginTop: 8 }}>
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
          Usa el menú lateral para navegar entre los módulos. Puedes colapsar la
          barra lateral con el botón de la esquina superior para tener más
          espacio.
        </span>
      </div>
    </div>
  );
}

function StatCard({ label, value, color, icon }) {
  return (
    <div className="stat-card">
      <div className="stat-icon" style={{ background: `${color}22`, color }}>
        {icon}
      </div>
      <p className="stat-value">{value}</p>
      <p className="stat-label">{label}</p>
    </div>
  );
}

function IconBox() {
  return (
    <svg
      width="22"
      height="22"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
    >
      <path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z" />
      <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
      <line x1="12" y1="22.08" x2="12" y2="12" />
    </svg>
  );
}
function IconMapPin() {
  return (
    <svg
      width="22"
      height="22"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
    >
      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z" />
      <circle cx="12" cy="10" r="3" />
    </svg>
  );
}
function IconUser() {
  return (
    <svg
      width="22"
      height="22"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
    >
      <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />
      <circle cx="12" cy="7" r="4" />
    </svg>
  );
}
function IconTruck() {
  return (
    <svg
      width="22"
      height="22"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
    >
      <rect x="1" y="3" width="15" height="13" />
      <polygon points="16 8 20 8 23 11 23 16 16 16 16 8" />
      <circle cx="5.5" cy="18.5" r="2.5" />
      <circle cx="18.5" cy="18.5" r="2.5" />
    </svg>
  );
}
