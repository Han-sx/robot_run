import sqlite3

conn = sqlite3.connect('person_info.db')
cur = conn.cursor()



sql_text_1 = "SELECT * FROM info"

# 执行sql语句
cur.execute(sql_text_1)



# 获取查询结果
r = cur.fetchall()

for i in r:
    have_namidou = i[3]
    qq = i[0]
    new_namidou = int(have_namidou) + 5000
    sql_text_3 = "UPDATE info SET 娜米豆 = " + str(new_namidou) + " WHERE QQ = " + str(qq)
    cur.execute(sql_text_3)
    print(i)

# 确认插入
conn.commit()
# 关闭游标
cur.close()
# 关闭连接
conn.close()