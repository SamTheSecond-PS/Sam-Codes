from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


# -----------------------------
# Lexer
# -----------------------------


@dataclass
class Token:
    kind: str
    value: str
    line: int
    col: int


class Lexer:
    KEYWORDS = {
        "fn",
        "let",
        "if",
        "else",
        "while",
        "return",
        "print",
        "true",
        "false",
    }

    TWO_CHAR = {"==", "!=", "<=", ">="}
    ONE_CHAR = set("+-*/(){};,=<>" )

    def __init__(self, text: str) -> None:
        self.text = text
        self.i = 0
        self.line = 1
        self.col = 1

    def _peek(self, n: int = 0) -> str:
        idx = self.i + n
        return self.text[idx] if idx < len(self.text) else ""

    def _advance(self) -> str:
        ch = self._peek()
        if not ch:
            return ""
        self.i += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def _skip_ws_and_comments(self) -> None:
        while True:
            ch = self._peek()
            if ch in (" ", "\t", "\r", "\n"):
                self._advance()
                continue
            if ch == "/" and self._peek(1) == "/":
                while self._peek() and self._peek() != "\n":
                    self._advance()
                continue
            break

    def tokens(self) -> List[Token]:
        out: List[Token] = []
        while True:
            self._skip_ws_and_comments()
            ch = self._peek()
            line, col = self.line, self.col

            if not ch:
                out.append(Token("EOF", "", line, col))
                return out

            pair = ch + self._peek(1)
            if pair in self.TWO_CHAR:
                self._advance()
                self._advance()
                out.append(Token(pair, pair, line, col))
                continue

            if ch in self.ONE_CHAR:
                self._advance()
                out.append(Token(ch, ch, line, col))
                continue

            if ch.isdigit():
                num = []
                while self._peek().isdigit() or self._peek() == ".":
                    num.append(self._advance())
                out.append(Token("NUMBER", "".join(num), line, col))
                continue

            if ch == '"':
                self._advance()
                s = []
                while self._peek() and self._peek() != '"':
                    if self._peek() == "\\":
                        self._advance()
                        nxt = self._peek()
                        if nxt == "n":
                            self._advance()
                            s.append("\n")
                        elif nxt == "t":
                            self._advance()
                            s.append("\t")
                        elif nxt in ('"', "\\"):
                            s.append(self._advance())
                        else:
                            s.append("\\")
                    else:
                        s.append(self._advance())
                if self._peek() != '"':
                    raise SyntaxError(f"Unterminated string at {line}:{col}")
                self._advance()
                out.append(Token("STRING", "".join(s), line, col))
                continue

            if ch.isalpha() or ch == "_":
                ident = []
                while self._peek().isalnum() or self._peek() == "_":
                    ident.append(self._advance())
                val = "".join(ident)
                kind = val if val in self.KEYWORDS else "IDENT"
                out.append(Token(kind, val, line, col))
                continue

            raise SyntaxError(f"Unexpected char '{ch}' at {line}:{col}")


# -----------------------------
# AST
# -----------------------------


class Node:
    pass


@dataclass
class Program(Node):
    funcs: List["FuncDef"]
    stmts: List[Node]


@dataclass
class FuncDef(Node):
    name: str
    params: List[str]
    body: List[Node]


@dataclass
class Block(Node):
    body: List[Node]


@dataclass
class Let(Node):
    name: str
    expr: Node


@dataclass
class Assign(Node):
    name: str
    expr: Node


@dataclass
class If(Node):
    cond: Node
    then_body: List[Node]
    else_body: List[Node]


@dataclass
class While(Node):
    cond: Node
    body: List[Node]


@dataclass
class Return(Node):
    expr: Optional[Node]


@dataclass
class Print(Node):
    expr: Node


@dataclass
class ExprStmt(Node):
    expr: Node


@dataclass
class Binary(Node):
    op: str
    left: Node
    right: Node


@dataclass
class Unary(Node):
    op: str
    expr: Node


@dataclass
class Number(Node):
    value: float


@dataclass
class String(Node):
    value: str


@dataclass
class Bool(Node):
    value: bool


