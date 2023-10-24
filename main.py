import sys,glob
from PyQt5 import QtGui, QtCore
from os.path import exists
from os import remove,mkdir
from PyQt5.QtWidgets import QApplication,QStackedWidget,QAbstractItemView, QWidget, QLabel, QPushButton,QBoxLayout,QLineEdit,QShortcut,QTableWidget,QTableWidgetItem
#make an error dialog box with init parameter of string to put a message to dialog and a button to close it labeled with "okay"
QFont=QtGui.QFont
QEventLoop=QtCore.QEventLoop
Qt=QtCore.Qt
class ErrorDialog(QWidget):
    def __init__(self,message:str):
        super().__init__()
        self.keyPressEvent=QShortcut("Return",self)
        self.keyPressEvent.activated.connect(self._finish)
        self.layout=QBoxLayout(QBoxLayout.TopToBottom)
        self.setStyleSheet("background-color: black; color:white;")
        self.setGeometry(100,100,300,300)
        self.setLayout(self.layout)
        self.setWindowTitle("Error")
        self.message=message
        self.label=QLabel(self.message)
        self.label.setStyleSheet("font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;")
        self.layout.addWidget(self.label)
        self.closeButton=QPushButton("Okay")
        self.closeButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;} QPushButton::hover{background-color: white; color: black;}")
        self.closeButton.clicked.connect(self.close)
        self.layout.addWidget(self.closeButton)
    def _finish(self):self.close()  
class MessageDialog(QWidget):
    def __init__(self,message:str)->None:
        super().__init__()
        self.keyPressEvent=QShortcut("Return",self)
        self.keyPressEvent.activated.connect(self._finish)
        self.layout=QBoxLayout(QBoxLayout.TopToBottom)
        self.setStyleSheet("background-color: black; color:white;")
        self.setGeometry(100,100,300,300)
        self.setLayout(self.layout)
        self.setWindowTitle("Message")
        self.message=message
        self.label=QLabel(self.message)
        self.label.setStyleSheet("font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;")
        self.layout.addWidget(self.label)
        self.closeButton=QPushButton("Okay")
        self.closeButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;} QPushButton::hover{background-color: white; color: black;}")
        self.closeButton.clicked.connect(self.close)
        self.layout.addWidget(self.closeButton)
    def _finish(self):self.close()
class AskStringDialog(QWidget):
    def __init__(self,message)->None:
        super().__init__()
        self.layout=QBoxLayout(QBoxLayout.TopToBottom)
        self.setAttribute(Qt.WA_DeleteOnClose)
        #add a keypress event to press the enter button 
        self.keyPressEvent=QShortcut("Return",self)
        self.keyPressEvent.activated.connect(self._finish)
        self.setStyleSheet("background-color: black; color:white;")
        self.setGeometry(100,100,300,300)
        self.setLayout(self.layout)
        self.setWindowTitle("Get String")
        self.message=message
        self.label=QLabel(self.message)
        self.label.setStyleSheet("font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;")
        self.layout.addWidget(self.label)
        self.l=QBoxLayout(QBoxLayout.LeftToRight)
        self.layout.addLayout(self.l)
        self.input=QLineEdit("")
        self.input.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
        self.l.addWidget(self.input)
        self.closeButton=QPushButton("enter")
        self.closeButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;} QPushButton::hover{background-color: white; color: black;}")
        self.closeButton.clicked.connect(self._finish)
        self.l.addWidget(self.closeButton)
        self.layout.addLayout(self.l)
    def _finish(self)->str:
        self.final=self.input.text()
        self.close()
    def get(self)->str:
        return self.final
class AskYesNoDialog(QWidget):
    def __init__(self,message)->None:
        super().__init__()
        self.final="yes"
        self.layout=QBoxLayout(QBoxLayout.TopToBottom)
        self.setAttribute(Qt.WA_DeleteOnClose)
        #add a keypress event to press the enter button 
        self.keyPressEvent=QShortcut("Return",self)
        self.keyPressEvent.activated.connect(self._yes)
        self.setStyleSheet("background-color: black; color:white;")
        self.setGeometry(100,100,300,300)
        self.setLayout(self.layout)
        self.setWindowTitle("Yes/No")
        self.message=message
        self.label=QLabel(self.message)
        self.label.setStyleSheet("font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;")
        self.layout.addWidget(self.label)
        self.l=QBoxLayout(QBoxLayout.LeftToRight)
        self.layout.addLayout(self.l)
        self.noButton=QPushButton("No")
        self.noButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;} QPushButton::hover{background-color: white; color: black;}")
        self.noButton.clicked.connect(self._finish)
        self.l.addWidget(self.noButton)
        self.yesButton=QPushButton("Yes")
        self.yesButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;}")
        self.yesButton.clicked.connect(self._yes)
        self.l.addWidget(self.yesButton)
        self.layout.addLayout(self.l)
    def _finish(self)->str:
        self.close()
    def _yes(self)->None:
        self.final="yes"
        self.close()
    def _no(self)->None:
        self.final="no"
        self.close()
