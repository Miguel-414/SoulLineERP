# Proyecto de gestion de inventarios Soul Line

Aqui comienza el primer proyecto grande que voy a hacer aplicando arquitectura de capas uff tengo nervios ajja

```plaintext
control_inventario_api/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada de la aplicación
│   ├── core/                   # Configuraciones globales del sistema
│   │   ├── config.py           # Variables de entorno (.env) y constantes
│   │   ├── database.py         # Conexión a MySQL (SQLAlchemy session)
│   │   └── security.py         # Hashing de contraseñas y tokens JWT
│   │
│   ├── models/                 # Modelos de SQLAlchemy (Espejo de tu BD)
│   │   ├── base.py             # Clase Base declarativa
│   │   ├── inventario.py       # Objeto, ItemSerializado, ObjetoAcumulable, Inventario...
│   │   ├── financiero.py       # Factura, DetalleFactura, Proveedor...
│   │   ├── personal.py         # Persona, Responsables...
│   │   └── auth.py             # Usuario, Rol, Permiso, Auditoria...
│   │
│   ├── schemas/                # Validaciones Pydantic (DTOs de entrada/salida)
│   │   ├── inventario.py
│   │   ├── financiero.py
│   │   ├── personal.py
│   │   └── auth.py
│   │
│   ├── crud/                   # Lógica de acceso a datos (Queries)
│   │   ├── crud_inventario.py
│   │   ├── crud_financiero.py
│   │   └── crud_auth.py
│   │
│   └── api/                    # Capa de Endpoints (Rutas)
│       ├── deps.py             # Dependencias comunes (get_db, current_user)
│       └── v1/
│           ├── api.py          # Enrutador principal que une los sub-módulos
│           ├── endpoints/
│           │   ├── objetos.py
│           │   ├── facturas.py
│           │   ├── ubicaciones.py
│           │   └── auth.py
│           └── middlewares/    # Control de permisos por módulo/operación
│
├── .env                        # Variables secretas (DB_USER, DB_PASSWORD, SECRET_KEY)
├── .gitignore
├── requirements.txt            # Dependencias (fastapi, uvicorn, sqlalchemy, pymysql)
└── README.md
```
