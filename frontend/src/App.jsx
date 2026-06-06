import { useState } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import { ToastProvider } from "./contexts/ToastContext";
import Sidebar from "./components/Sidebar";

import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import ObjetosPage from "./pages/objetos/ObjetosPage";
import TiposActivoPage from "./pages/objetos/TiposActivoPage";
import UbicacionesPage from "./pages/inventario/UbicacionesPage";
import InventarioPage from "./pages/inventario/InventarioPage";
import ItemsPage from "./pages/inventario/ItemsPage";
import ProveedoresPage from "./pages/facturas/ProveedoresPage";
import FacturasPage from "./pages/facturas/FacturasPage";
import PersonasPage from "./pages/personas/PersonasPage";
import UsuariosPage from "./pages/personas/UsuariosPage";
import MovimientosPage from "./pages/movimientos/MovimientosPage";
import TiposMovimientoPage from "./pages/movimientos/TiposMovimientoPage";
import RolesPage from "./pages/admin/RolesPage";
// todo Corregir los nombres de los archivos para que se pueda correr comodamente en linux

// Ruta protegida: redirige al login si no hay sesión
function PrivateRoute({ children }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

// Layout con sidebar
function AppLayout() {
  const [collapsed, setCollapsed] = useState(true); // empieza colapsado (igual que el mockup)

  return (
    <div className="app-layout">
      <Sidebar collapsed={collapsed} onToggle={() => setCollapsed((c) => !c)} />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          {/* Sección Objetos */}
          <Route path="/objetos" element={<ObjetosPage />} />
          <Route path="/tipos-activo" element={<TiposActivoPage />} />

          {/* Sección Inventario */}
          <Route path="/inventario" element={<InventarioPage />} />
          <Route path="/items" element={<ItemsPage />} />
          <Route path="/ubicaciones" element={<UbicacionesPage />} />

          {/* Sección Movimientos */}
          <Route path="/movimientos" element={<MovimientosPage />} />
          <Route path="/tipos-movimiento" element={<TiposMovimientoPage />} />

          {/* Sección Finanzas */}
          <Route path="/facturas" element={<FacturasPage />} />
          <Route path="/proveedores" element={<ProveedoresPage />} />

          {/* Sección Personal/Admin */}
          <Route path="/personas" element={<PersonasPage />} />
          <Route path="/usuarios" element={<UsuariosPage />} />
          <Route path="/roles" element={<RolesPage />} />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <ToastProvider>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/*"
              element={
                <PrivateRoute>
                  <AppLayout />
                </PrivateRoute>
              }
            />
          </Routes>
        </ToastProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}
