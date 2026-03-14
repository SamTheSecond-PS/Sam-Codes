import os
import shutil
import shlex
import sys


print("-----BYte SAMster---")
print("help - to show commands")
print("------------------------")
print("[warning: In development]")



def catf(name):
    found_files = []

    for root, dirs, files in os.walk("."):
        try:
            if name in files:
                found_files.append(os.path.join(root, name))

        except PermissionError:
            continue

    if not found_files:
        x = input(f"File '{name}' not found in current folder. Search whole system? [y/n]: ")
        if x.lower().startswith("y"):
            for root, dirs, files in os.walk("C:/"):
                try:
                    if name in files:
                        found_files.append(os.path.join(root, name))
                except PermissionError:
                    continue

    if found_files:
        print("Found the following files:")
        for idx, file_path in enumerate(found_files):
            print(f"{idx+1}. {file_path}")

        choice = input("Enter the number of the file you want to read: ")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(found_files):
                file_to_read = found_files[idx]
                print(f"\n--- Reading {file_to_read} ---")
                with open(file_to_read, "r") as f:
                    for line in f:
                        print(line, end="")
            else:
                print("Invalid choice. Cancelled.")
        except ValueError:
            print("Invalid input. Cancelled.")
    else:
        print("File still not found.")

def writeinfile(name, path="."):
    found = False
    files_to_choose = []

    if os.path.exists(name) and os.path.isfile(name):
        files_to_choose.append(name)
    else:
        print(f"file {name} is not found")

    for roots, dirs, files in os.walk(path):
        try:
            if name in files:
                files_to_choose.append(os.path.join(roots, name))
        except PermissionError:
            print("you do not have permission")

    if not files_to_choose:
        x = input("file not found, search the whole system?[y/n]: ")
        if x.lower().startswith("y"):
            for roots, dirs, files in os.walk("C:/"):
                try:
                    if name in files:
                        files_to_choose.append(os.path.join(roots, name))
                except PermissionError:
                    print("you do not have permission")

    if files_to_choose:
        print("Found the following files:")
        for idx, file_path in enumerate(files_to_choose):
            print(f"{idx + 1}. {file_path}")

        choice = input("Enter the number of the file you want to write in: ")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(files_to_choose):
                file_to_write = files_to_choose[idx]
                text = input("What do you want to write: ")
                with open(file_to_write, 'a') as f:
                    f.write(str(text))
                print(f"Written to file: {file_to_write}")
            else:
                print("Invalid choice. Cancelled.")
        except ValueError:
            print("Invalid input. Cancelled.")
    else:
        print("File still not found.")

def readfolder(name, path="."):
    folders_found = []

    if os.path.exists(name) and os.path.isdir(name):
        folders_found.append(name)

    for root, dirs, files in os.walk(path):
        try:
            if name in dirs:
                folders_found.append(os.path.join(root, name))
        except PermissionError:
            continue

    if not folders_found:
        x = input(f"Folder '{name}' not found in current path. Search whole system? [y/n]: ")
        if x.lower().startswith("y"):
            for root, dirs, files in os.walk("C:/"):
                try:
                    if name in dirs:
                        folders_found.append(os.path.join(root, name))
                except PermissionError:
                    continue

    if folders_found:
        print("Found the following folders:")
        for idx, folder_path in enumerate(folders_found):
            print(f"{idx+1}. {folder_path}")

        choice = input("Enter the number of the folder you want to read: ")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(folders_found):
                folder_to_read = folders_found[idx]
                print(f"Contents of folder '{folder_to_read}':")
                for item in os.listdir(folder_to_read):
                    print(item)
            else:
                print("Invalid choice. Cancelled.")
        except ValueError:
            print("Invalid input. Cancelled.")
    else:
        print("Folder still not found.")

def ls(path="."):
    try:
        for item in os.listdir(path):
            full = os.path.join(path, item)
            if os.path.isdir(full):
                print(f"[DIR]  {item}")
            else:
                print(f"[FILE]  {item}")
    except Exception as e:
        print("error ", e)

