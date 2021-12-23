from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import xml.etree.ElementTree as ET
import pymysql
import sys
import datetime
import csv
import json

class DB_Utils:

    def queryExecutor(self, db, sql, params):
        conn = pymysql.connect(
            host='localhost', user='guest', password='bemyguest', db='kleague', charset='utf8')

        try:
            # dictionary based cursor
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, params)
                tuples = cursor.fetchall()
                return tuples
        except Exception as e:
            print(e)
            print(type(e))
        finally:
            conn.close()

#################################################################################
#################################################################################

class DB_Queries:
    
    def selectPlayerTeam(self):
        sql = "SELECT DISTINCT team_name, team_id FROM team"
        params = ()

        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)
        return tuples

    def selectPlayerPosition(self):
        sql = "SELECT DISTINCT position FROM player"
        params = ()

        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)
        return tuples

    def selectPlayerNation(self):
        sql = "SELECT DISTINCT nation FROM player"
        params = ()

        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)
        return tuples

    def selectPlayer(self, team, teamIds, position, nation, height, heightCompare, weight, weightCompare):
        if (team == "ALL" and position == "ALL" and nation == "ALL"):
            sql = "SELECT * FROM player"
            params = []

        elif (team != "ALL" and position == "ALL" and nation == "ALL"):
            sql = "SELECT * FROM player WHERE team_id = %s"
            params = [teamIds[team]]

        elif (team == "ALL" and position != "ALL" and nation == "ALL"):
            if (position == "미정"):
                sql = "SELECT * FROM player WHERE position IS NULL"
                params = []
            else:
                sql = "SELECT * FROM player WHERE position = %s"
                params = [position]

        elif (team == "ALL" and position == "ALL" and nation != "ALL"):
            if (nation == "대한민국"):
                sql = "SELECT * FROM player WHERE nation IS NULL"
                params = []
            else:
                sql = "SELECT * FROM player WHERE nation = %s"
                params = [nation]

        elif (team != "ALL" and position != "ALL" and nation == "ALL"):
            if (position == "미정"):
                sql = "SELECT * FROM player WHERE team_id = %s AND position IS NULL"
                params = [teamIds[team]]
            else:
                sql = "SELECT * FROM player WHERE team_id = %s AND position = %s"
                params = [teamIds[team], position]

        elif (team != "ALL" and position == "ALL" and nation != "ALL"):
            if (nation == "대한민국"):
                sql = "SELECT * FROM player WHERE team_id = %s AND nation IS NULL"
                params = [teamIds[team]]
            else:
                sql = "SELECT * FROM player WHERE team_id = %s AND nation = %s"
                params = [teamIds[team], nation]

        elif (team == "ALL" and position != "ALL" and nation != "ALL"):
            if (position == "미정" and nation == "대한민국"):
                sql = "SELECT * FROM player WHERE position IS NULL AND nation IS NULL"
                params = []
            elif (position == "미정" and nation != "대한민국"):
                sql = "SELECT * FROM player WHERE position IS NULL AND nation = %s"
                params = [nation]
            elif (position != "미정" and nation == "대한민국"):
                sql = "SELECT * FROM player WHERE position = %s AND nation IS NULL"
                params = [position]
            else:
                sql = "SELECT * FROM player WHERE position = %s AND nation = %s"
                params = [position, nation]

        elif (team != "ALL" and position != "ALL" and nation != "ALL"):
            if (position == "미정" and nation == "대한민국"):
                sql = "SELECT * FROM player WHERE team_id = %s AND position IS NULL AND nation IS NULL"
                params = [teamIds[team]]
            elif (position == "미정" and nation != "대한민국"):
                sql = "SELECT * FROM player WHERE team_id = %s AND position IS NULL AND nation = %s"
                params = [teamIds[team], nation]
            elif (position != "미정" and nation == "대한민국"):
                sql = "SELECT * FROM player WHERE team_id = %s AND position = %s AND nation IS NULL"
                params = [teamIds[team], position]
            else:
                sql = "SELECT * FROM player WHERE team_id = %s AND position = %s AND nation = %s"
                params = [teamIds[team], position, nation]

        if (height != -1 and weight != -1):
            if (team == "ALL" and position == "ALL" and nation == "ALL"):
                sql += " WHERE height " + heightCompare + " %s AND weight " + weightCompare + " %s"
            else:
                sql += " AND height " + heightCompare + " %s AND weight " + weightCompare + " %s"
            params += [height, weight]

        elif (height != -1 and weight == -1):
            if (team == "ALL" and position == "ALL" and nation == "ALL"):
                sql += " WHERE height " + heightCompare + " %s"
            else:
                sql += " AND height " + heightCompare + " %s"
            params += [height]

        elif (height == -1 and weight != -1):
            if (team == "ALL" and position == "ALL" and nation == "ALL"):
                sql += " WHERE weight " + weightCompare + " %s"
            else:
                sql += " AND weight " + weightCompare + " %s"
            params += [weight]

        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)
        return tuples

