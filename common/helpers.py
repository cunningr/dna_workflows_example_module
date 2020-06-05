"""
Common helper functions
"""
import logging
import functools
from jinja2 import Template
import json

logger = logging.getLogger('main.helpers')


def dot_to_json(a):
    output = {}
    for key, value in a.items():
        path = key.split('.')
        if path[0] == 'json':
            path = path[1:]
        target = functools.reduce(lambda d, k: d.setdefault(k, {}), path[:-1], output)
        target[path[-1]] = value
    return output


def build_json_from_template(template, data):
    """Build a python dict from a json template

     Args:
         template: A jinja2 template containing a valid json string
         data: A dictionary containing values to be used when parsing the template

     Returns:
         A python dictionary loaded from json

     """
    t = Template(template)
    json_string = t.render(item=data)
    parsed = json.loads(json_string)

    return parsed


def get_object_id(object_list, **kwargs):
    """Get object id

    Args:
        object_list: A list of json objects
        **kwargs: a list of filters to search the object list for
            return_param: specify the key that should be returned (id = default)
            strict: True or False. Specifies the type of string match

    Returns:
        The value of the json key 'id' or 'None' is no object is found

    """
    if 'return_param' in kwargs:
        return_param = kwargs['return_param']
        kwargs.pop('return_param')
    else:
        return_param = 'id'

    if 'strict' in kwargs:
        strict = kwargs['strict']
        kwargs.pop('strict', None)
    else:
        strict = True

    for item in object_list:
        _match = 0
        for key, value in kwargs.items():
            if item[key] == value:
                logger.debug('{}'.format(item))
                _match = 1
            elif value in item[key] and not strict:
                logger.debug('{}'.format(item))
                _match = 1
            else:
                _match = 0
                break

        if _match:
            return item[return_param]

    return None
