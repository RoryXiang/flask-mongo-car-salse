#!/usr/bin/env python
# coding=utf-8

from datetime import datetime
from flask import render_template, session, url_for, current_app, abort, flash, request, make_response, request, jsonify
import json
import mongoengine
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
    person = Sales.objects(phone=login_data["phone"]).first()
    print(person.password, "????")
    if not person:
        result_data = {
            "code": 500,
            "msg": "帐号密码不匹配",
            "data": {}
        }
    elif md5(login_data["password"].encode()).hexdigest() != person.password:
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
    pwd = md5(register_data["password"].encode()).hexdigest()
    saler = Sales(name=register_data["name"], phone=register_data["phone"], email="", password=pwd, creater=register_data["creater"])
    try:
        saler.save()
        data = {
            "code": 200,
            "msg": "注册成功",
            "data": {}
        }
    except mongoengine.errors.NotUniqueError as e:
        print(e)
        data = {
            "code": 401,
            "msg": "手机号重复",
            "data": {}
        }

    return data
