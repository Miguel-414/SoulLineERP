# Soul Line

Soul Line es un sistema ERP diseñado con el fin de controlar el manejo de inventarios y el flujo de vida de los objetos, desde que llegan a la institución del cliente hasta que son dados de baja. Soul Line contempla los siguientes objetos:

- **Objetos serializados:** Son aquellos que reciben un ID único que los identifica físicamente (seriales, códigos de barras, etc.).
- **Objetos acumulables:** Estos objetos no son reconocibles individualmente. En su lugar, la forma de diferenciarlos es por su factura. Por ejemplo: 7 llantas llegaron el viernes y pertenecen a la factura X, pero otras 7 llantas llegaron el lunes con otra factura.

Soul Line contempla el histórico de los objetos y cómo su situación o estado puede cambiar a lo largo del tiempo.

# Cómo construirlo usted mismo

El proyecto **Soul Line** está estructurado con un backend desarrollado en Python utilizando FastAPI y una base de datos MySQL (gestionada a través de XAMPP). El frontend está construido con React, JavaScript y Vite.

## Configuración del Entorno (`.env`)

Antes de iniciar los servicios, es obligatorio configurar las variables de entorno. Dentro de la carpeta `backend`, encontrará un archivo llamado `.env.example`.

Deberá crear una copia de ese archivo, renombrarla como `.env` y ajustar los valores según su configuración local dentro de la carpeta `backend`.

## Gestión de la Base de Datos

Para levantar la base de datos, dispone de las siguientes dos opciones:

1. **Despliegue automático (Recomendado):** Por defecto, la base de datos se crea e inicializa automáticamente al iniciar la API. El sistema toma el nombre asignado en la variable `DB_NAME` dentro del archivo `.env` y ejecuta el script SQL ubicado en `backend/app/core/database/scripts/control_inventario.sql`.

   > **Nota técnica:** Se optó por este método para garantizar la integridad de la estructura relacional directamente en MySQL, evitando el uso de las herramientas nativas de SQLAlchemy debido a irregularidades detectadas durante el mapeo automático.

2. **Despliegue manual:** Si prefiere levantar la base de datos por su cuenta, puede copiar el contenido del script ubicado en `backend/app/core/database/scripts/control_inventario.sql` y ejecutarlo directamente en su gestor de MySQL.

   _Importante:_ Si elige esta opción, deberá mantener el nombre nativo de la base de datos (`control_inventario`), de lo contrario tendrá que reemplazar manualmente cada referencia a ese nombre dentro del script. Si utiliza el despliegue automático, puede asignarle cualquier nombre en el archivo `.env`.

## Inicialización de los Servicios (en Windows)

Siga estos pasos para ejecutar tanto la API como el frontend en su entorno local:

### 1. Configuración del Backend

Abra una terminal en la raíz del proyecto y ejecute los siguientes comandos:

```bash
# Desplazarse al directorio del backend
cd .\backend\

# Crear el entorno virtual
python -m venv ./env

# Activar el entorno virtual
.\env\Scripts\activate

# Instalar las dependencias del sistema
pip install -r requirements.txt

# Iniciar el servidor de desarrollo de FastAPI
uvicorn app.main:app --reload
```

### 2. Configuración del Frontend

Abra una **segunda terminal** en la raíz del proyecto y ejecute los siguientes comandos:

```bash
# Desplazarse al directorio del frontend
cd .\frontend\

# Instalar las dependencias de Node
npm install

# Iniciar el servidor de desarrollo de Vite
npm run dev
```

Una vez completados estos pasos, el proyecto estará en funcionamiento y podrá acceder a él a través de las direcciones locales que se muestren en sus respectivas terminales.