@dataclass
class Name(Node):
    value: str


@dataclass
class Call(Node):
    callee: Node
    args: List[Node]


# -----------------------------
# Parser
# -----------------------------


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.i = 0

    def _peek(self, n: int = 0) -> Token:
        idx = self.i + n
        return self.tokens[idx] if idx < len(self.tokens) else self.tokens[-1]

    def _match(self, *kinds: str) -> bool:
        if self._peek().kind in kinds:
            self.i += 1
            return True
        return False

    def _expect(self, kind: str, msg: str) -> Token:
        tok = self._peek()
        if tok.kind != kind:
            raise SyntaxError(f"{msg} at {tok.line}:{tok.col}")
        self.i += 1
        return tok

    def parse(self) -> Program:
        funcs: List[FuncDef] = []
        stmts: List[Node] = []
        while self._peek().kind != "EOF":
            if self._peek().kind == "fn":
                funcs.append(self._func_def())
            else:
                stmts.append(self._statement())
        return Program(funcs=funcs, stmts=stmts)

    def _func_def(self) -> FuncDef:
        self._expect("fn", "Expected 'fn'")
        name = self._expect("IDENT", "Expected function name").value
        self._expect("(", "Expected '('")
        params: List[str] = []
        if self._peek().kind != ")":
            while True:
                params.append(self._expect("IDENT", "Expected parameter").value)
                if not self._match(","):
                    break
        self._expect(")", "Expected ')' after params")
        body = self._block().body
        return FuncDef(name=name, params=params, body=body)

    def _block(self) -> Block:
        self._expect("{", "Expected '{'")
        body: List[Node] = []
        while self._peek().kind != "}":
            if self._peek().kind == "EOF":
                tok = self._peek()
                raise SyntaxError(f"Unclosed block at {tok.line}:{tok.col}")
            body.append(self._statement())
        self._expect("}", "Expected '}'")
        return Block(body=body)

    def _statement(self) -> Node:
        tok = self._peek()
        if tok.kind == "let":
            self._match("let")
            name = self._expect("IDENT", "Expected variable name").value
            self._expect("=", "Expected '='")
            expr = self._expression()
            self._match(";")
            return Let(name=name, expr=expr)
        if tok.kind == "if":
            self._match("if")
            self._expect("(", "Expected '(' after if")
            cond = self._expression()
            self._expect(")", "Expected ')' after condition")
            then_body = self._block().body
            else_body: List[Node] = []
            if self._match("else"):
                else_body = self._block().body
            return If(cond=cond, then_body=then_body, else_body=else_body)
        if tok.kind == "while":
            self._match("while")
            self._expect("(", "Expected '(' after while")
            cond = self._expression()
            self._expect(")", "Expected ')' after condition")
            return While(cond=cond, body=self._block().body)
        if tok.kind == "return":
            self._match("return")
            expr = None if self._peek().kind == ";" else self._expression()
            self._match(";")
            return Return(expr=expr)
        if tok.kind == "print":
            self._match("print")
            expr = self._expression()
            self._match(";")
            return Print(expr=expr)
        if tok.kind == "{":
            return self._block()
        if tok.kind == "IDENT" and self._peek(1).kind == "=":
            name = self._expect("IDENT", "Expected identifier").value
            self._expect("=", "Expected '='")
            expr = self._expression()
            self._match(";")
            return Assign(name=name, expr=expr)
        expr = self._expression()
        self._match(";")
        return ExprStmt(expr=expr)

    def _expression(self) -> Node:
        return self._equality()

    def _equality(self) -> Node:
        expr = self._comparison()
        while self._peek().kind in ("==", "!="):
            op = self._peek().kind
            self.i += 1
            right = self._comparison()
            expr = Binary(op=op, left=expr, right=right)
        return expr

    def _comparison(self) -> Node:
        expr = self._term()
        while self._peek().kind in ("<", "<=", ">", ">="):
            op = self._peek().kind
            self.i += 1
            right = self._term()
            expr = Binary(op=op, left=expr, right=right)
        return expr

    def _term(self) -> Node:
        expr = self._factor()
        while self._peek().kind in ("+", "-"):
            op = self._peek().kind
            self.i += 1
            right = self._factor()
            expr = Binary(op=op, left=expr, right=right)
        return expr

    def _factor(self) -> Node:
        expr = self._unary()
        while self._peek().kind in ("*", "/"):
            op = self._peek().kind
            self.i += 1
            right = self._unary()
            expr = Binary(op=op, left=expr, right=right)
        return expr

    def _unary(self) -> Node:
        if self._peek().kind in ("-",):
            op = self._peek().kind
            self.i += 1
            return Unary(op=op, expr=self._unary())
        return self._call()

    def _call(self) -> Node:
        expr = self._primary()
        while self._match("("):
            args: List[Node] = []
            if self._peek().kind != ")":
                while True:
                    args.append(self._expression())
                    if not self._match(","):
                        break
            self._expect(")", "Expected ')' after args")
            expr = Call(callee=expr, args=args)
        return expr

    def _primary(self) -> Node:
        tok = self._peek()
        if self._match("NUMBER"):
            return Number(float(tok.value) if "." in tok.value else int(tok.value))
        if self._match("STRING"):
            return String(tok.value)
        if self._match("true"):
            return Bool(True)
        if self._match("false"):
            return Bool(False)
        if self._match("IDENT"):
            return Name(tok.value)
        if self._match("("):
            expr = self._expression()
            self._expect(")", "Expected ')'")
            return expr
        raise SyntaxError(f"Expected expression at {tok.line}:{tok.col}")


