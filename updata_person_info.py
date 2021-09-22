import sqlite3
import time


while 1:

    conn = sqlite3.connect('person_info.db')
    cur = conn.cursor()

    # sql_text_3 = "SELECT * FROM study"
    # cur.execute(sql_text_3)

    sql_text_4 = "SELECT * FROM info"
    cur.execute(sql_text_4)

    # 获取查询结果
    r = cur.fetchall()

    # 遍历执行
    for i in r:
        print(i)
        qq = i[0]
        print(qq)
        sql_text_5 = "UPDATE info SET 签到状态 = 0 WHERE QQ = " + str(qq)
        cur.execute(sql_text_5)

    # 确认插入
    conn.commit()
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()

    # time.sleep(24*60*60)
    time.sleep(86400)