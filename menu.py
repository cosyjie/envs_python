from django.urls import reverse

menu = {
    'module_envs': {
        'child': [
            {
                'name': 'envs_python',
                'title': 'Python环境',
                'href': reverse('module_envs:envs_python:list'),
            },
        ]
    }
}