from __future__ import annotations

import json
import shlex
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Deque, Dict, Generator, List, Optional, Tuple


@dataclass
class VNode:
    name: str
    is_dir: bool
    parent: Optional["VNode"] = None
    children: Dict[str, "VNode"] = field(default_factory=dict)
    content: str = ""

    def path(self) -> str:
        if self.parent is None:
            return "/"
        parts = []
        node: Optional[VNode] = self
        while node and node.parent is not None:
            parts.append(node.name)
            node = node.parent
        return "/" + "/".join(reversed(parts))


class VirtualFileSystem:
    def __init__(self) -> None:
        self.root = VNode(name="/", is_dir=True, parent=None)
        self.cwd = self.root

    def _resolve(self, path: str) -> Optional[VNode]:
        if not path:
            return self.cwd
        node = self.root if path.startswith("/") else self.cwd
        parts = [p for p in path.split("/") if p not in ("", ".")]
        for part in parts:
            if part == "..":
                if node.parent is not None:
                    node = node.parent
                continue
            if not node.is_dir or part not in node.children:
                return None
            node = node.children[part]
        return node

    def _split_parent(self, path: str) -> Tuple[Optional[VNode], Optional[str]]:
        cleaned = path.rstrip("/")
        if cleaned in ("", "/"):
            return None, None
        if "/" in cleaned:
            parent_path, name = cleaned.rsplit("/", 1)
            parent = self._resolve(parent_path if parent_path else "/")
        else:
            parent = self.cwd
            name = cleaned
        if not name or name in (".", ".."):
            return None, None
        return parent, name

    def mkdir(self, path: str) -> Tuple[bool, str]:
        parent, name = self._split_parent(path)
        if parent is None or not parent.is_dir:
            return False, "mkdir: invalid parent path"
        if name in parent.children:
            return False, f"mkdir: {name}: already exists"
        parent.children[name] = VNode(name=name, is_dir=True, parent=parent)
        return True, ""

    def touch(self, path: str) -> Tuple[bool, str]:
        parent, name = self._split_parent(path)
        if parent is None or not parent.is_dir:
            return False, "touch: invalid parent path"
        if name in parent.children:
            node = parent.children[name]
            if node.is_dir:
                return False, "touch: cannot touch a directory"
            return True, ""
        parent.children[name] = VNode(name=name, is_dir=False, parent=parent)
        return True, ""

    def write_file(self, path: str, text: str) -> Tuple[bool, str]:
        node = self._resolve(path)
        if node is None:
            ok, err = self.touch(path)
            if not ok:
                return False, err
            node = self._resolve(path)
        if node is None or node.is_dir:
            return False, "write: target is not a file"
        node.content = text
        return True, ""

    def cat(self, path: str) -> Tuple[bool, str]:
        node = self._resolve(path)
        if node is None:
            return False, "cat: file not found"
        if node.is_dir:
            return False, "cat: cannot read directory"
        return True, node.content

    def ls(self, path: str = "") -> Tuple[bool, str]:
        node = self._resolve(path) if path else self.cwd
        if node is None:
            return False, "ls: path not found"
        if not node.is_dir:
            return True, node.name
        names = sorted(node.children)
        rendered = [name + ("/" if node.children[name].is_dir else "") for name in names]
        return True, "  ".join(rendered)

    def cd(self, path: str) -> Tuple[bool, str]:
        node = self._resolve(path)
        if node is None:
            return False, "cd: path not found"
        if not node.is_dir:
            return False, "cd: not a directory"
        self.cwd = node
        return True, ""

    def pwd(self) -> str:
        return self.cwd.path()

    def rm(self, path: str) -> Tuple[bool, str]:
        node = self._resolve(path)
        if node is None or node.parent is None:
            return False, "rm: invalid path"
        del node.parent.children[node.name]
        return True, ""

    def _node_to_dict(self, node: VNode) -> dict:
        if node.is_dir:
            return {
                "name": node.name,
                "is_dir": True,
                "children": [self._node_to_dict(child) for child in node.children.values()],
            }
        return {"name": node.name, "is_dir": False, "content": node.content}

    def _dict_to_node(self, data: dict, parent: Optional[VNode]) -> VNode:
        node = VNode(name=data["name"], is_dir=data["is_dir"], parent=parent)
        if node.is_dir:
            for child in data.get("children", []):
                child_node = self._dict_to_node(child, node)
                node.children[child_node.name] = child_node
        else:
            node.content = data.get("content", "")
        return node

    def save(self, filepath: str) -> Tuple[bool, str]:
        payload = {"root": self._node_to_dict(self.root), "cwd": self.cwd.path()}
        try:
            Path(filepath).write_text(json.dumps(payload, indent=2), encoding="utf-8")
            return True, ""
        except OSError as exc:
            return False, f"savefs: {exc}"

    def load(self, filepath: str) -> Tuple[bool, str]:
        try:
            raw = Path(filepath).read_text(encoding="utf-8")
            payload = json.loads(raw)
        except (OSError, json.JSONDecodeError) as exc:
            return False, f"loadfs: {exc}"

        root_data = payload.get("root")
        if not isinstance(root_data, dict):
            return False, "loadfs: malformed image"

        self.root = self._dict_to_node(root_data, None)
        self.cwd = self._resolve(payload.get("cwd", "/")) or self.root
        return True, ""


