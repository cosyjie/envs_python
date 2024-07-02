from django.apps import AppConfig


class EnvsPythonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.envs_python'
    verbose_name = 'Python环境'
    dependent_modules = ['module_envs']
    version = '0.0.1-Alpha'
    description = '管理配置Python开发语言环境'
