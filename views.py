import subprocess

from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts  import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView
from django.contrib import messages
from django.conf import settings

from appcommon.helper import subprocess_run
from panel.module_envs.views import EnvironmentMixin

from .models import PythonInfo
from .conf import *


class EnvsPythonMixin(EnvironmentMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = 'envs_python'
        context['is_init'] = False
        init_file = settings.APP_FILES / 'envs_python' / 'init'
        if init_file.exists():
            context['is_init'] = True
        return context

def python_init(request):
    from .install import setup
    setup()
    return redirect('module_envs:envs_python:list')

class PythonListView(EnvsPythonMixin, ListView):
    queryset = PythonInfo.objects.all()
    ordering = ['orders', 'is_install']
    template_name = 'envs_python/python_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['py_system'] = subprocess_run(subprocess, '/usr/bin/python3 -V').stdout.strip().split(' ')[1]
        context['page_title'] = 'Python环境'
        return context


class PythonPypiListView(EnvsPythonMixin, TemplateView):
    template_name = 'envs_python/pypi_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '配置pip包安装源'
        context['breadcrumb'] = [
            {'title': 'python环境', 'href': reverse('module_envs:envs_python:list'), 'active': False},
            {'title': '配置pip安装源', 'href': '', 'active': True},
        ]
        run_cmd = '{} config list'.format(settings.PYENV_DEFAULT_PIP_RUN)
        run_end = subprocess_run(subprocess, run_cmd).stdout.strip().split('\n')
        context['current_url'] = ''
        if run_end:
            for conf in run_end:
                if 'global.index-url=' in conf:
                    context['current_url'] = conf.replace("global.index-url='", '').replace("'", "")
        context['url_list'] = PYTHON_PIP_PYPI
        return context


class PypiConfigView(EnvsPythonMixin, RedirectView):
    url = reverse_lazy('module_envs:envs_python:pypi_list')

    def get(self, request, *args, **kwargs):
        url = PYTHON_PIP_PYPI[kwargs['mark']]['url']
        run_cmd = '{} config set global.index-url {}'.format(settings.PYENV_DEFAULT_PIP_RUN, url)
        subprocess_run(subprocess, run_cmd)
        run_cmd = '{} config set global.trusted-host {}'.format(settings.PYENV_DEFAULT_PIP_RUN, url)
        subprocess_run(subprocess, run_cmd)
        return super().get(request, *args, **kwargs)


class PythonInstallView(EnvsPythonMixin, TemplateView):
    template_name = 'envs_python/python_install.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'python安装'
        context['breadcrumb'] = [
            {'title': 'python环境', 'href': reverse_lazy('module_envs:envs_python:list'), 'active': False},
            {'title': 'python安装', 'href': '', 'active': True},
        ]
        context['pyinfo'] = PythonInfo.objects.get(pk=kwargs.get('pk'))
        return context


def python_install_run(request):
    pk = request.GET.get('pk')
    get_py = PythonInfo.objects.get(pk=pk)
    subprocess_run(subprocess, f"{settings.PYENV_RUN_FILE} uninstall -f {get_py.version}")
    run_end = subprocess_run(subprocess, f"{settings.PYENV_RUN_FILE} install {get_py.version}")
    return_dict = {'run_end': run_end.returncode, 'showprocess': ''}
    if run_end.returncode == 0:
        get_py.is_install = True
        get_py.save()
    return_dict['showprocess'] = (run_end.stdout + run_end.stderr).replace('\n', '</br>')
    return JsonResponse(return_dict, safe=False)


class UninstallView(EnvsPythonMixin, RedirectView):
    url = reverse_lazy('module_envs:envs_python:list')

    def get(self, request, *args, **kwargs):
        get_object = PythonInfo.objects.get(pk=self.kwargs.get('pk'))
        run = subprocess_run(subprocess, f"{settings.PYENV_RUN_FILE} uninstall -f {get_object.version}")
        if run.stderr:
            messages.warning(self.request, '服务器信息：{}'.format(run.stderr))
        if run.returncode == 0:
            get_object.is_install = False
            get_object.save()
            messages.success(request, f'Python {get_object.version} 卸载操作完成')

        return super().get(request, *args, **kwargs)