class StudySetException(Exception):
    pass
class StudySet:
    def __init__(self)->None:
        self.name=""
        #cards is a dictionary of the form {front:back}
        self.cards={}
        self._isEmpty=True
    def cards(self)->dict:return self.cards
    def addCard(self,front:str,back:str)->None:
        self._isEmpty=False
        self.cards[front]=back
    def loadSet(self)->None:
        """
        Can only be done if self.isEmpty
        """
        if not exists("./Cards"):mkdir("./Cards")
        if self._isEmpty:
            with open(f"./Cards/{self.name}.cards","r") as f:
                for line in f.readlines():
                    front,back=line.split(":")
                    self.cards[front]=back
                f.close()
            self._isEmpty=False
        else:raise StudySetException("Study Set is not empty")
    def setName(self,name:str)->None:self.name=name
    def isEmpty(self):return self._isEmpty
    def emptyStudySet(self)->None:self.cards,self._isEmpty={},True
    def removeCard(self,front:str)->None:
        """
        if KeyError Raised then send error message using ErrorDialog
        """
        try:del self.cards[front]
        except KeyError:raise KeyError("Card not found")
    def getName(self)->str:return self.name
    def saveSet(self,o:bool=None,empty:bool=True)->None:
        """
        Saves in ./Cards
        with filename format {self.name}.cards
        o is a boolean that is True if you want to overwrite the file
        """
        #check if ./Cards exists if not then create it
        if not exists("./Cards"):mkdir("./Cards")
        #if the file exists already, ask if they want to overwrite it
        if exists(f"./Cards/{self.name}.cards") and o is None:raise FileExistsError("File already exists")
        elif exists(f"./Cards/{self.name}.cards") and o is True:
            with open(f"./Cards/{self.name}.cards","w") as f:
                for front,back in self.cards.items():f.write(f"{front}:{back}\n")
                f.close()
            if empty:
                self.cards={}
                self._isEmpty=True
            return
        elif not exists(f"./Cards/{self.name}.cards"):
            with open(f"./Cards/{self.name}.cards","w") as f:
                for front,back in self.cards.items():f.write(f"{front}:{back}\n")
                f.close()
            if empty:
                self.cards={}
                self._isEmpty=True
            return
        else:return#unknown
