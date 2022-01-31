def world_state(data):
    return format(data)

def drone_get(data):
    return format(data)

def drone_state(data):
    return '\n'.join(format(drone) for drone in data)

def format(d, colsep=' │ '):
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
        if len(s) < 20:
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
        dashes = '─' * (width + 2)
        yield f'┌{dashes}┐'
        for i, line in enumerate(lines):
            yield '│ ' + line
        yield f'└{dashes}┘'

    width = max(len(k) for k in d)
    return '\n'.join(wrap(format_dict(d), width))
