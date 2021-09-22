import sqlite3

conn = sqlite3.connect('person_info.db')
cur = conn.cursor()

# 建表的sql语句 创建 info 表
# sql_text_1 = '''CREATE TABLE wugui
#     (游戏编号 INT, QQ TEXT, 答案 TEXT, 娜米豆 INT);'''

sql_text_1 = "SELECT * FROM info"

sql_text_2 = "UPDATE info SET 娜米豆 = 10000"

sql_text_3 = "ALTER TABLE info ADD COLUMN 成就 TEXT; "

sql_text_4 = "UPDATE info SET 成就 = '无'"
# # 建表的sql语句 创建 info 表
# sql_text_1 = '''CREATE TABLE info
#         (QQ TEXT, 等级 INT, 经验值 INT, 娜米豆 INT, 宠物 TEXT, 道具 TEXT, 签到状态 INT);'''

# 执行sql语句
cur.execute(sql_text_1)




# 确认插入
conn.commit()

# 获取查询结果
r = cur.fetchall()

for i in r:
    print(i)

# 关闭游标
cur.close()
# 关闭连接
conn.close()