class MainWindow(QStackedWidget):
    class CustomRemovePopup(QWidget):
        def __init__(self,parent:'MainWindow',e=None) -> None:
            super().__init__()
            self.p=parent
            self.setWindowTitle("Remove A Card From Study Set")
            self.setGeometry(200,200,750,400)
            self.layou=QBoxLayout(QBoxLayout.TopToBottom)
            self.layou.setObjectName("Remove Cards From Study Set")
            self.setLayout(self.layou)
            self.setStyleSheet("background-color: black; color:white;")
            #add a keypress event to press the enter button
            self.keyPressEvent=QShortcut("Return",self)
            self.keyPressEvent.activated.connect(self.remove)
            self.table=QTableWidget()
            self.table.setColumnCount(2)
            self.table.setEditTriggers(QTableWidget.NoEditTriggers)
            self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.table.setStyleSheet("font: 20pt Comic Sans MS;background-color:black; color: white;")
            self.table.setRowCount(0)
            #"font: 20pt Comic Sans MS; color: white;"
            self.table.setColumnWidth(0,300)
            self.table.setColumnWidth(1,300)
            self.table.setHorizontalHeaderLabels(["Term","Definition"])
            self.table.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: black;color: white;border: 1px solid #FFFFFF;}")
            self.table.verticalHeader().setStyleSheet("QHeaderView::section {background-color: black;color: white;border: 1px solid #FFFFFF;}")
            self.table.horizontalHeader().setStretchLastSection(True)
            self.layou.addWidget(self.table)
            #iterate over self.p.currentSet.cards and add them to the table in format where key is in column 0 and value is in column 1
            self._calculate()
            self.removeButton=QPushButton("Remove")
            self.removeButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;} QPushButton::hover{background-color: white; color: black;}")
            self.removeButton.clicked.connect(self.remove)
            self.layou.addWidget(self.removeButton)
            #make when user clicks on a row, it highlights the row and makes it the current selected row
            self.table.itemClicked.connect(self._select)
            self.table.itemDoubleClicked.connect(self._select)
        def _calculate(self):
            #clear table
            self.table.setRowCount(0)
            for front,back in self.p.currentSet.cards.items():
                self.table.insertRow(self.table.rowCount())
                self.table.setItem(self.table.rowCount()-1,0,QTableWidgetItem(front))
                self.table.setItem(self.table.rowCount()-1,1,QTableWidgetItem(back))
        def _select(self)->None:
            self.selectedRow=self.table.currentRow()
            self.selectedTerm=self.table.item(self.selectedRow,0).text()
            self.selectedDefinition=self.table.item(self.selectedRow,1).text()
        def remove(self)->None:
            """
            removes the current selected table entry and will be able to delete the card from the study set
            """
            try:
                self.p.currentSet.removeCard(self.selectedTerm)
                self.p.currentSet.saveSet(True)
            except KeyError:pass#Nothing left in table
            self._calculate()
    def __init__(self):
        super().__init__()
        self.FirstMenuQWidget=QWidget()
        self.addWidget(self.FirstMenuQWidget)   
        self.setCurrentWidget(self.FirstMenuQWidget)
        self.firstStudyStudio=True
        self.startlayoutStyle="background-color: black; color:white;"
        # Set up the layout
        self.STUDY_STUDIO=False
        self.msg=""
        self.EDIT=False
        self.Startlayout = QBoxLayout(QBoxLayout.TopToBottom)
        self.FirstMenuQWidget.setLayout(self.Startlayout)
        #set fullscreen
        self.showFullScreen()
        #add a shortcut to close the application with ctrl+q
        self.exitShortcut=QShortcut("Ctrl+Q",self)
        self.exitShortcut.activated.connect(self._exit)
        # Add a label and button to the layout
        #self.label = QLabel("Hello, world!")
        #self.layout.addWidget(self.label)
        #set background to black
        self.errMsg="Error. Please try again."
        self.setStyleSheet(self.startlayoutStyle)
        #add Title Saying Welcome to Study Time
        self.welcomeLabel = QLabel("Welcome to Study Time")
        self.welcomeLabel.setStyleSheet("font: 50pt Comic Sans MS; color: white;")
        #put to top left of screen
        self.welcomeLabel.move(0,0)
        self.Startlayout.addWidget(self.welcomeLabel)
        #add 2 buttons: One to Create a new Study Set and one to load an existing one. make them span below the title
        self.newSetButton = QPushButton("Create a new Study Set")
        #add borders to make them look like a button
        #add hover color change to the buttons so I know they are buttons
        self.newSetButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;} QPushButton::hover{background-color: white; color: black;}")
        self.newSetButton.move(0,100)
        self.newSetButton.clicked.connect(self.CreateNewStudySet)
        self.Startlayout.addWidget(self.newSetButton)
        self.loadSetButton = QPushButton("Load an existing Study Set")
        self.loadSetButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;} QPushButton::hover{background-color: white; color: black;}")
        self.loadSetButton.move(0,200)
        self.loadSetButton.clicked.connect(self.OpenExistingStudySet)
        self.Startlayout.addWidget(self.loadSetButton)
        self.ExitButton=QPushButton("Exit")
        self.ExitButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;} QPushButton::hover{background-color: white; color: black;}")
        self.ExitButton.move(0,300)
        self.ExitButton.clicked.connect(self._exit)
        self.Startlayout.addWidget(self.ExitButton)
        self.cardAlerts=True
        self.currentSet=StudySet()
    def _exit(self,e=None):
        if self.currentSet.getName()!="":sys.exit()
        self.currentSet.saveSet(True if exists(f"./Cards/{self.currentSet.getName()}.cards") else False)
        #if .cards file exists, then delete it
        if exists(f"./Cards/.cards"):remove(f"./Cards/.cards")
        sys.exit()
