from PySide6 import QtWidgets,QtCore
from json_parser import *
import datetime

app = QtWidgets.QApplication([])
window = QtWidgets.QMainWindow()
window.setWindowTitle("ToDo Manager")

widget = QtWidgets.QWidget(window)
QHBox = QtWidgets.QHBoxLayout()
QVBox = QtWidgets.QVBoxLayout()
QVBox3 = QtWidgets.QVBoxLayout()
QVBox1 = QtWidgets.QVBoxLayout()

ToDos = {}

json_path = ""

def setItems(json):
    List.clear()
    
    for i in json:
        QtWidgets.QListWidgetItem(i,List)

def json_file_dialog():
    global ToDos
    global json_path
    json_path = QtWidgets.QFileDialog.getOpenFileName()[0]
    ToDos = load_json(json_path)
    setItems(ToDos)
    
def load_text():
    TextField.setText(ToDos[List.currentItem().text()][0])
    TimeLable.setText(f"{ToDos[List.currentItem().text()][1]}.{ToDos[List.currentItem().text()][2]}.{ToDos[List.currentItem().text()][3]}")
    
def save_text():
    ToDos[List.currentItem().text()][0] = TextField.toPlainText()
    save_json(ToDos,json_path)

def create_todo():
    global ToDos
    Input_Todo = QtWidgets.QInputDialog.getText(window,"Новая задача","Введите название задачи:")
    now = datetime.datetime.now()
    ToDos.update({str(Input_Todo[0]):[" ",now.day,now.month,now.year]})
    save_json(ToDos,json_path)
    ToDos = load_json(json_path)
    setItems(ToDos)


def search_by_date():
    global ToDos
    Date = str(QDate.selectedDate().toPython()).split("-")
    
    for i in ToDos:
        if ToDos[i][1] == Date[2] and ToDos[i][2] == Date[2] and ToDos[i][3] == Date[0]:
            pass
            

CreateBtn = QtWidgets.QPushButton(text="Создать")
LoadBtn = QtWidgets.QPushButton(text="Загрузить")
SaveBtn = QtWidgets.QPushButton(text="Сохранить")
TimeLable = QtWidgets.QLabel(text="")

List = QtWidgets.QListWidget()
TextField = QtWidgets.QTextEdit()
QDate = QtWidgets.QCalendarWidget()

List.setFixedSize(100,250)
TextField.setFixedSize(450,250)
QDate.setFixedSize(300, 200)
QHBox.setSpacing(3)
QHBox.addLayout(QVBox)

QVBox.addWidget(List)
QVBox.addWidget(LoadBtn)
QVBox.addWidget(CreateBtn)
QVBox3.addWidget(QDate)
QVBox1.addWidget(TextField)
QVBox1.addWidget(TimeLable)
QVBox1.addWidget(SaveBtn)
QHBox.addLayout(QVBox1)
QHBox.addLayout(QVBox3)
window.setCentralWidget(widget)
widget.setLayout(QHBox)

CreateBtn.clicked.connect(create_todo)
LoadBtn.clicked.connect(json_file_dialog)
List.currentItemChanged.connect(load_text)
SaveBtn.clicked.connect(save_text)
QDate.clicked.connect(search_by_date)
if __name__ == "__main__":
    window.show()
    app.exec()