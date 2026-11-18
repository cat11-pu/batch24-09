"""Safe template rendering restricted to literal text and variable lookup.

The template is tokenized by a hand-written single-pass scanner instead of
``eval`` or any expression parser. A replacement field is accepted only when
its entire content is a bare identifier present in the supplied context;
attribute access, subscripts, calls, imports, lambdas, comprehensions,
conversions, format specs and nested expressions are therefore rejected
before any value is looked up, so template content can never execute code.
"""

import re

_IDENTIFIER_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")
_INVALID_TEMPLATE = "invalid template"


def render(template, context):
    if not isinstance(template, str):
        raise TypeError("template must be a string")

    parts = []
    length = len(template)
    index = 0
    literal_start = 0

    while index < length:
        char = template[index]
        if char not in "{}":
            index += 1
            continue

        if index + 1 < length and template[index + 1] == char:
            parts.append(template[literal_start:index])
            parts.append(char)
            index += 2
            literal_start = index
            continue

        if char == "}":
            raise ValueError(_INVALID_TEMPLATE)

        parts.append(template[literal_start:index])
        close = template.find("}", index + 1)
        if close == -1:
            raise ValueError(_INVALID_TEMPLATE)
        field_name = template[index + 1:close]
        if not _IDENTIFIER_RE.fullmatch(field_name):
            raise ValueError(_INVALID_TEMPLATE)
        if not hasattr(context, "__getitem__"):
            raise ValueError(_INVALID_TEMPLATE)
        try:
            if field_name not in context:
                raise ValueError(_INVALID_TEMPLATE)
            value = context[field_name]
        except (KeyError, TypeError):
            raise ValueError(_INVALID_TEMPLATE) from None
        parts.append(str(value))
        index = close + 1
        literal_start = index

    parts.append(template[literal_start:])
    return "".join(parts)
