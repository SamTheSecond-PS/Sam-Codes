import PySide6.QtWidgets as q # type: ignore

app = q.QApplication.instance() or q.QApplication([])

win = q.QWidget()
win.setWindowTitle("Hello, first.")
win.resize(600, 600)

but = q.QPushButton("CLICK")
lay = q.QVBoxLayout()
lab = q.QLabel("Pressed")
qa = q.QLineEdit()
but2 = q.QPushButton("SUBMIT")

def on_sub():
    text = qa.text()
    lab.setText(text)

but2.clicked.connect(on_sub)

win.setLayout(lay)

def click():
    lay.addWidget(lab)
    lay.addWidget(qa)
    lay.addWidget(but2)

but.clicked.connect(click)
lay.addWidget(but)

win.show()
app.exec()