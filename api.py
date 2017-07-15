# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import abort
from flask import render_template
from model import *
from tokenEncryption import TokenToEncryption
import json
import random

app = Flask(__name__,static_url_path='/static')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html'), 200

@app.route('/pwd_tool', methods=['GET','POST'])
def pwd_tool():
    if request.method == "GET":
        return pwd_tool_show(), 200
    else: return pwd_tool_post(), 200

@app.route('/pwd_tool_help', methods=['GET'])
def pwd_tool_help():
    return render_template('pwd_tool_help.html'), 200

def pwd_tool_show():
    return render_template('pwd_tool.html')

def pwd_tool_post():
    if not request.json or not 'phone' in request.json:
        abort(400)
    if not request.json or not 'token' in request.json:
        abort(400)

    phone = request.json.get("phone")
    token = request.json.get("token")
    action = request.json.get("action")

    if not phone.isdigit() and "@" not in phone:
        return "手机号码或邮箱格式不正确"

    account = getAccount(phone)

    if account is None:
        key = create_encryption_key()
        item = addEncryptionKey(key)
        createAccount(phone, item.id)
    else:
        item = getEncryptionKey(account.tbl_encryption_keys_id)

    if action == "reset":
        key = create_encryption_key()
        item = addEncryptionKey(key)
        createAccount(phone, item.id)

    tte = TokenToEncryption()
    createToken(token, item.id)
    code = tte.convert(token, item.key)
    return code

#http://127.0.0.1:8000/encryption_key/1
@app.route('/encryption_key/<string:phone>', methods=['GET'])
def get_encryption_key(phone):
    account = getAccount(phone)
    if account is None:
        key = create_encryption_key()
        item = addEncryptionKey(key)
        createAccount(phone, item.id)
    else:
        item = getEncryptionKey(account.tbl_encryption_keys_id)
    return json.dumps(item.serialize(),default=datetime_handler), 201


@app.route('/encryption_key', methods=['POST'])
def get_new_encryption_key():
    if not request.json or not 'id' in request.json:
       abort(400)

    id = -1
    if request.json.get("id"):
        id = int( request.json.get("id") )
    key = create_encryption_key()
    if id> 0:
        item = udpateEncryptionKey(id, key)
    else:
        item = addEncryptionKey(key)
    return json.dumps(item.serialize(), default=datetime_handler), 201


def create_encryption_key():
    items = ['0','1','2','3','4','5','6','7','8','9']
    random.shuffle(items)
    key = ''
    for item in items:
        key = key + item
    return key

if __name__ == '__main__':
    app.run(debug=True,port=8000)