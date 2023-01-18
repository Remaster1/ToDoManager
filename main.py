from PySide6 import QtWidgets,QtCore,QtGui
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
settings = load_json("settings.json")
json_path = settings["latest_json"] 


def setItems(json):
    List.clear()
    for i in json:
        QtWidgets.QListWidgetItem(i,List)

def json_file_dialog():
    global ToDos
    global json_path
    global settings
    json_path = QtWidgets.QFileDialog.getOpenFileName()[0]
    settings["latest_json"] = json_path
    save_json(settings,"settings.json")
    ToDos = load_json(json_path)
    setItems(ToDos)
    
def load_text():
    TextField.setText(ToDos[List.currentItem().text()]["text"])
    TimeLable.setText(str(ToDos[List.currentItem().text()]["date"][0])+"."+str(ToDos[List.currentItem().text()]["date"][1])+"."+str(ToDos[List.currentItem().text()]["date"][2]))
    
def save_text():
    ToDos[List.currentItem().text()]["text"] = TextField.toPlainText()
    save_json(ToDos,json_path)

def create_todo():
    global ToDos
    Input_Todo = QtWidgets.QInputDialog.getText(window,"Новая задача","Введите название задачи:")
    now = datetime.datetime.now()
    ToDos.update({str(Input_Todo[0]):{"text":" ","date":[now.day,now.month,now.year]}})
    save_json(ToDos,json_path)
    ToDos = load_json(json_path)
    setItems(ToDos)

def search_by_date():
    global ToDos
   
    for i in ToDos:
        CurrentSelectedToDos = List.findItems(i,QtCore.Qt.MatchFlag.MatchRegularExpression)
        for CurrentSelectToDo in CurrentSelectedToDos:
                CurrentSelectToDo.setBackground(QtGui.QColor(255, 255, 255))

    Date_cal = str(Date.selectedDate().toPython()).split("-")
    
    for i in ToDos:
        if ToDos[i]["date"][0] == int(Date_cal[2]) and ToDos[i]["date"][1] == int(Date_cal[1]) and ToDos[i]["date"][2] == int(Date_cal[0]):
            CurrentSelectedToDos = List.findItems(i,QtCore.Qt.MatchFlag.MatchRegularExpression)
            for CurrentSelectToDo in CurrentSelectedToDos:
                CurrentSelectToDo.setBackground(QtGui.QColor(3, 19, 252))

            
def delete_todo():
    global json_path
    ToDos.pop(List.currentItem().text())
    setItems(ToDos)
    save_json(ToDos,json_path)


CreateBtn = QtWidgets.QPushButton(text="Создать")
LoadBtn = QtWidgets.QPushButton(text="Загрузить")
SaveBtn = QtWidgets.QPushButton(text="Сохранить")
DeleteBtn = QtWidgets.QPushButton(text="Удалить")
TimeLable = QtWidgets.QLabel(text="")

List = QtWidgets.QListWidget()
TextField = QtWidgets.QTextEdit()
Date = QtWidgets.QCalendarWidget()

List.setFixedSize(100,250)
TextField.setFixedSize(450,250)
Date.setFixedSize(300, 200)
QHBox.setSpacing(3)
QHBox.addLayout(QVBox)

QVBox.addWidget(List)
QVBox.addWidget(LoadBtn)
QVBox.addWidget(CreateBtn)
QVBox3.addWidget(Date)
QVBox3.addWidget(TimeLable)
QVBox1.addWidget(TextField)
QVBox1.addWidget(DeleteBtn)
QVBox1.addWidget(SaveBtn)
QHBox.addLayout(QVBox1)
QHBox.addLayout(QVBox3)
window.setCentralWidget(widget)
widget.setLayout(QHBox)

CreateBtn.clicked.connect(create_todo)
LoadBtn.clicked.connect(json_file_dialog)
List.currentItemChanged.connect(load_text)
SaveBtn.clicked.connect(save_text)
Date.clicked.connect(search_by_date)
DeleteBtn.clicked.connect(delete_todo)

if settings["latest_json"] != "":
    ToDos = load_json(json_path)

if __name__ == "__main__":
    window.show()
    app.exec()