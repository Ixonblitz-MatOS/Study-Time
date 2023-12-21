import sys,glob
from PyQt5 import QtGui, QtCore
from os.path import exists
from platform import system
from os import remove,mkdir
from random import choice
from win32com.client import Dispatch
from PyQt5.QtWidgets import QApplication,QGraphicsOpacityEffect,QFrame,QVBoxLayout,QCheckBox,QStackedWidget,QAbstractItemView, QWidget, QLabel, QPushButton,QBoxLayout,QLineEdit,QShortcut,QTableWidget,QTableWidgetItem,QProgressBar,QHBoxLayout
#make an error dialog box with init parameter of string to put a message to dialog and a button to close it labeled with "okay"
QFont=QtGui.QFont
QEventLoop=QtCore.QEventLoop
Qt=QtCore.Qt
class TTS:
    def __init__(self,message:str)->None:
        self.msg=message
        self.speaker=Dispatch("SAPI.SpVoice")
    def read(self)->None:
        self.speaker.Speak(self.msg)
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
class CheckboxFrame(QFrame):
    def __init__(self, options):
        super().__init__()
        self.setStyleSheet("background-color: black; color:white;")
        self.layout = QVBoxLayout()
        self.checkboxes = []
        for option in options:
            checkbox = QCheckBox(option)
            checkbox.setStyleSheet("QCheckBox{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: white;} QCheckBox::indicator:checked{background-image:check.jpg;}")
            self.checkboxes.append(checkbox)
            self.layout.addWidget(checkbox)
        self.setLayout(self.layout)

    def get_checked_options(self)->list:
        checked_options = []
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                checked_options.append(checkbox.text())
        return checked_options
