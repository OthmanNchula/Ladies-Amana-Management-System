from django.contrib import admin
from django.urls import path, include
from loginApp import views
from loginApp import views as login_views


urlpatterns = [
    path('', login_views.login_view, name='home'), 
    path('admin/', admin.site.urls),
    path('account/', include('loginApp.urls',  namespace='login_App')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('mkopo/', include('mkopoApp.urls', namespace='mkopo_App')),
    path('adminApp/', include('adminApp.urls', namespace='Admin_App')),
    path('mtaji/', include('mtajiApp.urls', namespace="mtaji_App")),
    path('mchango/', include('michangoApp.urls', namespace="mchango_App")),
    path('swadaqa/', include('swadaqaApp.urls', namespace='swadaqa_App')),
]
