import sqlite3

conn = sqlite3.connect('jiaoyisuo.db')
cur = conn.cursor()

# 建表的sql语句 创建 jiaoyisuo 表
sql_text_10 = '''CREATE TABLE jiaoyisuo
    (编号 TEXT, 出售人 TEXT, QQ TEXT, 物品 TEXT, 价格 INT);'''

sql_text_1 = "SELECT * FROM jiaoyisuo"

sql_text_2 = "UPDATE info SET 娜米豆 = 10000"

sql_text_3 = "ALTER TABLE info ADD COLUMN 成就 TEXT; "

sql_text_4 = "UPDATE info SET 成就 = '无'"

sql_text_5 = "INSERT INTO jiaoyisuo VALUES('111111', '111111','111111', '111111', 1)"
# # 建表的sql语句 创建 info 表
# sql_text_1 = '''CREATE TABLE info
#         (QQ TEXT, 等级 INT, 经验值 INT, 娜米豆 INT, 宠物 TEXT, 道具 TEXT, 签到状态 INT);'''

# 执行sql语句
cur.execute(sql_text_1)

# 确认插入
conn.commit()

# 获取查询结果
r = cur.fetchall()
print(r)
for i in r:
    print(i)

# 关闭游标
cur.close()
# 关闭连接
conn.close()