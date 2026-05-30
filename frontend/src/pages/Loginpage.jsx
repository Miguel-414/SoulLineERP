import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export default function LoginPage() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const bolitaRef = useRef(null);
  const { login } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    if (!form.username || !form.password) {
      setError("Completa todos los campos");
      return;
    }
    setError("");
    setLoading(true);

    // Animación bolita
    bolitaRef.current?.style.setProperty("--size", "140%");

    try {
      await login(form.username, form.password);
      navigate("/", { replace: true });
    } catch (err) {
      setError(err.message);
      bolitaRef.current?.style.setProperty("--size", "0");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-bolita" ref={bolitaRef} />

        <form className="login-form" onSubmit={handleSubmit}>
          <h1 className="login-title">Soul Line</h1>
          <p className="login-subtitle">Control de Inventario ERP</p>

          {error && (
            <div className="login-error">
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="8" x2="12" y2="12" />
                <line x1="12" y1="16" x2="12.01" y2="16" />
              </svg>
              {error}
            </div>
          )}

          <div className="login-input-group">
            <input
              className="login-input"
              type="text"
              id="username"
              placeholder=" "
              autoComplete="off"
              value={form.username}
              onChange={(e) =>
                setForm((f) => ({ ...f, username: e.target.value }))
              }
            />
            <label className="login-label" htmlFor="username">
              Usuario
            </label>
            <span className="login-input-icon">
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
              >
                <path d="M8 7a4 4 0 108 0 4 4 0 00-8 0M6 21v-2a4 4 0 014-4h4a4 4 0 014 4v2" />
              </svg>
            </span>
          </div>

          <div className="login-input-group">
            <input
              className="login-input"
              type="password"
              id="password"
              placeholder=" "
              autoComplete="off"
              value={form.password}
              onChange={(e) =>
                setForm((f) => ({ ...f, password: e.target.value }))
              }
            />
            <label className="login-label" htmlFor="password">
              Contraseña
            </label>
            <span className="login-input-icon">
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
              >
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                <path d="M7 11V7a5 5 0 0110 0v4" />
              </svg>
            </span>
          </div>

          <button className="btn-login" type="submit" disabled={loading}>
            {loading ? "Iniciando sesión..." : "Iniciar Sesión"}
          </button>
        </form>
      </div>
    </div>
  );
}
