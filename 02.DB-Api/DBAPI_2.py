# PyMySQL 사용 절차

import pymysql

conn = pymysql.connect(host='localhost', user='guest', password='bemyguest', db='kleague', charset='utf8')

cursor = conn.cursor(pymysql.cursors.DictCursor)    # dictionary based cursor, 딕셔너리의 리스트
                                                    # 메소드의 argument는 패키지.모듈.클래스

sql = "SELECT * FROM player"
cursor.execute(sql)

players = cursor.fetchall()      # 딕셔너리의 리스트
print(len(players))
print(players)
print()

# value만 출력

for player in players:              # player는 딕셔너리임.
    for columnName in player:
        print(player[columnName], end=' ')
    print()

print()

# Key와 value를 같이 출력

for player in players:              # player는 딕셔너리임.
    for columnName in player:
        print(columnName, player[columnName], end=', ')
    print()

cursor.close()
conn.close()