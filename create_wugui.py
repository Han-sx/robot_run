import sqlite3

conn = sqlite3.connect('wugui.db')
cur = conn.cursor()


sql_text_1 = '''CREATE TABLE wugui
    (游戏编号 INT, QQ TEXT, 答案 TEXT, 娜米豆 INT);'''

# sql_text_1 = "SELECT * FROM wugui"

# 执行sql语句
cur.execute(sql_text_1)



# 确认插入
conn.commit()

# 获取查询结果
r = cur.fetchall()

print(r)

# 关闭游标
cur.close()
# 关闭连接
conn.close()
