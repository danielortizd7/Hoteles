"""
URL configuration for hotel_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        'message': 'API Backend Hotel MOTEL ECLIPSE',
        'version': '1.0',
        'endpoints': {
            'administracion': '/admin/',
            'api': '/api/',
            'cuentas': {
                'login': '/api/cuentas/login/',
                'perfil': '/api/cuentas/perfil/',
                'usuarios': '/api/cuentas/usuarios/'
            },
            'usuarios': {
                'login': '/api/usuarios/login/',
                'cerrar_sesion': '/api/usuarios/cerrar-sesion/',
                'usuarios': '/api/usuarios/usuarios/'
            },
            'habitaciones': {
                'lista': '/api/habitaciones/',
                'tipos': '/api/habitaciones/tipos/',
                'dashboard': '/api/habitaciones/dashboard/',
                'disponibles': '/api/habitaciones/disponibles/'
            },
            'inventario': {
                'productos': '/api/inventario/productos/',
                'categorias': '/api/inventario/categorias/',
                'movimientos': '/api/inventario/movimientos-stock/',
                'stock_bajo': '/api/inventario/productos/low_stock/'
            },
            'documentacion': '/api/docs/'
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/cuentas/', include('accounts.urls')),
    path('api/usuarios/', include('accounts.urls')),  # Alias para usuarios
    path('api/habitaciones/', include('rooms.urls')),
    path('api/inventario/', include('inventory.urls')),
    # URLs en inglés para compatibilidad
    path('api/accounts/', include('accounts.urls')),
    path('api/rooms/', include('rooms.urls')),
    path('api/inventory/', include('inventory.urls')),
    path('', api_root, name='home'),
]
