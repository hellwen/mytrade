import time
import datetime
import itertools

from wtforms import fields#, widgets
try:
    from wtforms.fields import _unset_value as unset_value
except ImportError:
    from wtforms.utils import unset_value

from .widgets import (
    DateTimePickerWidget,
    TimePickerWidget,
    Select2Widget,
    Select2TagsWidget,

    InlineFieldListWidget, 
    InlineFormWidget,
    AjaxSelect2Widget, 
    XEditableWidget, 
)

from mytrade.utils import _

"""
An understanding of WTForms's Custom Widgets is helpful for understanding this code: http://wtforms.simplecodes.com/docs/0.6.2/widgets.html#custom-widgets
"""

class DateTimeField(fields.DateTimeField):
    """
       Allows modifying the datetime format of a DateTimeField using form_args.
    """
    widget = DateTimePickerWidget()
    def __init__(self, label=None, validators=None, format=None, **kwargs):
        """
            Constructor

            :param label:
                Label
            :param validators:
                Field validators
            :param format:
                Format for text to date conversion. Defaults to '%Y-%m-%d %H:%M:%S'
            :param kwargs:
                Any additional parameters
        """
        super(DateTimeField, self).__init__(label, validators, **kwargs)

        self.format = format or '%Y-%m-%d %H:%M:%S'


class TimeField(fields.Field):
    """
        A text field which stores a `datetime.time` object.
        Accepts time string in multiple formats: 20:10, 20:10:00, 10:00 am, 9:30pm, etc.
    """
    widget = TimePickerWidget()

    def __init__(self, label=None, validators=None, formats=None,
                 default_format=None, widget_format=None, **kwargs):
        """
            Constructor

            :param label:
                Label
            :param validators:
                Field validators
            :param formats:
                Supported time formats, as a enumerable.
            :param default_format:
                Default time format. Defaults to '%H:%M:%S'
            :param kwargs:
                Any additional parameters
        """
        super(TimeField, self).__init__(label, validators, **kwargs)

        self.formats = formats or ('%H:%M:%S', '%H:%M',
                                   '%I:%M:%S%p', '%I:%M%p',
                                   '%I:%M:%S %p', '%I:%M %p')

        self.default_format = default_format or '%H:%M:%S'

    def _value(self):
        if self.raw_data:
            return u' '.join(self.raw_data)
        elif self.data is not None:
            return self.data.strftime(self.default_format)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            date_str = u' '.join(valuelist)

            if date_str.strip():
                for format in self.formats:
                    try:
                        timetuple = time.strptime(date_str, format)
                        self.data = datetime.time(timetuple.tm_hour,
                                                  timetuple.tm_min,
                                                  timetuple.tm_sec)
                        return
                    except ValueError:
                        pass

                raise ValueError(_('Invalid time format'))
            else:
                self.data = None


class Select2Field(fields.SelectField):
    """
        `Select2 <https://github.com/ivaynberg/select2>`_ styled select widget.

        You must include select2.js, form-x.x.x.js and select2 stylesheet for it to work.
    """
    widget = Select2Widget()

    def __init__(self, label=None, validators=None, coerce=str,
                 choices=None, allow_blank=False, blank_text=None,
                 **kwargs):
        super(Select2Field, self).__init__(
            label, validators, coerce, choices, **kwargs
        )
        self.allow_blank = allow_blank
        self.blank_text = blank_text or ' '

    def iter_choices(self):
        if self.allow_blank:
            yield (u'__None', self.blank_text, self.data is None)

        if self.choices:
            for value, label in self.choices:
                yield (value, label, self.coerce(value) == self.data)

    def process_data(self, value):
        if value is None:
            self.data = None
        else:
            try:
                self.data = self.coerce(value)
            except (ValueError, TypeError):
                self.data = None

    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] == '__None':
                self.data = None
            else:
                try:
                    self.data = self.coerce(valuelist[0])
                except ValueError:
                    raise ValueError(self.gettext(u'Invalid Choice: could not coerce'))

    def pre_validate(self, form):
        if self.allow_blank and self.data is None:
            return

        super(Select2Field, self).pre_validate(form)


