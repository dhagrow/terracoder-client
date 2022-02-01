import collections

def world_state(data):
    return format(data)

def drone_get(data):
    return format(data)

def drone_state(data):
    return '\n'.join(format(drone) for drone in data)

BoxChars = collections.namedtuple('BoxChars', 'tl tr bl br lr tb')

def format(d, colsep=None, boxchars=None):
    colsep = ' │ ' if colsep is None else colsep
    # boxchars = boxchars or BoxChars('┌', '┐', '└', '┘', '│', '─')
    # boxchars = boxchars or BoxChars('╭', '╮', '╰', '╯', '│', '─')
    # boxchars = boxchars or BoxChars('╭', '┐', '└', '╯', '│', '─')
    boxchars = boxchars or BoxChars('┌', '╮', '╰', '┘', '│', '─')

    def format_dict(d, indent=0, indent_first=True):
        width = max(len(k) for k in d)
        for i, (k, v) in enumerate(d.items()):
            w = width if (i == 0 and not indent_first) else width + indent
            if v and isinstance(v, dict):
                lines = list(format_dict(v, width + indent + len(colsep), indent_first=False))
                yield f'{k:>{w}}{colsep}' + lines[0]
                for line in lines[1:]:
                    yield line

            elif v and isinstance(v, (tuple, list, set)):
                lines = list(format_list(v, width + indent + len(colsep), indent_first=False))
                yield f'{k:>{w}}{colsep}' + lines[0]
                for line in lines[1:]:
                    yield line

            else:
                yield f'{k:>{w}}{colsep}{v}'

    def format_list(l, indent, indent_first=True):
        s = ', '.join(str(v) for v in l)
        if len(s) < 40:
            yield s
            return
        for i, v in enumerate(l):
            if v and isinstance(v, dict):
                yield ''
                width = max(len(k) for k in v)
                for line in wrap(format_dict(v), width):
                    yield line
            else:
                w = 0 if (i == 0 and not indent_first) else indent
                yield f'{"":<{w}}{v}'

    def wrap(lines, width):
        lines = list(lines)
        dashes = boxchars.tb * (width + 2)
        yield f'{boxchars.tl}{dashes}{boxchars.tr}'
        for i, line in enumerate(lines):
            yield f'{boxchars.lr} {line}'
        yield f'{boxchars.bl}{dashes}{boxchars.br}'

    width = max(len(k) for k in d)
    return '\n'.join(wrap(format_dict(d), width))