# -----------------------------
# Bytecode
# -----------------------------


@dataclass
class Instr:
    op: str
    arg: Any = None


@dataclass
class CompiledFunction:
    name: str
    params: List[str]
    code: List[Instr]
    call_count: int = 0
    jitted: Optional[Callable[..., Any]] = None


class Compiler:
    BIN_OPS = {
        "+": "ADD",
        "-": "SUB",
        "*": "MUL",
        "/": "DIV",
        "==": "EQ",
        "!=": "NE",
        "<": "LT",
        "<=": "LE",
        ">": "GT",
        ">=": "GE",
    }

    def __init__(self) -> None:
        self.functions: Dict[str, CompiledFunction] = {}
        self.code: List[Instr] = []

    def compile_program(self, prog: Program) -> Dict[str, CompiledFunction]:
        for fn in prog.funcs:
            self.compile_function(fn)

        self.code = []
        for st in prog.stmts:
            self.compile_stmt(st)
        self.emit("RET")
        self.functions["__main__"] = CompiledFunction("__main__", [], self.code)
        return self.functions

    def compile_function(self, fn: FuncDef) -> None:
        prev = self.code
        self.code = []
        for st in fn.body:
            self.compile_stmt(st)
        self.emit("CONST", None)
        self.emit("RET")
        self.functions[fn.name] = CompiledFunction(fn.name, fn.params, self.code)
        self.code = prev

    def emit(self, op: str, arg: Any = None) -> int:
        self.code.append(Instr(op, arg))
        return len(self.code) - 1

    def patch(self, index: int, value: int) -> None:
        self.code[index].arg = value

    def compile_block(self, body: List[Node]) -> None:
        for st in body:
            self.compile_stmt(st)

    def compile_stmt(self, node: Node) -> None:
        if isinstance(node, Let):
            self.compile_expr(node.expr)
            self.emit("STORE", node.name)
            return
        if isinstance(node, Assign):
            self.compile_expr(node.expr)
            self.emit("STORE", node.name)
            return
        if isinstance(node, Print):
            self.compile_expr(node.expr)
            self.emit("PRINT")
            return
        if isinstance(node, ExprStmt):
            self.compile_expr(node.expr)
            self.emit("POP")
            return
        if isinstance(node, Return):
            if node.expr is None:
                self.emit("CONST", None)
            else:
                self.compile_expr(node.expr)
            self.emit("RET")
            return
        if isinstance(node, Block):
            self.compile_block(node.body)
            return
        if isinstance(node, If):
            self.compile_expr(node.cond)
            jfalse = self.emit("JMP_IF_FALSE", None)
            self.compile_block(node.then_body)
            if node.else_body:
                jend = self.emit("JMP", None)
                self.patch(jfalse, len(self.code))
                self.compile_block(node.else_body)
                self.patch(jend, len(self.code))
            else:
                self.patch(jfalse, len(self.code))
            return
        if isinstance(node, While):
            start = len(self.code)
            self.compile_expr(node.cond)
            jfalse = self.emit("JMP_IF_FALSE", None)
            self.compile_block(node.body)
            self.emit("JMP", start)
            self.patch(jfalse, len(self.code))
            return
        raise TypeError(f"Unsupported statement node: {type(node).__name__}")

    def compile_expr(self, node: Node) -> None:
        if isinstance(node, Number):
            self.emit("CONST", node.value)
            return
        if isinstance(node, String):
            self.emit("CONST", node.value)
            return
        if isinstance(node, Bool):
            self.emit("CONST", node.value)
            return
        if isinstance(node, Name):
            self.emit("LOAD", node.value)
            return
        if isinstance(node, Unary):
            self.compile_expr(node.expr)
            if node.op == "-":
                self.emit("NEG")
                return
            raise TypeError(f"Unsupported unary op: {node.op}")
        if isinstance(node, Binary):
            self.compile_expr(node.left)
            self.compile_expr(node.right)
            self.emit(self.BIN_OPS[node.op])
            return
        if isinstance(node, Call):
            self.compile_expr(node.callee)
            for arg in node.args:
                self.compile_expr(arg)
            self.emit("CALL", len(node.args))
            return
        raise TypeError(f"Unsupported expression node: {type(node).__name__}")