#########################################################################################
#Study Studio and its functions
#:TODO: Make a flashcard system that shows the front of the card and when you click it, it shows the back of the card
#:TODO: Make a learn system that allows you to customize term/definition with multiple choice/written/read aloud to learn flashcards
#:TODO: Make a test system that allows you to customize term/definition with multiple choice/written/read aloud to test flashcards in a test form format
    def currentset(self)->StudySet:return self.currentSet
    def Flashcards(self):pass
    def Learn(self):pass
    def Test(self):pass
    def _editStudySet(self):
        self.EDIT=True
        self.CreateNewStudySet()
    def StudyStudio(self):
        """
        All studying done here
        """
        self.studyStudioLayout=QBoxLayout(QBoxLayout.TopToBottom,self)
        self.StudyStudioQWidget=QWidget()
        self.StudyStudioQWidget.setLayout(self.studyStudioLayout)
        self.addWidget(self.StudyStudioQWidget)
        self.setCurrentWidget(self.StudyStudioQWidget)
        self.studyStudioLayout.setObjectName("studyStudioLayout")
        self.backButton=QPushButton("<---")
        self.backButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;} QPushButton::hover{background-color: white; color: black;}")
        self.backButton.clicked.connect(self.__init__)
        self.backButton.move(0,0)
        self.studyStudioLayout.addWidget(self.backButton)
        self.studyStudioTitle=QLabel("Study Studio\nTime to study your study set: {}".format(self.currentSet.getName()))
        self.studyStudioTitle.setStyleSheet("font: 50pt Comic Sans MS; color: white;")
        self.studyStudioTitle.move(0,0)
        self.studyStudioLayout.addWidget(self.studyStudioTitle)
        #make a grid of 5 buttons that fit the same style of the application with different labels
        self.grid=QBoxLayout(QBoxLayout.LeftToRight)
        self.studyStudioLayout.addLayout(self.grid)
        self.flashcards=QPushButton("Flashcards")
        #QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;} QPushButton::hover{background-color: white; color: black;}
        self.flashcards.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;}QPushButton::hover{background-color: white; color: black;} ")
        self.flashcards.clicked.connect(self.Flashcards)
        self.grid.addWidget(self.flashcards)
        self.learnButton=QPushButton("Learn")
        self.learnButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;}QPushButton::hover{background-color: white; color: black;}")
        self.learnButton.clicked.connect(self.Learn)
        self.grid.addWidget(self.learnButton)
        self.test=QPushButton("Test")
        self.test.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;}QPushButton::hover{background-color: white; color: black;}")
        self.test.clicked.connect(self.Test)
        self.settings=QPushButton("Edit Study Set")
        self.settings.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;}QPushButton::hover{background-color: white; color: black;}")
        self.settings.clicked.connect(self._editStudySet)
        self.grid.addWidget(self.test)
        self.grid.addWidget(self.settings)
