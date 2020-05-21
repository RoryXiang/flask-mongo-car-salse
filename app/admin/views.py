
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
from ..models import Manager, Sales, Cars, Bills, Byeer
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import functools
from mongoengine.queryset.visitor import Q
from ..main.views import login_required, create_token, verify_token


token_key = "test"


@admin.route("/admin_login", methods=["POST"])
def login():
    login_data = request.get_data()
    login_data = json.loads(login_data)
    person = Manager.objects(phone=login_data["phone"]).first()
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
        session["manager_id"] = person._id
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
    manager_id = session.get("manager_id", None)
    pwd = md5(register_data["password"].encode()).hexdigest()
    saler = Sales(name=register_data["name"], 
                  phone=register_data["phone"],
                  ismaster=register_data.get("ismaster", 0),
                  email=register_data.get("email", ""), 
                  password=pwd,
                  education=register_data.get("education", ""),
                  self_introduction=register_data.get("self_introduction", ""),
                  master_blong=register_data.get("master_id", 0),
                  creater=manager_id
    )
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
    manager_id = session.get("manager_id", None)
    pwd = md5(register_data["password"].encode()).hexdigest()
    manager = Manager(name=register_data["name"], 
                  phone=register_data["phone"],
                  email=register_data.get("email", ""), 
                  ismaster=register_data.get("ismaster", 0),
                  password=pwd, 
                  creater=manager_id,
                  education=register_data.get("education", ""),
                  self_introduction=register_data.get("self_introduction", "")
    )
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
    manager_id = session.get("manager_id", None)
    car = Cars(
        name=car_info["name"],
        min_price=float(car_info["min_price"]),
        max_price=float(car_info["max_price"]),
        introduction=car_info["introduction"],
        brand=car_info["brand"],
        insert_manager=manager_id,
        saled_number=0
    )
    car.save()
    data = {
        "code": 200,
        "msg": "入库成功",
        "data": {}
    }
    return data


@admin.route("/creat_bill", methods=["POST"])
@login_required
def create_bill():
    parm_data = request.get_data()
    parm_data = jsonify(parm_data)
    manager_id = session.get("manager_id", None)
    bill = Bills(
        car_id=parm_data["car_id"],
        saler_id=parm_data["saler_id"],
        price_saled=parm_data["price_saled"],
        byeer_id=parm_data["byeer_id"],
        creater=manager_id,
    )
    bill.save()
    result_data = {
        "code": 200,
        "msg": "账单创建成功",
        "data": {}
    }
    return result_data


@admin.route("/bill", methods=["POST"])
@login_required
def get_bill():
    parm_data = request.get_data()
    parm_data = jsonify(parm_data)
    bill = Bills.objects(
        Q(car_id=parm_data.get("car_id", None)) | Q(saler_id=parm_data.get("saler_id", None)) | Q(byeer_id=parm_data.get("byeer_id", None)) | Q(creater=parm_data.get("manager_id", None))
    )
    if not bill:
        result_data = {
            "code": 404,
            "msg": "没有查到相应的账单",
            "data": {}
        }
        return result_data
    bill_info = jsonify(bill)
    car = Cars.objects(_id=bill.car_id).first()
    bill_info["car_name"] = car.name
    saler = Sales.objects(_id=bill.saler_id).first()
    bill_info["saler_name"] = saler.name
    byeer = Byeer.objects(_id=bill.byeer_id).first()
    bill_info["byeer_name"] = byeer.name
    result_data = {
        "code": 200,
        "msg": "成功",
        "data": bill_info
    }
    return result_data
