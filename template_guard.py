def render(template, context):
    return eval(f"f'''{template}'''", {"__builtins__": __builtins__}, dict(context))
