# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import g, url_for, flash, render_template


def set_current_view(view):
    g._admin_view = view


def get_current_view():
    """
        Get current administrative view.
    """
    return getattr(g, '_admin_view', None)


def get_url(endpoint, **kwargs):
    """
        Alternative to Flask `url_for`.
        If there's current administrative view, will call its `get_url`. If there's none - will
        use generic `url_for`.

        :param endpoint:
            Endpoint name
        :param kwargs:
            View arguments
    """
    view = get_current_view()

    if not view:
        return url_for(endpoint, **kwargs)

    return view.get_url(endpoint, **kwargs)


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                  .format(getattr(form, field).label.text, error), category)

def _(origin):
    return origin

def render(template, **kwargs):

    kwargs['_'] = _

    return render_template(template, **kwargs)

