from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'envs_python'

urlpatterns = [
    path('init/', login_required(views.python_init), name='init'),
    path('list/', login_required(views.PythonListView.as_view()), name='list'),
    path('install/<int:pk>/', login_required(views.PythonInstallView.as_view()), name='install'),
    path('uninstall/<int:pk>/', login_required(views.UninstallView.as_view()), name='uninstall'),
    path('install/run/', login_required(views.python_install_run), name='install_run'),
    path('pypi/list/', login_required(views.PythonPypiListView.as_view()), name='pypi_list'),
    path('pypi/conf/<str:mark>/', login_required(views.PypiConfigView.as_view()), name='pypi_conf'),
]