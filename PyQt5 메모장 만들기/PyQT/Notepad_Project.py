import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QTextCursor
from PyQt5 import QtCore
from PyQt5 import QtGui

form_class = uic.loadUiType("Notepad.ui")[0]

class FindWindow(QDialog):
    def __init__(self, parent):
        super(FindWindow, self).__init__(parent)
        uic.loadUi("Find.ui", self)
        self.show()

        self.parent = parent
        self.cursor = parent.plainTextEdit.textCursor()
        self.pe = parent.plainTextEdit

        self.pushButton_findnext.clicked.connect(self.findNext)
        self.pushButton_cancle.clicked.connect(self.close)

        self.radioButton_down.clicked.connect(self.updown_radio_button)
        self.radioButton_up.clicked.connect(self.updown_radio_button)
        self.up_down = "down"


    def updown_radio_button(self):
        if self.radioButton_up.isChecked():
            self.up_down = "up"
        elif self.radioButton_down.isChecked():
            self.up_down = "down"


    # 기본적으로 지원해주는 함수. (뒤에 event가 들어가면 기본 지원 함수라 봐도 됨)
    def keyReleaseEvent(self, event):
        if self.lineEdit.text():
            self.pushButton_findnext.setEnabled(True)
        else:
            self.pushButton_findnext.setEnabled(False)

    def findNext(self):
        pattern = self.lineEdit.text()  # 찾을 문자열
        text = self.pe.toPlainText()  # Note 의 내용
        reg = QtCore.QRegExp(pattern)  # 검색을 수행해주는는 기능 함수
        self.cursor = self.parent.plainTextEdit.textCursor()

        if self.checkBox_CaseSensitive.isChecked():
            cs = QtCore.Qt.CaseSensitive
        else:
            cs = QtCore.Qt.CaseInsensitive

        reg.setCaseSensitivity(cs)
        pos = self.cursor.position()

        if self.up_down == "down":
            index = reg.indexIn(text, pos)  # indexIn()에서 두번째 인자는 text 의 몇번째 문자 부터 검사할 지를 의미한다. (검색하기)
        else:
            pos -= len(pattern) + 1
            index = reg.lastIndexIn(text, pos)
            # index = reg.lastIndexIn(text, pos - (len(pattern) + 1)) # 이렇게 하니까 안됨..


        if (index != -1) and (pos > -1):    # 검색된 결과가 있다면
            self.setCursor(index, len(pattern) + index)
        else:
            self.notFoundMsg(pattern)

    def setCursor(self, start, end):
        print(self.cursor.selectionStart(), self.cursor.selectionEnd())

        self.cursor.setPosition(start)
        self.cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end-start)     # Anchor 이라는 영어 뜻은 전 줄을 묶다.
        self.pe.setTextCursor(self.cursor)

    def notFoundMsg(self, pattern):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('메모장')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('''"{}"을(를) 찾을 수 없습니다.'''.format(pattern))
        msgBox.addButton('확인', QMessageBox.YesRole)
        msgBox.exec_()


class ReplaceWindow(QDialog):
    def __init__(self, parent):
        super(ReplaceWindow, self).__init__(parent)
        uic.loadUi("Replace.ui", self)
        self.show()

        self.parent = parent
        self.cursor = parent.plainTextEdit.textCursor()
        self.pe = parent.plainTextEdit

        self.pushButton_findnext.clicked.connect(self.findNext)
        self.pushButton_replace_all.clicked.connect(self.replaceAll)
        self.pushButton_cancle.clicked.connect(self.close)


    # 기본적으로 지원해주는 함수. (뒤에 event가 들어가면 기본 지원 함수라 봐도 됨)
    def keyReleaseEvent(self, event):
        if self.lineEdit_find.text():
            self.pushButton_findnext.setEnabled(True)
            self.pushButton_replace.setEnabled(True)
            self.pushButton_replace_all.setEnabled(True)
        else:
            self.pushButton_findnext.setEnabled(False)
            self.pushButton_replace.setEnabled(False)
            self.pushButton_replace_all.setEnabled(False)

    def findNext(self):
        pattern = self.lineEdit_find.text()  # 찾을 문자열
        text = self.pe.toPlainText()  # Note 의 내용
        reg = QtCore.QRegExp(pattern)  # 검색을 수행해주는는 기능 함수
        self.cursor = self.parent.plainTextEdit.textCursor()

        if self.checkBox_CaseSensitive.isChecked():
            cs = QtCore.Qt.CaseSensitive
        else:
            cs = QtCore.Qt.CaseInsensitive

        reg.setCaseSensitivity(cs)
        pos = self.cursor.position()

        index = reg.indexIn(text, pos)  # indexIn()에서 두번째 인자는 text 의 몇번째 문자 부터 검사할 지를 의미한다. (검색하기)

        if (index != -1):    # 검색된 결과가 있다면
            self.setCursor(index, len(pattern) + index)
        else:
            self.notFoundMsg(pattern)

    def setCursor(self, start, end):
        print(self.cursor.selectionStart(), self.cursor.selectionEnd())

        self.cursor.setPosition(start)
        self.cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end-start)     # Anchor 이라는 영어 뜻은 전 줄을 묶다.
        self.pe.setTextCursor(self.cursor)

    def notFoundMsg(self, pattern):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('메모장')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('''"{}"을(를) 찾을 수 없습니다.'''.format(pattern))
        msgBox.addButton('확인', QMessageBox.YesRole)
        msgBox.exec_()

    def replaceAll(self):
        data = self.pe.toPlainText()
        pattern = self.lineEdit_find.text()  # 찾을 문자열
        replace = self.lineEdit_replace.text()  # 바꿀 문자열
        self.pe.setPlainText(data.replace(pattern, replace))



