import json

from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication, QThread, pyqtSignal, QRegularExpression, Qt
from PyQt5.QtGui import QIcon, QColor, QPalette, QFontMetrics, QSyntaxHighlighter, QTextCharFormat, QFont, QKeySequence, \
    QFontDatabase
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, qApp, QTextEdit, QFileDialog, QPlainTextEdit, \
    QPushButton, QDialog, QCheckBox
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name

import Utils
from Stream import Stream

language = ''
user = Utils.getMacAddress()


class MyTextEdit(QPlainTextEdit):
    def __init__(self, *args):
        QTextEdit.__init__(self, *args)
        fontdb = QFontDatabase()
        fontdb.addApplicationFont('JetBrainsMono-Regular.ttf')
        font = QFont()
        font.setFamily('JetBrainsMono-Regular')
        font.setPointSize(15)
        font.setStyleHint(QFont.Monospace)
        font.setFixedPitch(True)
        self.setFont(font)
        metrics = QFontMetrics(font)
        self.setTabStopWidth(metrics.width(' ') * 4)

        self.data = ''
        self.textChanged.connect(self.textChanged1)
        self.myTextCursor = self.textCursor()
        self.iterator = 0
        self.stackUndoRedo = list()
        self.stackCursor = list()
        self.yourself = True
        self.serverConnection = False

    def connectToServer(self, endpoint):
        self.stream = Stream()
        self.stream.log_signal.connect(self.print_log)
        self.stream.changeEndpoint(endpoint)
        self.stream.start()
        self.serverConnection = True

    def shareFile(self):
        self.stream = Stream()
        self.stream.log_signal.connect(self.print_log)
        url = Utils.getUrl()
        self.stream.changeEndpoint(url)
        self.stream.start()
        self.serverConnection = True

    def print_log(self, text):
        self.yourself = False
        # print(text)
        cursor = self.textCursor().position()
        self.setPlainText(text)
        self.myTextCursor.setPosition(cursor)
        self.setTextCursor(self.myTextCursor)



    def keyPressEvent(self, event):
        self.yourself = True
        # print('stack>>' + str(len(self.stackUndoRedo)) + ' iter >> ' + str(self.iterator))
        # print(self.stackUndoRedo)
        if event.matches(QKeySequence.Undo):
            self.yourself = False
            self.undo()
        elif event.matches(QKeySequence.Redo):
            self.yourself = False
            self.redo()
        else:
            pass
        # del self.stackUndoRedo[self.iterator:]
        # To get the remaining functionality back (e.g. without this, typing would not work):
        QPlainTextEdit.keyPressEvent(self, event)

    def undo(self):
        self.yourself = False
        # self.ownCursorPosition -= len(self.stack[self.iterator-1])
        # self.ownCursorPosition -= 1
        if 0 < self.iterator <= len(self.stackUndoRedo):
            self.iterator -= 1
            # print(self.iterator)
            # print(self.iterator)
            self.setPlainText(self.stackUndoRedo[self.iterator])
            self.myTextCursor.setPosition(self.stackCursor[self.iterator])
            self.setTextCursor(self.myTextCursor)
        # my own undo code

    def redo(self):
        self.yourself = False
        if self.iterator + 1 < len(self.stackUndoRedo):
            print('redo')
            self.iterator += 1
            print(len(self.stackUndoRedo))
            print(self.iterator)
            self.setPlainText(self.stackUndoRedo[self.iterator])
            self.myTextCursor.setPosition(self.stackCursor[self.iterator])
            self.setTextCursor(self.myTextCursor)

    def textChanged1(self):
        if self.toPlainText() != self.data and self.toPlainText() != '' and self.yourself:
            if self.iterator + 1 < len(self.stackUndoRedo):
                print(self.stackUndoRedo)
                del self.stackUndoRedo[self.iterator + 1:]
                del self.stackCursor[self.iterator + 1:]
                print(self.stackUndoRedo)

            self.data = self.toPlainText()
            self.stackUndoRedo.append(self.data)
            self.stackCursor.append(self.textCursor().position())
            self.iterator += 1
            if self.data[len(self.data) - 1] != ' ':
                self.data = self.data + ' '
            cursor = self.textCursor().position()
            self.selectAll()
            self.insertPlainText(self.data)
            self.myTextCursor.setPosition(cursor)
            self.setTextCursor(self.myTextCursor)
            if self.serverConnection:
                send = {'sender': user, 'message': self.data}
                self.stream.ws.send(json.dumps(send))

    def changeLanguage(self, lang):
        global language
        # print(lang)
        language = lang
        self.yourself = False
        print(language)
        # self.setHtml(self.getHTML(self.data))
