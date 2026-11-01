"""
URL configuration for PROJECT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.views.static import serve
from django.urls import path
from django.conf import settings
from APP import views
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('mobiles/',views.store_mobiles,name='mobiles'),
    path('laptops/',views.store_laptops,name='laptops'),
    path('casual_shoes/',views.store_shoe,name='casual_shoes'),
    path('furniture/',views.store_furniture,name='furniture'),
    path('kitchen/',views.store_kitchen,name='kitchen'),
     path('shirt/',views.store_shirt,name='shirt'),
     path('television/',views.store_television,name='television'),
     path('jeans/',views.store_jean,name='jeans'),
     path('formal_shoes/',views.store_formal_shoe,name='formal_shoes'),
     path('rice_cookers/',views.store_rice_cooker,name='rice_cookers'),
     path('table/',views.store_table,name='table'),
    path('beauty/',views.store_beauty,name='beauty'),
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('add_cart/<int:product_id>/<str:product_type>/',views.add_cart,name='add_cart'),
    path('view_cart/',views.view_cart,name='view_cart'),
    path('increase_quantity/<int:cart_id>/',views.increase_quantity,name='increase_quantity'),
    path('decrease_quantity/<int:cart_id>/',views.decrease_quantity,name='decrease_quantity'),
    path('remove_cart/<int:cart_id>/',views.remove_cart,name='remove_cart'),
    path('search/',views.search_product,name='search_product'),
    path('success/',views.success,name='success'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('wishlist/add/<str:product_type>/<int:product_id>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('view_wishlist/',views.view_wishlist,name='view_wishlist'),
    path('wishlist/remove/<int:wishlist_id>/',views.remove_from_wishlist,name='remove_from_wishlist'),


]


urlpatterns += [
    path('media/<path:path>', serve, {
        'document_root': settings.MEDIA_ROOT
    }),
]


