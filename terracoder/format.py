"""Functions to prettify standard type output."""

import pprint
import collections

LIST_TYPES = (tuple, list, set)
BoxChars = collections.namedtuple('BoxChars', 'tl tr bl br lr tb')
# boxchars = BoxChars('┌', '┐', '└', '┘', '│', '─')
# boxchars = BoxChars('╭', '╮', '╰', '╯', '│', '─')
boxchars = BoxChars('╭', '┐', '└', '╯', '│', '─')
# boxchars = BoxChars('┌', '╮', '╰', '┘', '│', '─')

def format(o):
    if isinstance(o, dict):
        width = max(len(k) for k in o)
        return '\n'.join(wrap(format_dict(o), width))
    elif isinstance(o, LIST_TYPES):
        return '\n'.join(format_list(o))
    else:
        return pprint.pformat(o)

def format_dict(d, indent=0, indent_first=True):
    colsep = ' │ '

    width = max(len(k) for k in d)
    for i, (k, v) in enumerate(d.items()):
        w = width if (i == 0 and not indent_first) else width + indent
        if v and isinstance(v, dict):
            lines = list(format_dict(v, width + indent + len(colsep), indent_first=False))
            yield f'{k:>{w}}{colsep}' + lines[0]
            for line in lines[1:]:
                yield line

        elif v and isinstance(v, LIST_TYPES):
            lines = list(format_list(v, width + indent + len(colsep), indent_first=False))
            yield f'{k:>{w}}{colsep}' + lines[0]
            for line in lines[1:]:
                yield line

        else:
            if v and isinstance(v, float):
                v = f'{v:.2}'
            yield f'{k:>{w}}{colsep}{v}'

def format_list(l, indent=0, indent_first=True):
    s = ', '.join(str(v) for v in l)
    if len(s) < 40:
        yield s
        return
    if l[0] and isinstance(l[0], dict):
        yield ''
    for i, v in enumerate(l):
        if v and isinstance(v, dict):
            width = max(len(k) for k in v)
            for line in wrap(format_dict(v), width):
                yield line
        else:
            w = 0 if (i == 0 and not indent_first) else indent
            yield f'{"":<{w}}{v}'

def wrap(lines, width):
    """Wraps lines with box characters."""
    lines = list(lines)
    dashes = boxchars.tb * (width + 2)
    yield f'{boxchars.tl}{dashes}{boxchars.tr}'
    for i, line in enumerate(lines):
        yield f'{boxchars.lr} {line}'
    yield f'{boxchars.bl}{dashes}{boxchars.br}'
