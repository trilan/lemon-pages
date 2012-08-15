import os

from django.forms.widgets import Select
from django.utils.encoding import force_unicode

from . import settings


class SelectPageTemplate(Select):

    def _is_template(self, dir_, f):
        f = os.path.join(dir_, f)
        if not os.path.isfile(f):
            return False
        return any(f.endswith(e) for e in settings.TEMPLATE_EXTENSIONS)

    def _get_template_choices(self):
        template_dirs = [os.path.join(d, 'pages') for d in settings.TEMPLATE_DIRS]
        templates = []
        for dir_ in template_dirs:
            try:
                files = os.listdir(dir_)
            except OSError:
                continue
            templates.extend(f for f in files if self._is_template(dir_, f))

        template_choices = []
        for template in sorted(set(templates)):
            template = force_unicode(template)
            template_choices.append((template, template))
        return template_choices

    def render_options(self, choices, selected_choices):
        self.choices = self._get_template_choices()
        return super(SelectPageTemplate, self).render_options(
            choices,
            selected_choices,
        )
