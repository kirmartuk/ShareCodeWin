#!/home/kirill/PycharmProjects/myproject/venv python
import os
import sys
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication, QThread, pyqtSignal, QRegularExpression, QSettings, QUrl
from PyQt5.QtGui import QIcon, QColor, QPalette, QFontMetrics, QSyntaxHighlighter, QTextCharFormat, QFont, QTextCursor, \
    QFontDatabase
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, qApp, QTextEdit, QFileDialog, QPlainTextEdit, \
    QPushButton, QDialog, QCheckBox, QMessageBox, QListWidget, QGridLayout, QLabel, QVBoxLayout, QWidget, QScrollArea, \
    QComboBox, QLineEdit

from MyTextEdit import MyTextEdit
import PythonHighlighter

settingTheme = False
settingLanguage = ''
filePath = ''
checkBoxState = 'CheckBoxState'
languageState = 'LanguageState'
ORGANIZATION_NAME = 'Martyuk'
ORGANIZATION_DOMAIN = 'martyuk.com'
APPLICATION_NAME = 'ShareCode'


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def print_log(self, text):
        # print('print log>>' + text)
        if text != self.textEdit.toPlainText():
            self.textEdit.setText(text)

    def state_changed(self, int):
        global settingTheme
        settings = QSettings()
        if self.checkBox.isChecked():
            settingTheme = True
            self.setTheme()

        else:
            settingTheme = False
            self.setTheme()
        settings.setValue(checkBoxState, settingTheme)
        settings.sync()

    def initSettings(self):
        global settingTheme, settingLanguage
        settings = QSettings()
        settingTheme = settings.value(checkBoxState, False, type=bool)
        PythonHighlighter.settingTheme = settingTheme
        settingLanguage = settings.value(languageState, '', type=str)
        self.textEdit.changeLanguage(settingLanguage)

    def initUI(self):
        self.textEdit = MyTextEdit()
        self.initSettings()
        self.textEdit.setUndoRedoEnabled(False)
        self.setTheme()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.openFile)

        saveFile = QAction('Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.saveFile)

        settings = QAction(QIcon("icons/font-color.png"), "Settings", self)
        settings.triggered.connect(self.settingsDialog)

        shareFile = QAction(QIcon('open.png'), 'Share', self)
        shareFile.setShortcut('Ctrl+Q')
        shareFile.setStatusTip('Share file')
        shareFile.triggered.connect(self.textEdit.shareFile)

        connectToServer = QAction('Connect', self)
        connectToServer.setStatusTip('Connect to ShareFile')
        connectToServer.triggered.connect(self.connectDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        fileMenu.addAction(settings)
        fileMenu.addAction(shareFile)
        fileMenu.addAction(connectToServer)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()

    def changeWindowTitle(self, text):
        self.setWindowTitle(text)

    def test(self, link):
        self.changeWindowTitle(link)
        self.textEdit.connectToServer(link)

    def connectDialog(self):
        dlg = QDialog(self)
        dlg.setObjectName("Dialog")
        # dlg.resize(400, 300)

        grid = QVBoxLayout()
        link = QLabel('Link')
        lineEdit = QLineEdit()
        connectButton = QPushButton('Connect')
        connectButton.clicked.connect(lambda: self.test(lineEdit.text()))
        grid.addWidget(link)
        grid.addWidget(lineEdit)
        grid.addWidget(connectButton)
        dlg.setLayout(grid)

        dlg.show()

    def setTheme(self):

        global high
        if (settingTheme):
            self.textEdit.setStyleSheet("""
                            QWidget {
                                background-color: "#24241d";
                                color: white;
                                selection-background-color: grey 
                                }
                            """)
            app.setStyleSheet("""
                           QWidget {
                               background-color: "#11110d";
                               color: white;
                               }
                           """)
            # self.textEdit.document().setDefaultStyleSheet(darkCss)
        else:
            self.textEdit.setStyleSheet("""
                            QWidget {
                                background-color: rgb(230, 230, 230);
                                color: black;
                                selection-background-color: grey

                                }
                            """)
            app.setStyleSheet("""
                           QWidget {
                               background-color: rgb(230, 230, 230);
                               color: black;
                               }
                           """)
        PythonHighlighter.settingTheme = settingTheme
        high = PythonHighlighter.Highlighter(self.textEdit.document())


    def openFile(self):
        global filePath
        qfiledialog = QFileDialog()
        fname = qfiledialog.getOpenFileName(self, 'Open file', '/ home')[0]
        if (fname != ''):
            f = open(fname, 'r')
            filePath = fname
            with f:
                data = f.read()
                self.textEdit.setPlainText(data)
            f.close()
        self.changeWindowTitle(QUrl(fname).fileName())

    def saveFile(self):
        global filePath
        if (filePath != ''):
            file = open(filePath, 'w')
            file.write(self.textEdit.toPlainText())
            file.close()
        else:
            name = QFileDialog.getSaveFileName(self, 'Save File')[0]
            filePath = name
            if (filePath != ''):
                file = open(name, 'w+')
                text = self.textEdit.toPlainText()
                file.write(text)
                file.close()

    def changeLang(self, args):
        global settingLanguage
        settings = QSettings()
        self.textEdit.changeLanguage(args)
        settingLanguage = args
        settings.setValue(languageState, settingLanguage)
        settings.sync()

    def settingsDialog(self):
        dlg = QDialog(self)
        dlg.setObjectName("Dialog")
        # dlg.resize(400, 300)

        grid = QVBoxLayout()

        themeTitle = QLabel('Theme')
        languageTitle = QLabel('Language')

        self.checkBox = QCheckBox()
        self.checkBox.setText('Darkios')
        self.checkBox.setChecked(settingTheme)
        self.checkBox.stateChanged.connect(self.state_changed)

        self.langSelector = QComboBox()
        langs = open('Languages.txt', 'r')
        for i in langs.readlines():
            self.langSelector.addItem(i[0:-1])
        self.langSelector.setCurrentText(settingLanguage)

        self.langSelector.activated[str].connect(self.changeLang)

        grid.addWidget(themeTitle)
        grid.addWidget(self.checkBox)
        grid.addWidget(languageTitle)
        grid.addWidget(self.langSelector)

        dlg.setLayout(grid)

        dlg.show()


if __name__ == '__main__':
    QCoreApplication.setApplicationName(ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(APPLICATION_NAME)
    app = QApplication(sys.argv)
    ex = Example()
    high = PythonHighlighter.Highlighter(ex.textEdit.document())
    sys.exit(app.exec_())