class Select2TagsField(fields.StringField):
    """`Select2 <http://ivaynberg.github.com/select2/#tags>`_ styled text field.
    You must include select2.js, form-x.x.x.js and select2 stylesheet for it to work.
    """
    widget = Select2TagsWidget()

    def __init__(self, label=None, validators=None, save_as_list=False, coerce=str, **kwargs):
        """Initialization

        :param save_as_list:
            If `True` then populate ``obj`` using list else string
        """
        self.save_as_list = save_as_list
        self.coerce = coerce

        super(Select2TagsField, self).__init__(label, validators, **kwargs)

    def process_formdata(self, valuelist):
        if self.save_as_list:
            self.data = [self.coerce(v.strip()) for v in valuelist[0].split(',') if v.strip()]
        else:
            self.data = self.coerce(valuelist[0])

    def _value(self):
        if isinstance(self.data, (list, tuple)):
            return u','.join(v for v in self.data)
        elif self.data:
            return self.data
        else:
            return u''

class InlineFieldList(fields.FieldList):
    widget = InlineFieldListWidget()

    def __init__(self, *args, **kwargs):
        super(InlineFieldList, self).__init__(*args, **kwargs)

    def __call__(self, **kwargs):
        # Create template
        meta = getattr(self, 'meta', None)
        if meta:
            template = self.unbound_field.bind(form=None, name='', _meta=meta)
        else:
            template = self.unbound_field.bind(form=None, name='')
        # Small hack to remove separator from FormField
        if isinstance(template, fields.FormField):
            template.separator = ''

        template.process(None)

        return self.widget(self,
                           template=template,
                           check=self.display_row_controls,
                           **kwargs)

    def display_row_controls(self, field):
        return True

    def process(self, formdata, data=None):
        res = super(InlineFieldList, self).process(formdata, data)

        # Postprocess - contribute flag
        if formdata:
            for f in self.entries:
                key = 'del-%s' % f.id
                f._should_delete = key in formdata

        return res

    def validate(self, form, extra_validators=tuple()):
        """
            Validate this FieldList.

            Note that FieldList validation differs from normal field validation in
            that FieldList validates all its enclosed fields first before running any
            of its own validators.
        """
        self.errors = []

        # Run validators on all entries within
        for subfield in self.entries:
            if not self.should_delete(subfield) and not subfield.validate(form):
                self.errors.append(subfield.errors)

        chain = itertools.chain(self.validators, extra_validators)
        self._run_validation_chain(form, chain)

        return len(self.errors) == 0

    def should_delete(self, field):
        return getattr(field, '_should_delete', False)

    def populate_obj(self, obj, name):
        values = getattr(obj, name, None)
        try:
            ivalues = iter(values)
        except TypeError:
            ivalues = iter([])

        candidates = itertools.chain(ivalues, itertools.repeat(None))
        _fake = type(str('_fake'), (object, ), {})

        output = []
        for field, data in zip(self.entries, candidates):
            if not self.should_delete(field):
                fake_obj = _fake()
                fake_obj.data = data
                field.populate_obj(fake_obj, 'data')
                output.append(fake_obj.data)

        setattr(obj, name, output)


class InlineFormField(fields.FormField):
    """
        Inline version of the ``FormField`` widget.
    """
    widget = InlineFormWidget()


class InlineModelFormField(fields.FormField):
    """
        Customized ``FormField``.

        Excludes model primary key from the `populate_obj` and
        handles `should_delete` flag.
    """
    widget = InlineFormWidget()

    def __init__(self, form_class, pk, form_opts=None, **kwargs):
        super(InlineModelFormField, self).__init__(form_class, **kwargs)

        self._pk = pk
        self.form_opts = form_opts

    def get_pk(self):
        return getattr(self.form, self._pk).data

    def populate_obj(self, obj, name):
        for name, field in iteritems(self.form._fields):
            if name != self._pk:
                field.populate_obj(obj, name)


