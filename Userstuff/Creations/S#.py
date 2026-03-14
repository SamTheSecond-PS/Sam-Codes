# language: --S

import re, sys, pprint

LANGUAGE_NAME = "--S"

version = "0.0.1"

language_type = "mid-high level"

print(f"{LANGUAGE_NAME}-v-{version}")
print("--S is a good language, trust")

TOKEN_SPEC = [
    ("PERMISSION", r"\$"),
    ("CMD", r">>"),
    ("CHAIN", r"-"),

    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),

    ("WORK_IF", r"work\?"),
    ("WORK_ELIF", r"\?work"),
    ("WORK_ELSE", r"!work"),

    ("STRING", r"'[^']*'|\"[^\"]*\""),
    ("IDENT", r"[a-zA-Z_][a-zA-Z0-9_]*"),

    ("SKIP", r"[ \t\n]+"),
    ("MISMATCH", r"."),
]

state = {
    "last_worked": None
}

def tokenize(code):
    tokens = []
    regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)
    for match in re.finditer(regex, code):
        kind = match.lastgroup
        value = match.group()
        if kind == "SKIP":
            continue
        elif kind == "MISMATCH":
            raise SyntaxError(f"unknown token: {value}")
        else:
            tokens.append((kind, value))

    return tokens

def execute(node):
    # add command
    if node["type"] == "add":
        print(node["value"])
        return True

    # block command
    elif node["type"] == "block":
        for stmt in node["body"]:
            if not execute(stmt):
                return False
        return True

    return False

class ParseError(Exception):
    pass

def expect(tokens, i, kind=None, value=None):
    if i >= len(tokens):
        raise ParseError("unexpected end of input")

    tk_kind, tk_val = tokens[i]

    if kind and tk_kind != kind:
        raise ParseError(f"expected {kind}, got {tk_kind}")

    if value and tk_val != value:
        raise ParseError(f"expected {value}, got {tk_kind}")

    return tk_val, i + 1

def parse_add(tokens):
    i = 0

    _, i = expect(tokens, i, "IDENT", "add")
    _, i = expect(tokens, i, "CMD", ">>")

    value, i = expect(tokens, i, "STRING")

    dest = "console"

    if i < len(tokens) and tokens[i][0] == "IDENT" and tokens[i][1] == "to":
        _, i = expect(tokens, i, "IDENT", "to")
        _, i = expect(tokens, i, "CMD", ">>")
        dest, i = expect(tokens, i, "IDENT")

    if i != len(tokens):
        raise ParseError(f"unexpected token: {tokens[i]}")

    return {
        "type": "add",
        "value": value,
        "destination": dest
    }


def split_on_chain(tokens):
    segments = []
    current = []

    for token in tokens:
        if token[0] == "CHAIN":
            segments.append(current)
            current = []
        else:
            current.append(token)

    if current:
        segments.append(current)

    return segments

def collect_block(tokens, start):
    block = []
    depth = 0
    i = start

    while i < len(tokens):
        token = tokens[i]

        if token[0] == "LBRACE":
            depth += 1
            if depth > 1:
                block.append(token)

        elif token[0] == "RBRACE":
            depth -= 1
            if depth == 0:
                return block, i
            else:
                block.append(token)

        else:
            block.append(token)

        i += 1

    raise SyntaxError("unclosed block")

def parse_work_if(tokens):
    i = 0
    _

def parse(tokens):
    if not tokens:
        raise ParseError("empty statement")

    kind, val = tokens[0]

    if kind == "IDENT" and val == "add":
        return parse_add(tokens)



    raise ParseError(f"unknown command: {val}")

def run(tokens):
    segments = split_on_chain(tokens)

    for segment in segments:
        node = parse(segment)
        execute(node)

def parse_block(tokens):
    body = []
    segments = split_on_chain(tokens)

    for segment in segments:
        node = parse(segment)
        body.append(node)

    return body

code = 'add>>"hello" to>>console-add>>"bye" to>>console'
tokens = tokenize(code)
run(tokens)