import sys
import os
import json
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QCalendarWidget, QWidget, QVBoxLayout, QHBoxLayout, QPlainTextEdit

        
# main window class
class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calendar")
        self.setFixedSize(QSize(1200, 600))

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        layout = QHBoxLayout()

        self.calendar = QCalendarWidget()
        self.calendar.setFixedSize(QSize(600, 600))
        layout.addWidget(self.calendar)

        buttonsLayout = QVBoxLayout()

        self.addNoteButton = QPushButton("Add a note")
        self.addNoteButton.clicked.connect(self.addNoteWindow)
        buttonsLayout.addWidget(self.addNoteButton)
        
        self.deleteNoteButton = QPushButton("Delete a note")
        self.deleteNoteButton.clicked.connect(self.deleteNote)
        buttonsLayout.addWidget(self.deleteNoteButton)
        
        self.checkNotesButton = QPushButton("Save notes to a file")
        self.checkNotesButton.clicked.connect(self.saveNotes)
        buttonsLayout.addWidget(self.checkNotesButton)
        
        self.importNotesButton = QPushButton("Import notes from a file")
        self.importNotesButton.clicked.connect(self.importNotes)
        buttonsLayout.addWidget(self.importNotesButton)

        self.textArea = QPlainTextEdit()
        self.textArea.setReadOnly(1)
        buttonsLayout.addWidget(self.textArea)

        layout.addLayout(buttonsLayout)
        centralWidget.setLayout(layout)

        self.notes = {}

        self.calendar.clicked.connect(self.dateSelected)

    def dateSelected(self):
        selectedDate = self.calendar.selectedDate()
        notesTemp = self.notes.get(selectedDate.toString(Qt.ISODate))
        self.textArea.clear()

        if notesTemp:
            self.textArea.setPlainText("\n".join(notesTemp))

    def addNoteWindow(self):
        self.addWindow = addNote(self)
        self.addWindow.show()

    def addNote(self, date, note):
        dateInStr = date.toString(Qt.ISODate)
        if dateInStr in self.notes:
            self.notes[dateInStr].append(note)
        else:
            self.notes[dateInStr] = [note]

    def updateNotes(self):
        self.dateSelected()

    def deleteNote(self):
        selectedDate = self.calendar.selectedDate()
        dateInStr = selectedDate.toString(Qt.ISODate)
        if dateInStr in self.notes:
            self.notes.pop(dateInStr)
        self.dateSelected()

    def saveNotes(self):
        outfile = open(os.path.expanduser("./notes.txt"), "w")
        outfile.write(json.dumps(self.notes))
        outfile.close()
        
    def importNotes(self):
        infile = open(os.path.expanduser("./notes.txt"), "r")
        self.notes = json.loads(infile.read())
        infile.close()

class addNote(QMainWindow):
    def __init__(self, mainWindow):
        super().__init__()

        self.mainWindow = mainWindow
        self.setFixedSize(QSize(440, 240))    
        self.setWindowTitle("Add a note") 
        self.textArea = QPlainTextEdit(self)
        self.textArea.resize(400,200)
        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.addButtonClicked)
        layout = QVBoxLayout()
        layout.addWidget(self.textArea)
        layout.addWidget(self.addButton)
        centralWidget = QWidget(self)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def addButtonClicked(self):
        text = self.textArea.toPlainText()
        selectedDate = self.mainWindow.calendar.selectedDate()
        self.mainWindow.addNote(selectedDate, text)
        self.mainWindow.updateNotes()
        self.close()

app = QApplication(sys.argv)
window = mainWindow()
window.show()
app.exec()
