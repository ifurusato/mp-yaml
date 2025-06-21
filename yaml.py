# Copyright 2020-2025 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2025-06-02
# modified: 2025-06-21
#
# This is a simple YAML parser for MicroPython, supporting a subset of the
# standard YAML grammar, as described below:
#
# - nested dictionaries with consistent indentation (4 spaces)
# - scalars: strings, integers, floats, booleans, and nulls
# - flat lists of scalar values
# - inline comments (after values, using '#')
# - automatic type conversion for scalars
# - pretty-printing in either JSON or YAML format
#
# Any features beyond those listed above, e.g., nested lists, multiline
# strings, anchors, complex keys, inline dictionaries and complex YAML
# syntax are not supported.
#

class FileNotFoundError(Exception):
    '''     
    An exception thrown when encountering a reference to a file that does not exist.
    '''     
    pass

# -----------------------------------------------------------------------------
def load(fpath):
    try:
        with open(fpath, 'r') as f:
            text = f.read()
            return parse(text)
    except OSError as e:
        raise FileNotFoundError("file not found: {}".format(fpath))

# -----------------------------------------------------------------------------
def dump(obj, file_path=None, indent=4):
    import pprint
    if file_path is None:
        # delegate the call to pprint.pretty_print
        pprint.pretty_print(obj, indent=indent)
    else:
        text = pprint.pretty_print(obj, indent=indent, return_text=True)
        with open(file_path, "w") as f:
            f.write(text)

# -----------------------------------------------------------------------------
def parse(text):
    lines = text.split('\n')
    def parse_value(val):
        v = val.strip()
        if v == '' or v.lower() in ('null', 'none'):
            return None
        if v.lower() == 'true':
            return True
        if v.lower() == 'false':
            return False
        try:
            if '.' in v:
                return float(v)
            return int(v)
        except:
            return v.strip('\'"')
    root = {}
    stack = [(-1, root)]
    for i, line in enumerate(lines):
        # remove comments
        line = line.split('#', 1)[0]
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(' '))
        content = line.strip()
        # pop stack until indent fits
        while indent <= stack[-1][0]:
            stack.pop()
        parent_indent, parent = stack[-1]
        if content.startswith('- '):
            # List item
            if not isinstance(parent, list):
                raise ValueError('list item found but parent is not a list')
            item_val = parse_value(content[2:])
            parent.append(item_val)
        elif content == '-':
            raise ValueError('empty list item not supported (no value after dash)')
        else:
            # key: value or key:
            if ':' not in content:
                raise ValueError('invalid line (no colon): {}'.format(content))
            key, val = content.split(':', 1)
            key = key.strip()
            val = val.strip()
            if val == '':
                # look ahead to next non-empty line to see if it's a list item
                val_obj = {}
                for j in range(i+1, len(lines)):
                    next_line = lines[j].split('#',1)[0].rstrip()
                    if not next_line.strip():
                        continue
                    next_indent = len(next_line) - len(next_line.lstrip(' '))
                    if next_indent <= indent:
                        # Not child line
                        break
                    if next_line.lstrip().startswith('- '):
                        val_obj = []
                    break
            else:
                val_obj = parse_value(val)
            if isinstance(parent, dict):
                parent[key] = val_obj
            else:
                raise ValueError('expected dict as parent')
            if val == '':
                # push new container for nested block
                stack.append((indent, val_obj))
    return root