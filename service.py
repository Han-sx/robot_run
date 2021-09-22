from flask import Flask, request
import requests

'''注意，这里的import api是另一个py文件，下文会提及'''
import api

app = Flask(__name__)

'''监听端口，获取QQ信息'''


@app.route('/', methods=["POST"])
def post_data():
    # 获取群聊数据
    if request.get_json().get('message_type') == 'group':
        # gid = request.get_json().get('group_id') #获取群号
        # uid = request.get_json().get('sender').get('user_id') #获取发送人q
        # message = request.get_json().get('raw_message') #获取信息
        api.keyword_g(request.get_json())

    # 获取私人数据
    # print(request.get_json())
    if request.get_json().get('message_type') == 'private':
        # uid = request.get_json().get('sender').get('user_id')
        # message = request.get_json().get('raw_message')
        api.keyword_p(request.get_json())
    return 'OK'


if __name__ == '__main__':
    # 此处的 host和 port对应上面 yml文件的设置
    app.run(debug=True, host='127.0.0.1', port=5799)
