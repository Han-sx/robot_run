import json
from sys import meta_path

import requests
import re
import random
import sqlite3
import time


'下面这个函数用来判断信息开头的几个字是否为关键词'
'如果是关键词则触发对应功能，群号默认为空'


def keyword_g(json):
    print(json)
    gid = json.get('group_id')  # 获取群号
    uid = json.get('sender').get('user_id')  # 获取发送人q
    raw_message = json.get('raw_message')  # 获取消息
    message = json.get('message')  # 获取全消息
    print('==============')
    print(message)
    account = 0

    # if '涩图' in message or '瑟图' in message or '色图' in message:
    # if message == '色图' or message == '涩图' or message == '瑟图':
    #     setu(message, gid, uid)

    # # 如果有人@娜娜米
    # if '[CQ:at,qq=2246376807]' in raw_message:

    # 返回图片
    if raw_message == '涩图' or raw_message == '瑟图' or raw_message == '色图' or raw_message == '来点色图' or raw_message == '来点瑟图' or raw_message == '来点涩图':
        while account != 3:
            r = requests.get("https://api.lolicon.app/setu/v2")  # 获取
            p_url = r.json()['data'][0]['urls']['original']  # 解析url
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=[CQ:image,file=" + str(p_url) + "]"
            requests.get(url)
            print(raw_message + str(uid))
            print(p_url)
            account += 1
            time.sleep(1)
        return 'OK'

    # 自主学习
    if raw_message[0:3] == '学习 ':
        try:
            # 拆分语句
            new_message = raw_message[3:]
            location = re.search(' ', new_message).span()
            print(location)
            question = new_message[:location[0]]  # 问
            print(question)
            answer = new_message[location[1]:]  # 答
            print(answer)

            # 与 data.db 数据库连接
            conn = sqlite3.connect('data.db')
            cur = conn.cursor()

            # # 建表的sql语句 创建 study 表
            # sql_text_1 = '''CREATE TABLE study
            #         (问题 TEXT,
            #             答案 TEXT);'''

            # # 执行sql语句
            # cur.execute(sql_text_1)

            # 插入单条数据
            sql_text_2 = "INSERT INTO study VALUES('" + \
                question + "', '" + answer + "')"
            print(sql_text_2)
            cur.execute(sql_text_2)

            # 确认插入
            conn.commit()

            # 关闭游标
            cur.close()
            # 关闭连接
            conn.close()

            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=太棒了！娜娜米又学到新的姿势了呢~！"
            requests.get(url)

            return 'OK'
        except:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=学习格式错误\n格式：学习-问题-回复~！"
            requests.get(url)
            return 'OK'

    # 删除问题
    if raw_message[0:5] == '删除回复 ':
        try:
            # 拆分语句
            new_message = raw_message[5:]
            print(new_message)

            # 与 data.db 数据库连接
            conn = sqlite3.connect('data.db')
            cur = conn.cursor()

            # # 建表的sql语句 创建 study 表
            # sql_text_1 = '''CREATE TABLE study
            #         (问题 TEXT,
            #             答案 TEXT);'''

            # # 执行sql语句
            # cur.execute(sql_text_1)

            # 查找单条数据
            sql_text_2 = "SELECT * FROM study WHERE 答案='" + new_message + "'"
            print(sql_text_2)
            cur.execute(sql_text_2)

            r = cur.fetchall()

            if len(r) == 0:
                # 关闭游标
                cur.close()
                # 关闭连接
                conn.close()

                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=娜娜米没有找到这条回复呢~"
                requests.get(url)
            else:
                sql_text_4 = "DELETE FROM study WHERE 答案='" + new_message + "'"
                cur.execute(sql_text_4)

                # 确认插入
                conn.commit()

                # 关闭游标
                cur.close()
                # 关闭连接
                conn.close()

                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=销毁记忆成功~"
                requests.get(url)
            return 'OK'
        except:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=删除格式错误\n格式：删除回复-回复内容"
            requests.get(url)
            return 'OK'

    # 查询个人信息
    if raw_message == '查询':
        try:
            # 与 data.db 数据库连接
            conn = sqlite3.connect('person_info.db')
            cur = conn.cursor()

            # # 建表的sql语句 创建 info 表
            # sql_text_1 = '''CREATE TABLE info
            #         (QQ TEXT, 等级 INT, 经验值 INT, 娜米豆 INT, 宠物 TEXT, 道具 TEXT, 签到状态 INT);'''

            # # 执行sql语句
            # cur.execute(sql_text_1)

            # 查找单条数据
            sql_text_2 = "SELECT * FROM info WHERE QQ='" + str(uid) + "'"
            print(sql_text_2)
            cur.execute(sql_text_2)

            r = cur.fetchall()

            print(r)
            if len(r) == 0:
                # 插入单条数据
                sql_text_3 = "INSERT INTO info VALUES('" + \
                    str(uid) + "', 1, 0, 0, '无', '无', 0, 0, '无')"
                print(sql_text_3)
                cur.execute(sql_text_3)

                # 确认插入
                conn.commit()
                # 关闭游标
                cur.close()
                # 关闭连接
                conn.close()

                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(
                    uid) + "]\n[CQ:face,id=74]等级：1\n[CQ:face,id=144]经验值：0\n[CQ:face,id=158]娜米豆：0\n[CQ:face,id=159]宠物：无\n[CQ:face,id=169]道具：无"
                print(url)
                requests.get(url)
            else:
                grade = r[0][1]
                exp = r[0][2]
                namicoin = r[0][3]
                pet = r[0][4]
                props = r[0][5]
                achievement = r[0][8]

                # 确认插入
                conn.commit()
                # 关闭游标
                cur.close()
                # 关闭连接
                conn.close()

                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(uid) + "]\n[CQ:face,id=74]等级：" + str(
                    grade) + "\n[CQ:face,id=144]经验值：" + str(exp) + "\n[CQ:face,id=158]娜米豆：" + str(namicoin) + "\n[CQ:face,id=159]宠物：" + str(pet) + "\n[CQ:face,id=169]道具：" + str(props) + "\n[CQ:face,id=190]成就：" + str(achievement)
                print(url)
                requests.get(url)
            return 'OK'
        except:
            return 'OK'

    # 签到获取娜米豆
    if raw_message == '签到':
        try:
            # 与 data.db 数据库连接
            conn = sqlite3.connect('person_info.db')
            cur = conn.cursor()

            # 查找单条数据
            sql_text_2 = "SELECT * FROM info WHERE QQ='" + str(uid) + "'"
            print(sql_text_2)
            cur.execute(sql_text_2)

            r = cur.fetchall()

            print(r)
            if len(r) == 0:
                nami_insert = random.randint(3500, 5000)
                # 插入单条数据
                sql_text_3 = "INSERT INTO info VALUES('" + str(
                    uid) + "', 1, 0, " + str(nami_insert) + ", '无', '无', 1, 0, '无')"
                print(sql_text_3)
                cur.execute(sql_text_3)

                # 确认插入
                conn.commit()
                # 关闭游标
                cur.close()
                # 关闭连接
                conn.close()

                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(uid) + "]\n\n签到成功，获取到" + str(
                    nami_insert) + "娜米豆~\n\n[CQ:face,id=74]等级：1\n[CQ:face,id=144]经验值：0\n[CQ:face,id=158]娜米豆：" + str(nami_insert) + "\n[CQ:face,id=159]宠物：无\n[CQ:face,id=169]道具：无\n[CQ:face,id=190]成就：无"
                print(url)
                requests.get(url)
                return 'OK'
            else:
                grade = r[0][1]
                exp = r[0][2]
                namicoin = r[0][3]
                pet = r[0][4]
                props = r[0][5]
                status = r[0][6]
                achievement = r[0][8]
                if status == 1:
                    # 确认插入
                    conn.commit()
                    # 关闭游标
                    cur.close()
                    # 关闭连接
                    conn.close()
                    url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                        str(gid) + "&message=[CQ:at,qq=" + str(uid) + \
                        "]\n[CQ:face,id=96]今天已经签过啦,明天再来吧~"
                    print(url)
                    requests.get(url)
                else:
                    nami_insert_2 = random.randint(3500, 5000)
                    if pet == '丽芙·蚀暗' or pet == '露西亚·鸦羽' or pet == '曲·雀翎' or pet == '露西亚·深红之渊' or pet == '露娜·银冕':
                        nami_insert_2 = nami_insert_2 * 3

                    if achievement == '娜娜米之友':
                        nami_insert_2 = nami_insert_2 + 10000

                    nami_insert_3 = int(nami_insert_2) + int(namicoin)

                    # 修改娜米豆的值
                    sql_text_3 = "UPDATE info SET 娜米豆 = " + \
                        str(nami_insert_3) + " WHERE QQ = " + str(uid)
                    print(sql_text_3)
                    cur.execute(sql_text_3)

                    # # 修改签到状态的值
                    sql_text_5 = "UPDATE info SET 签到状态 = 1 WHERE QQ = " + \
                        str(uid)
                    print(sql_text_5)
                    cur.execute(sql_text_5)

                    # 确认插入
                    conn.commit()
                    # 关闭游标
                    cur.close()
                    # 关闭连接
                    conn.close()
                    if achievement == '娜娜米之友':
                        url_add = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                            str(gid) + "&message=嘿!你是娜娜米的好朋友~我再送你10000豆哟！"
                        print(url_add)
                        requests.get(url_add)

                    if pet == '丽芙·蚀暗':
                        url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(uid) + "]\n\n[CQ:face,id=145]丽芙的祝福：三倍签到奖励[CQ:face,id=145]\n签到成功，获取到 " + str(
                            nami_insert_2) + " 娜米豆\n\n[CQ:face,id=74]等级：" + str(grade) + "\n[CQ:face,id=144]经验值：" + str(exp) + "\n[CQ:face,id=158]娜米豆：" + str(nami_insert_3) + "\n[CQ:face,id=159]宠物：" + str(pet) + "\n[CQ:face,id=169]道具：" + str(props) + "\n[CQ:face,id=190]成就：" + str(achievement)
                    elif pet == '露西亚·鸦羽':
                        url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(uid) + "]\n\n[CQ:face,id=145]鸦羽的祝福：三倍签到奖励[CQ:face,id=145]\n签到成功，获取到 " + str(
                            nami_insert_2) + " 娜米豆\n\n[CQ:face,id=74]等级：" + str(grade) + "\n[CQ:face,id=144]经验值：" + str(exp) + "\n[CQ:face,id=158]娜米豆：" + str(nami_insert_3) + "\n[CQ:face,id=159]宠物：" + str(pet) + "\n[CQ:face,id=169]道具：" + str(props) + "\n[CQ:face,id=190]成就：" + str(achievement)
                    elif pet == '曲·雀翎':
                        url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(uid) + "]\n\n[CQ:face,id=145]曲的祝福：三倍签到奖励[CQ:face,id=145]\n签到成功，获取到 " + str(
                            nami_insert_2) + " 娜米豆\n\n[CQ:face,id=74]等级：" + str(grade) + "\n[CQ:face,id=144]经验值：" + str(exp) + "\n[CQ:face,id=158]娜米豆：" + str(nami_insert_3) + "\n[CQ:face,id=159]宠物：" + str(pet) + "\n[CQ:face,id=169]道具：" + str(props) + "\n[CQ:face,id=190]成就：" + str(achievement)
                    elif pet == '露西亚·深红之渊':
                        url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(uid) + "]\n\n[CQ:face,id=145]白毛的祝福：三倍签到奖励[CQ:face,id=145]\n签到成功，获取到 " + str(
                            nami_insert_2) + " 娜米豆\n\n[CQ:face,id=74]等级：" + str(grade) + "\n[CQ:face,id=144]经验值：" + str(exp) + "\n[CQ:face,id=158]娜米豆：" + str(nami_insert_3) + "\n[CQ:face,id=159]宠物：" + str(pet) + "\n[CQ:face,id=169]道具：" + str(props) + "\n[CQ:face,id=190]成就：" + str(achievement)
                    elif pet == '露娜·银冕':
                        url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(uid) + "]\n\n[CQ:face,id=145]露娜的祝福：三倍签到奖励[CQ:face,id=145]\n签到成功，获取到 " + str(
                            nami_insert_2) + " 娜米豆\n\n[CQ:face,id=74]等级：" + str(grade) + "\n[CQ:face,id=144]经验值：" + str(exp) + "\n[CQ:face,id=158]娜米豆：" + str(nami_insert_3) + "\n[CQ:face,id=159]宠物：" + str(pet) + "\n[CQ:face,id=169]道具：" + str(props) + "\n[CQ:face,id=190]成就：" + str(achievement)
                    else:
                        url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(uid) + "]\n\n签到成功，获取到 " + str(nami_insert_2) + " 娜米豆\n\n[CQ:face,id=74]等级：" + str(
                            grade) + "\n[CQ:face,id=144]经验值：" + str(exp) + "\n[CQ:face,id=158]娜米豆：" + str(nami_insert_3) + "\n[CQ:face,id=159]宠物：" + str(pet) + "\n[CQ:face,id=169]道具：" + str(props) + "\n[CQ:face,id=190]成就：" + str(achievement)
                    print(url)
                    requests.get(url)
            return 'OK'
        except:
            return 'OK'

    # # 猜乌龟游戏
    # if raw_message == '猜乌龟':
    #     # 与 wugui.db 数据库连接
    #     conn = sqlite3.connect('wugui.db')
    #     cur = conn.cursor()

    #     # 查找单条数据
    #     sql_text_2 = "SELECT * FROM wugui WHERE 游戏编号 = 1"
    #     print(sql_text_2)
    #     cur.execute(sql_text_2)
    #     r = cur.fetchall()

    #     if len(r) == 0:
    #         # 新开一个乌龟游戏
    #         url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #             str(gid) + "&message=[CQ:face,id=43][CQ:face,id=43][CQ:face,id=43]\n\n[CQ:face,id=144]咻！娜娜米扔出了一只乌龟~\n[CQ:face,id=12]究竟会是什么乌龟呢？\n\n[CQ:face,id=140]格式：猜乌龟 中乌龟 1000"
    #         # url = escape_symbol(url)
    #         print(url)
    #         requests.get(url)
    #         sql_text_6 = "INSERT INTO wugui VALUES(1,'111111','111111',111111)"
    #         print(sql_text_6)
    #         cur.execute(sql_text_6)
    #         # 确认插入
    #         conn.commit()
    #         # 关闭游标
    #         cur.close()
    #         # 关闭连接
    #         conn.close()

    #         time.sleep(60)  # 60秒内用于接受数据

    #         # 随机结果
    #         game_wugui_result_int = random.randint(1, 100)
    #         if game_wugui_result_int > 0 and game_wugui_result_int <= 45:
    #             game_wugui_result = '小乌龟'
    #         elif game_wugui_result_int >= 46 and game_wugui_result_int < 56:
    #             game_wugui_result = '中乌龟'
    #         else:
    #             game_wugui_result = '大乌龟'

    #         # 宣布结果
    #         url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #             str(gid) + "&message=[CQ:face,id=0]娜娜米最终抛出的是~\n\n[CQ:face,id=137]" + str(
    #                 game_wugui_result) + "!!!"
    #         print(url)
    #         requests.get(url)
    #         time.sleep(0.5)

    #         # 与 wugui.db 数据库连接查询结果
    #         conn2 = sqlite3.connect('wugui.db')
    #         cur2 = conn2.cursor()

    #         # 查找单条数据
    #         sql_text_3 = "SELECT * FROM wugui WHERE 游戏编号 = 1"
    #         print(sql_text_3)
    #         cur2.execute(sql_text_3)
    #         r2 = cur2.fetchall()

    #         if len(r2) == 1:
    #             # 如果无人参加
    #             url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #                 str(gid) + "&message=[CQ:face,id=144]竟然没有人参加呢~"
    #             print(url)
    #             requests.get(url)
    #         else:
    #             # 如果有人参加
    #             for i in r2:
    #                 qq = i[1]
    #                 if qq == '111111':
    #                     continue
    #                 game_answer = i[2]
    #                 game_namidou = i[3]

    #                 # 与 person_info.db 数据库连接更新娜米豆
    #                 conn3 = sqlite3.connect('person_info.db')
    #                 cur3 = conn3.cursor()

    #                 # 获取原娜米豆
    #                 sql_text_8 = "SELECT * FROM info WHERE QQ='" + \
    #                     str(qq) + "'"
    #                 print(sql_text_8)
    #                 cur3.execute(sql_text_8)
    #                 r3 = cur3.fetchall()
    #                 root_namidou = r3[0][3]
    #                 root_namidou = int(root_namidou)
    #                 root_pet = r3[0][4]

    #                 # 中途可能变化的娜米豆
    #                 if root_namidou < game_namidou:
    #                     url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #                         str(gid) + "&message=[CQ:at,qq=" + str(qq) + \
    #                         "]\n\n[CQ:face,id=178]似乎豆豆发生了变化，已经不够了呢~"
    #                     print(url)
    #                     requests.get(url)
    #                     continue

    #                 if game_answer == game_wugui_result:
    #                     # 如果答案正确
    #                     # 更新娜米豆的值

    #                     # 检测是否是有红莲或者曲
    #                     if root_pet == '露西亚·红莲' or root_pet == '曲·雀翎':
    #                         random_r = random.randint(1, 10)
    #                         if random_r > 3 and random_r < 7:
    #                             game_namidou = int(game_namidou) * 2

    #                     if root_pet == '加百利·星陨':
    #                         random_r = random.randint(1, 10)
    #                         if random_r > 4 and random_r < 7:
    #                             game_namidou = int(game_namidou) * 2

    #                     # 检测是否是中乌龟
    #                     if game_wugui_result == '中乌龟':
    #                         game_namidou = int(game_namidou) * 5
    #                         new_namidou = root_namidou + int(game_namidou)
    #                     else:
    #                         new_namidou = root_namidou + int(game_namidou)
    #                     sql_text_7 = "UPDATE info SET 娜米豆 = " + \
    #                         str(new_namidou) + " WHERE QQ = " + str(qq)
    #                     print(sql_text_7)
    #                     cur3.execute(sql_text_7)
    #                     # 确认插入
    #                     conn3.commit()
    #                     # 关闭游标
    #                     cur3.close()
    #                     # 关闭连接
    #                     conn3.close()

    #                     if root_pet == '露西亚·红莲' or root_pet == '曲·雀翎':
    #                         if random_r > 3 and random_r < 7:
    #                             if root_pet == '露西亚·红莲':
    #                                 url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(
    #                                     qq) + "]\n[CQ:face,id=145]红莲将一直在您身边，指挥官\n[CQ:face,id=86]双倍获取 " + str(game_namidou) + " 娜米豆"
    #                                 print(url)
    #                                 requests.get(url)
    #                             else:
    #                                 url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(
    #                                     qq) + "]\n[CQ:face,id=145]呵~暂时将力量借给你而已\n[CQ:face,id=86]双倍获取 " + str(game_namidou) + " 娜米豆"
    #                                 print(url)
    #                                 requests.get(url)
    #                         else:
    #                             url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(
    #                                 qq) + "]\n[CQ:face,id=144]诶嘿！猜对啦~\n[CQ:face,id=86]成功赚取 " + str(game_namidou) + " 娜米豆"
    #                             print(url)
    #                             requests.get(url)
    #                     elif root_pet == '加百利·星陨':
    #                         if random_r > 4 and random_r < 7:
    #                             url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(
    #                                 qq) + "]\n[CQ:face,id=145]享受吧！无知的人类~\n[CQ:face,id=86]双倍获取 " + str(game_namidou) + " 娜米豆"
    #                             print(url)
    #                             requests.get(url)
    #                         else:
    #                             url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(
    #                                 qq) + "]\n[CQ:face,id=144]诶嘿！猜对啦~\n[CQ:face,id=86]成功赚取 " + str(game_namidou) + " 娜米豆"
    #                             print(url)
    #                             requests.get(url)
    #                     else:
    #                         url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(
    #                             qq) + "]\n[CQ:face,id=144]诶嘿！猜对啦~\n[CQ:face,id=86]成功赚取 " + str(game_namidou) + " 娜米豆"
    #                         print(url)
    #                         requests.get(url)
    #                 else:
    #                     # 如果答案错误
    #                     # 更新娜米豆的值

    #                     # 宠物发动效果
    #                     if root_pet == '里·异火' or root_pet == '露西亚·鸦羽':
    #                         random_r = random.randint(1, 10)
    #                         if random_r > 3 and random_r < 7:
    #                             # 如果随机成功
    #                             new_namidou = root_namidou + int(game_namidou)
    #                             sql_text_7 = "UPDATE info SET 娜米豆 = " + \
    #                                 str(new_namidou) + " WHERE QQ = " + str(qq)
    #                             print(sql_text_7)
    #                             cur3.execute(sql_text_7)
    #                             # 确认插入
    #                             conn3.commit()
    #                             # 关闭游标
    #                             cur3.close()
    #                             # 关闭连接
    #                             conn3.close()
    #                             if root_pet == '里·异火':
    #                                 url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(
    #                                     qq) + "]\n[CQ:face,id=54]火神，是你不变的信仰！[CQ:face,id=54]\n[CQ:face,id=29]扭转乾坤~赢取 " + str(game_namidou) + " 娜米豆"
    #                                 print(url)
    #                                 requests.get(url)
    #                             else:
    #                                 url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(
    #                                     qq) + "]\n[CQ:face,id=54]鸦羽，是你不变的信仰！[CQ:face,id=54]\n[CQ:face,id=29]扭转乾坤~赢取 " + str(game_namidou) + " 娜米豆"
    #                                 print(url)
    #                                 requests.get(url)
    #                         else:
    #                             new_namidou = root_namidou - int(game_namidou)
    #                             sql_text_7 = "UPDATE info SET 娜米豆 = " + \
    #                                 str(new_namidou) + " WHERE QQ = " + str(qq)
    #                             print(sql_text_7)
    #                             cur3.execute(sql_text_7)
    #                             # 确认插入
    #                             conn3.commit()
    #                             # 关闭游标
    #                             cur3.close()
    #                             # 关闭连接
    #                             conn3.close()

    #                             url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(
    #                                 qq) + "]\n[CQ:face,id=19]可惜可惜~\n[CQ:face,id=18]失去了 " + str(game_namidou) + " 娜米豆"
    #                             print(url)
    #                             requests.get(url)
    #                     elif root_pet == '加百利·星陨':
    #                         random_r = random.randint(1, 10)
    #                         if random_r > 4 and random_r < 7:
    #                             # 如果随机成功
    #                             new_namidou = root_namidou + int(game_namidou)
    #                             sql_text_7 = "UPDATE info SET 娜米豆 = " + \
    #                                 str(new_namidou) + " WHERE QQ = " + str(qq)
    #                             print(sql_text_7)
    #                             cur3.execute(sql_text_7)
    #                             # 确认插入
    #                             conn3.commit()
    #                             # 关闭游标
    #                             cur3.close()
    #                             # 关闭连接
    #                             conn3.close()
    #                             url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(
    #                                 qq) + "]\n[CQ:face,id=54]就这？我加老爷一句话的事~[CQ:face,id=54]\n[CQ:face,id=29]扭转乾坤~赢取 " + str(game_namidou) + " 娜米豆"
    #                             print(url)
    #                             requests.get(url)
    #                         else:
    #                             new_namidou = root_namidou - int(game_namidou)
    #                             sql_text_7 = "UPDATE info SET 娜米豆 = " + \
    #                                 str(new_namidou) + " WHERE QQ = " + str(qq)
    #                             print(sql_text_7)
    #                             cur3.execute(sql_text_7)
    #                             # 确认插入
    #                             conn3.commit()
    #                             # 关闭游标
    #                             cur3.close()
    #                             # 关闭连接
    #                             conn3.close()

    #                             url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(
    #                                 qq) + "]\n[CQ:face,id=19]可惜可惜~\n[CQ:face,id=18]失去了 " + str(game_namidou) + " 娜米豆"
    #                             print(url)
    #                             requests.get(url)
    #                     else:
    #                         new_namidou = root_namidou - int(game_namidou)
    #                         sql_text_7 = "UPDATE info SET 娜米豆 = " + \
    #                             str(new_namidou) + " WHERE QQ = " + str(qq)
    #                         print(sql_text_7)
    #                         cur3.execute(sql_text_7)
    #                         # 确认插入
    #                         conn3.commit()
    #                         # 关闭游标
    #                         cur3.close()
    #                         # 关闭连接
    #                         conn3.close()

    #                         url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(
    #                             qq) + "]\n[CQ:face,id=19]可惜可惜~\n[CQ:face,id=18]失去了 " + str(game_namidou) + " 娜米豆"
    #                         print(url)
    #                         requests.get(url)

    #         # 删除wugui.db的数据
    #         sql_text_9 = "DELETE FROM wugui WHERE 游戏编号 = 1"
    #         print(sql_text_9)
    #         cur2.execute(sql_text_9)

    #         # 确认插入
    #         conn2.commit()
    #         # 关闭游标
    #         cur2.close()
    #         # 关闭连接
    #         conn2.close()

    #         return 'OK'
    #     else:
    #         # 确认插入
    #         conn.commit()
    #         # 关闭游标
    #         cur.close()
    #         # 关闭连接
    #         conn.close()
    #         url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #             str(gid) + "&message=[CQ:face,id=29]乌龟游戏进行中~快来猜猜看吧~"
    #         print(url)
    #         requests.get(url)
    #         return 'OK'

    # 收集乌龟答案
    if raw_message[0:4] == '猜乌龟 ':
        # 与 wugui.db 数据库连接 检查是否开始游戏
        conn4 = sqlite3.connect('wugui.db')
        cur4 = conn4.cursor()

        # 查找单条数据
        sql_text_1 = "SELECT * FROM wugui WHERE QQ='111111'"
        print(sql_text_1)
        cur4.execute(sql_text_1)

        r4 = cur4.fetchall()
        if len(r4) == 0:
            # 关闭游标
            cur4.close()
            # 关闭连接
            conn4.close()
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=[CQ:face,id=29]游戏还没开始呢~输入“猜乌龟”开始游戏吧！"
            print(url)
            requests.get(url)
            return 'OK'

        try:
            # 拆分语句
            new_message = raw_message[4:]
            location = re.search(' ', new_message).span()
            print(location)
            result = new_message[:location[0]]  # 结果
            print(result)
            nami_dou = new_message[location[1]:]  # 娜米豆
            print(nami_dou)

            if result != "大乌龟" and result != "小乌龟" and result != '中乌龟':
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=你在说啥呢~我娜娜米听不懂~"
                print(url)
                requests.get(url)
                return 'OK'

            try:
                nami_dou = int(nami_dou)
                if nami_dou <= 0:
                    url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                        str(gid) + "&message=你在说啥呢~我娜娜米听不懂~"
                    print(url)
                    requests.get(url)
                    return 'OK'

                # 与 person_info.db 数据库连接
                conn = sqlite3.connect('person_info.db')
                cur = conn.cursor()

                # 查找单条数据
                sql_text_2 = "SELECT * FROM info WHERE QQ='" + str(uid) + "'"
                print(sql_text_2)
                cur.execute(sql_text_2)

                r = cur.fetchall()

                # 如果没这个人
                if len(r) == 0:
                    url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                        str(gid) + "&message=查不到你的信息呢~快输入“签到”获得娜米豆吧！"
                    print(url)
                    requests.get(url)
                    return 'OK'

                # 检查豆豆是否充足
                nami_dou_have = r[0][3]
                print(nami_dou_have)

                if nami_dou_have < nami_dou:
                    url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                        str(gid) + "&message=[CQ:face,id=218]豆豆不够了呢~嘿嘿~"
                    print(url)
                    requests.get(url)
                    return 'OK'

                # 与 wugui.db 数据库连接
                conn2 = sqlite3.connect('wugui.db')
                cur2 = conn2.cursor()

                # 如果已经参加
                sql_text_0 = "SELECT * FROM wugui WHERE QQ= '" + str(uid) + "'"
                print(sql_text_0)
                cur2.execute(sql_text_0)
                r2 = cur2.fetchall()

                if len(r2) != 0:
                    url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                        str(gid) + "&message=[CQ:at,qq=" + str(uid) + \
                        "] [CQ:face,id=144]你已经参加过了~请等待下一轮哦！"
                    print(url)
                    requests.get(url)
                    return 'OK'

                sql_text_6 = "INSERT INTO wugui VALUES(1,'" + str(
                    uid) + "','" + str(result) + "'," + str(nami_dou) + ")"
                print(sql_text_6)
                cur2.execute(sql_text_6)

                # 确认插入
                conn2.commit()
                # 关闭游标
                cur2.close()
                # 关闭连接
                conn2.close()

                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=[CQ:at,qq=" + \
                    str(uid) + "]娜娜米已收到~祝你好运哟~"
                print(url)
                requests.get(url)
                return 'OK'

            except:
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=格式似乎不太对呢~"
                print(url)
                requests.get(url)
                return 'OK'
        except:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=[CQ:face,id=144]似乎格式不太对呢！"
            print(url)
            requests.get(url)
            return 'OK'

    if raw_message == '娜米榜':
        conn = sqlite3.connect('person_info.db')
        cur = conn.cursor()
        sql_text_1 = "SELECT * FROM info ORDER BY 娜米豆 DESC;"
        cur.execute(sql_text_1)
        # 确认插入
        conn.commit()

        # 获取查询结果
        r = cur.fetchall()

        # 排名
        first_qq = r[0][0]
        second_qq = r[1][0]
        third_qq = r[2][0]
        fourest_qq = r[3][0]
        fivest_qq = r[4][0]

        # 豆子
        first_namidou = r[0][3]
        second_namidou = r[1][3]
        third_namidou = r[2][3]
        fourest_namidou = r[3][3]
        fivest_namidou = r[4][3]

        # 获取nickname
        url1 = "http://127.0.0.1:5700/get_group_member_info?group_id=" + \
            str(gid) + "&user_id=" + str(first_qq)
        url2 = "http://127.0.0.1:5700/get_group_member_info?group_id=" + \
            str(gid) + "&user_id=" + str(second_qq)
        url3 = "http://127.0.0.1:5700/get_group_member_info?group_id=" + \
            str(gid) + "&user_id=" + str(third_qq)
        url4 = "http://127.0.0.1:5700/get_group_member_info?group_id=" + \
            str(gid) + "&user_id=" + str(fourest_qq)
        url5 = "http://127.0.0.1:5700/get_group_member_info?group_id=" + \
            str(gid) + "&user_id=" + str(fivest_qq)
        r_1 = requests.get(url1)
        r_2 = requests.get(url2)
        r_3 = requests.get(url3)
        r_4 = requests.get(url4)
        r_5 = requests.get(url5)
        first_name = r_1.json()['data']['card']
        second_name = r_2.json()['data']['card']
        third_name = r_3.json()['data']['card']
        fourest_name = r_4.json()['data']['card']
        fivest_name = r_5.json()['data']['card']

        if len(first_name) == 0:
            first_name = r_1.json()['data']['nickname']
        if len(second_name) == 0:
            second_name = r_2.json()['data']['nickname']
        if len(third_name) == 0:
            third_name = r_3.json()['data']['nickname']
        if len(fourest_name) == 0:
            fourest_name = r_4.json()['data']['nickname']
        if len(fivest_name) == 0:
            fivest_name = r_5.json()['data']['nickname']

        url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:face,id=137]娜米豆排行榜[CQ:face,id=137]\n\n[CQ:face,id=143]一：" + str(first_name) + " " + str(first_namidou) + "\n[CQ:face,id=143]二：" + str(second_name) + " " + str(
            second_namidou) + "\n[CQ:face,id=143]三：" + str(third_name) + " " + str(third_namidou) + "\n[CQ:face,id=143]四：" + str(fourest_name) + " " + str(fourest_namidou) + "\n[CQ:face,id=143]五：" + str(fivest_name) + " " + str(fivest_namidou)
        print(url)
        requests.get(url)

        # 关闭游标
        cur.close()
        # 关闭连接
        conn.close()

    # if raw_message == '娜米商店':
    #     url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #         str(gid) + "&message=[CQ:face,id=138]娜娜米良心商店[CQ:face,id=138]\n\n[CQ:face,id=159]丽芙·蚀暗：10w nmd\n[CQ:face,id=54]功能：签到获取双倍娜米豆\n\n[CQ:face,id=159]露西亚·红莲:10w nmd\n[CQ:face,id=54]功能：猜乌龟成功时，20%概率豆豆翻倍\n\n[CQ:face,id=159]里·异火：10w nmd\n[CQ:face,id=54]功能：猜乌龟失败时，20%概率逆转结果\n\n[CQ:face,id=169]鱼竿：2w nmd\n[CQ:face,id=54]功能：发送“钓鱼”即可使用，3小时后收获1500-2000娜米豆"
    #     print(url)
    #     requests.get(url)

    # 转豆功能
    if raw_message[0:3] == '转豆 ':
        try:
            # 拆分语句
            new_message = raw_message[3:]
            location = re.search(' ', new_message).span()
            print(location)
            to_qq = new_message[:location[0]]  # 转入QQ号
            print(to_qq)
            nami_dou = new_message[location[1]:]  # 娜米豆数量
            print(nami_dou)

            # 检测此用户是否在用户表中
            conn = sqlite3.connect('person_info.db')
            cur = conn.cursor()
            sql_text_1 = "SELECT * FROM info WHERE QQ = '" + str(to_qq) + "'"
            cur.execute(sql_text_1)

            # 获取查询结果
            r = cur.fetchall()

            # 如果没有这个QQ则失败
            if len(r) == 0:
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=娜娜米没有找到这个人呢~"
                print(url)
                requests.get(url)
                return 'OK'

            # 检测是否给自己转豆
            if str(to_qq) == str(uid):
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + \
                    "&message=[CQ:face,id=146]怎么还有给自己转豆的人~没事不要来烦娜娜米！"
                print(url)
                requests.get(url)
                return 'OK'

            # 娜米豆逻辑检测
            try:
                nami_dou = int(nami_dou)
                # 检测是否小于0
                if nami_dou <= 0:
                    url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                        str(gid) + "&message=似乎哪里不太对呢~"
                    print(url)
                    requests.get(url)
                    return 'OK'

                # 检测是否有足够娜米豆
                sql_text_2 = "SELECT * FROM info WHERE QQ = '" + str(uid) + "'"
                cur.execute(sql_text_2)

                # 获取查询结果
                r = cur.fetchall()

                # 拥有娜米豆为
                nami_dou_have = r[0][3]
                print(nami_dou_have)

                # 检测是否足够
                if int(nami_dou_have) < int(nami_dou):
                    url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                        str(gid) + "&message=[CQ:face,id=218]豆豆不够了呢~嘿嘿~"
                    print(url)
                    requests.get(url)
                    return 'OK'

                # 开始转豆

                # 获取被转QQ的豆数量
                sql_text_3 = "SELECT * FROM info WHERE QQ = '" + \
                    str(to_qq) + "'"
                cur.execute(sql_text_3)
                # 获取查询结果
                r = cur.fetchall()
                to_qq_have_namidou = r[0][3]

                new_namidou_from = int(nami_dou_have) - int(nami_dou)
                new_namidou_to = int(to_qq_have_namidou) + int(nami_dou)

                sql_text_4 = "UPDATE info SET 娜米豆 = " + \
                    str(new_namidou_from) + " WHERE QQ = " + str(uid)
                cur.execute(sql_text_4)

                sql_text_5 = "UPDATE info SET 娜米豆 = " + \
                    str(new_namidou_to) + " WHERE QQ = " + str(to_qq)
                cur.execute(sql_text_5)

                # 确认插入
                conn.commit()
                # 关闭游标
                cur.close()
                # 关闭连接
                conn.close()

                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:face,id=144]转豆成功~\n你还剩余 " + str(
                    new_namidou_from) + " 娜米豆~\n[CQ:at,qq=" + str(to_qq) + "]\n获得 " + str(nami_dou) + " 娜米豆"
                print(url)
                requests.get(url)
                return 'OK'

            except:
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=你在说啥呢~我娜娜米听不懂~"
                print(url)
                requests.get(url)
                # 关闭游标
                cur.close()
                # 关闭连接
                conn.close()
                return 'OK'
        except:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=你在说什么呢，我娜娜米听不懂~\格式：转豆-QQ号-娜米豆数量"
            print(url)
            requests.get(url)

    # 购买宠物功能
    if raw_message[0:4] == '买宠物 ':
        try:
            # 拆分语句
            new_message = raw_message[4:]  # 宠物名称
            print(new_message)
            if new_message != '露西亚·红莲' and new_message != '丽芙·蚀暗' and new_message != '里·异火':
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=似乎没有这个宠物呢~"
                print(url)
                requests.get(url)
                return 'OK'

            # 检查是否有豆
            conn = sqlite3.connect('person_info.db')
            cur = conn.cursor()
            sql_text_1 = "SELECT * FROM info WHERE QQ='" + str(uid) + "'"
            cur.execute(sql_text_1)

            r = cur.fetchall()
            have_namidou = r[0][3]
            have_chongwu = r[0][4]

            if int(have_namidou) < 100000:
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=豆豆似乎不够呢~"
                print(url)
                requests.get(url)
                return 'OK'

            new_namidou = int(have_namidou) - 100000
            print(new_namidou)

            sql_text_2 = "UPDATE info SET 娜米豆 = " + \
                str(new_namidou) + " WHERE QQ = '" + str(uid) + "'"
            cur.execute(sql_text_2)

            # 如果已经有宠物了，则放进宠物背包
            if have_chongwu != '无':
                conn2 = sqlite3.connect('have_things.db')
                cur2 = conn2.cursor()
                sql_text_4 = "INSERT INTO have_pets VALUES('" + str(
                    uid) + "', '" + str(new_message) + "')"
                cur2.execute(sql_text_4)
                # 确认插入
                conn2.commit()
                # 关闭游标
                cur2.close()
                # 关闭连接
                conn2.close()

                # 确认插入
                conn.commit()
                # 关闭游标
                cur.close()
                # 关闭连接
                conn.close()
            else:
                sql_text_3 = "UPDATE info SET 宠物 = '" + \
                    str(new_message) + "' WHERE QQ = '" + str(uid) + "'"
                cur.execute(sql_text_3)

                # 确认插入
                conn.commit()
                # 关闭游标
                cur.close()
                # 关闭连接
                conn.close()

            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=[CQ:at,qq=" + \
                str(uid) + "]购买宠物成功~消费100000娜米豆~"
            print(url)
            requests.get(url)
            return 'OK'

        except:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=你在说什么呢，我娜娜米听不懂~"
            print(url)
            requests.get(url)

    # 卖宠物功能
    if raw_message[0:4] == '卖宠物 ':
        try:
            # 拆分语句
            new_message = raw_message[4:]  # 宠物名称
            print(new_message)
            if new_message != '露西亚·红莲' and new_message != '丽芙·蚀暗' and new_message != '里·异火':
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=似乎没有这个宠物呢~"
                print(url)
                requests.get(url)
                return 'OK'

            # 检查宠物名称
            conn = sqlite3.connect('person_info.db')
            cur = conn.cursor()
            sql_text_1 = "SELECT * FROM info WHERE QQ='" + str(uid) + "'"
            cur.execute(sql_text_1)

            r = cur.fetchall()
            have_namidou = r[0][3]
            have_chongwu = r[0][4]
            if have_chongwu == '无':
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=想啥呢？你还没有宠物呢~"
                print(url)
                requests.get(url)
                return 'OK'
            else:
                if have_chongwu == new_message:
                    # 拥有此宠物，可以出售
                    new_namidou = int(have_namidou) + 60000
                    print(new_namidou)

                    sql_text_2 = "UPDATE info SET 娜米豆 = " + \
                        str(new_namidou) + " WHERE QQ = '" + str(uid) + "'"
                    cur.execute(sql_text_2)

                    sql_text_3 = "UPDATE info SET 宠物 = '无' WHERE QQ = '" + \
                        str(uid) + "'"
                    cur.execute(sql_text_3)

                    # 确认插入
                    conn.commit()
                    # 关闭游标
                    cur.close()
                    # 关闭连接
                    conn.close()
                    url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                        str(gid) + "&message=宠物出售成功~获得60000娜米豆"
                    print(url)
                    requests.get(url)
                else:
                    url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                        str(gid) + "&message=似乎没有这个宠物呢~"
                    print(url)
                    requests.get(url)
        except:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=你在说什么呢，我娜娜米听不懂~"
            print(url)
            requests.get(url)

    # 购买道具功能
    if raw_message[0:4] == '买道具 ':
        try:
            # 拆分语句
            new_message = raw_message[4:]  # 道具名称
            print(new_message)
            if new_message != '鱼竿':
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=似乎没有这个道具呢~"
                print(url)
                requests.get(url)
                return 'OK'

            # 检查是否有豆
            conn = sqlite3.connect('person_info.db')
            cur = conn.cursor()
            sql_text_1 = "SELECT * FROM info WHERE QQ='" + str(uid) + "'"
            cur.execute(sql_text_1)

            r = cur.fetchall()
            have_namidou = r[0][3]
            have_chongwu = r[0][4]
            have_daoju = r[0][5]

            if int(have_namidou) < 20000:
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=豆豆似乎不够呢~"
                print(url)
                requests.get(url)
                return 'OK'

            if have_daoju != '无':
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=[CQ:at,qq=" + \
                    str(uid) + "]你已经有一个道具了呢~"
                print(url)
                requests.get(url)
                return 'OK'

            new_namidou = int(have_namidou) - 20000
            print(new_namidou)

            sql_text_2 = "UPDATE info SET 娜米豆 = " + \
                str(new_namidou) + " WHERE QQ = '" + str(uid) + "'"
            cur.execute(sql_text_2)

            sql_text_3 = "UPDATE info SET 道具 = '" + \
                str(new_message) + "' WHERE QQ = '" + str(uid) + "'"
            cur.execute(sql_text_3)

            # 确认插入
            conn.commit()
            # 关闭游标
            cur.close()
            # 关闭连接
            conn.close()

            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=[CQ:at,qq=" + \
                str(uid) + "]\n\n[CQ:face,id=144]购买道具成功~消费20000娜米豆~"
            print(url)
            requests.get(url)
            return 'OK'

        except:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=你在说什么呢，我娜娜米听不懂~\n格式：买道具-道具名称"
            print(url)
            requests.get(url)

    # 卖道具功能
    if raw_message[0:4] == '卖道具 ':
        try:
            # 拆分语句
            new_message = raw_message[4:]  # 道具名称
            print(new_message)
            if new_message != '鱼竿':
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=似乎没有这个道具呢~"
                print(url)
                requests.get(url)
                return 'OK'

            # 检查道具名称
            conn = sqlite3.connect('person_info.db')
            cur = conn.cursor()
            sql_text_1 = "SELECT * FROM info WHERE QQ='" + str(uid) + "'"
            cur.execute(sql_text_1)

            r = cur.fetchall()
            have_namidou = r[0][3]
            have_chongwu = r[0][4]
            have_daoju = r[0][5]
            if have_daoju == '无':
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=想啥呢？你还没有道具呢~"
                print(url)
                requests.get(url)
                return 'OK'
            else:
                if have_daoju == new_message:
                    # 拥有此道具，可以出售
                    new_namidou = int(have_namidou) + 10000
                    print(new_namidou)

                    sql_text_2 = "UPDATE info SET 娜米豆 = " + \
                        str(new_namidou) + " WHERE QQ = '" + str(uid) + "'"
                    cur.execute(sql_text_2)

                    sql_text_3 = "UPDATE info SET 道具 = '无' WHERE QQ = '" + \
                        str(uid) + "'"
                    cur.execute(sql_text_3)

                    # 确认插入
                    conn.commit()
                    # 关闭游标
                    cur.close()
                    # 关闭连接
                    conn.close()
                    url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                        str(gid) + "&message=[CQ:face,id=144]道具出售成功~获得10000娜米豆"
                    print(url)
                    requests.get(url)
                else:
                    url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                        str(gid) + "&message=似乎没有这个道具呢~"
                    print(url)
                    requests.get(url)
        except:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=你在说什么呢，我娜娜米听不懂~\n格式：卖道具-道具名称"
            print(url)
            requests.get(url)

    if raw_message == '宠物':
        url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
            str(gid) + "&message=宠物已扩展为“宠物商店”和“稀有宠物”~"
        print(url)
        requests.get(url)
        return 'OK'
    # 发送“宠物商店”
    if raw_message == '宠物商店':
        url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
            str(gid) + "&message=[CQ:face,id=138]娜娜米良心商店[CQ:face,id=138]\n\n[CQ:face,id=159]丽芙·蚀暗：10w nmd\n[CQ:face,id=54]功能：签到获取三倍娜米豆\n\n[CQ:face,id=159]露西亚·红莲:10w nmd\n[CQ:face,id=54]功能：猜乌龟成功时，30%概率豆豆翻倍\n\n[CQ:face,id=159]里·异火：10w nmd\n[CQ:face,id=54]功能：猜乌龟失败时，30%概率逆转结果"
        print(url)
        requests.get(url)
        return 'OK'
    # \n\n[CQ:face,id=159]露西亚·鸦羽：通过【气息】召唤\n[CQ:face,id=54]功能1：猜乌龟失败时，30%概率逆转结果\n[CQ:face,id=54]功能2：签到获取三倍娜米豆

    if raw_message == '稀有宠物':
        url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
            str(gid) + "&message=[CQ:face,id=138]稀有宠物图鉴[CQ:face,id=138]\n\n[CQ:face,id=159]曲·雀翎：通过【气息】召唤\n[CQ:face,id=54]功能1：猜乌龟成功时，30%概率豆豆翻倍\n[CQ:face,id=54]功能2：签道获取三倍娜米豆\n\n[CQ:face,id=159]露西亚·鸦羽：通过【气息】召唤\n[CQ:face,id=54]功能1：猜乌龟失败时，30%概率逆转结果\n[CQ:face,id=54]功能2：签到获取三倍娜米豆\n\n[CQ:face,id=159]露西亚·深红之渊：通过【气息】召唤\n[CQ:face,id=54]功能1：探索出货概率增至20%\n[CQ:face,id=54]功能2：签道获取三倍娜米豆\n\n[CQ:face,id=159]露娜·银冕：通过【气息】召唤\n[CQ:face,id=54]功能1：扭蛋出货不会为空\n[CQ:face,id=54]功能2：签道获取三倍娜米豆\n\n[CQ:face,id=159]加百利·星陨：通过【气息】召唤\n[CQ:face,id=54]功能1：猜乌龟失败时，20%概率逆转结果\n[CQ:face,id=54]功能2：猜乌龟成功时，20%概率豆豆翻倍"
        print(url)
        requests.get(url)
        return 'OK'

    # 发送“道具”
    if raw_message == '道具':
        url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
            str(gid) + "&message=[CQ:face,id=138]娜娜米道具图鉴[CQ:face,id=138]\n\n[CQ:face,id=169]鱼竿：2w nmd\n[CQ:face,id=54]功能：发送“钓鱼”即可使用，3小时后收获1500-2000娜米豆"
        print(url)
        requests.get(url)

    # 新增图鉴功能
    if raw_message == '图鉴':
        url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
            str(gid) + "&message=[CQ:face,id=138][CQ:face,id=138][CQ:face,id=138]世界图鉴一览表[CQ:face,id=138][CQ:face,id=138][CQ:face,id=138]\n\n[CQ:face,id=161][CQ:face,id=161] 世界宠物大全 [CQ:face,id=161][CQ:face,id=161]\n\n[CQ:face,id=159] 丽芙·蚀暗\n[CQ:face,id=159] 露西亚·红莲\n[CQ:face,id=159] 里·异火\n[CQ:face,id=159] 露西亚·鸦羽\n[CQ:face,id=159] 曲·雀翎\n[CQ:face,id=159] 露西亚·深红之渊\n[CQ:face,id=159] 露娜·银冕\n[CQ:face,id=159] 加百利·星陨\n\n[CQ:face,id=161][CQ:face,id=161] 世界道具大全 [CQ:face,id=161][CQ:face,id=161]\n\n[CQ:face,id=169] 鱼竿\n\n[CQ:face,id=161][CQ:face,id=161] 娜娜米随身系列 [CQ:face,id=161][CQ:face,id=161]\n\n[CQ:face,id=190] 娜娜米的鞋\n[CQ:face,id=190] 娜娜米的发卡\n[CQ:face,id=190] 娜娜米的胖次\n[CQ:face,id=190] 娜娜米的项链\n[CQ:face,id=190] 娜娜米的袜子\n[CQ:face,id=190] 娜娜米的裙子\n[CQ:face,id=190] 娜娜米的鞋带\n[CQ:face,id=190] 娜娜米遛过的狗\n[CQ:face,id=190] 娜娜米用过的勺子\n[CQ:face,id=190] 娜娜米吃过的棒棒糖\n\n[CQ:face,id=161][CQ:face,id=161] 合成物品成就大全 [CQ:face,id=161][CQ:face,id=161]\n\n[CQ:face,id=113] 娜娜米之友\n[CQ:face,id=113] 终极铁片人\n[CQ:face,id=113] 最没用的废物\n[CQ:face,id=113] 乌龟之友\n[CQ:face,id=113] 幸福的小熊\n[CQ:face,id=113] 这条街最靓的仔\n[CQ:face,id=113] 大富翁"
        print(url)
        requests.get(url)

    # 钓鱼功能
    if raw_message == '钓鱼':
        # 检查是否有鱼竿
        conn = sqlite3.connect('person_info.db')
        cur = conn.cursor()
        sql_text_1 = "SELECT * FROM info WHERE QQ='" + str(uid) + "'"
        cur.execute(sql_text_1)

        r = cur.fetchall()
        have_namidou = r[0][3]
        have_chongwu = r[0][4]
        have_daoju = r[0][5]
        # 钓鱼状态
        diaoyu_status = r[0][7]

        # 关闭游标
        cur.close()
        # 关闭连接
        conn.close()

        if have_daoju == '鱼竿':
            # 检测是否正在钓鱼
            if int(diaoyu_status) == 1:
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=[CQ:at,qq=" + \
                    str(uid) + "]\n[CQ:face,id=204]在钓了~在钓了~急什么急~"
                print(url)
                requests.get(url)
                return 'OK'

            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=[CQ:at,qq=" + \
                str(uid) + \
                "]\n[CQ:face,id=132]钓鱼去咯~\n[CQ:face,id=190]三小时后再回来看看吧~"
            print(url)
            r = requests.get(url)
            r.close()

            # 将钓鱼状态设为1
            conn3 = sqlite3.connect('person_info.db')
            cur3 = conn3.cursor()
            sql_text_4 = "UPDATE info SET 钓鱼状态 = 1 WHERE QQ = '" + \
                str(uid) + "'"
            cur3.execute(sql_text_4)

            # 确认插入
            conn3.commit()
            # 关闭游标
            cur3.close()
            # 关闭连接
            conn3.close()

            # 开始钓鱼 3小时
            time.sleep(3600)  # 1小时
            print("一小时过去了")
            time.sleep(3600)  # 1小时
            print("两小时过去了")
            time.sleep(3600)  # 1小时

            # 检查是否还有鱼竿
            conn2 = sqlite3.connect('person_info.db')
            cur2 = conn2.cursor()
            sql_text_2 = "SELECT * FROM info WHERE QQ='" + str(uid) + "'"
            cur2.execute(sql_text_2)
            r2 = cur2.fetchall()

            have_namidou_still = r2[0][3]
            have_chongwu_still = r2[0][4]
            have_daoju_still = r2[0][5]
            if have_daoju_still == '鱼竿':
                # 下发娜米豆
                insert_namidou = random.randint(1500, 2000)  # 新获取的娜米豆
                new_insert_namidou = int(
                    insert_namidou) + int(have_namidou_still)  # 最终娜米豆数量
                sql_text_3 = "UPDATE info SET 娜米豆 = " + \
                    str(new_insert_namidou) + " WHERE QQ = '" + str(uid) + "'"
                cur2.execute(sql_text_3)

                # 钓鱼状态归 0
                sql_text_5 = "UPDATE info SET 钓鱼状态 = 0 WHERE QQ = '" + \
                    str(uid) + "'"
                cur2.execute(sql_text_5)

                # 确认插入
                conn2.commit()
                # 关闭游标
                cur2.close()
                # 关闭连接
                conn2.close()

                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=[CQ:at,qq=" + \
                    str(uid) + "]\n[CQ:face,id=131]辛苦劳作~收获满满~\n[CQ:face,id=144]钓鱼获取到" + \
                    str(insert_namidou) + "娜米豆~"
                print(url)
                requests.get(url)
                return 'OK'
            else:
                # 钓鱼状态归 0
                sql_text_5 = "UPDATE info SET 钓鱼状态 = 0 WHERE QQ = '" + \
                    str(uid) + "'"
                cur2.execute(sql_text_5)
                # 确认插入
                conn2.commit()
                # 关闭游标
                cur2.close()
                # 关闭连接
                conn2.close()

                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=[CQ:at,qq=" + \
                    str(uid) + "]\n[CQ:face,id=146]鱼竿似乎弄丢了，看来是白钓了呢~"
                print(url)
                requests.get(url)
                return 'OK'
        else:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=[CQ:at,qq=" + \
                str(uid) + "]\n[CQ:face,id=96]似乎还没有鱼竿呢，快去买一个吧~"
            print(url)
            requests.get(url)
            return 'OK'

    # 背包功能转换为宠物背包和物品背包
    if raw_message == '背包':
        url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
            str(gid) + "&message=背包功能已扩展，尝试输入“宠物背包”或“物品背包”吧~"
        print(url)
        requests.get(url)
        return 'OK'

    # 宠物背包功能 have_pets 表
    if raw_message == '宠物背包':
        conn = sqlite3.connect('have_things.db')
        cur = conn.cursor()
        sql_text_1 = "SELECT * FROM have_pets WHERE QQ = '" + str(uid) + "'"
        # 执行sql语句
        cur.execute(sql_text_1)
        # 确认插入
        conn.commit()
        # 获取查询结果
        r = cur.fetchall()
        # 关闭游标
        cur.close()
        # 关闭连接
        conn.close()

        # 空背包
        if len(r) == 0:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=[CQ:at,qq=" + \
                str(uid) + "]\n[CQ:face,id=180]似乎一只宠物也没得呢~"
            print(url)
            requests.get(url)
            return 'OK'

        url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
            str(gid) + "&message=[CQ:at,qq=" + \
            str(uid) + "]\n[CQ:face,id=69]背包宠物：\n"
        for i in r:
            url = url + "\n[CQ:face,id=86]" + str(i[1])

        print(url)
        requests.get(url)
        return 'OK'

    # 物品背包功能
    if raw_message == '物品背包':
        conn = sqlite3.connect('have_things.db')
        cur = conn.cursor()
        sql_text_1 = "SELECT * FROM have_things WHERE QQ = '" + str(uid) + "'"
        # 执行sql语句
        cur.execute(sql_text_1)
        # 确认插入
        conn.commit()
        # 获取查询结果
        r = cur.fetchall()
        # 关闭游标
        cur.close()
        # 关闭连接
        conn.close()

        # 空背包
        if len(r) == 0:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=[CQ:at,qq=" + \
                str(uid) + "]\n[CQ:face,id=180]你的背包空空如也~"
            print(url)
            requests.get(url)
            return 'OK'

        url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
            str(gid) + "&message=[CQ:at,qq=" + \
            str(uid) + "]\n[CQ:face,id=69]背包物品：\n"
        for i in r:
            url = url + "\n[CQ:face,id=86]" + str(i[1])

        print(url)
        requests.get(url)
        return 'OK'

    # 扭蛋功能
    if raw_message == '扭蛋':
        # 检查是否有豆
        conn = sqlite3.connect('person_info.db')
        cur = conn.cursor()
        sql_text_1 = "SELECT * FROM info WHERE QQ='" + str(uid) + "'"
        cur.execute(sql_text_1)

        r = cur.fetchall()
        have_namidou = r[0][3]
        have_chongwu = r[0][4]
        have_daoju = r[0][5]

        if int(have_namidou) < 10000:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=需要10000豆哦，豆豆似乎不够呢~"
            print(url)
            requests.get(url)
            return 'OK'

        # 有豆则扣除10000豆
        new_namidou = int(have_namidou) - 10000
        sql_text_2 = "UPDATE info SET 娜米豆 = " + \
            str(new_namidou) + " WHERE QQ = '" + str(uid) + "'"
        cur.execute(sql_text_2)
        conn.commit()
        # 关闭游标
        cur.close()
        # 关闭连接
        conn.close()

        url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
            str(gid) + \
            "&message=[CQ:face,id=172]消费10000娜米豆~\n[CQ:face,id=190]咕噜咕噜~~扭蛋扭蛋~~\n[CQ:face,id=202]究竟会出现什么呢？"
        print(url)
        requests.get(url)

        conn2 = sqlite3.connect('have_things.db')
        cur2 = conn2.cursor()
        if have_chongwu == '露娜·银冕':
            r_int = random.randint(1, 30)
        else:
            r_int = random.randint(1, 50)

        time.sleep(5)

        if r_int > 30:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=[CQ:at,qq=" + \
                str(uid) + "]\n[CQ:face,id=203]恭喜你获得:\n[CQ:face,id=144]啥都没获得！！"
            print(url)
            requests.get(url)
            return 'OK'

        sql_text_3 = "SELECT * FROM things WHERE 序号 = '" + str(r_int) + "'"
        # 执行sql语句
        cur2.execute(sql_text_3)

        # 获取查询结果
        r = cur2.fetchall()

        # 获取到的物品
        r_get_thing = r[0][1]

        # 将物品加入背包
        sql_text_4 = "INSERT INTO have_things VALUES('" + str(
            uid) + "', '" + str(r_get_thing) + "')"
        cur2.execute(sql_text_4)

        # 确认插入
        conn2.commit()
        # 关闭游标
        cur2.close()
        # 关闭连接
        conn2.close()

        if have_chongwu == '露娜·银冕':
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=[CQ:at,qq=" + \
                str(uid) + \
                "]\n[CQ:face,id=203]【露娜守护】恭喜你获得:\n[CQ:face,id=144]" + \
                str(r_get_thing)
            print(url)
            requests.get(url)
            return 'OK'
        else:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=[CQ:at,qq=" + \
                str(uid) + \
                "]\n[CQ:face,id=203]恭喜你获得:\n[CQ:face,id=144]" + \
                str(r_get_thing)
            print(url)
            requests.get(url)
            return 'OK'

    # 出售功能
    if raw_message[0:3] == '出售 ':
        try:
            # 拆分语句
            new_message = raw_message[3:]
            location = re.search(' ', new_message).span()
            print(location)
            things_name = new_message[:location[0]]  # 物品信息
            print(things_name)
            things_number = new_message[location[1]:]  # 物品数量
            things_number = int(things_number)
            print(things_number)

            if things_number == 0:
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=请不要做一些无聊的事情哦~"
                print(url)
                requests.get(url)
                return 'OK'

            # 检查物品名称和价值
            conn = sqlite3.connect('have_things.db')
            cur = conn.cursor()
            sql_text_1 = "SELECT * FROM things WHERE 物品='" + \
                str(things_name) + "'"
            cur.execute(sql_text_1)

            r = cur.fetchall()

            if len(r) == 0:
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=似乎没有这个物品呢~"
                print(url)
                requests.get(url)
                return 'OK'

            things_value = int(r[0][2])

            # 检查是否有足够的物品
            sql_text_2 = "SELECT * FROM have_things WHERE 物品 ='" + \
                str(things_name) + "' AND QQ = '" + str(uid) + "'"
            cur.execute(sql_text_2)
            r2 = cur.fetchall()

            if len(r2) < things_number:
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=似乎没有足够的数量呢~"
                print(url)
                requests.get(url)
                return 'OK'

            # 清除相应的物品且获取娜米豆
            if len(r2) == things_number:
                # 全部删除
                sql_text_3 = "DELETE FROM have_things WHERE 物品 ='" + \
                    str(things_name) + "' AND QQ = '" + str(uid) + "'"
                cur.execute(sql_text_3)
                get_namidou = things_number * things_value
            else:
                save_number = len(r2) - things_number
                # 删除所有
                sql_text_4 = "DELETE FROM have_things WHERE 物品 ='" + \
                    str(things_name) + "' AND QQ = '" + str(uid) + "'"
                cur.execute(sql_text_4)
                # 插入保留的
                sql_text_5 = "INSERT INTO have_things VALUES('" + str(
                    uid) + "', '" + str(things_name) + "')"
                print(save_number)
                for i in range(save_number):
                    cur.execute(sql_text_5)
                get_namidou = things_number * things_value

            # 确认插入
            conn.commit()
            # 关闭游标
            cur.close()
            # 关闭连接
            conn.close()

            # 连接个人信息数据库加入娜米豆
            conn2 = sqlite3.connect('person_info.db')
            cur2 = conn2.cursor()
            sql_text_6 = "SELECT * FROM info WHERE QQ='" + str(uid) + "'"
            cur2.execute(sql_text_6)
            r3 = cur2.fetchall()
            have_namidou = int(r3[0][3])
            have_chongwu = r3[0][4]
            have_daoju = r3[0][5]

            # 加入新的娜米豆
            new_namidou = have_namidou + get_namidou
            sql_text_7 = "UPDATE info SET 娜米豆 = " + \
                str(new_namidou) + " WHERE QQ = '" + str(uid) + "'"
            cur2.execute(sql_text_7)

            # 确认插入
            conn2.commit()
            # 关闭游标
            cur2.close()
            # 关闭连接
            conn2.close()

            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=[CQ:at,qq=" + \
                str(uid) + "]\n[CQ:face,id=130]出售物品成功:\n[CQ:face,id=144]共获得 " + \
                str(get_namidou) + " 娜米豆~"
            print(url)
            requests.get(url)
            return 'OK'
        except:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=格式似乎不太对呢~"
            print(url)
            requests.get(url)
            return 'OK'

    # 转让功能
    if raw_message[0:3] == '转让 ':
        try:
            # 拆分语句
            new_message = raw_message[3:]
            location = re.search(' ', new_message).span()
            print(location)
            to_qq = new_message[:location[0]]  # 转让qq
            print(to_qq)
            things_name = new_message[location[1]:]  # 物品名称
            print(things_name)

            # 检测此用户是否在用户表中
            conn = sqlite3.connect('person_info.db')
            cur = conn.cursor()
            sql_text_1 = "SELECT * FROM info WHERE QQ = '" + str(to_qq) + "'"
            cur.execute(sql_text_1)

            # 获取查询结果
            r = cur.fetchall()

            # 如果没有这个QQ则失败
            if len(r) == 0:
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=娜娜米没有找到这个人呢~"
                print(url)
                requests.get(url)
                return 'OK'

            # 检测是否给自己转物品
            if str(to_qq) == str(uid):
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + \
                    "&message=[CQ:face,id=146]怎么还有给自己转物品的人~没事不要来烦娜娜米！"
                print(url)
                requests.get(url)
                return 'OK'

            # 确认插入
            conn.commit()
            # 关闭游标
            cur.close()
            # 关闭连接
            conn.close()

            # 检查物品名称和价值
            conn = sqlite3.connect('have_things.db')
            cur = conn.cursor()
            sql_text_2 = "SELECT * FROM things WHERE 物品='" + \
                str(things_name) + "'"
            cur.execute(sql_text_2)

            r = cur.fetchall()

            if len(r) == 0:
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=似乎没有这个物品呢~"
                print(url)
                requests.get(url)
                return 'OK'

            # things_value = int(r[0][2])

            # 检查是否有足够的物品
            sql_text_3 = "SELECT * FROM have_things WHERE 物品 ='" + \
                str(things_name) + "' AND QQ = '" + str(uid) + "'"
            cur.execute(sql_text_3)
            r2 = cur.fetchall()

            if len(r2) == 0:
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=似乎没有足够的物品呢~"
                print(url)
                requests.get(url)
                return 'OK'

            save_number = len(r2) - 1
            # 删除所有
            sql_text_4 = "DELETE FROM have_things WHERE 物品 ='" + \
                str(things_name) + "' AND QQ = '" + str(uid) + "'"
            cur.execute(sql_text_4)
            # 插入保留的
            sql_text_5 = "INSERT INTO have_things VALUES('" + str(
                uid) + "', '" + str(things_name) + "')"
            print(save_number)
            for i in range(save_number):
                cur.execute(sql_text_5)
            # 转入QQ物品
            sql_text_6 = "INSERT INTO have_things VALUES('" + str(
                to_qq) + "', '" + str(things_name) + "')"
            cur.execute(sql_text_6)

            # 确认插入
            conn.commit()
            # 关闭游标
            cur.close()
            # 关闭连接
            conn.close()

            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=[CQ:face,id=86]转让成功~\n[CQ:at,qq=" + \
                str(to_qq) + "]\n[CQ:face,id=144]恭喜获得：" + str(things_name)
            print(url)
            requests.get(url)
            return 'OK'
        except:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=格式似乎不太对呢~"
            print(url)
            requests.get(url)
            return 'OK'

    # 查询别人功能
    if raw_message[0:3] == '查询 ':
        try:
            # 拆分语句
            find_qq = raw_message[3:]  # 对方QQ
            print(find_qq)

            # 检测此用户是否在用户表中
            conn = sqlite3.connect('person_info.db')
            cur = conn.cursor()
            sql_text_1 = "SELECT * FROM info WHERE QQ = '" + str(find_qq) + "'"
            cur.execute(sql_text_1)

            # 获取查询结果
            r = cur.fetchall()

            # 如果没有这个QQ则失败
            if len(r) == 0:
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=娜娜米没有找到这个人呢~"
                print(url)
                requests.get(url)
                return 'OK'

            grade = r[0][1]
            exp = r[0][2]
            namicoin = r[0][3]
            pet = r[0][4]
            props = r[0][5]
            achievement = r[0][8]

            # 确认插入
            conn.commit()
            # 关闭游标
            cur.close()
            # 关闭连接
            conn.close()

            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:at,qq=" + str(find_qq) + "]\n[CQ:face,id=74]等级：" + str(
                grade) + "\n[CQ:face,id=144]经验值：" + str(exp) + "\n[CQ:face,id=158]娜米豆：" + str(namicoin) + "\n[CQ:face,id=159]宠物：" + str(pet) + "\n[CQ:face,id=169]道具：" + str(props) + "\n[CQ:face,id=190]成就：" + str(achievement)
            print(url)
            requests.get(url)
            return 'OK'
        except:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=格式似乎不太对呢~"
            print(url)
            requests.get(url)
            return 'OK'

    # 合成功能
    if raw_message[0:3] == '合成 ':
        try:
            # 拆分语句
            new_message = raw_message[3:]  # 物品名称
            print(new_message)
            if new_message != '娜娜米之友' and new_message != '乌龟之友' and new_message != '最没用的废物' and new_message != '终极铁片人' and new_message != '幸福的小熊' and new_message != '这条街最靓的仔' and new_message != '大富翁':
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=似乎没有这个成就呢~"
                print(url)
                requests.get(url)
                return 'OK'

            # 连接 have_things 数据库
            conn = sqlite3.connect('have_things.db')
            cur = conn.cursor()
            # 处理
            if new_message == '娜娜米之友':
                sql_text_1 = "SELECT * FROM have_things WHERE QQ ='" + \
                    str(uid) + "' AND 物品 = '娜娜米的鞋'"
                cur.execute(sql_text_1)
                # 获取查询结果
                r = cur.fetchall()
                xiezi_len = len(r)

                sql_text_1 = "SELECT * FROM have_things WHERE QQ ='" + \
                    str(uid) + "' AND 物品 = '娜娜米的发卡'"
                cur.execute(sql_text_1)
                # 获取查询结果
                r = cur.fetchall()
                faqia_len = len(r)

                sql_text_1 = "SELECT * FROM have_things WHERE QQ ='" + \
                    str(uid) + "' AND 物品 = '娜娜米的胖次'"
                cur.execute(sql_text_1)
                # 获取查询结果
                r = cur.fetchall()
                pangci_len = len(r)

                sql_text_1 = "SELECT * FROM have_things WHERE QQ ='" + \
                    str(uid) + "' AND 物品 = '娜娜米的项链'"
                cur.execute(sql_text_1)
                # 获取查询结果
                r = cur.fetchall()
                xianglian_len = len(r)

                sql_text_1 = "SELECT * FROM have_things WHERE QQ ='" + \
                    str(uid) + "' AND 物品 = '娜娜米的袜子'"
                cur.execute(sql_text_1)
                # 获取查询结果
                r = cur.fetchall()
                wazi_len = len(r)

                sql_text_1 = "SELECT * FROM have_things WHERE QQ ='" + \
                    str(uid) + "' AND 物品 = '娜娜米的裙子'"
                cur.execute(sql_text_1)
                # 获取查询结果
                r = cur.fetchall()
                qunzi_len = len(r)

                sql_text_1 = "SELECT * FROM have_things WHERE QQ ='" + \
                    str(uid) + "' AND 物品 = '娜娜米的鞋带'"
                cur.execute(sql_text_1)
                # 获取查询结果
                r = cur.fetchall()
                xiedai_len = len(r)

                sql_text_1 = "SELECT * FROM have_things WHERE QQ ='" + \
                    str(uid) + "' AND 物品 = '娜娜米遛过的狗'"
                cur.execute(sql_text_1)
                # 获取查询结果
                r = cur.fetchall()
                gou_len = len(r)

                sql_text_1 = "SELECT * FROM have_things WHERE QQ ='" + \
                    str(uid) + "' AND 物品 = '娜娜米用过的勺子'"
                cur.execute(sql_text_1)
                # 获取查询结果
                r = cur.fetchall()
                shaozi_len = len(r)

                sql_text_1 = "SELECT * FROM have_things WHERE QQ ='" + \
                    str(uid) + "' AND 物品 = '娜娜米吃过的棒棒糖'"
                cur.execute(sql_text_1)
                # 获取查询结果
                r = cur.fetchall()
                bangbangtang_len = len(r)
                if xiezi_len != 0 and faqia_len != 0 and pangci_len != 0 and xianglian_len != 0 and wazi_len != 0 and qunzi_len != 0 and xiedai_len != 0 and gou_len != 0 and shaozi_len != 0 and bangbangtang_len != 0:
                    # 可以合成

                    # 剩余物品数量
                    xiezi_len_save = xiezi_len - 1
                    faqia_len_save = faqia_len - 1
                    pangci_len_save = pangci_len - 1
                    xianglian_len_save = xianglian_len - 1
                    wazi_len_save = wazi_len - 1
                    qunzi_len_save = qunzi_len - 1
                    xiedai_len_save = xiedai_len - 1
                    gou_len_save = gou_len - 1
                    shaozi_len_save = shaozi_len - 1
                    bangbangtang_len_save = bangbangtang_len - 1

                    # 删除所有
                    sql_text_1 = "DELETE FROM have_things WHERE 物品 ='娜娜米的鞋' AND QQ = '" + \
                        str(uid) + "'"
                    cur.execute(sql_text_1)
                    # 插入保留的
                    sql_text_1 = "INSERT INTO have_things VALUES('" + str(
                        uid) + "', '娜娜米的鞋')"
                    for i in range(xiezi_len_save):
                        cur.execute(sql_text_1)

                    # 删除所有
                    sql_text_1 = "DELETE FROM have_things WHERE 物品 ='娜娜米的发卡' AND QQ = '" + \
                        str(uid) + "'"
                    cur.execute(sql_text_1)
                    # 插入保留的
                    sql_text_1 = "INSERT INTO have_things VALUES('" + str(
                        uid) + "', '娜娜米的发卡')"
                    for i in range(faqia_len_save):
                        cur.execute(sql_text_1)

                    # 删除所有
                    sql_text_1 = "DELETE FROM have_things WHERE 物品 ='娜娜米的胖次' AND QQ = '" + \
                        str(uid) + "'"
                    cur.execute(sql_text_1)
                    # 插入保留的
                    sql_text_1 = "INSERT INTO have_things VALUES('" + str(
                        uid) + "', '娜娜米的胖次')"
                    for i in range(pangci_len_save):
                        cur.execute(sql_text_1)

                    # 删除所有
                    sql_text_1 = "DELETE FROM have_things WHERE 物品 ='娜娜米的项链' AND QQ = '" + \
                        str(uid) + "'"
                    cur.execute(sql_text_1)
                    # 插入保留的
                    sql_text_1 = "INSERT INTO have_things VALUES('" + str(
                        uid) + "', '娜娜米的项链')"
                    for i in range(xianglian_len_save):
                        cur.execute(sql_text_1)

                    # 删除所有
                    sql_text_1 = "DELETE FROM have_things WHERE 物品 ='娜娜米的袜子' AND QQ = '" + \
                        str(uid) + "'"
                    cur.execute(sql_text_1)
                    # 插入保留的
                    sql_text_1 = "INSERT INTO have_things VALUES('" + str(
                        uid) + "', '娜娜米的袜子')"
                    for i in range(wazi_len_save):
                        cur.execute(sql_text_1)

                    # 删除所有
                    sql_text_1 = "DELETE FROM have_things WHERE 物品 ='娜娜米的裙子' AND QQ = '" + \
                        str(uid) + "'"
                    cur.execute(sql_text_1)
                    # 插入保留的
                    sql_text_1 = "INSERT INTO have_things VALUES('" + str(
                        uid) + "', '娜娜米的裙子')"
                    for i in range(qunzi_len_save):
                        cur.execute(sql_text_1)

                    # 删除所有
                    sql_text_1 = "DELETE FROM have_things WHERE 物品 ='娜娜米的鞋带' AND QQ = '" + \
                        str(uid) + "'"
                    cur.execute(sql_text_1)
                    # 插入保留的
                    sql_text_1 = "INSERT INTO have_things VALUES('" + str(
                        uid) + "', '娜娜米的鞋带')"
                    for i in range(xiedai_len_save):
                        cur.execute(sql_text_1)

                    # 删除所有
                    sql_text_1 = "DELETE FROM have_things WHERE 物品 ='娜娜米遛过的狗' AND QQ = '" + \
                        str(uid) + "'"
                    cur.execute(sql_text_1)
                    # 插入保留的
                    sql_text_1 = "INSERT INTO have_things VALUES('" + str(
                        uid) + "', '娜娜米遛过的狗')"
                    for i in range(gou_len_save):
                        cur.execute(sql_text_1)

                    # 删除所有
                    sql_text_1 = "DELETE FROM have_things WHERE 物品 ='娜娜米用过的勺子' AND QQ = '" + \
                        str(uid) + "'"
                    cur.execute(sql_text_1)
                    # 插入保留的
                    sql_text_1 = "INSERT INTO have_things VALUES('" + str(
                        uid) + "', '娜娜米用过的勺子')"
                    for i in range(shaozi_len_save):
                        cur.execute(sql_text_1)

                    # 删除所有
                    sql_text_1 = "DELETE FROM have_things WHERE 物品 ='娜娜米吃过的棒棒糖' AND QQ = '" + \
                        str(uid) + "'"
                    cur.execute(sql_text_1)
                    # 插入保留的
                    sql_text_1 = "INSERT INTO have_things VALUES('" + str(
                        uid) + "', '娜娜米吃过的棒棒糖')"
                    for i in range(bangbangtang_len_save):
                        cur.execute(sql_text_1)

                    # 加入娜娜米的宝藏
                    sql_text_1 = "INSERT INTO have_things VALUES('" + str(
                        uid) + "', '娜娜米的宝藏')"
                    cur.execute(sql_text_1)

                    # 确认插入
                    conn.commit()
                    # 关闭游标
                    cur.close()
                    # 关闭连接
                    conn.close()

                    # 获得成就
                    # 连接 person_info 数据库
                    conn2 = sqlite3.connect('person_info.db')
                    cur2 = conn2.cursor()
                    sql_text_3 = "UPDATE info SET 成就 = '娜娜米之友' WHERE QQ = '" + \
                        str(uid) + "'"
                    print(sql_text_3)
                    cur2.execute(sql_text_3)

                    # 确认插入
                    conn2.commit()
                    # 关闭游标
                    cur2.close()
                    # 关闭连接
                    conn2.close()

                    url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                        str(gid) + "&message=[CQ:at,qq=" + \
                        str(uid) + "]\n[CQ:face,id=190][CQ:face,id=190][CQ:face,id=190]合成物品成功[CQ:face,id=190][CQ:face,id=190][CQ:face,id=190]\n[CQ:face,id=144]获得：娜娜米的宝藏\n[CQ:face,id=144]获得：娜娜米之友 成就~"
                    print(url)
                    requests.get(url)
                    return 'OK'
                else:
                    url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                        str(gid) + "&message=似乎缺少了某样物品呢~"
                    print(url)
                    requests.get(url)
                    return 'OK'
        except:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=格式似乎不太对呢~"
            print(url)
            requests.get(url)
            return 'OK'

    # 新增地图
    if raw_message == '地图':
        url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
            str(gid) + "&message=[CQ:face,id=54][CQ:face,id=54]世界地图[CQ:face,id=54][CQ:face,id=54]\n\n[CQ:face,id=37]九龙古都[CQ:face,id=37]\n[CQ:face,id=158]探索成本：2.5w nmd"
        print(url)
        requests.get(url)

    # 探索地图功能
    if raw_message[0:3] == '探索 ':
        try:
            # 拆分语句
            new_message = raw_message[3:]  # 地图名称
            print(new_message)
            if new_message != '九龙古都':
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=咦？没听说过这地方啊~"
                print(url)
                requests.get(url)
                return 'OK'

            # 检查是否有豆
            conn = sqlite3.connect('person_info.db')
            cur = conn.cursor()
            sql_text_1 = "SELECT * FROM info WHERE QQ='" + str(uid) + "'"
            cur.execute(sql_text_1)

            r = cur.fetchall()
            have_namidou = r[0][3]
            have_chongwu = r[0][4]
            have_daoju = r[0][5]

            if int(have_namidou) < 25000:
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=需要25000豆哦，豆豆似乎不够呢~"
                print(url)
                requests.get(url)
                return 'OK'

            # 有豆则扣除25000豆
            new_namidou = int(have_namidou) - 25000
            sql_text_2 = "UPDATE info SET 娜米豆 = " + \
                str(new_namidou) + " WHERE QQ = '" + str(uid) + "'"
            cur.execute(sql_text_2)
            conn.commit()
            # 关闭游标
            cur.close()
            # 关闭连接
            conn.close()

            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + \
                "&message=[CQ:face,id=172]消费25000娜米豆~\n[CQ:face,id=37]走进这神秘的九龙古都~\n[CQ:face,id=190]究竟会发生什么呢？"
            print(url)
            requests.get(url)
            time.sleep(5)

            # 在1-10中随机
            r_int = random.randint(1, 10)
            if have_chongwu == '露西亚·深红之渊':
                if r_int != 5 and r_int != 6:
                    url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                        str(gid) + "&message=[CQ:at,qq=" + \
                        str(uid) + \
                        "]\n[CQ:face,id=37]【白毛守护】经过一番探索~\n[CQ:face,id=200]没有感受到生命的气息~"
                    print(url)
                    requests.get(url)
                    return 'OK'
            else:
                if r_int != 5:
                    url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                        str(gid) + "&message=[CQ:at,qq=" + \
                        str(uid) + \
                        "]\n[CQ:face,id=37]经过一番探索~\n[CQ:face,id=200]没有感受到生命的气息~"
                    print(url)
                    requests.get(url)
                    return 'OK'

            # 抽中了则在5个气息中随机
            r_int_2 = random.randint(201, 205)
            conn2 = sqlite3.connect('have_things.db')
            cur2 = conn2.cursor()

            sql_text_3 = "SELECT * FROM things WHERE 序号 = '" + \
                str(r_int_2) + "'"
            # 执行sql语句
            cur2.execute(sql_text_3)

            # 获取查询结果
            r = cur2.fetchall()

            # 获取到的物品
            r_get_thing = r[0][1]

            # 将物品加入背包
            sql_text_4 = "INSERT INTO have_things VALUES('" + str(
                uid) + "', '" + str(r_get_thing) + "')"
            cur2.execute(sql_text_4)

            # 确认插入
            conn2.commit()
            # 关闭游标
            cur2.close()
            # 关闭连接
            conn2.close()

            if have_chongwu == '露西亚·深红之渊':
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=[CQ:at,qq=" + \
                    str(uid) + "]\n[CQ:face,id=203]古都中传来阵阵声响！\n[CQ:face,id=144]【白毛守护】出现了：\n[CQ:face,id=54]" + str(
                        r_get_thing)
                print(url)
                requests.get(url)
                return 'OK'
            else:
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=[CQ:at,qq=" + \
                    str(uid) + "]\n[CQ:face,id=203]古都中传来阵阵声响！\n[CQ:face,id=144]出现了：\n[CQ:face,id=54]" + str(
                        r_get_thing)
                print(url)
                requests.get(url)
                return 'OK'
        except:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=格式似乎不太对呢~"
            print(url)
            requests.get(url)
            return 'OK'

    # 宠物召唤
    if raw_message[0:3] == '召唤 ':
        try:
            # 拆分语句
            new_message = raw_message[3:]  # 宠物名称
            print(new_message)
            if new_message != '露西亚·鸦羽' and new_message != '曲·雀翎' and new_message != '露西亚·深红之渊' and new_message != '露娜·银冕' and new_message != '加百利·星陨':
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=似乎不存在这个宠物呢~"
                print(url)
                requests.get(url)
                return 'OK'

            # 检查是否有气息
            conn = sqlite3.connect('have_things.db')
            cur = conn.cursor()
            sql_text_1 = "SELECT * FROM have_things WHERE 物品 ='【气息】-" + \
                str(new_message) + "' AND QQ = '" + str(uid) + "'"
            cur.execute(sql_text_1)

            r = cur.fetchall()

            if len(r) == 0:
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=似乎缺少了某种【气息】~"
                print(url)
                requests.get(url)
                return 'OK'

            # 如果拥有则进行召唤
            save_number = len(r) - 1
            # 删除所有
            sql_text_4 = "DELETE FROM have_things WHERE 物品 ='【气息】-" + \
                str(new_message) + "' AND QQ = '" + str(uid) + "'"
            cur.execute(sql_text_4)
            # 插入保留的
            sql_text_5 = "INSERT INTO have_things VALUES('" + str(
                uid) + "', '【气息】-" + str(new_message) + "')"
            print(save_number)
            for i in range(save_number):
                cur.execute(sql_text_5)

            # 开始召唤
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=[CQ:face,id=190]召唤仪式开启~请稍后..."
            print(url)
            requests.get(url)
            time.sleep(5)

            random_pet_call = random.randint(1, 10)
            if random_pet_call > 3 and random_pet_call < 7:
                # 宠物召唤成功
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=[CQ:at,qq=" + \
                    str(uid) + "]\n[CQ:face,id=190][CQ:face,id=190][CQ:face,id=190]宠物召唤成功[CQ:face,id=190][CQ:face,id=190][CQ:face,id=190]\n[CQ:face,id=144]获得宠物：" + str(new_message)
                print(url)
                requests.get(url)

                sql_text_6 = "INSERT INTO have_pets VALUES('" + str(
                    uid) + "', '" + str(new_message) + "')"
                cur.execute(sql_text_6)
                # 确认插入
                conn.commit()
                # 关闭游标
                cur.close()
                # 关闭连接
                conn.close()
            else:
                # 召唤失败
                # 确认插入
                conn.commit()
                # 关闭游标
                cur.close()
                # 关闭连接
                conn.close()
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=[CQ:at,qq=" + \
                    str(uid) + "]\n[CQ:face,id=212]很可惜~差一点就成功了呢！"
                print(url)
                requests.get(url)

        except:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=格式似乎不太对呢~"
            print(url)
            requests.get(url)
            return 'OK'

    # # 交易所功能
    # if raw_message == '交易所':
    #     conn = sqlite3.connect('jiaoyisuo.db')
    #     cur = conn.cursor()

    #     # 查询问题
    #     sql_text_1 = "SELECT * FROM jiaoyisuo"
    #     cur.execute(sql_text_1)
    #     r = cur.fetchall()

    #     if len(r) == 1:
    #         url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #             str(gid) + \
    #             "&message=[CQ:face,id=158][CQ:face,id=158]娜娜米交易所[CQ:face,id=158][CQ:face,id=158]\n\n暂无上架商品"
    #         requests.get(url)
    #         return 'OK'

    #     url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #         str(gid) + \
    #         "&message=[CQ:face,id=158][CQ:face,id=158]娜娜米交易所[CQ:face,id=158][CQ:face,id=158]"

    #     for i in r:
    #         if str(i[2]) == "111111":
    #             continue
    #         url = url + "\n\n商品编号：" + str(i[0]) + "\n[CQ:face,id=46]出售人：" + str(
    #             i[1]) + "\n[CQ:face,id=57]物品：" + str(i[3]) + "\n[CQ:face,id=158]价格：" + str(i[4])
    #     print(url)
    #     requests.get(url)
    #     return 'OK'

    # # 交易所上架功能
    # if raw_message[0:3] == '上架 ':
    #     try:
    #         # 拆分语句
    #         new_message = raw_message[3:]
    #         location = re.search(' ', new_message).span()
    #         print(location)
    #         sale_thing = new_message[:location[0]]  # 上架物品
    #         print(sale_thing)
    #         sale_namidou = new_message[location[1]:]  # 上架价格
    #         print(sale_namidou)

    #         # 检测上架金额是否合理
    #         if sale_namidou <= 0:
    #             url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #                 str(gid) + "&message=格式似乎不太对呢~"
    #             print(url)
    #             requests.get(url)
    #             return 'OK'
    #         try:
    #             sale_namidou = int(sale_namidou)
    #         except:
    #             url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #                 str(gid) + "&message=格式似乎不太对呢~"
    #             print(url)
    #             requests.get(url)
    #             return 'OK'

    #         # 检测是否有此物品
    #         conn = sqlite3.connect('have_things.db')
    #         cur = conn.cursor()

    #         # 查询问题
    #         sql_text_1 = "SELECT * FROM have_things WHERE QQ = '" + \
    #             str(uid) + "' AND 物品 = '" + str(sale_thing) + "'"
    #         cur.execute(sql_text_1)
    #         r = cur.fetchall()

    #         # 没有此物品
    #         if len(r) == 0:
    #             url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #                 str(gid) + "&message=似乎没有这个物品呢~"
    #             print(url)
    #             requests.get(url)
    #             return 'OK'

    #         # 有此物品则上架一个
    #         save_number = len(r) - 1
    #         # 删除所有
    #         sql_text_4 = "DELETE FROM have_things WHERE 物品 ='" + \
    #             str(sale_thing) + "' AND QQ = '" + str(uid) + "'"
    #         cur.execute(sql_text_4)
    #         # 插入保留的
    #         sql_text_5 = "INSERT INTO have_things VALUES('" + str(
    #             uid) + "', '" + str(sale_thing) + "')"
    #         print(save_number)
    #         for i in range(save_number):
    #             cur.execute(sql_text_5)
    #         # 确认插入
    #         conn.commit()
    #         # 关闭游标
    #         cur.close()
    #         # 关闭连接
    #         conn.close()

    #         # 加入交易所
    #         conn2 = sqlite3.connect('jiaoyisuo.db')
    #         cur2 = conn2.cursor()

    #         # 获取当前商品编号进度
    #         sql_text_6 = "SELECT * FROM jiaoyisuo WHERE QQ = '111111'"
    #         cur2.execute(sql_text_6)
    #         r = cur2.fetchall()
    #         sale_number = int(r[0][4]) + 1

    #         # 更新商品编号
    #         sql_text_7 = "UPDATE jiaoyisuo SET 价格 = " + \
    #             str(sale_number) + " WHERE QQ = '111111'"
    #         cur2.execute(sql_text_7)

    #         # 获取当前人的昵称
    #         url1 = "http://127.0.0.1:5700/get_group_member_info?group_id=" + \
    #             str(gid) + "&user_id=" + str(uid)
    #         r_1 = requests.get(url1)
    #         name = r_1.json()['data']['card']
    #         if len(name) == 0:
    #             name = r_1.json()['data']['nickname']

    #         # 上架
    #         sql_text_8 = "INSERT INTO jiaoyisuo VALUES('" + str(sale_number) + "', '" + str(
    #             name) + "','" + str(uid) + "', '" + str(sale_thing) + "', " + str(sale_namidou) + ")"
    #         cur2.execute(sql_text_8)

    #         # 确认插入
    #         conn2.commit()
    #         # 关闭游标
    #         cur2.close()
    #         # 关闭连接
    #         conn2.close()

    #         url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #             str(gid) + "&message=物品上架成功~"
    #         print(url)
    #         requests.get(url)
    #         return 'OK'

    #     except:
    #         url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #             str(gid) + "&message=格式似乎不太对呢~"
    #         print(url)
    #         requests.get(url)
    #         return 'OK'

    # # 交易所下架功能
    # if raw_message[0:3] == '下架 ':
    #     try:
    #         # 拆分语句
    #         new_message = raw_message[3:]  # 下架编号

    #         # 查询交易所
    #         conn = sqlite3.connect('jiaoyisuo.db')
    #         cur = conn.cursor()

    #         # 检查是否是本人操作
    #         sql_text_1 = "SELECT * FROM jiaoyisuo WHERE 编号 = '" + \
    #             str(new_message) + "'"
    #         cur.execute(sql_text_1)
    #         r = cur.fetchall()
    #         if len(r) == 0:
    #             url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #                 str(gid) + "&message=似乎没有这个编号呢~"
    #             print(url)
    #             requests.get(url)
    #             return 'OK'
    #         if str(r[0][2]) != str(uid):
    #             url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #                 str(gid) + "&message=还想下架别人的商品？哼！"
    #             print(url)
    #             requests.get(url)
    #             return 'OK'
    #         # 获取商品名称
    #         xiajia_thing = r[0][3]
    #         # 开始下架
    #         sql_text_2 = "DELETE FROM jiaoyisuo WHERE 编号='" + \
    #             str(new_message) + "'"
    #         cur.execute(sql_text_2)
    #         # 确认插入
    #         conn.commit()
    #         # 关闭游标
    #         cur.close()
    #         # 关闭连接
    #         conn.close()

    #         # 返还到本人背包
    #         conn2 = sqlite3.connect('have_things.db')
    #         cur2 = conn2.cursor()

    #         # 加入背包
    #         sql_text_3 = "INSERT INTO have_things VALUES('" + str(
    #             uid) + "','" + str(xiajia_thing) + "')"
    #         cur2.execute(sql_text_3)
    #         # 确认插入
    #         conn2.commit()
    #         # 关闭游标
    #         cur2.close()
    #         # 关闭连接
    #         conn2.close()

    #         url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #             str(gid) + "&message=物品下架成功~"
    #         print(url)
    #         requests.get(url)
    #         return 'OK'

    #     except:
    #         url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #             str(gid) + "&message=格式似乎不太对呢~"
    #         print(url)
    #         requests.get(url)
    #         return 'OK'

    # # 交易所物品购买功能
    # if raw_message[0:3] == '购买 ':
    #     try:
    #         # 拆分语句
    #         new_message = raw_message[3:]  # 购买编号
    #         # 查询交易所
    #         conn = sqlite3.connect('jiaoyisuo.db')
    #         cur = conn.cursor()
    #         sql_text_1 = "SELECT * FROM jiaoyisuo WHERE 编号 = '" + \
    #             str(new_message) + "'"
    #         cur.execute(sql_text_1)
    #         r = cur.fetchall()
    #         if len(r) == 0:
    #             url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #                 str(gid) + "&message=似乎没有这个商品编号呢~"
    #             print(url)
    #             requests.get(url)
    #             return 'OK'
    #         if str(r[0][2]) == str(uid):
    #             url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #                 str(gid) + "&message=买自己的物品，闲的无聊？"
    #             print(url)
    #             requests.get(url)
    #             return 'OK'
    #         # 开始购买
    #         sale_qq = r[0][2]
    #         sale_thing = r[0][3]
    #         sale_namidou = r[0][4]

    #         # 检查是否有足够娜米豆
    #         conn2 = sqlite3.connect('person_info.db')
    #         cur2 = conn2.cursor()
    #         sql_text_2 = "SELECT * FROM info WHERE QQ = '" + str(uid) + "'"
    #         cur2.execute(sql_text_2)
    #         r2 = cur2.fetchall()
    #         have_namidou = r2[0][3]

    #         # 获取出售人娜米豆信息
    #         sql_text_3 = "SELECT * FROM info WHERE QQ = '" + str(sale_qq) + "'"
    #         cur2.execute(sql_text_3)
    #         r3 = cur2.fetchall()
    #         have_namidou_sale = r3[0][3]

    #         # 购买人豆不够则退出
    #         if int(have_namidou) < int(sale_namidou):
    #             url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #                 str(gid) + "&message=豆豆似乎不够呢~"
    #             print(url)
    #             requests.get(url)
    #             return 'OK'

    #         # 购买人扣除娜米豆
    #         new_namidou_buy = int(have_namidou) - int(sale_namidou)
    #         # 出售人获得娜米豆
    #         new_namidou_sale = int(have_namidou_sale) + int(sale_namidou)
    #         # 更新娜米豆信息
    #         sql_text_4 = "UPDATE info SET 娜米豆 = " + \
    #             str(new_namidou_buy) + " WHERE QQ = " + str(uid)
    #         print(sql_text_4)
    #         cur2.execute(sql_text_4)
    #         sql_text_5 = "UPDATE info SET 娜米豆 = " + \
    #             str(new_namidou_sale) + " WHERE QQ = " + str(sale_qq)
    #         print(sql_text_5)
    #         cur2.execute(sql_text_5)
    #         # 确认插入
    #         conn2.commit()
    #         # 关闭游标
    #         cur2.close()
    #         # 关闭连接
    #         conn2.close()

    #         # 交易所下架物品
    #         sql_text_6 = "DELETE FROM jiaoyisuo WHERE 编号='" + \
    #             str(new_message) + "'"
    #         cur.execute(sql_text_6)
    #         # 确认插入
    #         conn.commit()
    #         # 关闭游标
    #         cur.close()
    #         # 关闭连接
    #         conn.close()

    #         # 加入购买者背包
    #         conn3 = sqlite3.connect('have_things.db')
    #         cur3 = conn3.cursor()

    #         # 加入背包
    #         sql_text_7 = "INSERT INTO have_things VALUES('" + str(
    #             uid) + "','" + str(sale_thing) + "')"
    #         cur3.execute(sql_text_7)
    #         # 确认插入
    #         conn3.commit()
    #         # 关闭游标
    #         cur3.close()
    #         # 关闭连接
    #         conn3.close()

    #         url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:face,id=144]购买成功~\n你还剩余 " + str(
    #             new_namidou_buy) + " 娜米豆~\n[CQ:at,qq=" + str(sale_qq) + "]\n获得 " + str(sale_namidou) + " 娜米豆"
    #         print(url)
    #         requests.get(url)
    #         return 'OK'
    #     except:
    #         url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
    #             str(gid) + "&message=格式似乎不太对呢~"
    #         print(url)
    #         requests.get(url)
    #         return 'OK'

    # 更换携带宠物
    if raw_message[0:3] == '携带 ':
        try:
            # 拆分语句
            new_message = raw_message[3:]  # 携带宠物名字
            # 查询是否背包拥有
            conn = sqlite3.connect('have_things.db')
            cur = conn.cursor()

            sql_text_1 = "SELECT * FROM have_pets WHERE QQ = '" + \
                str(uid) + "' AND 宠物 = '" + str(new_message) + "'"
            cur.execute(sql_text_1)
            r = cur.fetchall()

            if len(r) == 0:
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=似乎没有这个宠物呢~"
                print(url)
                requests.get(url)
                return 'OK'

            # 检查是否携带宠物
            conn2 = sqlite3.connect('person_info.db')
            cur2 = conn2.cursor()

            sql_text_2 = "SELECT * FROM info WHERE QQ = '" + str(uid) + "'"
            cur2.execute(sql_text_2)
            r2 = cur2.fetchall()
            have_chongwu = r2[0][4]

            # 如果为空则直接携带
            if str(have_chongwu) == '无':
                # 更新为新宠物
                sql_text_3 = "UPDATE info SET 宠物 = '" + \
                    str(new_message) + "' WHERE QQ = '" + str(uid) + "'"
                cur2.execute(sql_text_3)
                # 从背包删除一个
                save_number = len(r) - 1
                # 删除所有
                sql_text_4 = "DELETE FROM have_pets WHERE 宠物 ='" + \
                    str(new_message) + "' AND QQ = '" + str(uid) + "'"
                cur.execute(sql_text_4)
                # 插入保留的
                sql_text_5 = "INSERT INTO have_pets VALUES('" + str(
                    uid) + "', '" + str(new_message) + "')"
                print(save_number)
                for i in range(save_number):
                    cur.execute(sql_text_5)
                # 确认插入
                conn.commit()
                # 关闭游标
                cur.close()
                # 关闭连接
                conn.close()
                # 确认插入
                conn2.commit()
                # 关闭游标
                cur2.close()
                # 关闭连接
                conn2.close()
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=宠物携带成功~"
                print(url)
                requests.get(url)
                return 'OK'
            else:
                # 更新为新宠物
                sql_text_3 = "UPDATE info SET 宠物 = '" + \
                    str(new_message) + "' WHERE QQ = '" + str(uid) + "'"
                cur2.execute(sql_text_3)
                # 从背包删除一个
                save_number = len(r) - 1
                # 删除所有
                sql_text_4 = "DELETE FROM have_pets WHERE 宠物 ='" + \
                    str(new_message) + "' AND QQ = '" + str(uid) + "'"
                cur.execute(sql_text_4)
                # 插入保留的
                sql_text_5 = "INSERT INTO have_pets VALUES('" + str(
                    uid) + "', '" + str(new_message) + "')"
                print(save_number)
                for i in range(save_number):
                    cur.execute(sql_text_5)
                # 将携带的宠物加入背包
                sql_text_6 = "INSERT INTO have_pets VALUES('" + str(
                    uid) + "', '" + str(have_chongwu) + "')"
                cur.execute(sql_text_6)
                # 确认插入
                conn.commit()
                # 关闭游标
                cur.close()
                # 关闭连接
                conn.close()
                # 确认插入
                conn2.commit()
                # 关闭游标
                cur2.close()
                # 关闭连接
                conn2.close()
                url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                    str(gid) + "&message=宠物携带成功~"
                print(url)
                requests.get(url)
                return 'OK'
        except:
            url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
                str(gid) + "&message=格式似乎不太对呢~"
            print(url)
            requests.get(url)
            return 'OK'

    # 日常回答 ============================================================================================
    # 查询数据库问题
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    # 查询问题
    sql_text_4 = "SELECT * FROM study"
    cur.execute(sql_text_4)

    # 获取查询结果
    r = cur.fetchall()

    # print(r)

    tmp = []

    for i in r:
        if i[0] in raw_message:
            tmp.append(i)

    print(tmp)

    r = tmp
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()

    if len(r) == 0:
        # url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=娜娜米听不懂你在说什么呢~"
        # requests.get(url)
        # a = random.randint(0,10)
        # if a < 3:
        #     time.sleep(0.5)
        #     url2 = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=试试发送：“学习-问题-回复” 让我学习新的知识吧~（中间用空格分开,不用@我哦~）"
        #     requests.get(url2)
        #     time.sleep(0.5)
        #     url3 = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=比如：学习 你在干嘛呢 我在吃好吃的呢~"
        #     requests.get(url3)
        return 'OK'
    else:
        # 获取随机答案
        answer_location = random.randint(0, len(r)-1)
        print(answer_location)
        print(r[answer_location][1])
        url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
            str(gid) + "&message=" + r[answer_location][1]
        requests.get(url)

    # if raw_message == '娜娜米':
    #     url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=听说有人叫我？"
    #     requests.get(url)
