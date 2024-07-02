import subprocess

from django.conf import settings
from django.http import HttpResponse
from appcommon.helper import subprocess_run

from .models import PythonInfo


def setup():
    target_major, target_minor = 3, 8
    get_version = subprocess_run(subprocess, f'{settings.PYENV_RUN_FILE} install --list').stdout.splitlines()
    versions = []
    for version in get_version:
        version = version.strip()
        version_list = version.split('.')
        if len(version_list) == 3:
            try:
                if (int(version_list[0]) >= target_major and int(version_list[1]) >= target_minor
                        and int(version_list[2]) >= 0):
                    versions.append(version)
            except ValueError:
                continue

    PythonInfo.objects.all().delete()
    i = 1
    for version in versions:
        print(version)
        is_install = False
        is_used = False
        is_default = False
        if version == settings.PYENV_DEFAULT_PYTHON:
            is_install = True
            is_used = True
            is_default = True
        PythonInfo.objects.create(
            version=version, is_install=is_install, is_used=is_used,
            orders=i, is_default=is_default
        )
        i += 1
    return True
    
    
def uninstall()：
    return True
