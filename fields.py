#-*- coding: utf-8 -*-
import os
from django.db.models.fields.files import ImageField
from django.forms.fields import ImageField as ImageFormField

from widgets import PreviewAdminFileWidget

class BetterImageFormField(ImageFormField):
    def clean(self, data, initial=None):
        if data != '__deleted__':
            return super(BetterImageFormField, self).clean(data, initial)
        else:
            return '__deleted__'

class BetterImageField(ImageField):
    '''
    Django field that behaves as ImageField, with some extra features like:
        - preview & deletion in admin
    '''

    def save_form_data(self, instance, data):
        '''
            Overwrite save_form_data to delete images if "delete" checkbox
            in admin is selected
        '''
        if data == '__deleted__':
            filename = getattr(instance, self.name).path
            if os.path.exists(filename):
                os.remove(filename)
            setattr(instance, self.name, None)
        else:
            super(BetterImageField, self).save_form_data(instance, data)

    def get_db_prep_save(self, value):
        '''
            Overwrite get_db_prep_save to allow saving nothing to the database
            if image has been deleted
        '''
        if value:    
            return super(BetterImageField, self).get_db_prep_save(value)
        else:
            return u''

    def formfield(self, **kwargs):
        '''
        Specify form field and widget to be used on the forms
        '''
        kwargs['widget'] = PreviewAdminFileWidget(deletable=self.blank)
        kwargs['form_class'] = BetterImageFormField
        return super(BetterImageField, self).formfield(**kwargs)


