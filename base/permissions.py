#implementar permisos del tipo:
from rest_framework import permissions


#permiso para Empresa
class IsEmpresa(permissions.BasePermission):
    """
    Permite el acceso solo a usuarios en el grupo 'inventario'.
    """
    def has_permission(self, request, view):
        #Verifica que haya un usuario en la request y que esté autenticado — osea que tenga un token JWT válido.
        if not request.user or not request.user.is_authenticated:
            return False
        #Si está autenticado, busca en los grupos del usuario si existe uno que se llame 'IsEmpresa'. Si existe devuelve True y deja pasar, si no existe devuelve False y bloquea
        return request.user.groups.filter(name='IsEmpresa').exists()
    
#permiso para inventario
class IsUser(permissions.BasePermission):
    """
    Permite el acceso solo a usuarios en el grupo 'inventario'.
    """
    def has_permission(self, request, view):
        #Verifica que haya un usuario en la request y que esté autenticado — osea que tenga un token JWT válido.
        if not request.user or not request.user.is_authenticated:
            return False
        #Si está autenticado, busca en los grupos del usuario si existe uno que se llame 'IsUser'. Si existe devuelve True y deja pasar, si no existe devuelve False y bloquea
        return request.user.groups.filter(name='IsUser').exists()