#################################################################################
#################################################################################

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.teamName = "ALL"
        self.position = "ALL"
        self.nation = "ALL"
        self.height = -1
        self.heightCompare = ">="
        self.weight = -1
        self.weightCompare = ">="
        self.fileType = "csv"

    def setupUI(self):
        # 윈도우 설정
        self.setWindowTitle("Report 1")
        self.setGeometry(100, 100, 1000, 800)

        # 팀명
        self.teamNameLabel = QLabel("팀명 :", self)
        self.teamNameComboBox = QComboBox(self)
        query = DB_Queries()
        rows = query.selectPlayerTeam()
        columnName = list(rows[0].keys())[0]
        items = [row[columnName] for row in rows]
        self.teamNameComboBox.addItem("ALL")
        self.teamNameComboBox.addItems(items)
        self.teamNameComboBox.activated.connect(self.teamNameComboBox_Activated)
        self.teamNameComboBox.setCurrentIndex(0)

        self.teamIds = {}
        t_name = list(rows[0].keys())[0]
        t_id = list(rows[0].keys())[1]
        for row in rows:
            self.teamIds[row[t_name]] = row[t_id]

        # 포지션
        self.positionLabel = QLabel("포지션 :", self)
        self.positionComboBox = QComboBox(self)
        query = DB_Queries()
        rows = query.selectPlayerPosition()
        columnName = list(rows[0].keys())[0]
        items = ['미정' if row[columnName] == None else row[columnName] for row in rows]
        self.positionComboBox.addItem("ALL")
        self.positionComboBox.addItems(items)
        self.positionComboBox.activated.connect(self.positionComboBox_Activated)
        self.positionComboBox.setCurrentIndex(0)

        # 출신국
        self.nationLabel = QLabel("출신국 :", self)
        self.nationComboBox = QComboBox(self)
        query = DB_Queries()
        rows = query.selectPlayerNation()
        columnName = list(rows[0].keys())[0]
        items = ['대한민국' if row[columnName] == None else row[columnName] for row in rows]
        self.nationComboBox.addItem("ALL")
        self.nationComboBox.addItems(items)
        self.nationComboBox.activated.connect(self.nationComboBox_Activated)
        self.nationComboBox.setCurrentIndex(0)

        # 키
        self.heightLabel = QLabel("키 :", self)
        self.heightLineEdit = QLineEdit("", self)

        self.heightUpBtn = QRadioButton("이상", self)
        self.heightUpBtn.setChecked(True)
        self.heightUpBtn.clicked.connect(self.heightRadioBtn_Clicked)

        self.heightDownBtn = QRadioButton("이하", self)
        self.heightDownBtn.clicked.connect(self.heightRadioBtn_Clicked)

        self.heightBtnGroup = QButtonGroup()
        self.heightBtnGroup.addButton(self.heightUpBtn)
        self.heightBtnGroup.addButton(self.heightDownBtn)

        # 몸무게
        self.weightLabel = QLabel("몸무게 :", self)
        self.weightLineEdit = QLineEdit("", self)

        self.weightUpBtn = QRadioButton("이상", self)
        self.weightUpBtn.setChecked(True)
        self.weightUpBtn.clicked.connect(self.weightRadioBtn_Clicked)

        self.weightDownBtn = QRadioButton("이하", self)
        self.weightDownBtn.clicked.connect(self.weightRadioBtn_Clicked)

        self.weightBtnGroup = QButtonGroup()
        self.weightBtnGroup.addButton(self.weightUpBtn)
        self.weightBtnGroup.addButton(self.weightDownBtn)

        # 버튼
        self.btnClear = QPushButton("초기화", self)
        self.btnClear.resize(self.btnClear.sizeHint())
        self.btnClear.setToolTip("초기화")
        self.btnClear.clicked.connect(self.btnClear_Clicked)

        self.btnSearch = QPushButton("검색", self)
        self.btnSearch.resize(self.btnSearch.sizeHint())
        self.btnSearch.setToolTip("검색")
        self.btnSearch.clicked.connect(self.btnSearch_Clicked)

        # 선수 검색 레이아웃
        self.searchLayout_inner_1 = QHBoxLayout()
        self.searchLayout_inner_1.addWidget(self.teamNameLabel)
        self.searchLayout_inner_1.addWidget(self.teamNameComboBox)
        self.searchLayout_inner_1.addSpacing(60)
        self.searchLayout_inner_1.addWidget(self.positionLabel)
        self.searchLayout_inner_1.addWidget(self.positionComboBox)
        self.searchLayout_inner_1.addSpacing(60)
        self.searchLayout_inner_1.addWidget(self.nationLabel)
        self.searchLayout_inner_1.addWidget(self.nationComboBox)
        self.searchLayout_inner_1.addSpacing(60)
        self.searchLayout_inner_1.addWidget(self.btnClear)

        self.searchLayout_inner_2 = QHBoxLayout()
        self.searchLayout_inner_2.addWidget(self.heightLabel)
        self.searchLayout_inner_2.addWidget(self.heightLineEdit)
        self.searchLayout_inner_2.addSpacing(20)
        self.searchLayout_inner_2.addWidget(self.heightUpBtn)
        self.searchLayout_inner_2.addWidget(self.heightDownBtn)
        self.searchLayout_inner_2.addSpacing(60)
        self.searchLayout_inner_2.addWidget(self.weightLabel)
        self.searchLayout_inner_2.addWidget(self.weightLineEdit)
        self.searchLayout_inner_2.addSpacing(20)
        self.searchLayout_inner_2.addWidget(self.weightUpBtn)
        self.searchLayout_inner_2.addWidget(self.weightDownBtn)
        self.searchLayout_inner_2.addSpacing(60)
        self.searchLayout_inner_2.addWidget(self.btnSearch)

        self.searchLayout = QVBoxLayout()
        self.searchLayout.addLayout(self.searchLayout_inner_1)
        self.searchLayout.addLayout(self.searchLayout_inner_2)

        self.searchGroupBox = QGroupBox("선수 검색", self)
        self.searchGroupBox.setLayout(self.searchLayout)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(1000, 500)

        # 결과 출력 레이아웃
        self.tableLayout = QVBoxLayout()
        self.tableLayout.addWidget(self.tableWidget)

        self.tableGroupBox = QGroupBox("검색된 선수들", self)
        self.tableGroupBox.setLayout(self.tableLayout)

        # 파일 버튼
        self.csvBtn = QRadioButton("CSV", self)
        self.csvBtn.setChecked(True)
        self.csvBtn.clicked.connect(self.fileRadioBtn_Clicked)

        self.jsonBtn = QRadioButton("JSON", self)
        self.jsonBtn.clicked.connect(self.fileRadioBtn_Clicked)

        self.xmlBtn = QRadioButton("XML", self)
        self.xmlBtn.clicked.connect(self.fileRadioBtn_Clicked)

        self.fileBtnGroup = QButtonGroup()
        self.fileBtnGroup.addButton(self.csvBtn)
        self.fileBtnGroup.addButton(self.jsonBtn)
        self.fileBtnGroup.addButton(self.xmlBtn)

        # 저장 버튼
        self.btnSave = QPushButton("저장", self)
        self.btnSave.resize(self.btnSave.sizeHint())
        self.btnSave.setToolTip("저장")
        self.btnSave.clicked.connect(self.btnSave_Clicked)

        # 파일 출력 레이아웃
        self.fileLayout = QHBoxLayout()
        self.fileLayout.addWidget(self.csvBtn)
        self.fileLayout.addSpacing(60)
        self.fileLayout.addWidget(self.jsonBtn)
        self.fileLayout.addSpacing(60)
        self.fileLayout.addWidget(self.xmlBtn)
        self.fileLayout.addSpacing(60)
        self.fileLayout.addWidget(self.btnSave)

        self.fileGroupBox = QGroupBox("파일 출력", self)
        self.fileGroupBox.setLayout(self.fileLayout)

        # 메인 레이아웃
        self.subLayout = QVBoxLayout()
        self.subLayout.addSpacing(20)
        self.subLayout.addWidget(self.searchGroupBox)
        self.subLayout.addSpacing(30)
        self.subLayout.addWidget(self.tableGroupBox)
        self.subLayout.addSpacing(30)
        self.subLayout.addWidget(self.fileGroupBox)
        self.subLayout.addSpacing(20)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addSpacing(40)
        self.mainLayout.addLayout(self.subLayout)
        self.mainLayout.addSpacing(40)

        self.setLayout(self.mainLayout)

    def teamNameComboBox_Activated(self):
        self.teamName = self.teamNameComboBox.currentText()

    def positionComboBox_Activated(self):
        self.position = self.positionComboBox.currentText()

    def nationComboBox_Activated(self):
        self.nation = self.nationComboBox.currentText()

    def heightRadioBtn_Clicked(self):
        self.heightCompare = ">="
        if self.heightUpBtn.isChecked():
            self.heightCompare = ">="
        elif self.heightDownBtn.isChecked():
            self.heightCompare = "<="

    def weightRadioBtn_Clicked(self):
        self.weightCompare = ">="
        if self.weightUpBtn.isChecked():
            self.weightCompare = ">="
        elif self.weightDownBtn.isChecked():
            self.weightCompare = "<="

    def btnClear_Clicked(self):
        self.teamName = "ALL"
        self.teamNameComboBox.setCurrentIndex(0)
        self.position = "ALL"
        self.positionComboBox.setCurrentIndex(0)
        self.nation = "ALL"
        self.nationComboBox.setCurrentIndex(0)

        self.height = -1
        self.heightLineEdit.setText("")
        self.weight = -1
        self.weightLineEdit.setText("")
        self.heightCompare = ">="
        self.heightUpBtn.setChecked(True)
        self.weightCompare = ">="
        self.weightUpBtn.setChecked(True)

    def btnSearch_Clicked(self):
        # 정수값이 입력 안될 시 고려
        if (self.heightLineEdit.text().isdigit() and self.heightLineEdit.text() != ""):
            self.height = int(self.heightLineEdit.text())
        elif(self.heightLineEdit.text() == ""):
            self.height = -1
        else:
            dialog = QMessageBox(self)
            dialog.setWindowTitle("Information")
            dialog.setText("\'키\'에 정수를 입력하시오.")
            dialog.setIcon(QMessageBox.Icon.Information)
            dialog.exec()

            self.height = -1
            self.heightLineEdit.setText("")
            return

        if (self.weightLineEdit.text().isdigit() and self.weightLineEdit.text() != ""):
            self.weight = int(self.weightLineEdit.text())
        elif(self.weightLineEdit.text() == ""):
            self.weight = -1
        else:
            dialog = QMessageBox(self)
            dialog.setWindowTitle("Information")
            dialog.setText("\'몸무게\'에 정수를 입력하시오.")
            dialog.setIcon(QMessageBox.Icon.Information)
            dialog.exec()

            self.weight = -1
            self.weightLineEdit.setText("")
            return

        query = DB_Queries()
        players = query.selectPlayer(self.teamName, self.teamIds, self.position, self.nation, self.height, self.heightCompare, self.weight, self.weightCompare)

        self.tableWidget.clearContents()

        # Index out of range 고려
        if(len(players) > 0):
            self.tableWidget.setRowCount(len(players))
            self.tableWidget.setColumnCount(len(players[0]))
            columnNames = list(players[0].keys())
            self.tableWidget.setHorizontalHeaderLabels(columnNames)
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            self.tableWidget.setRowCount(len(players))

        for player in players:

            rowIDX = players.index(player)

            for k, v in player.items():
                columnIDX = list(player.keys()).index(k)

                if k == "POSITION" and v == None:
                    item = QTableWidgetItem(str("미정"))
                elif k == "NATION" and v == None:
                    item = QTableWidgetItem(str("대한민국"))
                elif isinstance(v, datetime.date):
                    item = QTableWidgetItem(v.strftime('%Y-%m-%d'))
                else:
                    item = QTableWidgetItem(str(v))

                self.tableWidget.setItem(rowIDX, columnIDX, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    def btnSave_Clicked(self):
        # 정수값이 입력 안될 시 고려
        if (self.heightLineEdit.text().isdigit() and self.heightLineEdit.text() != ""):
            self.height = int(self.heightLineEdit.text())
        elif(self.heightLineEdit.text() == ""):
            self.height = -1
        else:
            dialog = QMessageBox(self)
            dialog.setWindowTitle("Information")
            dialog.setText("\'키\'에 정수를 입력하시오.")
            dialog.setIcon(QMessageBox.Icon.Information)
            dialog.exec()

            self.height = -1
            self.heightLineEdit.setText("")
            return

        if (self.weightLineEdit.text().isdigit() and self.weightLineEdit.text() != ""):
            self.weight = int(self.weightLineEdit.text())
        elif(self.weightLineEdit.text() == ""):
            self.weight = -1
        else:
            dialog = QMessageBox(self)
            dialog.setWindowTitle("Information")
            dialog.setText("\'몸무게\'에 정수를 입력하시오.")
            dialog.setIcon(QMessageBox.Icon.Information)
            dialog.exec()

            self.weight = -1
            self.weightLineEdit.setText("")
            return

        query = DB_Queries()
        players = query.selectPlayer(self.teamName, self.teamIds, self.position, self.nation, self.height, self.heightCompare, self.weight, self.weightCompare)

        # Index out of range 고려
        # 저장할 결과가 없을 경우 고려
        if(len(players) == 0):
            dialog = QMessageBox(self)
            dialog.setWindowTitle("Information")
            dialog.setText("저장할 데이터가 없습니다.")
            dialog.setIcon(QMessageBox.Icon.Information)
            dialog.exec()
            return

        if (self.fileType == "csv"):
            with open('player.csv', 'w', encoding='utf-8', newline='') as f:
                wr = csv.writer(f)

                # 테이블 헤더를 출력
                columnNames = list(players[0].keys())

                wr.writerow(columnNames)

                # 테이블 내용을 출력
                for player in players:
                    for k, v in player.items():
                        if k == "POSITION" and v == None:
                            player[k] = "미정"
                        elif k == "NATION" and v == None:
                            player[k] = "대한민국"

                    row = list(player.values())
                    wr.writerow(row)

        elif (self.fileType == "json"):
            for player in players:
                for k, v in player.items():
                    if k == "POSITION" and v == None:
                        player[k] = "미정"
                    elif k == "NATION" and v == None:
                        player[k] = "대한민국"
                    elif isinstance(v, datetime.date):
                        player[k] = v.strftime('%Y-%m-%d')

            newDict = dict(player=players)

            with open('player.json', 'w', encoding='utf-8') as f:
                json.dump(newDict, f, ensure_ascii=False)

        elif (self.fileType == "xml"):
            for player in players:
                for k, v in player.items():
                    if k == "POSITION" and v == None:
                        player[k] = "미정"
                    elif k == "NATION" and v == None:
                        player[k] = "대한민국"
                    elif isinstance(v, datetime.date):
                        player[k] = v.strftime('%Y-%m-%d')

            newDict = dict(player=players)

            # XDM 트리 생성
            tableName = list(newDict.keys())[0]
            tableRows = list(newDict.values())[0]

            rootElement = ET.Element('Table')
            rootElement.attrib['name'] = tableName

            for row in tableRows:
                rowElement = ET.Element('Row')
                rootElement.append(rowElement)

                for columnName in list(row.keys()):
                    if row[columnName] == None:
                        rowElement.attrib[columnName] = ''
                    else:
                        rowElement.attrib[columnName] = row[columnName]

                    if type(row[columnName]) == int:
                        rowElement.attrib[columnName] = str(row[columnName])

            # XDM 트리를 화일에 출력
            ET.ElementTree(rootElement).write('player.xml', encoding='utf-8', xml_declaration=True)

    def fileRadioBtn_Clicked(self):
        self.fileType = "csv"
        if self.csvBtn.isChecked():
            self.fileType = "csv"
        elif self.jsonBtn.isChecked():
            self.fileType = "json"
        elif self.xmlBtn.isChecked():
            self.fileType = "xml"

#################################################################################
#################################################################################

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

main()
