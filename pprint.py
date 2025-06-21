# Copyright 2020-2025 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2025-06-02
# modified: 2025-06-21
#
# A simple MicroPython-compatible YAML pretty printer.
# This also prints a subset of JSON, meant only to be used with mp-yaml.
#

from stringbuilder import StringBuilder

# -----------------------------------------------------------------------------
def _pretty_print_yaml(obj, indent=4, _current_indent=0, return_text=False):
    '''
    Pretty-print dicts/lists as YAML-like text.

    Args:
        obj: object to print (dict/list/primitive)
        indent: number of spaces per indentation level
        _current_indent: current number of spaces to indent
        return_text: whether to return the generated text instead of printing it
    '''
    space = ' ' * _current_indent
    result = StringBuilder()  # Create a StringBuilder instance

    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                result.append("{}{}:\n".format(space, k))
                result.append(_pretty_print_yaml(v, indent, _current_indent + indent, return_text=True))
            else:
                result.append("{}{}: {}\n".format(space, k, v))
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, (dict, list)):
                result.append("{}-\n".format(space))
                result.append(_pretty_print_yaml(item, indent, _current_indent + indent, return_text=True))
            else:
                result.append("{}- {}\n".format(space, item))
    else:
        result.append("{}{}\n".format(space, obj))

    # If return_text is True, return the result as a string
    if return_text:
        return str(result)

    # Default behavior: print the result
    print(str(result))

# -----------------------------------------------------------------------------
def _pretty_print_json(obj, indent=4, _depth=0, return_text=False):
    '''
    Pretty-print nested dicts and lists in JSON-like style.

    Args:
        obj: object to print (dict/list/primitive)
        indent: number of spaces per indentation level
        _depth: current depth of recursion
        return_text: whether to return the generated text instead of printing it
    '''
    space = ' ' * indent * _depth
    result = StringBuilder()  # Create a StringBuilder instance

    if isinstance(obj, dict):
        result.append(space + '{\n')
        for k, v in obj.items():
            result.append(space + ' ' * indent + '{}: '.format(repr(k)))
            if isinstance(v, (dict, list)):
                result.append('\n')
                result.append(_pretty_print_json(v, indent=indent, _depth=_depth + 1, return_text=True))
            else:
                result.append(repr(v) + '\n')
        result.append(space + '}')
    elif isinstance(obj, list):
        result.append(space + '[\n')
        for item in obj:
            if isinstance(item, (dict, list)):
                result.append(_pretty_print_json(item, indent=indent, _depth=_depth + 1, return_text=True))
            else:
                result.append(space + ' ' * indent + repr(item) + '\n')
        result.append(space + ']')
    else:
        result.append(space + repr(obj))

    # If return_text is True, return the result as a string
    if return_text:
        return str(result)

    # Default behavior: print the result
    print(str(result))

# -----------------------------------------------------------------------------
def pretty_print(obj, indent=4, markup='yaml', return_text=False):
    '''
    Public pretty print function.

    Args:
    :param obj:           The object (dict/list/primitive) to pretty print.
    :param markup:        A string indicating 'yaml' (default) or 'json'.
    :param return_text:   Flag to indicate whether to return the generated text instead of printing.
    '''
    if markup == 'yaml':
        return _pretty_print_yaml(obj, indent=indent, return_text=return_text)
    else:
        return _pretty_print_json(obj, indent=indent, return_text=return_text)
