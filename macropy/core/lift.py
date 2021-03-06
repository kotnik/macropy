from macropy.core.macros import *


def u(node):
    """Stub to make the IDE happy"""
    pass

def unquote_search(node, unquotes):
    if isinstance(node, BinOp) and type(node.left) is Name and type(node.op) is Mod:
        if 'u' == node.left.id:
            unquotes.append(node.right)
            return Placeholder()
    return node

@expr_macro
def q(node):
    unquotes = []

    node = Walker(lambda x: unquote_search(x, unquotes)).recurse(node)
    unquote_calcs = [unparse(u) for u in unquotes]
    string = "interp_ast("+repr(node)+",["+",".join(unquote_calcs)+"])"
    out = parse_expr(string)

    return out

@block_macro
def q(node):
    unquotes = []
    body = Walker(lambda x: unquote_search(x, unquotes)).recurse(node.body)
    unquote_calcs = [unparse(u) for u in unquotes]
    body_txt = "interp_ast("+repr(body)+",["+",".join(unquote_calcs)+"])"
    out = parse_stmt(node.optional_vars.id + " = " + body_txt)
    return out
