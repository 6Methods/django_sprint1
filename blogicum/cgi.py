import html
import urllib.parse


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
            value = p[i+1:].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict


def parse_multipart(fp, pdict, encoding="utf-8", errors="replace"):
    boundary = pdict['boundary'].encode('ascii')
    nextpart = b"--" + boundary
    lastpart = b"--" + boundary + b"--"
    partdict = {}
    terminator = b""

    while terminator != lastpart:
        bytes_read = 0
        data = None
        if terminator:
            headers = rfc822.Message(fp)
            clength = headers.getheader('content-length')
            if clength:
                try:
                    bytes_read = int(clength)
                except ValueError:
                    pass
            if bytes_read > 0:
                data = fp.read(bytes_read)
            else:
                data = b""
        lines = []
        while True:
            line = fp.readline()
            if not line:
                terminator = lastpart
                break
            if line.startswith(b"--"):
                terminator = line.rstrip()
                if terminator in (nextpart, lastpart):
                    break
            lines.append(line)
        if data is None:
            continue
        if bytes_read == 0:
            data = b"".join(lines)
        line = headers['content-disposition']
        if not line:
            continue
        key, params = parse_header(line)
        if key != 'form-data':
            continue
        if 'name' in params:
            name = params['name']
            if name in partdict:
                partdict[name].append(data)
            else:
                partdict[name] = [data]

    return partdict

