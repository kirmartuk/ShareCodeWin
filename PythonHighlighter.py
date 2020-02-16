from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
import re

settingTheme = False


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        keywordFormat = QTextCharFormat()

        keywordFormat.setFontWeight(QFont.Bold)

        keywordPatterns = [r"\band\b", r"\bas\b", r"\bassert\b",
                           r"\bbreak\b", r"\bclass\b", r"\bcontinue\b",
                           r"\bdef\b", r"\bdel\b", r"\belif\b", r"\belse\b",
                           r"\bexcept\b", r"\bexec\b", r"\bfinally\b", r"\bfor\b",
                           r"\bfrom\b", r"\bglobal\b", r"\bif\b", r"\bimport\b",
                           r"\bin\b", r"\bis\b", r"\blambda\b", r"\bnot\b",
                           r"\bor\b", r"\bpass\b", r"\bprint\b", r"\braise\b",
                           r"\breturn\b", r"\btry\b", r"\bwhile\b", r"\bwith\b",
                           r"\byield\b", r"\bTrue\b", r"\bFalse\b", r"\bin\b", r"\bNone\b"]

        quotationFormat = QTextCharFormat()
        stringRe = QRegExp(r"""(?:'[^']*'|"[^"]*")""")
        classFormat = QTextCharFormat()
        functionFormat = QTextCharFormat()
        singleLineCommentFormat = QTextCharFormat()
        stringRe.setMinimal(True)
        classFormat.setFontWeight(QFont.Bold)
        functionFormat.setFontItalic(True)
        self.multiLineCommentFormat = QTextCharFormat()
        self.stringFormat = QTextCharFormat()

        if settingTheme:
            quotationFormat.setForeground(QColor('#006b10'))
            classFormat.setForeground(QColor('#FFFFFF'))
            functionFormat.setForeground(QColor('#a6e22e'))
            singleLineCommentFormat.setForeground(QColor('#75715e'))
            self.multiLineCommentFormat.setForeground(Qt.red)
            self.stringFormat.setForeground(QColor('#e6db74'))
            keywordFormat.setForeground(QColor('#f92672'))
        else:
            quotationFormat.setForeground(QColor('#006b10'))
            classFormat.setForeground(QColor('#0000FF'))
            functionFormat.setForeground(QColor('#0000FF'))
            singleLineCommentFormat.setForeground(QColor('#408080'))
            self.multiLineCommentFormat.setForeground(Qt.red)
            self.stringFormat.setForeground(QColor('#BA2121'))
            keywordFormat.setForeground(QColor('#008000'))

        self.highlightingRules = [(QRegExp(pattern), keywordFormat)
                                  for pattern in keywordPatterns]
        self.highlightingRules.append((QRegExp('\"[^\"\n]*\"'), quotationFormat))
        self.highlightingRules.append((QRegExp('\"{3}[^\"]*\"{3}'), quotationFormat))
        self.highlightingRules.append((stringRe, self.stringFormat))
        self.highlightingRules.append((QRegExp("\\bQ[A-Za-z]+\\b"),
                                       classFormat))
        self.highlightingRules.append((QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
                                       functionFormat))
        self.highlightingRules.append((QRegExp("#[^\n]*"),
                                       singleLineCommentFormat))

        self.commentStartExpression = QRegExp('/\*')
        self.commentEndExpression = QRegExp('\*/')

    # commentFormat = QTextCharFormat()
    # commentFormat.setForeground(QColor('#888888'))
    # commentFormat.setFontItalic(True)
    # self.highlightingRules.append((QRegExp(r"^#.*"),
    #                                commentFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)
            if (pattern.pattern() == """(?:'[^']*'|"[^"]*")"""):
                ss = re.findall(r"""(?:'[^']*'|"[^"]*")""", text)
                if (len(ss) > 0):
                    text = re.sub(r"""(?:'[^']*'|"[^"]*")""", ' ' * len(ss[0]), text)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength,
                           self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text,
                                                             startIndex + commentLength);