# -----------------------------
# VM + JIT
# -----------------------------


@dataclass
class Frame:
    fn: CompiledFunction
    locals: Dict[str, Any]
    stack: List[Any]
    pc: int = 0


class JITCompiler:
    def compile_function(self, fn: CompiledFunction) -> Callable[["VirtualCPU", List[Any]], Any]:
        lines: List[str] = []
        lines.append("def _jit_func(vm, args):")
        lines.append("    stack = []")
        lines.append("    locals_ = {}")
        for idx, p in enumerate(fn.params):
            lines.append(f"    locals_[{p!r}] = args[{idx}] if len(args) > {idx} else None")
        lines.append("    pc = 0")
        lines.append("    while True:")
        lines.append(f"        if pc < 0 or pc >= {len(fn.code)}:")
        lines.append("            return None")

        for idx, ins in enumerate(fn.code):
            lines.append(f"        if pc == {idx}:")
            lines.extend(self._emit_instr(ins, idx))

        src = "\n".join(lines)
        ns: Dict[str, Any] = {}
        exec(src, ns, ns)
        return ns["_jit_func"]

    def _emit_instr(self, ins: Instr, idx: int) -> List[str]:
        op = ins.op
        arg = ins.arg
        n = idx + 1
        out: List[str] = []

        if op == "CONST":
            out += [f"            stack.append({arg!r})", f"            pc = {n}", "            continue"]
        elif op == "LOAD":
            out += [
                f"            _name = {arg!r}",
                "            if _name in locals_:",
                "                stack.append(locals_[_name])",
                "            elif _name in vm.functions:",
                "                stack.append(vm.functions[_name])",
                "            elif _name in vm.builtins:",
                "                stack.append(vm.builtins[_name])",
                "            else:",
                "                raise NameError(f\"Undefined name: {_name}\")",
                f"            pc = {n}",
                "            continue",
            ]
        elif op == "STORE":
            out += [f"            locals_[{arg!r}] = stack.pop()", f"            pc = {n}", "            continue"]
        elif op in ("ADD", "SUB", "MUL", "DIV", "EQ", "NE", "LT", "LE", "GT", "GE"):
            py = {
                "ADD": "+",
                "SUB": "-",
                "MUL": "*",
                "DIV": "/",
                "EQ": "==",
                "NE": "!=",
                "LT": "<",
                "LE": "<=",
                "GT": ">",
                "GE": ">=",
            }[op]
            out += [
                "            b = stack.pop()",
                "            a = stack.pop()",
                f"            stack.append(a {py} b)",
                f"            pc = {n}",
                "            continue",
            ]
        elif op == "NEG":
            out += ["            stack.append(-stack.pop())", f"            pc = {n}", "            continue"]
        elif op == "POP":
            out += ["            stack.pop()", f"            pc = {n}", "            continue"]
        elif op == "PRINT":
            out += ["            vm.output(stack.pop())", f"            pc = {n}", "            continue"]
        elif op == "JMP":
            out += [f"            pc = {arg}", "            continue"]
        elif op == "JMP_IF_FALSE":
            out += [
                "            c = stack.pop()",
                f"            pc = {arg} if not c else {n}",
                "            continue",
            ]
        elif op == "CALL":
            out += [
                f"            _argc = {int(arg)}",
                "            _args = [stack.pop() for _ in range(_argc)]",
                "            _args.reverse()",
                "            _callee = stack.pop()",
                "            stack.append(vm._call_value(_callee, _args))",
                f"            pc = {n}",
                "            continue",
            ]
        elif op == "RET":
            out += ["            return stack.pop() if stack else None"]
        else:
            out += [f"            raise RuntimeError('Unsupported op in JIT: {op}')"]

        return out


