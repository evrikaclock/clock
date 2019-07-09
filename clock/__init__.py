from sanic import Sanic
from sanic_jinja2 import SanicJinja2

app = Sanic(__name__)

jinja = SanicJinja2(app)
app.static('/static', './clock/static')

import clock.controllers