class MemoryManager:
    def __init__(self, total_size: int = 256) -> None:
        self.total_size = total_size
        self.free_blocks: List[Tuple[int, int]] = [(0, total_size)]
        self.allocations: Dict[int, Tuple[int, int]] = {}

    def _merge_free(self) -> None:
        self.free_blocks.sort(key=lambda b: b[0])
        merged: List[Tuple[int, int]] = []
        for start, size in self.free_blocks:
            if not merged:
                merged.append((start, size))
                continue
            last_start, last_size = merged[-1]
            if last_start + last_size == start:
                merged[-1] = (last_start, last_size + size)
            else:
                merged.append((start, size))
        self.free_blocks = merged

    def allocate(self, pid: int, size: int) -> Tuple[bool, str]:
        if size <= 0:
            return False, "memory: size must be > 0"
        for idx, (start, block_size) in enumerate(self.free_blocks):
            if block_size >= size:
                self.allocations[pid] = (start, size)
                if block_size == size:
                    self.free_blocks.pop(idx)
                else:
                    self.free_blocks[idx] = (start + size, block_size - size)
                return True, ""

        free_total = sum(block[1] for block in self.free_blocks)
        if free_total >= size:
            return False, "memory: allocation failed due to fragmentation"
        return False, "memory: out of memory"

    def free(self, pid: int) -> None:
        block = self.allocations.pop(pid, None)
        if block is None:
            return
        self.free_blocks.append(block)
        self._merge_free()

    def status_lines(self) -> List[str]:
        used = sum(size for _, size in self.allocations.values())
        free = self.total_size - used
        lines = [f"Total={self.total_size} Used={used} Free={free}"]
        if self.allocations:
            for pid, (start, size) in sorted(self.allocations.items()):
                lines.append(f"  PID {pid}: start={start} size={size}")
        else:
            lines.append("  No allocations")
        lines.append(
            "  Free blocks: "
            + ", ".join(f"[{start}:{start + size - 1}]" for start, size in self.free_blocks)
        )
        return lines


ProgramFactory = Callable[[List[str]], Generator[str, None, None]]


class ProgramRegistry:
    def __init__(self) -> None:
        self.programs: Dict[str, ProgramFactory] = {
            "count": self.count_program,
            "echo": self.echo_program,
            "fib": self.fib_program,
        }

    def names(self) -> List[str]:
        return sorted(self.programs)

    def create(self, name: str, args: List[str]) -> Optional[Generator[str, None, None]]:
        factory = self.programs.get(name)
        return factory(args) if factory else None

    @staticmethod
    def count_program(args: List[str]) -> Generator[str, None, None]:
        n = int(args[0]) if args else 5
        for i in range(1, n + 1):
            yield f"count: {i}"

    @staticmethod
    def echo_program(args: List[str]) -> Generator[str, None, None]:
        if not args:
            yield "echo:"
            return
        for token in args:
            yield f"echo: {token}"

    @staticmethod
    def fib_program(args: List[str]) -> Generator[str, None, None]:
        n = int(args[0]) if args else 8
        a, b = 0, 1
        for _ in range(max(n, 0)):
            yield f"fib: {a}"
            a, b = b, a + b


