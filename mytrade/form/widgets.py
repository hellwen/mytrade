from jinja2 import escape
from flask.globals import _request_ctx_stack
from flask import json
from wtforms import widgets

from mytrade.utils import _, get_url


class Select2Widget(widgets.Select):
    """
        `Select2 <https://github.com/ivaynberg/select2>`_ styled select widget.

        You must include select2.js, form-x.x.x.js and select2 stylesheet for it to
        work.
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-role', u'select2')

        allow_blank = getattr(field, 'allow_blank', False)
        if allow_blank and not self.multiple:
            kwargs['data-allow-blank'] = u'1'

        return super(Select2Widget, self).__call__(field, **kwargs)


class Select2TagsWidget(widgets.TextInput):
    """`Select2 <http://ivaynberg.github.com/select2/#tags>`_ styled text widget.
    You must include select2.js, form-x.x.x.js and select2 stylesheet for it to work.
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-role', u'select2')
        kwargs.setdefault('data-tags', u'1')
        return super(Select2TagsWidget, self).__call__(field, **kwargs)


class DatePickerWidget(widgets.TextInput):
    """
        Date picker widget.

        You must include bootstrap-datepicker.js and form-x.x.x.js for styling to work.
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-role', u'datepicker')
        kwargs.setdefault('data-date-format', u'YYYY-MM-DD')

        self.date_format = kwargs['data-date-format']
        return super(DatePickerWidget, self).__call__(field, **kwargs)


class DateTimePickerWidget(widgets.TextInput):
    """
        Datetime picker widget.

        You must include bootstrap-datepicker.js and form-x.x.x.js for styling to work.
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-role', u'datetimepicker')
        kwargs.setdefault('data-date-format', u'YYYY-MM-DD HH:mm:ss')
        return super(DateTimePickerWidget, self).__call__(field, **kwargs)


