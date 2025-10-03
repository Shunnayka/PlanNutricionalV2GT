from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from nutricion import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('registro/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='nutricion/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('nutricion/', include('nutricion.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)