#     print(message + str(gid) + str(uid))
#     p_url = "https://i.pixiv.cat/img-original/img/2018/10/31/00/29/45/71425447_p0.jpg"
#     url1 = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=你好！[CQ:at,qq=" + str(uid) + "]"
#     url2 = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + str(gid) + "&message=[CQ:image,file=" + str(p_url) + ",type=show,id=40000]"
#     if message == '你好':
#         requests.get(url2)


# 处理私人关键字=============================================================================================


def keyword_p(json):

    uid = json.get('sender').get('user_id')  # 获取私人uid
    raw_message = json.get('raw_message')  # 获取消息
    message = json.get('message')  # 获取全消息
    print('==============')
    print(message)
    account = 0

    # # 返回图片
    # if '涩图' in raw_message or '瑟图' in raw_message or '色图' in raw_message:
    #     while account != 5:
    #         r = requests.get("https://api.lolicon.app/setu/v2")  # 获取
    #         p_url = r.json()['data'][0]['urls']['original']  # 解析url
    #         url = "http://127.0.0.1:5700/send_msg?message_type=private&user_id=" + \
    #             str(uid) + "&message=[CQ:image,file=" + str(p_url) + "]"
    #         print(raw_message + str(uid))
    #         print(p_url)
    #         requests.get(url)
    #         account += 1
    #         time.sleep(1)
    #     return 'OK'

    # 查询图片
    if message[0:9] == '[CQ:image':
        print('收到一个图片')

        # 获取url
        re_result = re.search('url=', message).span()
        a = re_result[1]
        image_url = message[a:len(message)-1]

        # 用saucenao查询
        search_url = "https://saucenao.com/search.php"
        data = {'file': '(binary)', 'url': image_url}
        r_search = requests.post(search_url, data)
        r_search = r_search.content.decode('utf-8')

        # 匹配寻找图片地址
        re_a = re.search('<div class="resultcontentcolumn">', r_search).span()
        r_search = r_search[re_a[1]:]
        re_b = re.search('<a href="', r_search).span()
        r_search = r_search[re_b[1]:]
        re_c = re.search('"', r_search).span()
        result = str(r_search[:re_c[0]])
        print(result)

        # 返回给用户
        # 实现转义
        result = escape_symbol(result)

        print(result)
        url = "http://127.0.0.1:5700/send_msg?message_type=private&user_id=" + \
            str(uid) + "&message=" + result
        print(str(uid) + "查询成功")
        requests.get(url)
        return 'OK'

    # 自主学习
    if raw_message[0:3] == '学习 ':
        # 拆分语句
        new_message = raw_message[3:]
        location = re.search(' ', new_message).span()
        print(location)
        question = new_message[:location[0]]  # 问
        print(question)
        answer = new_message[location[1]:]  # 答
        print(answer)

        # 与 data.db 数据库连接
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()

        # # 建表的sql语句 创建 study 表
        # sql_text_1 = '''CREATE TABLE study
        #         (问题 TEXT,
        #             答案 TEXT);'''

        # # 执行sql语句
        # cur.execute(sql_text_1)

        # 插入单条数据
        sql_text_2 = "INSERT INTO study VALUES('" + \
            question + "', '" + answer + "')"
        print(sql_text_2)
        cur.execute(sql_text_2)

        # 确认插入
        conn.commit()

        # 关闭游标
        cur.close()
        # 关闭连接
        conn.close()

        url = "http://127.0.0.1:5700/send_msg?message_type=private&user_id=" + \
            str(uid) + "&message=太棒了！娜娜米又学到了新知识呢！"
        requests.get(url)

        return 'OK'

    # 查询数据库问题
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    # # 查询问题
    # sql_text_4 = "SELECT * FROM study WHERE 问题='" + raw_message + "'"
    # cur.execute(sql_text_4)

    # # 获取查询结果
    # r = cur.fetchall()

    # # 关闭游标
    # cur.close()
    # # 关闭连接
    # conn.close()

    # if len(r) == 0:
    #     url = "http://127.0.0.1:5700/send_msg?message_type=private&user_id=" + str(uid) + "&message=娜娜米不知道你在说什么呢~"
    #     requests.get(url)
    # else:
    #     # 获取随机答案
    #     answer_location = random.randint(0,len(r)-1)
    #     print(answer_location)
    #     print(r[answer_location][1])
    #     url = "http://127.0.0.1:5700/send_msg?message_type=private&user_id=" + str(uid) + "&message=" + r[answer_location][1]
    #     requests.get(url)

    # 查询问题
    sql_text_4 = "SELECT * FROM study"
    cur.execute(sql_text_4)

    # 获取查询结果
    r = cur.fetchall()

    # print(r)

    tmp = []

    for i in r:
        if i[0] in raw_message:
            tmp.append(i)

    print(tmp)

    r = tmp
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()

    if len(r) == 0:
        url = "http://127.0.0.1:5700/send_msg?message_type=private&user_id=" + \
            str(uid) + "&message=娜娜米听不懂你在说什么呢~"
        requests.get(url)
        a = random.randint(0, 10)
        if a < 3:
            time.sleep(0.5)
            url2 = "http://127.0.0.1:5700/send_msg?message_type=private&user_id=" + \
                str(uid) + "&message=试试给我发送：“学习-问题-回复” 让我学习新的知识吧~（中间用空格分开哦）"
            requests.get(url2)
            time.sleep(0.5)
            url3 = "http://127.0.0.1:5700/send_msg?message_type=private&user_id=" + \
                str(uid) + "&message=比如：学习 你在干嘛呢 我在吃好吃的呢~"
            requests.get(url3)
    else:
        # 获取随机答案
        answer_location = random.randint(0, len(r)-1)
        print(answer_location)
        print(r[answer_location][1])
        url = "http://127.0.0.1:5700/send_msg?message_type=private&user_id=" + \
            str(uid) + "&message=" + r[answer_location][1]
        requests.get(url)

# =================================================================================================================


def setu(message, gid, uid):
    r = requests.get("https://api.lolicon.app/setu/v2")  # 获取
    p_url = r.json()['data'][0]['urls']['original']  # 解析url
    print(message + str(gid) + str(uid))
    url = "http://127.0.0.1:5700/send_msg?message_type=group&group_id=" + \
        str(gid) + "&message=[CQ:image,file=" + str(p_url) + ",id=40000]"
    requests.get(url)

# 实现url转义功能


def escape_symbol(url):
    url = url.replace('"', "%22")
    url = url.replace('#', "%23")
    url = url.replace('%', "%25")
    url = url.replace('&', "%26")
    url = url.replace('(', "%28")
    url = url.replace(')', "%29")
    url = url.replace('+', "%2B")
    url = url.replace(',', "%2C")
    # url = url.replace('/', "%2F")
    url = url.replace(':', "%3A")
    url = url.replace(';', "%3B")
    url = url.replace('<', "%3C")
    url = url.replace('=', "%3D")
    # url = url.replace('>', "%3E")
    # url = url.replace('?', "%3F")
    url = url.replace('@', "%40")
    url = url.replace('|', "%7C")
    return url