class TimePickerWidget(widgets.TextInput):
    """
        Date picker widget.

        You must include bootstrap-datepicker.js and form-x.x.x.js for styling to work.
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-role', u'timepicker')
        kwargs.setdefault('data-date-format', u'HH:mm:ss')
        return super(TimePickerWidget, self).__call__(field, **kwargs)


class RenderTemplateWidget(object):
    """
        WTForms widget that renders Jinja2 template
    """
    def __init__(self, template):
        """
            Constructor

            :param template:
                Template path
        """
        self.template = template

    def __call__(self, field, **kwargs):
        ctx = _request_ctx_stack.top
        jinja_env = ctx.app.jinja_env

        kwargs.update({
            'field': field,
            '_gettext': _,
            '_ngettext': _,
        })

        template = jinja_env.get_template(self.template)
        return template.render(kwargs)


class InlineFieldListWidget(RenderTemplateWidget):
    def __init__(self):
        super(InlineFieldListWidget, self).__init__('widgets/inline_field_list.html')


class InlineFormWidget(RenderTemplateWidget):
    def __init__(self):
        super(InlineFormWidget, self).__init__('widgets/inline_form.html')

    def __call__(self, field, **kwargs):
        kwargs.setdefault('form_opts', getattr(field, 'form_opts', None))
        return super(InlineFormWidget, self).__call__(field, **kwargs)


class AjaxSelect2Widget(object):
    def __init__(self, multiple=False):
        self.multiple = multiple

    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-role', 'select2-ajax')
        kwargs.setdefault('data-url', get_url('.ajax_lookup', name=field.loader.name))

        allow_blank = getattr(field, 'allow_blank', False)
        if allow_blank and not self.multiple:
            kwargs['data-allow-blank'] = u'1'

        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', 'hidden')

        if self.multiple:
            result = []
            ids = []

            for value in field.data:
                data = field.loader.format(value)
                result.append(data)
                ids.append(data[0])

            separator = getattr(field, 'separator', ',')

            kwargs['value'] = separator.join(ids)
            kwargs['data-json'] = json.dumps(result)
            kwargs['data-multiple'] = u'1'
        else:
            data = field.loader.format(field.data)

            if data:
                kwargs['value'] = data[0]
                kwargs['data-json'] = json.dumps(data)

        placeholder = _(field.loader.options.get('placeholder', 'Please select model'))
        kwargs.setdefault('data-placeholder', placeholder)

        return widgets.HTMLString('<input %s>' % widgets.html_params(name=field.name, **kwargs))


class XEditableWidget(object):
    """
        WTForms widget that provides in-line editing for the list view.

        Determines how to display the x-editable/ajax form based on the
        field inside of the FieldList (StringField, IntegerField, etc).
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-value', kwargs.pop('value', ''))

        kwargs.setdefault('data-role', 'x-editable')
        kwargs.setdefault('data-url', './ajax/update/')

        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)
        kwargs.setdefault('href', '#')

        if not kwargs.get('pk'):
            raise Exception('pk required')
        kwargs['data-pk'] = str(kwargs.pop("pk"))

        kwargs['data-csrf'] = kwargs.pop("csrf", "")

        # subfield is the first entry (subfield) from FieldList (field)
        subfield = field.entries[0]

        kwargs = self.get_kwargs(subfield, kwargs)

        return widgets.HTMLString(
            '<a %s>%s</a>' % (widgets.html_params(**kwargs),
                              escape(kwargs['data-value']))
        )

    def get_kwargs(self, subfield, kwargs):
        """
            Return extra kwargs based on the subfield type.
        """
        if subfield.type == 'StringField':
            kwargs['data-type'] = 'text'
        elif subfield.type == 'TextAreaField':
            kwargs['data-type'] = 'textarea'
            kwargs['data-rows'] = '5'
        elif subfield.type == 'BooleanField':
            kwargs['data-type'] = 'select'
            # data-source = dropdown options
            kwargs['data-source'] = {'': 'False', '1': 'True'}
            kwargs['data-role'] = 'x-editable-boolean'
        elif subfield.type == 'Select2Field':
            kwargs['data-type'] = 'select'
            choices = [{'value': x, 'text': y} for x, y in subfield.choices]

            # prepend a blank field to choices if allow_blank = True
            if getattr(subfield, 'allow_blank', False):
                choices.insert(0, {'value': '__None', 'text': ''})

            # json.dumps fixes issue with unicode strings not loading correctly
            kwargs['data-source'] = json.dumps(choices)
        elif subfield.type == 'DateField':
            kwargs['data-type'] = 'combodate'
            kwargs['data-format'] = 'YYYY-MM-DD'
            kwargs['data-template'] = 'YYYY-MM-DD'
        elif subfield.type == 'DateTimeField':
            kwargs['data-type'] = 'combodate'
            kwargs['data-format'] = 'YYYY-MM-DD HH:mm:ss'
            kwargs['data-template'] = 'YYYY-MM-DD  HH:mm:ss'
            # x-editable-combodate uses 1 minute increments
            kwargs['data-role'] = 'x-editable-combodate'
        elif subfield.type == 'TimeField':
            kwargs['data-type'] = 'combodate'
            kwargs['data-format'] = 'HH:mm:ss'
            kwargs['data-template'] = 'HH:mm:ss'
            kwargs['data-role'] = 'x-editable-combodate'
        elif subfield.type == 'IntegerField':
            kwargs['data-type'] = 'number'
        elif subfield.type in ['FloatField', 'DecimalField']:
            kwargs['data-type'] = 'number'
            kwargs['data-step'] = 'any'
        elif subfield.type in ['QuerySelectField', 'ModelSelectField']:
            # QuerySelectField and ModelSelectField are for relations
            kwargs['data-type'] = 'select'

            choices = []
            for choice in subfield:
                try:
                    choices.append({'value': str(choice._value()),
                                    'text': str(choice.label.text)})
                except TypeError:
                    # unable to display text value
                    choices.append({'value': str(choice._value()),
                                    'text': ''})

            # blank field is already included if allow_blank
            kwargs['data-source'] = json.dumps(choices)
        else:
            raise Exception('Unsupported field type: %s' % (type(subfield),))

        return kwargs
