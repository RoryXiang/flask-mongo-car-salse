#!/usr/bin/env python
# coding=utf-8

from datetime import datetime
from flask import session, url_for, current_app, abort, flash, request, make_response, request, jsonify
import json
import mongoengine
from hashlib import md5
from . import main
from .. import db
from .. import config
from ..models import Sales, Byeer, Cars, Bills
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import functools
from mongoengine.queryset.visitor import Q


token_key = "test"


def login_required(view_func):
    @functools.wraps(view_func)
    def verify_token(*args, **kwargs):
        try:
            # 在请求头上拿到token
            token = request.headers["z-token"]
        except Exception:
            # 没接收的到token,给前端抛出错误
            # 这里的code推荐写一个文件统一管理。这里为了看着直观就先写死了。
            return jsonify(code=4103, msg='缺少参数token')

        s = Serializer(token_key)
        try:
            s.loads(token)
        except Exception:
            return jsonify(code=4101, msg="登录已过期")

        return view_func(*args, **kwargs)

    return verify_token


def create_token(user_phone):
    '''
    生成token
    :param api_user:用户id
    :return: token
    '''

    # 第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    # 第二个参数是有效期(秒)
    s = Serializer(token_key, expires_in=3600)
    # 接收用户id转换与编码
    token = s.dumps({"phone": user_phone}).decode("ascii")
    return token


def verify_token(Model, token):
    '''
    校验token
    :param token: 
    :return: 用户信息 or None
    '''

    # 参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(token_key)
    try:
        # 转换为字典
        data = s.loads(token)
    except Exception:
        return None
    # 拿到转换后的数据，根据模型类去数据库查询用户信息
    user = Model.objects(phone=data["phone"]).first()
    return user


@main.route("/login", methods=["POST"])
def login():
    login_data = request.get_data()
    login_data = json.loads(login_data)
    print(login_data)
    person = Sales.objects(phone=login_data["phone"]).first()
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
        session["saler_id"] = person._id
        token = create_token(person.phone)
        result_data = {
            "code": 200,
            "msg": "登录成功",
            "data": jsonify(person),
            "token": token 
        }
    return result_data


@main.route("/insert_cars", methods=["POST"])
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


@main.route("/cars", methods=["POST"])
@login_required
def get_cars():
    parm_data = request.get_data()
    parm_data = json.loads(parm_data)
    if not parm_data:
        cars = Cars.objects().limit(20).order_by("-saled_number")
    else:
        cars = Cars.objects(
            Q(name__contains=parm_data.get("name", "")) & Q(brand=parm_data.get("brand", "")) & Q(min_price__gte=parm_data.get("min_price", 0)) & Q(max_price__lte=parm_data.get("max_price", 999999999999))
        ).limit(20).order_by("-saled_number")
    return jsonify(cars)
    # TODO 需要解决分页问题