def rm_file(a):
    if os.path.exists(a) and os.path.isfile(a):
        n = input("are you sure?[y/n]: ")
        if n.lower().startswith("y"):
            os.remove(a)
            print("deleted")
        else:
            print("cancelled")
    else:
        print("file does not exist or isn't a file")

def rm_folder(a):
    if os.path.exists(a) and os.path.isdir(a):
        n = input("are you sure?[y/n]: ")
        if n.lower().startswith("y"):
            shutil.rmtree(a)
            print("deleted")
        else:
            print("cancelled")
    else:
        print("folder does not exist or isn't a folder")

def mkfolder(a):
    if not os.path.exists(a):
        os.mkdir(a)
        print(f"folder {a} created")
    else:
        x = input("folder exists, overwrite?[y/n]: ")
        if x.lower().startswith("y"):
            shutil.rmtree(a)
            os.mkdir(a)
            print(f"folder {a} overwritten")
        else:
            print("cancelled")


def mkfile(name, path="."):
    full_path = os.path.join(path, name)

    if not os.path.exists(full_path):
        with open(full_path, "w") as f:
            pass
        print(f"file {full_path} created")

    elif os.path.isfile(full_path):
        try:
            x = input("file exists, overwrite? [y/n]: ")
            if x.lower().startswith("y"):
                with open(full_path, "w") as f:
                    pass
                print(f"file {full_path} overwritten")
            else:
                print("cancelled")
        except FileNotFoundError:
            print("file not found")
            

    else:
        print("folder dosnt exist or isn't a folder")




def cp(src, dst):
    try:
        if not os.path.exists(src):
            print(f"{src} does not exist")
            return

        if os.path.isdir(src):
            if os.path.exists(dst) and os.path.isdir(dst):
                dst = os.path.join(dst, os.path.basename(src))

            shutil.copytree(src, dst)
            print("copied folder")

        else:
            if os.path.exists(dst) and os.path.isdir(dst):
                dst = os.path.join(dst, os.path.basename(src))

            shutil.copy2(src, dst)
            print("copied file")

    except FileExistsError:
        print("destination already exists")
    except PermissionError:
        print("permission denied")
    except Exception as e:
        print("error:", e)

def clear():

    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")
    else:
        print("\n" * 200)

def pwd():
    print("current path: ", os.getcwd())

def showenv():
    for k,v in os.environ.items():
        print(f"{k}= {v}")

def current_fd():
    print(f"current folder: {os.path.basename(os.getcwd()) or os.getcwd()}")

def cd(folder_name):

    if os.path.isdir(folder_name):
        os.chdir(folder_name)
        print("current folder:", os.getcwd())
        return

    found_paths = []


    for root, dirs, files in os.walk("."):
        try:
            for d in dirs:
                if d.lower() == folder_name.lower():
                    found_paths.append(os.path.join(root, d))
        except PermissionError:
            continue


    if not found_paths:
        x = input(f"Folder '{folder_name}' not found here. Search whole PC? [y/n]: ")
        if x.lower().startswith("y"):
            for root, dirs, files in os.walk("C:/"):
                try:
                    for d in dirs:
                        if d.lower() == folder_name.lower():
                            found_paths.append(os.path.join(root, d))
                except PermissionError:
                    continue

    if not found_paths:
        print("No folder found.")
        return

    print("Found the following folders:")
    for i, p in enumerate(found_paths):
        print(f"{i+1}. {p}")

    choice = input("Enter the number of the folder you want to open: ")

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(found_paths):
            os.chdir(found_paths[idx])
            print("current folder:", os.getcwd())
        else:
            print("Invalid choice.")
    except ValueError:
        print("not in code")

