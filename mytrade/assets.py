# -*- coding: utf-8 -*-
from flask_assets import Bundle, Environment

css = Bundle(
    "libs/bootstrap/css/bootstrap.css",
    "libs/bootstrap/css/bootstrap-theme.css",
    "libs/font-awesome4/css/font-awesome.min.css",
    "css/style.css",
    filters="cssmin",
    output="public/css/common.css"
)

js = Bundle(
    "libs/jQuery/dist/jquery.js",
    "libs/bootstrap/js/bootstrap.js",
    "js/plugins.js",
    filters='jsmin',
    output="public/js/common.js"
)

form_css = Bundle(
    "libs/select2/select2.css",
    "libs/select2/select2-bootstrap3.css",
    filters="cssmin",
    output="public/css/form_common.css"
)

form_js = Bundle(
    "libs/select2/select2.min.js",
    "js/form.js",
    filters='jsmin',
    output="public/js/form_common.js"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)

assets.register("js_form", form_js)
assets.register("css_form", form_css)