class LearnSettingsDialog(QWidget):
    def __init__(self,parent) -> None:
        """
        Learn Settings:
        Question Type Choice:
                Flashcard
                Multiple Choice
                Written
                Read Aloud
                (All/some/one) allowed
            Card Order:
                shuffle=True/False
            Answer with:
                Term
                Definition
                (Both/One) allowed
        Storage:
            {Question Type Choice: [Flashcard, Multiple Choice, Written, Read Aloud], Card Order: [Shuffle], Answer with: [Term, Definition]}
        """
        super().__init__()
        self.p=parent
        self.layout=QBoxLayout(QBoxLayout.TopToBottom)
        self.layout.setSpacing(3)
        self.setAttribute(Qt.WA_DeleteOnClose)
        #add a keypress event to press the enter button
        self.keyPressEvent=QShortcut("Return",self)
        self.keyPressEvent.activated.connect(self._finish)
        QShortcut("Ctrl+Q",self).activated.connect(self._exit)
        self.setStyleSheet("background-color: black; color:white;")
        self.setGeometry(100,100,500,500)
        self.setLayout(self.layout)
        self.setWindowTitle("Learn Settings")
        self.message="Learn Settings"
        self.label=QLabel(self.message)
        self.label.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
        self.layout.addWidget(self.label)
        self.QuestionOptionsLabel=QLabel("Question Type Choice:")
        self.QuestionOptionsLabel.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
        self.layout.addWidget(self.QuestionOptionsLabel)
        options = ["Flashcard", "Multiple Choice", "Written", "Read Aloud"]
        self.checkbox_frame = CheckboxFrame(options)
        self.layout.addWidget(self.checkbox_frame)
        self.CardOrderLabel=QLabel("Card Order:")
        self.CardOrderLabel.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
        self.layout.addWidget(self.CardOrderLabel)
        options = ["Shuffle"]
        self.checkbox_frame = CheckboxFrame(options)
        self.layout.addWidget(self.checkbox_frame)
        self.AnswerOptionsLabel=QLabel("Answer with:")
        self.AnswerOptionsLabel.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
        self.layout.addWidget(self.AnswerOptionsLabel)
        options = ["Term","Definition"]
        self.checkbox_frame = CheckboxFrame(options)
        self.layout.addWidget(self.checkbox_frame)
        self.closeButton=QPushButton("Okay")
        self.closeButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px;border-color: white;} QPushButton::hover{background-color: white; color: black;}")
        self.closeButton.clicked.connect(self._finish)
        self.layout.addWidget(self.closeButton)
        self.layout.addStretch()
    def _getSettings(self)->dict:
        settings={}
        settings["Question Type Choice"]=self.checkbox_frame.get_checked_options()
        settings["Card Order"]=self.checkbox_frame.get_checked_options()
        settings["Answer with"]=self.checkbox_frame.get_checked_options()
        return settings
    def _finish(self)->None:
        self.p.LearnSettings=self._getSettings()
        self.close()
    def _exit(self):self.p._exit()
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
class LearnCard(QWidget):
    """
    Used for learn with implemented fade in/out QAnimation
    """
    def _learnNextQuestionType(self)->str:
        """
        depending on Learn Settings will determine what is allowed to be chosen
        """
        allowed_question_types=self.settings["Question Type Choice"]
        return choice(allowed_question_types)
    def fadein(self):
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)
        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
    def _learnNewQuestion(self)->None:
        """
        This function will get a new question and answer and change the text of the question and answer
        :NOTE: Must check if Shuffle is On, the Answer types, and the allowed Question types. The _learnNextQuestionType() keeps track of allowed question types
        """
        self.correctAnswer=""
        if self.settings["Card Order"]==["Shuffle"]:
            question=choice(list(self.cards.keys()))
            self.correctAnswer=self.cards[question]
            self.learnRightPanelQuestion.setText(question)
        else:pass

        self.fadein()#show new question at the end
    def getAnswer(self)->str:return self.learnRightPanelAnswer.text().rstrip()
    def fadeout(self):
        """
        Fade out after each question then call a new question before fading back in
        """
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)
        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()
        self._learnNewQuestion()
    def _learnSubmit(self):
        """
        This is run when submit is clicked. We must add an enter Shortcut to press the submit button
        This function evaluates the answer and changes the text of the button to Correct or Incorrect and changes the background to green or red
        Then get the next Question and Answer and change the text of the question and answer
        """
        if self.getAnswer()==self.correctAnswer:
            self.learnRightPanelSubmitButton.setText("Correct!")
            self.learnRightPanelSubmitButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; background-color: green; color: white;} QPushButton::hover{background-color: green; color: white;}")
            self.fadeout()
        else:
            self.learnRightPanelSubmitButton.setText("Incorrect!")
            self.learnRightPanelSubmitButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: red;} QPushButton::hover{background-color: red; color: white;}")
            self.fadeout()
    def _setProgressbars(self,amountOfQuestions:int)->None:
        self.Parent.learnLeftPanelProgressCorrect.setMaximum(amountOfQuestions)
        self.Parent.learnLeftPanelProgressIncorrect.setMaximum(amountOfQuestions)
    def _addCorrect(self)->None:self.Parent.learnLeftPanelProgressCorrect.setValue(self.Parent.learnLeftPanelProgressCorrect.value()+1)
    def _addIncorrect(self)->None:self.Parent.learnLeftPanelProgressIncorrect.setValue(self.Parent.learnLeftPanelProgressIncorrect.value()+1)
    def __init__(self,parent) -> None:
        super().__init__()
        self.Parent=parent
        self.learnRightPanelLayout=QBoxLayout(QBoxLayout.TopToBottom,self)
        self.setLayout(self.learnRightPanelLayout)
        self.setStyleSheet("background-color: black; color:white;border-style: outset; border-width: 2px; border-radius: 10px;border-color: white;")
        self.learnRightPanelTitle=QLabel("Question")
        self.learnRightPanelTitle.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
        self.learnRightPanelLayout.addWidget(self.learnRightPanelTitle)
        self.learnRightPanelQuestion=QLabel("What is the definition of the term?")
        self.learnRightPanelQuestion.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
        self.learnRightPanelLayout.addWidget(self.learnRightPanelQuestion)
        self.learnRightPanelAnswer=QLineEdit("")
        self.learnRightPanelAnswer.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
        self.learnRightPanelLayout.addWidget(self.learnRightPanelAnswer)
        self.learnRightPanelSubmitButton=QPushButton("Submit")
        self.learnRightPanelSubmitButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;} QPushButton::hover{background-color: white; color: black;}")
        self.learnRightPanelSubmitButton.clicked.connect(self._learnSubmit)
        self.learnRightPanelLayout.addWidget(self.learnRightPanelSubmitButton)
        #Set first card
        self.cards=self.Parent.currentset().cards
        self.settings=self.Parent.LearnSettings
        #we must calculate the amount of questions by the length of the amount of terms in the dictionary of self.cards
        self.amountOfQuestions=len(self.cards)
        self._setProgressbars(self.amountOfQuestions)
        self._learnNewQuestion()#All Question handling is done in this function
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
    class LearnLeftPanelQBox(QBoxLayout):
        def __init__(self):
            super().__init__(QBoxLayout.TopToBottom)
            self.setContentsMargins(0,0,0,0)
            self.setSpacing(0)

    def __init__(self):
        super().__init__()
        self.FirstMenuQWidget=QWidget()
        self.addWidget(self.FirstMenuQWidget)   
        self.setCurrentWidget(self.FirstMenuQWidget)
        self.LearnSettings={}
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
    def Flashcards(self):
        """
        Making flashcard system:
            using QPushButtons we can use large text with margins and padding to allow for a rounded card experience
            when you click on the card, it flips to the back
            when you click on the back, it flips to the front
            when you click on the next button, it goes to the next card
            when you click on the previous button, it goes to the previous card
            when you click on the exit button, it goes back to the study set menu
            All key binds are inherited from the main menu
        """
        self.FlashcardsObj=QWidget()
        self.FlashcardsLayout=QBoxLayout(QBoxLayout.TopToBottom,self)
        self.FlashcardsObj.setLayout(self.FlashcardsLayout)
        self.addWidget(self.FlashcardsObj)
        self.setCurrentWidget(self.FlashcardsObj)
        self.FlashcardsLayout.setObjectName("FlashcardsLayout")
        self.backButton=QPushButton("<---")
        self.backButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px;border-color: white;} QPushButton::hover{background-color: white; color: black;}")
        self.backButton.clicked.connect(self.StudyStudio)
        self.backButton.move(0,0)
        self.FlashcardsLayout.addWidget(self.backButton)
        #Create a frame that covers the screen where the left side has a correct/incorrect info section with a bar and the buttons for settings and in the middle another frame where flashcards go and buttons below it for next and previous
        self.flashcardFrame=QWidget()
        self.flashcardFrameLayout=QBoxLayout(QBoxLayout.LeftToRight,self)
        self.flashcardFrame.setLayout(self.flashcardFrameLayout)
        self.FlashcardsLayout.addWidget(self.flashcardFrame)
        self.flashcardFrame.setObjectName("flashcardFrame")
        self.flashcardFrame.setStyleSheet("background-color: black; color:white;border-style: outset; border-width: 2px; border-radius: 10px;border-color: white;")
        self.flashcardLeftPanel=QWidget()
        self.flashcardLeftPanelLayout=QBoxLayout(QBoxLayout.TopToBottom,self)
        self.flashcardLeftPanel.setLayout(self.flashcardLeftPanelLayout)
        self.flashcardFrameLayout.addWidget(self.flashcardLeftPanel)
        self.flashcardLeftPanel.setObjectName("flashcardLeftPanel")
        self.flashcardLeftPanel.setStyleSheet("background-color: black; color:white;border-style: outset; border-width: 2px; border-radius: 10px;border-color: white;")
    def _showLearnSettings(self):
        self.learnSettingsDialog=LearnSettingsDialog(self)
        self.learnSettingsDialog.show()
    def Learn(self):
        """
        Using a similar system to quizlet we can use multiple choice, written, read aloud, and flashcard to learn the study set
        flashcard:
            same as flashcard mode
        multiple choice:
            show the term and 4 definitions and you have to choose the correct definition
            clicking the definition will change the text to "Correct!" or "Incorrect" and change the background of the button to red or green
        written:
            Given the term or definition write the definition or term accordingly

        read aloud:

        global settings:
            Question Type Choice:
                Flashcard
                Multiple Choice
                Written
                Read Aloud
                (All/some/one) allowed
            Card Order:
                shuffle=True/False
            Answer with:
                Term
                Definition
                (Both/One) allowed
            Card Alerts:Off
        """
