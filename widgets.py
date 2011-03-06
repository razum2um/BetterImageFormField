#-*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminFileWidget
from django.db.models.fields.files import ImageFieldFile

class PreviewAdminFileWidget(AdminFileWidget):
    '''
    A AdminFileWidget that shows a delete checkbox
    and possible preview pic
    '''
    input_type = 'file'
    def __init__(self, deletable=True, *args, **kwargs):
        self.deletable = deletable
        super(PreviewAdminFileWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        input = super(forms.widgets.FileInput, self).render(name, value, attrs)
        if isinstance(value, ImageFieldFile):
            item = '<tr>%s<td style="vertical-align: middle;">%s</td><td>%s</td>'
            preview = isinstance(value, ImageFieldFile) and \
                '<td rowspan="3"><a target="_blank" href="%(prefix)s%(path)s"><img src="%(prefix)s%(path)s" height="90px" /></a></td>' % {
                    'prefix': settings.MEDIA_URL, 
                    'path': str(value)
                    } or \
                ''
            output = []
            output.append('<table style="border-style: none;">')
            output.append(item % (
                preview,
                u'Сейчас:', 
                '<a target="_blank" href="%s%s">%s</a>' % (settings.MEDIA_URL, str(value), str(value)))
                )
            output.append(item % ('', u'Поменять:', input))
            output.append(item % (
                '', 
                u'Удалить:', 
                self.deletable and '<input type="checkbox" name="%s_delete"/>' % name or u'нельзя (только заменить)'
                )) 
            output.append('</table>')
            return mark_safe(u''.join(output))
        else:
            return mark_safe(input)

    def value_from_datadict(self, data, files, name):
        if not data.get('%s_delete' % name):
            return super(PreviewAdminFileWidget, self).value_from_datadict(data, files, name)
        else:
            return '__deleted__'

