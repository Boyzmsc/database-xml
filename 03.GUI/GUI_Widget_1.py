import sys
# 모듈명으로 import하지 않았으므로, 해당 모듈(QtWidgets.pyd)에 정의된 변수, 함수, 클래스를 모듈 이름을 통해 접근할 필요 없이 바로 사용할 수 있음.
from PyQt5.QtWidgets import QWidget, QApplication, QToolTip, QPushButton, QMessageBox
from PyQt5.QtGui import QFont

class MainWindow(QWidget):          # QWidget 클래스의 서브클래스
    def __init__(self):
        super().__init__()          # MainWindow 클래스의 생성자, QWidget.__init__()을 호출
        self.setupUI()              # self는 해당 클래스의 인스턴스를 의미

    def setupUI(self):              # UI를 구성함
        # 툴팁 설정
        QToolTip.setFont(QFont("SansSerif", 12))    # QToolTip 객체를 생성하는 것이 아님. 단지 QToolTip.setFont() 메소드 실행

        # 윈도우 설정
        self.setWindowTitle("윈도우 생성 예제")
        # self.setGeometry(0, 0, 400, 300)      # x, y, w, h
        self.move(0, 0)         # x, y
        self.resize(400, 300)   # w, h

        # 버튼 설정
        self.pushButton = QPushButton("ToolTip 버튼", self)
        self.pushButton.move(50, 50)
        self.pushButton.resize(self.pushButton.sizeHint())
        self.pushButton.setToolTip("버튼 툴팁")
        self.pushButton.clicked.connect(self.pushButton_Clicked)    # button 객체의 'clicked' 시그널에 대해 'pushButton_Clicked' 슬롯을 연결함.

    def pushButton_Clicked(self):
        QMessageBox.about(self, "메세지 박스", "Push Button Clicked")
        # self.messageBox = QMessageBox(self)
        # self.messageBox.about(self, "메세지 박스", "Push Button Clicked")
        print('Push Button Clicked')

#########################################

if __name__ == "__main__":          # GUI_Widget_1.py가 실행될 때 __main__ (True), import될 때는 모듈명 (False)
    app = QApplication(sys.argv)    # event loop 생성을 위해, QApplication 객체를 생성함.
    mainWindow = MainWindow()       # 윈도우를 생성함 (UI 구성함).
    mainWindow.show()
    app.exec_()                     # 윈도우의 event loop에 들어감.
    # sys.exit(app.exec_())           # 종료 이벤트가 일어나면, 윈도우를 종료함.