class VirtualCPU:
    def __init__(self, functions: Dict[str, CompiledFunction], jit: bool = True, jit_threshold: int = 30) -> None:
        self.functions = functions
        self.jit = jit
        self.jit_threshold = jit_threshold
        self.jit_compiler = JITCompiler()

        self.builtins: Dict[str, Callable[..., Any]] = {
            "print": self._builtin_print,
            "clock": self._builtin_clock,
            "int": int,
            "float": float,
            "str": str,
            "len": len,
        }

    def output(self, value: Any) -> None:
        print(value)

    @staticmethod
    def _builtin_print(*vals: Any) -> Any:
        print(*vals)
        return None

    @staticmethod
    def _builtin_clock() -> float:
        import time

        return time.time()

    def run(self, entry: str = "__main__") -> Any:
        fn = self.functions.get(entry)
        if fn is None:
            raise RuntimeError(f"Missing entry function: {entry}")
        return self._call_user_function(fn, [])

    def _resolve_name(self, frame: Frame, name: str) -> Any:
        if name in frame.locals:
            return frame.locals[name]
        if name in self.functions:
            return self.functions[name]
        if name in self.builtins:
            return self.builtins[name]
        raise NameError(f"Undefined name: {name}")

    def _call_value(self, callee: Any, args: List[Any]) -> Any:
        if isinstance(callee, CompiledFunction):
            return self._call_user_function(callee, args)
        if callable(callee):
            return callee(*args)
        raise TypeError(f"Object not callable: {callee!r}")

    def _call_user_function(self, fn: CompiledFunction, args: List[Any]) -> Any:
        fn.call_count += 1
        if self.jit and fn.jitted is None and fn.call_count >= self.jit_threshold:
            fn.jitted = self.jit_compiler.compile_function(fn)

        if fn.jitted is not None:
            return fn.jitted(self, args)

        locals_map = {p: (args[i] if i < len(args) else None) for i, p in enumerate(fn.params)}
        frame = Frame(fn=fn, locals=locals_map, stack=[], pc=0)
        code = fn.code

        while frame.pc < len(code):
            ins = code[frame.pc]
            op = ins.op
            arg = ins.arg

            if op == "CONST":
                frame.stack.append(arg)
                frame.pc += 1
            elif op == "LOAD":
                frame.stack.append(self._resolve_name(frame, arg))
                frame.pc += 1
            elif op == "STORE":
                frame.locals[arg] = frame.stack.pop()
                frame.pc += 1
            elif op == "ADD":
                b = frame.stack.pop()
                a = frame.stack.pop()
                frame.stack.append(a + b)
                frame.pc += 1
            elif op == "SUB":
                b = frame.stack.pop()
                a = frame.stack.pop()
                frame.stack.append(a - b)
                frame.pc += 1
            elif op == "MUL":
                b = frame.stack.pop()
                a = frame.stack.pop()
                frame.stack.append(a * b)
                frame.pc += 1
            elif op == "DIV":
                b = frame.stack.pop()
                a = frame.stack.pop()
                frame.stack.append(a / b)
                frame.pc += 1
            elif op == "NEG":
                frame.stack.append(-frame.stack.pop())
                frame.pc += 1
            elif op == "EQ":
                b = frame.stack.pop()
                a = frame.stack.pop()
                frame.stack.append(a == b)
                frame.pc += 1
            elif op == "NE":
                b = frame.stack.pop()
                a = frame.stack.pop()
                frame.stack.append(a != b)
                frame.pc += 1
            elif op == "LT":
                b = frame.stack.pop()
                a = frame.stack.pop()
                frame.stack.append(a < b)
                frame.pc += 1
            elif op == "LE":
                b = frame.stack.pop()
                a = frame.stack.pop()
                frame.stack.append(a <= b)
                frame.pc += 1
            elif op == "GT":
                b = frame.stack.pop()
                a = frame.stack.pop()
                frame.stack.append(a > b)
                frame.pc += 1
            elif op == "GE":
                b = frame.stack.pop()
                a = frame.stack.pop()
                frame.stack.append(a >= b)
                frame.pc += 1
            elif op == "POP":
                frame.stack.pop()
                frame.pc += 1
            elif op == "PRINT":
                self.output(frame.stack.pop())
                frame.pc += 1
            elif op == "JMP":
                frame.pc = int(arg)
            elif op == "JMP_IF_FALSE":
                cond = frame.stack.pop()
                frame.pc = int(arg) if not cond else frame.pc + 1
            elif op == "CALL":
                argc = int(arg)
                call_args = [frame.stack.pop() for _ in range(argc)]
                call_args.reverse()
                callee = frame.stack.pop()
                frame.stack.append(self._call_value(callee, call_args))
                frame.pc += 1
            elif op == "RET":
                return frame.stack.pop() if frame.stack else None
            else:
                raise RuntimeError(f"Unknown opcode: {op}")

        return None


