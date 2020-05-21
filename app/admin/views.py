
#!/usr/bin/env python
# coding=utf-8

from datetime import datetime
from flask import session, url_for, current_app, abort, flash, request, make_response, request, jsonify
import json
import mongoengine
from hashlib import md5
from . import admin
from .. import db
from .. import config
from ..models import Manager, Sales, Cars
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import functools
from mongoengine.queryset.visitor import Q
from ..main.views import login_required, create_token, verify_token


token_key = "test"


@admin.route("/admin_login", methods=["POST"])
def login():
    login_data = request.get_data()
    login_data = json.loads(login_data)
    print(login_data)
    person = Manager.objects(phone=login_data["phone"]).first()
    print(person.password, "????")
    if not person:
        result_data = {
            "code": 401,
            "msg": "帐号不存在",
            "data": {}
        }
    elif md5(login_data["password"].encode()).hexdigest() != person.password:
        result_data = {
            "code": 401,
            "msg": "帐号密码不匹配",
            "data": {}
        }
    else:
        session["user"] = person.phone
        token = create_token(person.phone)
        result_data = {
            "code": 200,
            "msg": "登录成功",
            "data": jsonify(person),
            "token": token
        }
    return result_data


@admin.route("/saler_register", methods=["POST"])
@login_required
def saler_register():
    register_data = request.get_data()
    register_data = json.loads(register_data)
    pwd = md5(register_data["password"].encode()).hexdigest()
    saler = Sales(name=register_data["name"], 
                  phone=register_data["phone"],
                  ismaster=register_data.get("ismaster", 0),
                  email="", 
                  password=pwd, 
                  creater=register_data["creater"])
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


@admin.route("/manager_register", methods=["POST"])
@login_required
def manager_register():
    register_data = request.get_data()
    register_data = json.loads(register_data)
    pwd = md5(register_data["password"].encode()).hexdigest()
    manager = Manager(name=register_data["name"], 
                  phone=register_data["phone"],
                  email="", 
                  ismaster=register_data.get("ismaster", 0),
                  password=pwd, 
                  creater=register_data["creater"])
    try:
        manager.save()
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


@admin.route("/master_salers", methods=["GET"])
@login_required
def get_saler_masters():
    saler_masters = Sales.objects(ismaster=True).limit(20)
    return jsonify(saler_masters)


@admin.route("/insert_cars", methods=["POST"])
@login_required
def insert_cars():
    car_info = request.get_data()
    car_info = json.loads(car_info)
    car = Cars(
        name=car_info["name"],
        min_price=float(car_info["min_price"]),
        max_price=float(car_info["max_price"]),
        introduction=car_info["introduction"],
        brand=car_info["brand"],
        saled_number=0
    )
    car.save()
    data = {
        "code": 200,
        "msg": "入库成功",
        "data": {}
    }
    return data
