import html


def escape(s, quote=True):
    s = html.escape(s, quote)
    if quote:
        s = s.replace('"', "&quot;")
    return s


def parse_header(line):
    parts = line.split(';')
    key = parts[0].strip()
    pdict = {}
    for p in parts[1:]:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1:].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict
