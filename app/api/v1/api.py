from fastapi import APIRouter

from app.api.v1.endpoints import auth, facturas, objetos, ubicaciones

# Router principal de la versión 1 de la API.
# Cada sub-router se monta bajo un prefijo y recibe tags para la documentación.
api_router = APIRouter()
# todo el admin no puede manejar a los usuarios que existen en la base de datos, no se si aplicar esto sera demasiado
# ? crear ruta de personas para poder consultar crear, actualizar y eliminar a personas de la base de datos
# ! manejo de roles la api no esta considerando el manejo de roles, creacion de un rol o roles por defecto
# ? al crear la base de datos deberia haber un usuario por defecto el admin
# ? este es el que deberia poder crear a los demas usuarios y asignarles sus roles
# ! manejo y creacion de roles, que puede hacer cada rol, que permiso tiene sobre que tablas, analizar esta parte
# ? al ingresar el usuario o la persona se crea, no hay forma de accinarle despues rol a esos usuarios que luego ingresan sin rol
# ? como funciona la carpeta middlewares
# ? construir los test por que probar endpoint por endpoint es muy lento
# ! definir ruta de accion para poder automatizar los test
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(objetos.router, prefix="/objetos", tags=["Objetos"])
api_router.include_router(
    facturas.router, prefix="/facturas", tags=["Facturas"])
api_router.include_router(
    ubicaciones.router, prefix="/ubicaciones", tags=["Ubicaciones"])
