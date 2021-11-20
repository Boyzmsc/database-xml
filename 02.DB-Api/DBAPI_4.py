# Dynamic SQL (SQL injection 공격에 대비)

import pymysql

conn = pymysql.connect(host='localhost', user='guest', password='bemyguest', db='kleague', charset='utf8')

try:
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM player WHERE team_id = %s AND position = %s"        # dynamic SQL
        params = ('K02','GK')
        cursor.execute(sql, params)
        players = cursor.fetchall()
        print(players)
except Exception as e:
    print(e)
    print(type(e))
finally:
    conn.close()