#!/usr/bin/env python
# coding=utf-8

from datetime import datetime
from flask import render_template, session, url_for, current_app, abort, flash, request, make_response, request, jsonify
import json
from hashlib import md5
from . import main
from .. import db
from .. import config
from ..models import Manager, Sales, Byeer, Cars, Bills

@main.route("/login", methods=["POST"])
def login():
    login_data = request.get_data()
    login_data = json.loads(login_data)
    print(login_data)
    person = Sales.objects.find({"phone": login_data["phone"]}).first()
    if not person:
        result_data = {
            "code": 500,
            "msg": "帐号密码不匹配",
            "data": {}
        }
    elif md5(login_data["password"].encode()).hexdigest() != person["password"]:
        result_data = {
            "code": 500,
            "msg": "帐号密码不匹配",
            "data": {}
        }
    else:
        session["user"] = person
        result_data = {
            "code": 200,
            "msg": "登录成功",
            "data": {"data": person}
        }
    return result_data


@main.route("/register", methods=["POST"])
def register():
    register_data = request.get_data()
    register_data = json.loads(register_data)
    saler = Sales(id="1", name=register_data["name"], phone=register_data["phone"], email="", password=register_data["password"], creater=register_data["creater"])
    saler.save()
    return {"code":"ok"}