@dataclass
class Process:
    pid: int
    name: str
    memory: int
    program: Generator[str, None, None]
    state: str = "ready"


class ProcessManager:
    def __init__(self, memory: MemoryManager, registry: ProgramRegistry) -> None:
        self.memory = memory
        self.registry = registry
        self.next_pid = 1
        self.processes: Dict[int, Process] = {}
        self.ready: Deque[int] = deque()

    def launch(self, name: str, args: List[str], memory_size: int) -> Tuple[bool, str]:
        prog = self.registry.create(name, args)
        if prog is None:
            return False, f"run: unknown program '{name}'"

        pid = self.next_pid
        ok, err = self.memory.allocate(pid, memory_size)
        if not ok:
            return False, err

        process = Process(pid=pid, name=name, memory=memory_size, program=prog)
        self.processes[pid] = process
        self.ready.append(pid)
        self.next_pid += 1
        return True, f"started PID {pid} ({name}, mem={memory_size})"

    def kill(self, pid: int) -> Tuple[bool, str]:
        proc = self.processes.pop(pid, None)
        if proc is None:
            return False, "kill: pid not found"
        proc.state = "terminated"
        self.memory.free(pid)
        self.ready = deque(p for p in self.ready if p != pid)
        return True, f"killed PID {pid}"

    def tick(self, cycles: int = 1) -> List[str]:
        output: List[str] = []
        for _ in range(max(1, cycles)):
            if not self.ready:
                output.append("scheduler: idle")
                break
            pid = self.ready.popleft()
            proc = self.processes.get(pid)
            if proc is None:
                continue
            proc.state = "running"
            try:
                line = next(proc.program)
                output.append(f"PID {pid} -> {line}")
                proc.state = "ready"
                self.ready.append(pid)
            except StopIteration:
                proc.state = "terminated"
                output.append(f"PID {pid} finished")
                self.memory.free(pid)
                del self.processes[pid]
        return output

    def ps_lines(self) -> List[str]:
        if not self.processes:
            return ["no running processes"]
        lines = []
        for pid, proc in sorted(self.processes.items()):
            lines.append(f"PID={pid} NAME={proc.name} STATE={proc.state} MEM={proc.memory}")
        return lines


