from PySide6 import QtWidgets,QtCore,QtGui
from json_parser import *
import datetime

ToDos = {}
settings = load_json("settings.json")
json_path = settings["latest_json"] 

app = QtWidgets.QApplication([])
window = QtWidgets.QMainWindow()
window.setWindowTitle("ToDo Manager")

widget = QtWidgets.QWidget(window)
MainQVBox = QtWidgets.QVBoxLayout()
QHBox = QtWidgets.QHBoxLayout()
QVBox = QtWidgets.QVBoxLayout()
QVBox3 = QtWidgets.QVBoxLayout()
QVBox1 = QtWidgets.QVBoxLayout()
QHBox2 = QtWidgets.QHBoxLayout()


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
    CheckBoxComplete.setChecked(int(ToDos[List.currentItem().text()]["completed"]))
    
def save_text():
    ToDos[List.currentItem().text()]["text"] = TextField.toPlainText()
    save_json(ToDos,json_path)

def create_todo():
    global ToDos
    Input_Todo = QtWidgets.QInputDialog.getText(window,"Новая задача","Введите название задачи:")
    now = datetime.datetime.now()
    ToDos.update({str(Input_Todo[0]):{"text":" ","date":[now.day,now.month,now.year],"completed":0}})
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


def change_complete_status():
    if CheckBoxComplete.isChecked():
        ToDos[List.currentItem().text()]["completed"] = int(1)
    else:
        ToDos[List.currentItem().text()]["completed"] = int(0)
    save_json(ToDos,json_path)

Menu = QtWidgets.QMenuBar()
CreateBtn = QtWidgets.QPushButton(text="+")
SaveBtn = QtWidgets.QPushButton(text="Сохранить")
DeleteBtn = QtWidgets.QPushButton(text="-")
TimeLable = QtWidgets.QLabel(text="")
List = QtWidgets.QListWidget()
TextField = QtWidgets.QTextEdit()
Date = QtWidgets.QCalendarWidget()
LoadAction = QtGui.QAction("Загрузить")
SaveAction = QtGui.QAction("Сохранить")
CheckBoxComplete = QtWidgets.QCheckBox(text="Выполнено")


CreateBtn.setFixedWidth(49)
DeleteBtn.setFixedWidth(49)
List.setFixedSize(100,250)
TextField.setFixedSize(450,250)
Date.setFixedSize(300, 200)
MainQVBox.setContentsMargins(4,0,4,4)



ToDoListMenu = Menu.addMenu("Список")
ToDoListMenu.addAction(LoadAction)
ToDoListMenu.addAction(SaveAction)

MainQVBox.addWidget(Menu)
MainQVBox.addLayout(QHBox)
QHBox.setSpacing(3)
QHBox.addLayout(QVBox)
QVBox.addWidget(List)
QVBox.addLayout(QHBox2)
QHBox2.addWidget(CreateBtn)
QHBox2.addWidget(DeleteBtn)
QVBox3.addWidget(Date)
QVBox3.addWidget(TimeLable)
QVBox3.addWidget(CheckBoxComplete)
QVBox1.addWidget(TextField)
QVBox1.addWidget(SaveBtn)
QHBox.addLayout(QVBox1)
QHBox.addLayout(QVBox3)
window.setCentralWidget(widget)
widget.setLayout(MainQVBox)

CreateBtn.clicked.connect(create_todo)
LoadAction.triggered.connect(json_file_dialog)
SaveAction.triggered.connect(save_text)
List.currentItemChanged.connect(load_text)
Date.clicked.connect(search_by_date)
DeleteBtn.clicked.connect(delete_todo)
CheckBoxComplete.clicked.connect(change_complete_status)

if settings["latest_json"] != "":
    ToDos = load_json(json_path)
    setItems(ToDos)

if __name__ == "__main__":
    window.show()
    app.exec()