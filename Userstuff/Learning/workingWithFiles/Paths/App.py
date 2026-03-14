from pathlib import Path as P
import shutil

src = P("Ecommerce/__init__.py")
trg = P() / "__init__.py"

#trg.write_text(src.read_text)

shutil.copy(src, trg)