#########################################################################################
    def addCard(self,e=None):
        front=self.termInput.text()
        back=self.definitionInput.text()
        if front=="" or back=="":
            self.errMsg="Error. Please fill out both fields."
            self.showErrorDialog()
            return
        self.currentSet.addCard(front,back)
        if self.cardAlerts:self.showMessageDialog(f"Card added: {front}:{back}")
        else:pass
        #clear the input fields
        self.termInput.setText("")
        self.definitionInput.setText("")
        self.termInput.setFocus()
    def showErrorDialog(self):
        self.errorDialog=ErrorDialog(self.errMsg)
        self.errorDialog.show()
    def showMessageDialog(self,msg:str)->None:
        self.msg=MessageDialog(msg)
        self.msg.show()
    def showAskStringDialog(self,msg:str)->str:
        self.askStringDialog=AskStringDialog(msg)
        self.askStringDialog.show()
        loop = QEventLoop()
        self.askStringDialog.destroyed.connect(loop.quit)
        loop.exec()
        try:return self.askStringDialog.get()
        except RuntimeError:return ""
    def showYesNoDialog(self,msg:str)->str:
        self.askYesNoDialog=AskYesNoDialog(msg)
        self.askYesNoDialog.show()
        loop = QEventLoop()
        self.askYesNoDialog.destroyed.connect(loop.quit)
        loop.exec()
        return self.askYesNoDialog.final
    def saveStudySet(self,e=None):
        name=self.showAskStringDialog("Enter a name for the study set")
        if name=="":
            self.errMsg="Error. Please enter a name."
            self.showErrorDialog()
            return
        self.currentSet.setName(name)
        try:self.currentSet.saveSet(None,False)
        except FileExistsError:
            if self.showYesNoDialog("File already exists. Would you like to overwrite it?")=="yes":self.currentSet.saveSet(True)
            else:return
        if self.cardAlerts:self.showMessageDialog(f"Study Set Saved: {name}")
        self.StudyStudio()
    def clearStudySet(self,e=None):
        self.currentSet.emptyStudySet()
        self.showMessageDialog("Study Set Cleared")
    def showCustomPopup(self,e=None):
        self.customPopup=self.CustomRemovePopup(parent=self)
        self.customPopup.show()
    def _EditStudy(self,e=None):
        """
        Create A Popup with a QTableWidget of all terms being coordinated with their definitions and a button to remove it from the table which removes it from the study set
        """
        self.showCustomPopup()
    def CreateNewStudySet(self,e=None):
        self.createNewStudyLayout=QBoxLayout(QBoxLayout.TopToBottom,self)
        self.CREATENEWQWidget=QWidget()
        self.CREATENEWQWidget.setLayout(self.createNewStudyLayout)
        self.addWidget(self.CREATENEWQWidget)
        self.setCurrentWidget(self.CREATENEWQWidget)
        #add a go back button with a back arrow on the top left of the layout
        self.keyPressEvent=QShortcut("return",self)
        self.keyPressEvent.activated.connect(self.addCard)
        self.keyPressEvent=QShortcut("ctrl+s",self)
        self.keyPressEvent.activated.connect(self.saveStudySet)
        self.backButton=QPushButton("<---")
        self.backButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;} QPushButton::hover{background-color: white; color: black;}")
        self.backButton.clicked.connect(self.__init__)
        self.backButton.move(0,0)
        self.createNewStudyLayout.addWidget(self.backButton)
        if self.EDIT:
            self.createTitle=QLabel("Edit Your Study Set: {}".format(self.currentSet.getName()))
            self.createTitle.setStyleSheet("font: 50pt Comic Sans MS; color: white;")
            self.createTitle.move(0,0)
            self.createNewStudyLayout.addWidget(self.createTitle)
            #make a setup where you can add a term and definition in a form style manner with a button to add more terms and definitions
            self.TermBox=QBoxLayout(QBoxLayout.LeftToRight)
            self.termLabel=QLabel("Term:")
            self.termLabel.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
            self.TermBox.addWidget(self.termLabel)
            self.termInput=QLineEdit("")
            self.termInput.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
            self.termInput.setFocus()
            self.TermBox.addWidget(self.termInput)
            self.createNewStudyLayout.addLayout(self.TermBox)
            self.definitionBox=QBoxLayout(QBoxLayout.LeftToRight)
            self.definitionLabel=QLabel("Definition:")
            self.definitionLabel.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
            self.definitionBox.addWidget(self.definitionLabel)
            self.definitionInput=QLineEdit("")
            self.definitionInput.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
            self.definitionBox.addWidget(self.definitionInput)
            self.createNewStudyLayout.addLayout(self.definitionBox)
            self.addCardButton=QPushButton("Add Card")
            self.addCardButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;} QPushButton::hover{background-color: white; color: black;}")
            self.addCardButton.clicked.connect(self.addCard)
            self.createNewStudyLayout.addWidget(self.addCardButton)
            #make a button to save the study set
            self.saveButton=QPushButton("Save Study Set")
            self.saveButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;} QPushButton::hover{background-color: white; color: black;}")
            self.saveButton.clicked.connect(self.saveStudySet)
            self.createNewStudyLayout.addWidget(self.saveButton)
            #make a button to clear the study set
            self.clearButton=QPushButton("Remove A Card From Study Set")
            self.clearButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;} QPushButton::hover{background-color: white; color: black;}")
            self.clearButton.clicked.connect(self._EditStudy)
            self.createNewStudyLayout.addWidget(self.clearButton)
        else:
            self.createTitle=QLabel("Create a new Study Set")
            self.createTitle.setStyleSheet("font: 50pt Comic Sans MS; color: white;")
            self.createTitle.move(0,0)
            self.createNewStudyLayout.addWidget(self.createTitle)
            #make a setup where you can add a term and definition in a form style manner with a button to add more terms and definitions
            self.TermBox=QBoxLayout(QBoxLayout.LeftToRight)
            self.termLabel=QLabel("Term:")
            self.termLabel.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
            self.TermBox.addWidget(self.termLabel)
            self.termInput=QLineEdit("")
            self.termInput.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
            self.termInput.setFocus()
            self.TermBox.addWidget(self.termInput)
            self.createNewStudyLayout.addLayout(self.TermBox)
            self.definitionBox=QBoxLayout(QBoxLayout.LeftToRight)
            self.definitionLabel=QLabel("Definition:")
            self.definitionLabel.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
            self.definitionBox.addWidget(self.definitionLabel)
            self.definitionInput=QLineEdit("")
            self.definitionInput.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
            self.definitionBox.addWidget(self.definitionInput)
            self.createNewStudyLayout.addLayout(self.definitionBox)
            self.addCardButton=QPushButton("Add Card")
            self.addCardButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;} QPushButton::hover{background-color: white; color: black;}")
            self.addCardButton.clicked.connect(self.addCard)
            self.createNewStudyLayout.addWidget(self.addCardButton)
            #make a button to save the study set
            self.saveButton=QPushButton("Save Study Set")
            self.saveButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;} QPushButton::hover{background-color: white; color: black;}")
            self.saveButton.clicked.connect(self.saveStudySet)
            self.createNewStudyLayout.addWidget(self.saveButton)
            #make a button to clear the study set
            self.clearButton=QPushButton("Clear Study Set")
            self.clearButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;} QPushButton::hover{background-color: white; color: black;}")
            self.clearButton.clicked.connect(self.clearStudySet)
            self.createNewStudyLayout.addWidget(self.clearButton)
    def loadStudySet(self)->None:
        name=self.table.selectedItems()[0].text()
        self.currentSet.setName(name)
        self.currentSet.loadSet()
        self.StudyStudio()
    def check_study(self)->None:
        #create a threading timer that goes every second to check if SWITCH_STUDY=true
        #if it is, then call StudyStudio()
        if self.STUDY_STUDIO:self.StudyStudio()      
    def OpenExistingStudySet(self,e=None):
        #show a table that lists all the filenames in the ./Cards directory with a doubleclick event to choose one
        self.openExistingStudyLayout=QBoxLayout(QBoxLayout.TopToBottom,self)
        self.OPENEXISTINGQWidget=QWidget()
        self.OPENEXISTINGQWidget.setLayout(self.openExistingStudyLayout)
        self.addWidget(self.OPENEXISTINGQWidget)
        self.setCurrentWidget(self.OPENEXISTINGQWidget)
        self.openExistingStudyTitle=QLabel("Open an existing Study Set")
        self.openExistingStudyTitle.setStyleSheet("font: 50pt Comic Sans MS; color: white;")
        self.openExistingStudyTitle.move(0,0)
        self.openExistingStudyLayout.addWidget(self.openExistingStudyTitle)
        self.backButton=QPushButton("<---")
        self.backButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;} QPushButton::hover{background-color: white; color: black;}")
        self.backButton.clicked.connect(self.__init__)
        self.backButton.move(0,0)
        self.openExistingStudyLayout.addWidget(self.backButton)
        #make a table to select the correct file
        self.table=QTableWidget()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setStyleSheet("font: 20pt Comic Sans MS;background-color:black; color: white;")
        self.table.setColumnCount(1)
        self.table.setRowCount(0)
        #"font: 20pt Comic Sans MS; color: white;"
        self.table.setColumnWidth(0,300)
        self.table.setHorizontalHeaderLabels(["Study Set Name"])
        self.table.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: black;color: white;border: 1px solid #FFFFFF;}")
        self.table.verticalHeader().setStyleSheet("QHeaderView::section {background-color: black;color: white;border: 1px solid #FFFFFF;}")
        #self.table.horizontalHeader().setStyle(QStyleFactory.create('fusion'))
        self.table.cellDoubleClicked.connect(self.loadStudySet)
        self.openExistingStudyLayout.addWidget(self.table)
        self.files=glob.glob("./Cards/*.cards")
        #add all elements in self.files to table
        for file in self.files:
            file=file[8:]
            self.table.insertRow(self.table.rowCount())
            self.table.setItem(self.table.rowCount()-1,0,QTableWidgetItem(file.split("/")[-1].split(".")[0]))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

