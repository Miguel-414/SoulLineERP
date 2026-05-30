// components/ui.jsx — Componentes reutilizables

import { useEffect, useRef } from "react";

// ── Modal base ────────────────────────────────────────────────────────────

export function Modal({
  open,
  onClose,
  title,
  icon,
  children,
  size = "",
  footer,
}) {
  // Cerrar con Escape
  useEffect(() => {
    if (!open) return;
    const h = (e) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div
      className="modal-overlay"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div className={`modal-box ${size}`}>
        <div className="modal-header">
          <div className="modal-title">
            {icon}
            {title}
          </div>
          <button className="modal-close" onClick={onClose}>
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <path d="M18 6L6 18M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div className="modal-body">{children}</div>
        {footer && <div className="modal-footer">{footer}</div>}
      </div>
    </div>
  );
}

// ── Confirm dialog ────────────────────────────────────────────────────────

export function ConfirmDialog({
  open,
  onClose,
  onConfirm,
  title,
  message,
  loading,
}) {
  return (
    <Modal
      open={open}
      onClose={onClose}
      title=""
      footer={
        <>
          <button
            className="btn btn-ghost"
            onClick={onClose}
            disabled={loading}
          >
            Cancelar
          </button>
          <button
            className="btn btn-danger"
            onClick={onConfirm}
            disabled={loading}
          >
            {loading ? <Spinner size={16} /> : null}
            Eliminar
          </button>
        </>
      }
    >
      <div className="confirm-icon">
        <svg
          width="26"
          height="26"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6" />
        </svg>
      </div>
      <p className="confirm-title">{title ?? "¿Eliminar registro?"}</p>
      <p className="confirm-text">
        {message ?? "Esta acción no se puede deshacer."}
      </p>
    </Modal>
  );
}

// ── Floating label input ──────────────────────────────────────────────────

export function FloatingInput({ id, label, error, ...props }) {
  return (
    <div className="form-group">
      <input id={id} className="floating-input" placeholder=" " {...props} />
      <label className="floating-label" htmlFor={id}>
        {label}
      </label>
      {error && <p className="form-error">{error}</p>}
    </div>
  );
}

// ── Loading spinner ───────────────────────────────────────────────────────

export function Spinner({ size = 24 }) {
  return <div className="spinner" style={{ width: size, height: size }} />;
}

export function LoadingState({ text = "Cargando..." }) {
  return (
    <div className="loading-spinner">
      <Spinner />
      <span>{text}</span>
    </div>
  );
}

// ── Empty state ───────────────────────────────────────────────────────────

export function EmptyState({ text = "Sin registros", action }) {
  return (
    <div className="table-empty">
      <svg
        width="48"
        height="48"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="1"
        style={{ display: "block", margin: "0 auto 12px" }}
      >
        <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
      </svg>
      <p>{text}</p>
      {action && <div style={{ marginTop: 16 }}>{action}</div>}
    </div>
  );
}

// ── Badge de estado ───────────────────────────────────────────────────────

export function EstadoBadge({ value }) {
  const map = {
    OPERATIVO: "badge-green",
    FALLANDO: "badge-yellow",
    RETIRADO: "badge-red",
    BUENO: "badge-green",
    REGULAR: "badge-yellow",
    MALO: "badge-red",
    unico: "badge-purple",
    acumulable: "badge-pink",
  };
  return <span className={`badge ${map[value] ?? "badge-gray"}`}>{value}</span>;
}

// ── Search bar ────────────────────────────────────────────────────────────

export function SearchBar({ value, onChange, placeholder = "Buscar..." }) {
  return (
    <div className="table-search">
      <svg
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
      >
        <circle cx="11" cy="11" r="8" />
        <path d="m21 21-4.35-4.35" />
      </svg>
      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
      />
    </div>
  );
}