class MiniOS:
    def __init__(self) -> None:
        self.fs = VirtualFileSystem()
        self.memory = MemoryManager(total_size=256)
        self.registry = ProgramRegistry()
        self.pm = ProcessManager(self.memory, self.registry)
        self.running = True

    @staticmethod
    def split_chained_commands(line: str) -> List[Tuple[str, str]]:
        segments: List[Tuple[str, str]] = []
        current: List[str] = []
        in_quote: Optional[str] = None
        relation = "start"
        i = 0
        while i < len(line):
            ch = line[i]
            if ch in ("'", '"'):
                if in_quote == ch:
                    in_quote = None
                elif in_quote is None:
                    in_quote = ch
                current.append(ch)
                i += 1
                continue
            if in_quote is None and line.startswith("&&", i):
                text = "".join(current).strip()
                if text:
                    segments.append((relation, text))
                relation = "and"
                current = []
                i += 2
                continue
            if in_quote is None and ch == ";":
                text = "".join(current).strip()
                if text:
                    segments.append((relation, text))
                relation = "seq"
                current = []
                i += 1
                continue
            current.append(ch)
            i += 1
        text = "".join(current).strip()
        if text:
            segments.append((relation, text))
        return segments

    def execute_line(self, line: str) -> bool:
        segments = self.split_chained_commands(line)
        last_ok = True
        for relation, cmd in segments:
            if relation == "and" and not last_ok:
                continue
            last_ok = self.execute_command(cmd)
        return last_ok

    def execute_command(self, cmd_line: str) -> bool:
        try:
            tokens = shlex.split(cmd_line)
        except ValueError as exc:
            print(f"parse error: {exc}")
            return False

        if not tokens:
            return True

        cmd, *args = tokens

        if cmd in ("exit", "quit"):
            self.running = False
            return True

        if cmd == "help":
            print(
                "Commands: help, exit, pwd, ls [path], cd <path>, mkdir <path>, "
                "touch <path>, write <path> <text>, cat <path>, rm <path>, "
                "savefs <file>, loadfs <file>, programs, run <name> [args] [--mem N], "
                "tick [n], ps, kill <pid>, mem"
            )
            print("Chaining supported: ';' and '&&'")
            return True

        if cmd == "pwd":
            print(self.fs.pwd())
            return True

        if cmd == "ls":
            ok, msg = self.fs.ls(args[0] if args else "")
            if not ok:
                print(msg)
                return False
            print(msg)
            return True

        if cmd == "cd":
            if not args:
                print("cd: missing path")
                return False
            ok, msg = self.fs.cd(args[0])
            if not ok:
                print(msg)
                return False
            return True

        if cmd == "mkdir":
            if not args:
                print("mkdir: missing path")
                return False
            ok, msg = self.fs.mkdir(args[0])
            if not ok:
                print(msg)
            return ok

        if cmd == "touch":
            if not args:
                print("touch: missing path")
                return False
            ok, msg = self.fs.touch(args[0])
            if not ok:
                print(msg)
            return ok

        if cmd == "write":
            if len(args) < 2:
                print("write: usage write <path> <text>")
                return False
            ok, msg = self.fs.write_file(args[0], " ".join(args[1:]))
            if not ok:
                print(msg)
            return ok

        if cmd == "cat":
            if not args:
                print("cat: missing path")
                return False
            ok, msg = self.fs.cat(args[0])
            if not ok:
                print(msg)
                return False
            print(msg)
            return True

        if cmd == "rm":
            if not args:
                print("rm: missing path")
                return False
            ok, msg = self.fs.rm(args[0])
            if not ok:
                print(msg)
            return ok

        if cmd == "savefs":
            if not args:
                print("savefs: missing file")
                return False
            ok, msg = self.fs.save(args[0])
            if not ok:
                print(msg)
                return False
            print(f"saved to {args[0]}")
            return True

        if cmd == "loadfs":
            if not args:
                print("loadfs: missing file")
                return False
            ok, msg = self.fs.load(args[0])
            if not ok:
                print(msg)
                return False
            print(f"loaded from {args[0]}")
            return True

        if cmd == "programs":
            print(" ".join(self.registry.names()))
            return True

        if cmd == "run":
            if not args:
                print("run: usage run <program> [args] [--mem N]")
                return False
            mem = 16
            run_args: List[str] = []
            i = 1
            while i < len(args):
                if args[i] == "--mem":
                    if i + 1 >= len(args):
                        print("run: --mem needs a value")
                        return False
                    try:
                        mem = int(args[i + 1])
                    except ValueError:
                        print("run: memory must be an integer")
                        return False
                    i += 2
                else:
                    run_args.append(args[i])
                    i += 1
            ok, msg = self.pm.launch(args[0], run_args, mem)
            print(msg)
            return ok

        if cmd == "tick":
            cycles = 1
            if args:
                try:
                    cycles = int(args[0])
                except ValueError:
                    print("tick: cycles must be an integer")
                    return False
            for line in self.pm.tick(cycles):
                print(line)
            return True

        if cmd == "ps":
            for line in self.pm.ps_lines():
                print(line)
            return True

        if cmd == "kill":
            if not args:
                print("kill: missing pid")
                return False
            try:
                pid = int(args[0])
            except ValueError:
                print("kill: pid must be integer")
                return False
            ok, msg = self.pm.kill(pid)
            print(msg)
            return ok

        if cmd == "mem":
            for line in self.memory.status_lines():
                print(line)
            return True

        print(f"unknown command: {cmd}")
        return False

    def repl(self) -> None:
        print("MiniOS Simulator - type 'help' for commands")
        while self.running:
            try:
                line = input(f"miniOS:{self.fs.pwd()}$ ")
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if line.strip():
                self.execute_line(line)


def main() -> None:
    os_sim = MiniOS()
    os_sim.repl()


if __name__ == "__main__":
    main()
