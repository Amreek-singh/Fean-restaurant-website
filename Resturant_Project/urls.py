"""
URL configuration for Resturant_Project project.

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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Base_app.views import *
urlpatterns = [
    path("admin/", admin.site.urls),
    path('',HomeView,name="home"),
    path('book_table/',BookTableView,name="book_table"),
    path('menu/',MenuView, name="menu"),
    path('about/',AboutView,name="about"),
    path('feedback/',feedback,name="feedback"),
    path('read_more/',read_more,name="read_more"),
    #path('order_now/',order_now,name="order_now"),
    path("cart/", order_now, name="order_now"),
    path("remove/<int:cart_item_id>/", remove_from_cart, name="remove_from_cart"),
    path('signup/',signup,name="signup"),
    path('signin/',signin,name="signin"),
    #path("dashboard/",dashboard,name='dashboard'),
    path("logout/",signout,name='signout'),
    path("add_to_cart/<int:item_id>/", add_to_cart, name="add_to_cart"),
    #path("place_order/", place_order, name="place_order"),
    #path("track_order/", track_order, name="track_order"),
    path('place_order/', place_order, name='place_order'),
    path('order_status/<int:order_id>/', order_status, name='order_status'),
    path('place_order/', place_order, name='place_order'),
    path('order_status/<int:order_id>/', order_status, name='order_status'),
    path('view_orders/', view_orders, name='view_orders'),  # New route
    path('fake_payment/', fake_payment, name='fake_payment'),  # New payment route
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)