def find(name, path="."):
    found_items = []

    for root, dirs, files in os.walk(path):
        try:
            if name in files:
                found_items.append(os.path.join(root, name))
            if name in dirs:
                found_items.append(os.path.join(root, name))
        except PermissionError:
            continue

    if not found_items:
        x = input(f"'{name}' not found locally. Search whole system? [y/n]: ")
        if not x.lower().startswith("y"):
            print("Cancelled.")
            return

        # Search all drives (C:/ for now)
        for root, dirs, files in os.walk("C:/"):
            try:
                if name in files:
                    found_items.append(os.path.join(root, name))
                if name in dirs:
                    found_items.append(os.path.join(root, name))
            except PermissionError:
                continue

    if found_items:
        print("\nFound the following paths:")
        for i, item in enumerate(found_items, 1):
            print(f"{i}. {item}")
    else:
        print("Still not found.")

def ping(host):
    flag = "-n" if os.name == "nt" else "-c"
    command = f"ping {flag} 1 {host}"
    result = os.system(command)
    if result == 0:
        print(f"{host} is reachable")
    else:
        print(f"{host} is unreachable or blocking requests")


def mvf(a, b):
    if not os.path.exists(a):
        print(f"File {a} does not exist")
        return
    if not os.path.isfile(a):
        print(f"File {a} is not a file")
        return

    try:
        os.rename(a,b)
        print(f"File {a} renamed to {b}")
    except PermissionError:
        print("you do not have permission")
    except Exception as e:
        print("Error ",e)

def echo(a):
    print("".join(a))

print("type 'help' to see commands")

while True:
    raw = input("BYte~:>>> ")
    try:
        parts = shlex.split(raw)
    except ValueError:
        print("invalid quotes")
        continue
    if not parts: continue
    cmd, args = parts[0].lower(), parts[1:]

    if cmd == "help":
        print('''
exit - exit terminal
catf (file) - read a file
writeinfile(file) - write in a file
readfolder(folder) - list folder contents
ls [path] - list files/folders
cp src dst - copy file
rm_file file - delete a file
rm_folder folder - delete a folder
mkfile file - create a file
mkfolder folder - create a folder
clear - clear terminal
pwd - show current path
current_fd - show current folder
cd folder - change folder
ping host - ping a host
showenv - show environment variables
find filename - search for file
mvf old file ,name new filename/destination - mrenames, moves file to another place''')
    elif cmd == "exit":
        break
    elif cmd == "catf" and args:
        catf(args[0])
    elif cmd == "writeinfile" and args:
        writeinfile(args[0])
    elif cmd == "readfolder" and args:
        readfolder(args[0])
    elif cmd == "ls":
        ls(args[0] if args else ".")
    elif cmd == "rm_file" and args:
        rm_file(args[0])
    elif cmd == "rm_folder" and args:
        rm_folder(args[0])
    elif cmd == "mkfile" and args:
        if len(args) == 1:
            mkfile(args[0])
        else:
            mkfile(args[0], args[1])

    elif cmd == "mkfolder" and args:
        mkfolder(args[0])
    elif cmd == "cp" and len(args) == 2:
        cp(args[0], args[1])
    elif cmd == "clear":
        clear()
    elif cmd == "pwd":
        pwd()
    elif cmd == "current_fd":
        current_fd()
    elif cmd == "cd" and args:
        cd(args[0])
    elif cmd == "ping" and args:
        ping(args[0])
    elif cmd == "showenv":
        showenv()
    elif cmd == "find" and args:
        find(args[0])
    elif cmd.lower().startswith("echo") and args:
        echo(args)
    elif cmd == "mvf":
        if len(args) < 2:
            print("Usage: mvf <oldname> <newname>")
        else:
            mvf(args[0], args[1])
    elif cmd == "k":
        print(".BYte.")
        print("b  y  t  e")
    elif cmd.lower() == "open":
        print("there are options to open files and folders, you may find them in the help command.")
    elif cmd.lower() == "mvf" and len(args) == 2:
        mvf(args[0], args[1])
    else:
        print("unknown command or missing argument")































