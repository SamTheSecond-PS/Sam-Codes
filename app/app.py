from PySide6 import QtWidgets as q
from PySide6.QtGui import QIcon
import pathlib as pb
import time

new_click_count = 0
open_click_count = 0

app = q.QApplication.instance() or q.QApplication([])

win = q.QWidget()
win.setWindowTitle("Note#")
win.resize(600, 600)

win.setWindowIcon(QIcon("icon.ico"))


main_lay = q.QVBoxLayout()
win.setLayout(main_lay)

txt = q.QHBoxLayout()
but = q.QVBoxLayout()

make = q.QPushButton("New")
but.addWidget(make)
openn = q.QPushButton("Open")
but.addWidget(openn)
main_lay.addWidget(openn)

'''NEW'''
fn = q.QLabel("Filename")
filename = q.QLineEdit()
filename.setPlaceholderText("-filename-")
sub = q.QPushButton("MAKE")
but.addWidget(fn)
but.addWidget(filename)
but.addWidget(sub)
fn.hide()
filename.hide()
sub.hide()


text_area = q.QTextEdit()
txt.addWidget(text_area)

def on_new():
    global new_click_count
    new_click_count += 1
    show = (new_click_count % 2 != 0)
    fn.setVisible(show)
    filename.setVisible(show)
    sub.setVisible(show)
    

def on_submit():
    name = filename.text().strip()
    if not name:
        filename.setPlaceholderText("Enter a filename")
    try:
        path = pb.Path(name)
        if path.exists():
            filename.setPlaceholderText("File already exists")
        else:
            try:
                path.touch()
                text_area.setPlainText(f"File {name} created.")
            except Exception:
                text_area.setPlainText("Error creating file {name}.")
    except FileNotFoundError:
        text_area.setPlainText("File {name} not found.")


'''OPEN'''
fn2 = q.QLabel("Filename")
filename2 = q.QLineEdit()
filename2.setPlaceholderText("-filename-")
sub2 = q.QPushButton("SEARCH")
subm = q.QPushButton("WRITE")

but.addWidget(fn2)
but.addWidget(filename2)
but.addWidget(sub2)
but.addWidget(subm)

fn2.hide()
filename2.hide()
sub2.hide()
subm.hide()

def on_openn():
    global open_click_count
    open_click_count += 1

    show = (open_click_count % 2 != 0)

    for w in [fn2, filename2, sub2]:
        w.setVisible(show)

    if not show:
        subm.hide()
    
def on_search():
    filenamee = filename2.text()
    
    if pb.Path(filenamee).exists():
        text_area.setPlaceholderText("File Found\nWrite...")
        subm.show()
    else:
        text_area.setPlaceholderText(f"File {filenamee} not found")
        
    

def on_sub():
    filenamee = filename2.text()
    try:
        with open(filenamee, 'a') as f:
                f.write(f"{text_area.toPlainText()}\n")
    except FileNotFoundError:
        text_area.setPlainText("File {filenamee} not found")




make.clicked.connect(on_new)
sub.clicked.connect(on_submit)
subm.clicked.connect(on_sub)
sub2.clicked.connect(on_search)
openn.clicked.connect(on_openn)

main_lay.addLayout(but)
main_lay.addLayout(txt)

win.show()
app.exec()