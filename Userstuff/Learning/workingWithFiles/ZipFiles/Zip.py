from pathlib import Path
from zipfile import ZipFile

#with ZipFile("flies.zip", "w") as zip:
 #   for path in Path("ecommerce").rglob("*.*"):
  #    zip.write(path)
#zip.close()

with ZipFile("flies.zip") as zip:
    print(zip.namelist())
    info = zip.getinfo("Ecommerce/__init__.py")
    print(info.file_size)
    print(info.compress_size)
    