class ListEditableFieldList(fields.FieldList):
    """
        Modified FieldList to allow for alphanumeric primary keys.

        Used in the editable list view.
    """
    widget = XEditableWidget()

    def __init__(self, *args, **kwargs):
        super(ListEditableFieldList, self).__init__(*args, **kwargs)
        # min_entries = 1 is required for the widget to determine the type
        self.min_entries = 1

    def _extract_indices(self, prefix, formdata):
        offset = len(prefix) + 1
        for name in formdata:
            # selects only relevant field (not CSRF, other fields, etc)
            if name.startswith(prefix):
                # exclude offset (prefix-), remaining text is the index
                yield name[offset:]

    def _add_entry(self, formdata=None, data=unset_value, index=None):
        assert not self.max_entries or len(self.entries) < self.max_entries, \
            'You cannot have more than max_entries entries in this FieldList'
        if index is None:
            index = self.last_index + 1
        self.last_index = index

        # '%s-%s' instead of '%s-%d' to allow alphanumeric
        name = '%s-%s' % (self.short_name, index)
        id = '%s-%s' % (self.id, index)

        # support both wtforms 1 and 2
        meta = getattr(self, 'meta', None)
        if meta:
            field = self.unbound_field.bind(
                form=None, name=name, prefix=self._prefix, id=id, _meta=meta
            )
        else:
            field = self.unbound_field.bind(
                form=None, name=name, prefix=self._prefix, id=id
            )

        field.process(formdata, data)
        self.entries.append(field)
        return field

    def populate_obj(self, obj, name):
        # return data from first item, instead of a list of items
        setattr(obj, name, self.data.pop())


class AjaxSelectField(fields.SelectFieldBase):
    """
        Ajax Model Select Field
    """
    widget = AjaxSelect2Widget()

    separator = ','

    def __init__(self, loader, label=None, validators=None, allow_blank=False, blank_text=u'', **kwargs):
        super(AjaxSelectField, self).__init__(label, validators, **kwargs)
        self.loader = loader

        self.allow_blank = allow_blank
        self.blank_text = blank_text

    def _get_data(self):
        if self._formdata:
            model = self.loader.get_one(self._formdata)

            if model is not None:
                self._set_data(model)

        return self._data

    def _set_data(self, data):
        self._data = data
        self._formdata = None

    data = property(_get_data, _set_data)

    def _format_item(self, item):
        value = self.loader.format(self.data)
        return (value[0], value[1], True)

    def process_formdata(self, valuelist):
        if valuelist:
            if self.allow_blank and valuelist[0] == u'__None':
                self.data = None
            else:
                self._data = None
                self._formdata = valuelist[0]

    def pre_validate(self, form):
        if not self.allow_blank and self.data is None:
            raise ValidationError(self.gettext(u'Not a valid choice'))


class AjaxSelectMultipleField(AjaxSelectField):
    """
        Ajax-enabled model multi-select field.
    """
    widget = AjaxSelect2Widget(multiple=True)

    def __init__(self, loader, label=None, validators=None, default=None, **kwargs):
        if default is None:
            default = []

        super(AjaxSelectMultipleField, self).__init__(loader, label, validators, default=default, **kwargs)
        self._invalid_formdata = False

    def _get_data(self):
        formdata = self._formdata
        if formdata:
            data = []

            # TODO: Optimize?
            for item in formdata:
                model = self.loader.get_one(item) if item else None

                if model:
                    data.append(model)
                else:
                    self._invalid_formdata = True

            self._set_data(data)

        return self._data

    def _set_data(self, data):
        self._data = data
        self._formdata = None

    data = property(_get_data, _set_data)

    def process_formdata(self, valuelist):
        self._formdata = set()

        for field in valuelist:
            for n in field.split(self.separator):
                self._formdata.add(n)

    def pre_validate(self, form):
        if self._invalid_formdata:
            raise ValidationError(self.gettext(u'Not a valid choice'))
