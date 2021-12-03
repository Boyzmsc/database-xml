import pymysql
from PyQt5.QtWidgets import *
import sys, datetime                # Python은 date 데이타 타입을 제공하지 않음.

class DB_Utils:

    def queryExecutor(self, db, sql, params):
        conn = pymysql.connect(host='localhost', user='guest', password='bemyguest', db=db, charset='utf8')

        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:     # dictionary based cursor
                cursor.execute(sql, params)
                tuples = cursor.fetchall()
                return tuples
        except Exception as e:
            print(e)
            print(type(e))
        finally:
            conn.close()

    def updateExecutor(self, db, sql, params):
        conn = pymysql.connect(host='localhost', user='root', password='hyeokman', db=db, charset='utf8')

        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
            conn.commit()
        except Exception as e:
            print(e)
            print(type(e))
        finally:
            conn.close()

class DB_Queries:
    # 검색문은 여기에 각각 하나의 메소드로 정의
    def selectPlayerUsingPosition(self, position):
        sql = "SELECT * FROM player WHERE position = %s"
        params = (position)

        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)
        return tuples

class DB_Updates:
    # 갱신문은 여기에 각각 하나의 메소드로 정의
    def insertPlayer(self, player_id, player_name, team_id, position):
        sql = "INSERT INTO player (player_id, player_name, team_id, position) VALUES (%s, %s, %s, %s)"
        params = (player_id, player_name, team_id, position)

        util = DB_Utils()
        util.updateExecutor(db="kleague", sql=sql, params=params)

#########################################

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):

        # DB 검색문 실행
        query = DB_Queries()
        players = query.selectPlayerUsingPosition("GK")     # 딕셔너리의 리스트
        print(players)

        # 윈도우 설정
        self.setWindowTitle("DBAPI를 통한 테이블 위젯 생성 예제")
        self.setGeometry(0, 0, 1100, 600)

        # 테이블위젯 설정
        self.tableWidget = QTableWidget(self)   # QTableWidget 객체 생성
        self.tableWidget.move(50, 50)
        self.tableWidget.resize(1000, 500)
        self.tableWidget.setRowCount(len(players))              # 43
        self.tableWidget.setColumnCount(len(players[0]))        # 13
        columnNames = list(players[0].keys())
        # ['PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'E_PLAYER_NAME', 'NICKNAME', 'JOIN_YYYY', 'POSITION', 'BACK_NO', 'NATION', 'BIRTH_DATE', 'SOLAR', 'HEIGHT', 'WEIGHT']
        self.tableWidget.setHorizontalHeaderLabels(columnNames)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for player in players:                              # player는 딕셔너리임.
            rowIDX = players.index(player)                  # 테이블 위젯의 row index 할당

            for k, v in player.items():
                columnIDX = list(player.keys()).index(k)    # 테이블 위젯의 column index 할당

                if v == None:                               # 파이썬이 DB의 널값을 None으로 변환함.
                    continue                                # QTableWidgetItem 객체를 생성하지 않음
                elif isinstance(v, datetime.date):          # QTableWidgetItem 객체 생성
                    item = QTableWidgetItem(v.strftime('%Y-%m-%d'))     # MySQL의 format specifier
                else:
                    item = QTableWidgetItem(str(v))

                self.tableWidget.setItem(rowIDX, columnIDX, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

#########################################

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

main()