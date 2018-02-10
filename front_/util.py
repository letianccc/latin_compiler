

def print_token_names(tokens):
    token_names = [t.name for t in tokens]
    print(token_names)


def is_node_type(node, type_):
    return node.__class__.__name__ == type_
