code = '''prt~"hello"\nx = 10\nprt~x'''

env = {}

def tokenize(code):
    tokens = []
    i = 0

    codes = ["inp~", "prt~", "if~", "else~", "ef~"]

    while i < len(code):
        c = code[i]

        if c.isspace():
            i += 1
            continue


        elif code[i:i+3] == "if~":
            tokens.append(("IF", "if~"))
            i += 3
            continue

        elif c == "|":
            i += 1
            expr = ""
            while i < len(code) and code[i] != "|":
                expr += code[i]
                i += 1
            tokens.append(("EXPRESSION", str(expr)))
            i += 1
            continue

        elif code[i:i+5] == "else~":
            tokens.append(("ELSE","else~"))
            i += 5
            continue

        elif code[i:i+3] == "ef~":
            tokens.append(("ELIF", "ef~"))
            i += 3
            continue
                          
        elif c == '"':
            i += 1
            string = ""
            while i < len(code) and code[i] != '"':
                string += code[i]
                i += 1
            tokens.append(("STRING", string))
            i += 1
            continue

        elif code[i:i+4] == "prt~":
            tokens.append(("PRINT","prt~"))
            i += 4
            continue

        elif code[i:i+4] == "inp~":
            tokens.append(("INPUT", "inp~"))
            i += 4
            continue

        elif c == "{":
            i += 1
            x = 0
            codes = []
            currstr = ""
            while i < len(code) and x > 0:
                if code[i] == "{":
                    x += 1
                elif code[i] == "}":
                    x -= 1
                    if x == 0:
                        i += 1
                        break
                currstr += code[i]
                i += 1
            tokens.append(("BLOCK", currstr))
            i += 1
            continue

        elif c == "(":
            i += 1
            x = 1
            codes = []
            currstr = ""
            while i < len(code) and x > 0:
                if code[i] == "(":
                    x += 1
                elif code[i] == ")":
                    x -= 1
                    if x == 0:
                        i += 1
                        break
                currstr += code[i]
                i += 1
            tokens.append(("PBLOCK", currstr))
            continue
        
        elif c.isalpha():
            if not any(code.startswith(k, i) for k in codes):
                name = c
                i += 1
                while i < len(code) and code[i].isalnum():
                    name += code[i]
                    i += 1
                tokens.append(("IDENT", str(name)))
                continue
        
        elif c.isdigit():
            num = c
            i += 1
            while i < len(code) and code[i].isdigit():
                num += code[i]
                i += 1
            tokens.append(("NUMBER", int(num)))
            continue

        elif c == '=':
            tokens.append(("EQUAL","="))
            i += 1
            continue


        elif c == '+':
            tokens.append(("PLUS", '+'))
            i += 1
            continue

        elif c == '*':
            tokens.append(("MULTIPLICATION", '*'))
            i += 1
            continue

        elif c == '/':
            tokens.append(("DIVISION", '/'))
            i += 1
            continue
 
    return tokens




def parse_expr(tokens):
    left = parse_term(tokens)
    while tokens and tokens[0][0] in ("PLUS", "MINUS"):
        op = tokens.pop(0)
        right = parse_term(tokens)
        left = {
            "type":"add" if op[0] == "PLUS" else "sub", "left":left, "right":right
        }
    return left

def parse_term(tokens):
    left = parse_fact(tokens)
    while tokens and tokens[0][0] in ("MULTIPLICATION", "DIVISION"):
        op = tokens.pop(0)
        right = parse_fact(tokens)
        left = {"type":"mul" if op[0] == "MULTIPLICATION" else "div", "left":left, "right":right}
    return left

def parse_fact(tokens):
    t = tokens.pop(0)
    if t[0] == "NUMBER":
        return {
            "type":"number",
            "value":t[1]    
        }
    if t[0] == "IDENT":
        return {
            "type":"ident",
            "value":t[1]
        }
    if t[0] == "PBLOCK":
        return {
            "type":"pb",
            "value":parse_expr(tokenize(t[1]))
        }
    if t[0] == "STRING":
        return {
            "type":"string",
            "value":t[1]
        }
    return {"type": t[0].lower(), "value": t[1]}
    



def parse(tokens):
    if len(tokens) > 3 and tokens[1][0] == "EQUAL":
        return {
            "type":"assign",
            "left":tokens[0][1],
            "right": parse_expr(tokens[2:])
        }
    
    if tokens[0][0] == "PRINT":
        return {
            "type":"print",
            "value":parse_expr(tokens[1:])
        }
    
    if tokens[0][0] == "INPUT":
        return {
            "type":"input",
            "value":tokens[1]
        }
    
    if tokens[0][0] == "IF":
        return {
            "type":"if",
            "expr":tokens[1]
        }

    if tokens[0][0] == "ELIF":
        return {
            "type":"elif",
            "expr":tokens[1]
        }
     
    if tokens[0][0] == "ELSE":
        return {
            "type":"else",
            "expr":tokens[1]
        }
  
    return parse_expr(tokens)

def evale(par, env):
    if isinstance(par, tuple):
        if par[0] == "NUMBER":
            return par[1]
        if par[0] == "IDENT":
            return env[par[1]]
        if par[0] == "STRING":
            return par[1]
        
    if isinstance(par, dict):
        if par["type"] == "pb":
            return evale(par["value"], env)
        if par["type"] == "add":
            return evale(par["left"], env) + evale(par["right"], env)
        if par["type"] == "sub":
            return evale(par["left"], env) - evale(par["right"], env)
        if par["type"] == "mul":
            return evale(par["left"], env) * evale(par["right"], env)
        if par["type"] == "div":
            return evale(par["left"], env) / evale(par["right"], env)

        if par["type"] == "assign":
            value = evale(par["right"], env)
            env[par["left"]] = value
            return value 

        if par["type"] == "print":
            value = evale(par["value"], env)
            print(value)
            return value
        
        if par["type"] == "input":
            value = evale(par["value"], env)
            rtnv = input(value)
            return rtnv

        if par["type"] == "string":
            return par["value"] 
            
        

def run(code):
    last = None
    lines = code.split('\n')
    for line in lines:
        if not line.strip():
            continue
        tokens = tokenize(line)
        ast = parse(tokens)
        last = evale(ast, env)  
    return last


run(code)
print(env)

