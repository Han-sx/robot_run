import sqlite3
import requests

# have_things数据库包括have_things表和 things 表
conn = sqlite3.connect('have_things.db')
cur = conn.cursor()

# 建表的sql语句 创建 things 表
sql_text_1 = '''CREATE TABLE things
    (序号 TEXT, 物品 TEXT, 价值 INT);'''

# sql_text_2 = "SELECT * FROM info ORDER BY 娜米豆 DESC;"
sql_text_3 = "SELECT * FROM things"
# have_things:(QQ TEXT, 物品 TEXT)
# sql_text_3 = "SELECT * FROM things"
sql_text_4 = "UPDATE things SET 物品 = '【气息】-加百利·星陨' WHERE 序号 = '205'"

sql_text_5 = "INSERT INTO things VALUES('205','【气息】-加百利·星陨', 30000)"

sql_text_6 = "ALTER TABLE things ADD COLUMN 价值 INT"

sql_text_7 = "DELETE FROM things WHERE 序号='202'"

# 建表的sql语句 创建 have_pets 表
sql_text_8 = '''CREATE TABLE have_pets
    (QQ TEXT, 宠物 TEXT);'''


# 执行sql语句
cur.execute(sql_text_3)

# sql_text_4 = "DELETE FROM have_things WHERE 物品 ='" + str("生锈的贴片") + "' AND QQ = '" + str("1399300412") + "'"
# cur.execute(sql_text_4)
# 插入保留的
# sql_text_5 = "INSERT INTO have_things VALUES('" + str("1399300412") + "', '" + str("生锈的铁片") + "')"
# for i in range(1):
#     cur.execute(sql_text_5)

# 确认插入
conn.commit()

# 获取查询结果
r = cur.fetchall()

for i in r:
    print(i)

# first_qq = r[0][3]
# second_qq = r[1][0]
# third_qq = r[2][0]
# fourest_qq = r[3][0]
# fivest_qq = r[4][0]

# print(str(first_qq) + second_qq + third_qq + fourest_qq + fivest_qq)

# 关闭游标
cur.close()
# 关闭连接
conn.close()

# for i in range(5):
#     print("你好")
# gid = 811784497

# gid2 = 656058487

# first_namidou = 12345
# second_namidou = 323232
# third_namidou = 434343
# fourest_namidou = 5656
# fivest_namidou = 5353

# first_name = "发的冯绍峰"
# second_name = "重复问问"
# third_name = "年率王老吉"
# fourest_name ="发动机发链接" 
# fivest_name = "保温农田"

# url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid2) + "&message=[CQ:face,id=137]娜米豆排行榜[CQ:face,id=137]\n\n[CQ:face,id=143]一：" + str(first_name) + " " + str(first_namidou) + "\n[CQ:face,id=143]二：" + str(second_name) + " " + str(second_namidou) + "\n[CQ:face,id=143]三：" + str(third_name) + " " + str(third_namidou) + "\n[CQ:face,id=143]四：" + str(fourest_name) + " " + str(fourest_namidou) + "\n[CQ:face,id=143]五：" + str(fivest_name) + " " + str(fivest_namidou)
# print(url)
# requests.get(url)
# url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid2) + "&message=[CQ:face,id=138]娜娜米良心商店[CQ:face,id=138]\n\n[CQ:face,id=159]丽芙·蚀暗：10w nmd\n[CQ:face,id=159]露西亚·红莲:10w nmd\n[CQ:face,id=159]里·异火：10w nmd\n\n[CQ:face,id=169]禁言卡(1分钟)：1w nmd"

# url = "http://127.0.0.1:5700/get_group_member_info?group_id=656058487&user_id=980675326"
# url2 = "http://127.0.0.1:5700/get_group_member_info?group_id=656058487&user_id=1399300412"
# r = requests.get(url)
# card = r.json()['data']['card']
# nickname = r.json()['data']['nickname']
# print(len(card))
# print(nickname)