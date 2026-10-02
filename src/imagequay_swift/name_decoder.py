# Derived public name API from ktool; Copyright (c) 0cyn 2022, MIT in LICENSE.
"""Length-checked simple nominal names; not a full Swift demangler."""
import imagequay_boundary as _name_boundary


def _identifier(text, start):
    end = start
    while end < len(text) and '0' <= text[end] <= '9':
        end += 1
    if end == start or end-start > 5 or text[start] == '0':
        return None
    count = int(text[start:end])
    if count == 0 or count > 16384 or end+count > len(text):
        return None
    value = text[end:end+count]
    if any(ord(char) < 32 for char in value):
        return None
    return value, end+count


def quay_demangle(name):
    if not isinstance(name, str):
        raise TypeError('Swift name must be text')
    if len(name) > 16384:
        raise ValueError('Swift name exceeds 16384 characters')
    if name.startswith('_TtC'):
        cursor, legacy = 4, True
    elif name.startswith(('$s', '$S', '_T0')):
        cursor, legacy = (3 if name.startswith('_T0') else 2), False
    else:
        return '', ''
    module = _identifier(name, cursor)
    if module is None:
        return '', ''
    nominal = _identifier(name, module[1])
    if nominal is None:
        return '', ''
    suffix = name[nominal[1]:]
    if (legacy and suffix) or (not legacy and suffix not in ('C', 'V', 'O')):
        return '', ''
    return module[0], nominal[0]


_name_boundary.module_contract(globals(), {'demangle': 'quay_demangle'})
