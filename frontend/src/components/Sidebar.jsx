import { useState } from "react";
import { NavLink, useLocation } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

const MENU = [
  {
    label: "Inventario",
    icon: <IconBox />,
    children: [
      { label: "Gestionar Inventario", path: "/inventario" },
      { label: "Items Serializados", path: "/items" },
      { label: "Objetos", path: "/objetos" },
      { label: "Tipos de Activo", path: "/tipos-activo" },
      { label: "Ubicaciones", path: "/ubicaciones" },
    ],
  },
  {
    label: "Movimientos",
    // icon: <IconArrowsLeftRight />,
    icon: <IconReceipt />,
    children: [
      { label: "Historial Movimientos", path: "/movimientos" },
      { label: "Tipos de Movimiento", path: "/tipos-movimiento" },
    ],
  },
  {
    label: "Finanzas",
    icon: <IconReceipt />,
    children: [
      { label: "Facturas", path: "/facturas" },
      { label: "Proveedores", path: "/proveedores" },
    ],
  },
  {
    label: "Personal y Seguridad",
    icon: <IconUsers />,
    children: [
      { label: "Personas", path: "/personas" },
      { label: "Usuarios", path: "/usuarios" },
      { label: "Roles", path: "/roles" },
    ],
  },
];

export default function Sidebar({ collapsed, onToggle }) {
  const location = useLocation();
  const { user, logout } = useAuth();

  // Determina qué sección está abierta basándose en la ruta activa
  const activeSection = MENU.findIndex((s) =>
    s.children?.some((c) => location.pathname.startsWith(c.path)),
  );
  const [openIdx, setOpenIdx] = useState(
    activeSection >= 0 ? activeSection : 0,
  );

  const initials = user?.nombre_usuario?.slice(0, 2).toUpperCase() ?? "SL";

  return (
    <aside className={`sidebar ${collapsed ? "collapsed" : ""}`}>
      {/* Header */}
      <div className="sidebar-header">
        <span className="sidebar-logo">Soul Line</span>
        <button
          className="sidebar-toggle"
          onClick={onToggle}
          title="Colapsar menú"
        >
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M15 18l-6-6 6-6" />
          </svg>
        </button>
      </div>

      {/* Nav */}
      <nav style={{ flex: 1, overflow: "hidden" }}>
        {!collapsed && <p className="sidebar-section-label">Navegación</p>}

        {MENU.map((section, idx) => {
          const isOpen = openIdx === idx;
          const hasActive = section.children?.some((c) =>
            location.pathname.startsWith(c.path),
          );

          return (
            <div className="menu-item" key={section.label}>
              <div
                className={`menu-item-header ${hasActive ? "active" : ""}`}
                onClick={() => {
                  if (collapsed) return;
                  setOpenIdx(isOpen ? -1 : idx);
                }}
              >
                <span className="menu-link" style={{ cursor: "pointer" }}>
                  {section.icon}
                  <span className="menu-link-label">{section.label}</span>
                </span>
                {!collapsed && (
                  <button
                    className={`menu-chevron ${isOpen ? "open" : ""}`}
                    onClick={(e) => {
                      e.stopPropagation();
                      setOpenIdx(isOpen ? -1 : idx);
                    }}
                  >
                    <svg
                      width="14"
                      height="14"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2.5"
                    >
                      <path d="M6 9l6 6 6-6" />
                    </svg>
                  </button>
                )}
              </div>

              {/* Submenú — normal cuando expandido */}
              {!collapsed && (
                <div className={`submenu ${isOpen ? "open" : ""}`}>
                  <div className="submenu-inner">
                    {section.children.map((child) => (
                      <NavLink
                        key={child.path}
                        to={child.path}
                        className={({ isActive }) =>
                          `submenu-item ${isActive ? "active" : ""}`
                        }
                      >
                        {child.label}
                      </NavLink>
                    ))}
                  </div>
                </div>
              )}

              {/* Submenú — flotante cuando colapsado */}
              {collapsed && (
                <div className="submenu-collapsed-popup">
                  {section.children.map((child) => (
                    <NavLink
                      key={child.path}
                      to={child.path}
                      className={({ isActive }) =>
                        `submenu-item ${isActive ? "active" : ""}`
                      }
                    >
                      {child.label}
                    </NavLink>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="sidebar-footer">
        <div className="sidebar-user">
          <div className="sidebar-avatar">{initials}</div>
          <div className="sidebar-user-info">
            <p className="sidebar-user-name">{user?.nombre_usuario}</p>
            <p className="sidebar-user-role">Usuario</p>
          </div>
          <button className="btn-logout" onClick={logout} title="Cerrar sesión">
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9" />
            </svg>
          </button>
        </div>
      </div>
    </aside>
  );
}

// ── Iconos inline (SVG) ───────────────────────────────────────────────────
function IconBox() {
  return (
    <svg
      width="18"
      height="18"
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
function IconReceipt() {
  return (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
    >
      <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
      <polyline points="14 2 14 8 20 8" />
      <line x1="16" y1="13" x2="8" y2="13" />
      <line x1="16" y1="17" x2="8" y2="17" />
    </svg>
  );
}
function IconUsers() {
  return (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
    >
      <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" />
      <circle cx="9" cy="7" r="4" />
      <path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75" />
    </svg>
  );
}