class LookingPicture(QDialog):
    def __init__(self, parent):
        super(LookingPicture, self).__init__(parent)
        uic.loadUi("Pictures.ui", self)
        self.show()

        self.pushButton_picture1.clicked.connect(self.selectPicture_1)
        self.pushButton_picture2.clicked.connect(self.selectPicture_2)

    def selectPicture_1(self):
        self.label_picture.setPixmap(QtGui.QPixmap("Picture_1.png"))

    def selectPicture_2(self):
        self.label_picture.setPixmap(QtGui.QPixmap("Picture_2.png"))



class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.actionOpen.triggered.connect(self.openFunction)
        self.actionSave.triggered.connect(self.saveFunction)
        self.actionSave_As.triggered.connect(self.saveAsFunction)
        self.actionClose.triggered.connect(self.close)

        self.actionUndo.triggered.connect(self.undoFunction)
        self.actionCut.triggered.connect(self.cutFunction)
        self.actionCopy.triggered.connect(self.copyFunction)
        self.actionPaste.triggered.connect(self.pasteFunction)

        self.actionFind.triggered.connect(self.findFunction)
        self.actionReplace.triggered.connect(self.replaceFunction)

        self.actionLooking_Picture.triggered.connect(self.lookingPicture)


        self.opened = False
        self.opened_file_path = '제목 없음'

    # Note 변경사항 존재 == True, 없으면 False
    def ischanged(self):
        if not self.opened:
            if self.plainTextEdit.toPlainText().strip(): # 열린적이 없고 Note 내용이 있으면 True
                return True
            return False

        current_data = self.plainTextEdit.toPlainText() # 현재 데이터

        # 파일에 저장된 데이터
        with open(self.opened_file_path, encoding='UTF8') as f:
            file_data = f.read()

        if current_data == file_data:
            return False
        else:
            return True


    def save_changed_data(self):
        msgBox = QMessageBox()
        msgBox.setText("변경 내용을 {}에 저장하시겠습니까?".format(self.opened_file_path))
        msgBox.addButton('저장', QMessageBox.YesRole) #0
        msgBox.addButton('저장 안함', QMessageBox.NoRole) #1
        msgBox.addButton('취소', QMessageBox.RejectRole) #2
        ret = msgBox.exec_()
        if ret == 0:
            self.saveFunction()
        else:   # 1 아니면 2인 경우.
            return ret


    def closeEvent(self, event):
        if self.ischanged(): # 열린적 있고 변경사항 있을 때
            ret = self.save_changed_data()

            if ret == 2:
                event.ignore()


    def open_file(self, fname):
        with open(fname, encoding='UTF8') as f:
            data = f.read()
        self.plainTextEdit.setPlainText(data)

        self.opened = True
        self.opened_file_path = fname

        print("open {}!!".format(fname))

    def save_file(self, fname):
        data = self.plainTextEdit.toPlainText()

        with open(fname, 'w', encoding='UTF8') as f:
            f.write(data)

        self.opened = True
        self.opened_file_path = fname

        print("save {}!!".format(fname))

    def openFunction(self):
        ret = 0
        if self.ischanged(): # 열린적 있고 변경사항 있을 때
            ret = self.save_changed_data()

        if not ret == 2:
            fname = QFileDialog.getOpenFileName(self)
            if fname[0]:
                self.open_file(fname[0])

    def saveFunction(self):
        if self.opened:
            self.save_file(self.opened_file_path)
        else:
            self.saveAsFunction()

    def saveAsFunction(self):
        fname = QFileDialog.getSaveFileName(self)
        if fname[0]:
            self.save_file(fname[0])

    def undoFunction(self):
        self.plainTextEdit.undo()

    def cutFunction(self):
        self.plainTextEdit.cut()

    def copyFunction(self):
        self.plainTextEdit.copy()

    def pasteFunction(self):
        self.plainTextEdit.paste()

    def findFunction(self):
        FindWindow(self)

    def replaceFunction(self):
        ReplaceWindow(self)

    def lookingPicture(self):
        LookingPicture(self)


app = QApplication(sys.argv)
mainWindow = WindowClass()
mainWindow.show()
app.exec_()