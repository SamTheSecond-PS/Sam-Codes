import os, shutil, shlex, sys, base64, subprocess, socket, hashlib

print("ETHICAL HACKING TOOLKIT")
print("-----------------------")


def ping(host):
    flag = "-n" if os.name == "nt" else "-c"
    command = f"ping {flag} 1 {host}"
    result = os.system(command)

    if result == 0:
        print(f"{host} is reachable")
    else:
        print(f"{host} is unreachable or blocking requests")


def find(name, path="."):
    found = False
    found_paths = []

    # Search current location
    for root, dirs, files in os.walk(path):
        try:
            if name in files:
                found_paths.append(os.path.join(root, name))
                found = True
            if name in dirs:
                found_paths.append(os.path.join(root, name))
                found = True
        except PermissionError:
            continue

    if not found:
        x = input("Not found. Search whole system? [y/n]: ")
        if x.lower().startswith("n"):
            print("Cancelled.")
            return
        # Whole system search
        for root, dirs, files in os.walk("C:/"):
            try:
                if name in files:
                    found_paths.append(os.path.join(root, name))
                    found = True
                if name in dirs:
                    found_paths.append(os.path.join(root, name))
                    found = True
            except PermissionError:
                continue

    if found:
        print("Found:")
        for p in found_paths:
            print("  ", p)
    else:
        print("Still not found.")


def showenv():
    for k, v in os.environ.items():
        print(f"{k} = {v}")

def scanport(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((host, int(port)))
    if result == 0:
        print(f"Port {port} on {host} is OPEN")
    else:
        print(f"Port {port} on {host} is CLOSED")
    s.close()


# -----------------------------------------------------------
# 2) WHOIS lookup (Windows requires 'whois' installed)
# -----------------------------------------------------------
def whois(domain):
    try:
        output = subprocess.check_output(["whois", domain], text=True)
        print(output)
    except Exception:
        print("whois not available (install 'whois' first).")


# -----------------------------------------------------------
# 3) DNS Lookup
# -----------------------------------------------------------
def dnslookup(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"{domain} -> {ip}")
    except socket.gaierror:
        print("DNS lookup failed.")


# -----------------------------------------------------------
# 4) HASH a string (SHA256)
# -----------------------------------------------------------
def hashsha(text):
    h = hashlib.sha256(text.encode()).hexdigest()
    print("SHA256:", h)


# -----------------------------------------------------------
# 5) Base64 encode/decode
# -----------------------------------------------------------
def b64(action, text):
    try:
        if action == "enc":
            out = base64.b64encode(text.encode()).decode()
            print("Base64 Encoded:", out)
        elif action == "dec":
            out = base64.b64decode(text.encode()).decode()
            print("Base64 Decoded:", out)
        else:
            print("Use: b64 enc <text>  OR  b64 dec <text>")
    except Exception:
        print("Invalid Base64 data.")

while True:
    raw = input("HAK---> ")

    try:
        parts = shlex.split(raw)
    except ValueError:
        print("invalid quotes")
        continue

    if not parts:
        continue

    cmd, args = parts[0].lower(), parts[1:]

    # ping usage: ping google.com
    if cmd == "ping" and args:
        ping(args[0])

    # find usage: find filename
    elif cmd == "find" and args:
        find(args[0])

    # showenv
    elif cmd == "showenv":
        showenv()

    elif cmd == "scanport" and len(args) == 2:
        scanport(args[0], args[1])

    elif cmd == "whois" and args:
        whois(args[0])

    elif cmd == "dnslookup" and args:
        dnslookup(args[0])

    elif cmd == "hash" and args:
        hashsha(" ".join(args))

    elif cmd == "b64" and len(args) >= 2:
        b64(args[0], " ".join(args[1:]))

    else:
        print("Unknown command.")