###########################################################################################################################
########GUI ONLY###########################################################################################################
###########################################################################################################################
        self.LearnObj=QWidget()
        self.LearnLayout=QBoxLayout(QBoxLayout.TopToBottom,self)
        self.LearnObj.setLayout(self.LearnLayout)
        self.addWidget(self.LearnObj)
        self.setCurrentWidget(self.LearnObj)
        self.LearnLayout.setObjectName("LearnLayout")
        self.backButton=QPushButton("<---")
        self.backButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px;border-color: white;} QPushButton::hover{background-color: white; color: black;}")
        self.backButton.clicked.connect(self.StudyStudio)
        self.backButton.move(0,0)
        self.LearnLayout.addWidget(self.backButton)
        #Create a frame that covers the screen where the left side has a correct/incorrect info section with a bar and the buttons for settings and in the middle another frame where flashcards go and buttons below it for next and previous
        self.learnFrame=QWidget()
        self.learnFrameLayout=QBoxLayout(QBoxLayout.LeftToRight,self)
        self.learnFrame.setLayout(self.learnFrameLayout)
        self.LearnLayout.addWidget(self.learnFrame)
        self.learnFrame.setObjectName("learnFrame")
        self.learnFrame.setStyleSheet("background-color: black; color:white;")
        self.learnLeftPanel=QWidget()
        self.learnLeftPanelLayout=self.LearnLeftPanelQBox()
        self.learnLeftPanel.setLayout(self.learnLeftPanelLayout)
        self.learnFrameLayout.addWidget(self.learnLeftPanel)
        self.learnLeftPanel.setObjectName("learnLeftPanel")
        self.learnLeftPanel.setStyleSheet("background-color: black; color:white;")
        self.learnLeftPanelTop=QWidget()
        self.learnLeftPanelTopLayout=QBoxLayout(QBoxLayout.TopToBottom,self)
        self.learnLeftPanelTop.setLayout(self.learnLeftPanelTopLayout)
        self.learnLeftPanelTitle=QLabel("Correct:")
        self.learnLeftPanelTopLayout.addWidget(self.learnLeftPanelTitle)
        self.learnLeftPanelTitle.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
        self.learnLeftPanelTopLayout.addWidget(self.learnLeftPanelTitle)
        self.learnLeftPanelProgressCorrect=QProgressBar()
        self.learnLeftPanelProgressCorrect.setStyleSheet("font: 20pt Comic Sans MS; color: green;")
        self.learnLeftPanelTopLayout.addWidget(self.learnLeftPanelProgressCorrect)
        self.learnLeftPanelTitle=QLabel("Incorrect:")
        self.learnLeftPanelTopLayout.addWidget(self.learnLeftPanelTitle)
        self.learnLeftPanelTitle.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
        self.learnLeftPanelProgressIncorrect=QProgressBar()
        self.learnLeftPanelProgressIncorrect.setStyleSheet("font: 20pt Comic Sans MS; color: red;")
        self.learnLeftPanelTopLayout.addWidget(self.learnLeftPanelProgressIncorrect)
        self.learnLeftPanelLayout.addWidget(self.learnLeftPanelTop)
        self.learnLeftPanelSettingsButton=QPushButton("Settings")
        self.learnLeftPanelSettingsButton.setStyleSheet("QPushButton{font: 20pt Comic Sans MS; color: white;border-style: outset; border-width: 2px; border-radius: 10px;border-color:white;} QPushButton::hover{background-color: white; color: black;}")
        self.learnLeftPanelSettingsButton.clicked.connect(self._showLearnSettings)
        self.learnLeftPanelLayout.addWidget(self.learnLeftPanelSettingsButton)
        self.learnRightPanel=LearnCard(self)
        self.learnFrameLayout.addWidget(self.learnRightPanel)

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
    if not system()=="Windows":
        print("This program is only supported on Windows")
        sys.exit(-1)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