# -----------------------------
# Frontend helpers (compile/run/repl)
# -----------------------------


def compile_source(source: str) -> Dict[str, CompiledFunction]:
    tokens = Lexer(source).tokens()
    ast = Parser(tokens).parse()
    return Compiler().compile_program(ast)


def run_source(source: str, jit: bool = True, jit_threshold: int = 30) -> Any:
    functions = compile_source(source)
    vm = VirtualCPU(functions, jit=jit, jit_threshold=jit_threshold)
    return vm.run("__main__")


def repl(jit: bool = True, jit_threshold: int = 30) -> None:
    print("MiniCPU Language REPL")
    print("Type :run to execute buffered code, :clear to clear, :quit to exit")

    buffer: List[str] = []
    balance = 0

    while True:
        prompt = "... " if balance > 0 else "mini> "
        try:
            line = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print()
            break

        stripped = line.strip()
        if stripped == ":quit":
            break
        if stripped == ":clear":
            buffer.clear()
            balance = 0
            print("buffer cleared")
            continue
        if stripped == ":run":
            src = "\n".join(buffer)
            try:
                run_source(src, jit=jit, jit_threshold=jit_threshold)
            except Exception as exc:  # noqa: BLE001
                print(f"error: {exc}")
            continue

        buffer.append(line)
        balance += line.count("{") - line.count("}")
        if balance < 0:
            balance = 0


def main() -> None:
    ap = argparse.ArgumentParser(description="Tiny language -> bytecode -> virtual CPU (+optional JIT)")
    ap.add_argument("file", nargs="?", help="Source file to run")
    ap.add_argument("--no-jit", action="store_true", help="Disable JIT")
    ap.add_argument("--jit-threshold", type=int, default=30, help="Calls before JIT compilation")
    ap.add_argument("--repl", action="store_true", help="Start interactive REPL")
    args = ap.parse_args()

    jit = not args.no_jit

    if args.repl or not args.file:
        repl(jit=jit, jit_threshold=args.jit_threshold)
        return

    source = Path(args.file).read_text(encoding="utf-8")
    run_source(source, jit=jit, jit_threshold=args.jit_threshold)


if __name__ == "__main__":
    main()
