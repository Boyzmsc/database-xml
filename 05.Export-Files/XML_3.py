# XML 화일을 읽어서, DB Table에 쓰는 예제.

import pymysql
import xml.etree.ElementTree as ET

class DB_Utils:

    def updateExecutor(self, db, sql, params):
        conn = pymysql.connect(host='localhost', user='guest', password='bemyguest', db=db, charset='utf8')

        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
            conn.commit()
        except Exception as e:
            print(e)
            print(type(e))
        finally:
            conn.close()

class DB_Updates:

    def dropPlayerGK(self):
        sql = "DROP TABLE IF EXISTS playerGK"
        params = ()             # 넘겨줄 파라미터가 없음

        util = DB_Utils()
        util.updateExecutor(db="kleague", sql=sql, params=params)

    def createPlayerGK(self):
        sql = '''CREATE TABLE playerGK (
                    player_id     CHAR(7) 		NOT NULL,
                    player_name   VARCHAR(20) 	NOT NULL,
                    team_id       CHAR(3) 		NOT NULL,
                    e_player_name VARCHAR(40),
                    nickname      VARCHAR(30),
                    join_YYYY     CHAR(4),
                    position      VARCHAR(10),
                    back_no       TINYINT,
                    nation        VARCHAR(20),
                    birth_date    DATE,
                    solar         CHAR(1),
                    height        SMALLINT,
                    weight        SMALLINT,
                    CONSTRAINT 	  pk_player 		PRIMARY KEY (player_id)
                )'''
        params = ()             # 넘겨줄 파라미터가 없음

        util = DB_Utils()
        util.updateExecutor(db="kleague", sql=sql, params=params)

    def populatePlayerGK(self, player_id, player_name, team_id, e_player_name, nickname, join_YYYY, position, back_no, nation, birth_date, solar, height, weight):
        sql = "INSERT INTO playerGK VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        params = (player_id, player_name, team_id, e_player_name, nickname, join_YYYY, position, back_no, nation, birth_date, solar, height, weight)

        util = DB_Utils()
        util.updateExecutor(db="kleague", sql=sql, params=params)

#########################################

def readXML_writeDB():

    # DB에 PlayerGK 테이블을 생성
    update = DB_Updates()
    update.dropPlayerGK()
    update.createPlayerGK()

    # XML 화일을 XDM 트리로 메모리에 로딩
    tree = ET.parse('playerGK.xml')
    rootElement = tree.getroot()

    # XDM 트리를 파이썬 객체(딕셔너리)로 변환
    players = []
    for childElement in rootElement:
        print(childElement.tag, childElement.attrib)
        players.append(childElement.attrib)
    print()

    # DB의 PlayerGK 테이블에 레코드를 삽입
    columnNames = list(players[0].keys())

    for player in players:
        row = []
        for columnName in columnNames:
            if player[columnName] == '':
                player[columnName] = None
            row.append(player[columnName])
        print(row)

        update.populatePlayerGK(*row)       # * operator 사용
        # update.populatePlayerGK(row[0], row[1], ... row[12])

readXML_writeDB()