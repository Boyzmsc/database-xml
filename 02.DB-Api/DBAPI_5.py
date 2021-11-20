# 클래스로 정의함.

import pymysql

class DB_Utils:

    # SQL 질의문(sql과 params)을 전달받아서, 실행하는 메소드
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
            cursor.close()
            conn.close()

    # SQL 갱신문(sql과 params)을 전달받아서, 실행하는 메소드
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
            cursor.close()
            conn.close()

class DB_Queries:
    # 검색문을 각각 하나의 메소드로 정의

    def selectPlayer(self, position):
        sql = "SELECT * FROM player WHERE position = %s"
        params = (position)

        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)
        return tuples

class DB_Updates:
    # 갱신문을 각각 하나의 메소드로 정의

    def insertPlayer(self, player_id, player_name, team_id, position):
        sql = "INSERT INTO player (player_id, player_name, team_id, position) VALUES (%s, %s, %s, %s)"
        params = (player_id, player_name, team_id, position)

        util = DB_Utils()
        util.updateExecutor(db="kleague", sql=sql, params=params)

#########################################

if __name__ == "__main__":      # DBAPI_5.py가 실행될 때 __main__ (True), import될 때는 모듈명 즉 DBAPI_5 (False)
    query = DB_Queries()
    players = query.selectPlayer("GK")
    print(len(players))
    print(players)
    print()

    update = DB_Updates()
    update.insertPlayer("2020004", "홍길동", "K01", "GK")

    players = query.selectPlayer("GK")
    print(len(players))
    print(players)
