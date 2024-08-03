# myapp/jinja2_env.py
from jinja2 import Environment
from tsinc.templatetags.custom_filters import currency, naturaltime_es

def environment(**options):
    env = Environment(**options)
    env.filters['cop'] = currency
    env.filters['naturaltime_es'] = naturaltime_es
    return env
