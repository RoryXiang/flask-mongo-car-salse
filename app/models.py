#!/usr/bin/env python
# coding=utf-8

from . import mongo
import datetime


class BasePerson(mongo.Document):
    id = mongo.SequenceField(primary_key=True)
    name = mongo.StringField()
    phone = mongo.StringField(required=True, max_length=11, unique=True)
    email = mongo.StringField()
    password = mongo.StringField(required=True)
    create_tiem = mongo.DateTimeField(default=datetime.datetime.now, required=True)
    ismaster = mongo.BooleanField()
    education = mongo.StringField()
    self_introduction = mongo.StringField()

    meta = {
        "allow_inheritance": True
    }
    # 如果用类继承的话在数据库，都是存在baseperson这个集合里面，只是用_cls字段（基础类名.继承雷鸣：BasePerson.Manager)来区分


class Manager(mongo.Document):
    id = mongo.SequenceField(primary_key=True)
    name = mongo.StringField(required=True)
    phone = mongo.StringField(required=True, max_length=11, unique=True)
    email = mongo.StringField()
    password = mongo.StringField(required=True)
    create_tiem = mongo.DateTimeField(default=datetime.datetime.now, required=True)
    ismaster = mongo.BooleanField()
    education = mongo.StringField()
    self_introduction = mongo.StringField()
    creater = mongo.StringField(required=True)
    is_deleted = mongo.BooleanField(default=0)
    meta = {
        "collection": "manager",
        "index": [{
            'fields': ['_id', 'phone'],
            'unique': True,
        }]
    }


class Sales(mongo.Document):
    id = mongo.SequenceField(primary_key=True)
    name = mongo.StringField(required=True)
    phone = mongo.StringField(required=True, max_length=11, unique=True)
    email = mongo.StringField()
    password = mongo.StringField(required=True)
    create_tiem = mongo.DateTimeField(default=datetime.datetime.now, required=True)
    ismaster = mongo.BooleanField()
    education = mongo.StringField()
    self_introduction = mongo.StringField()
    master_belong = mongo.IntField()
    creater = mongo.ReferenceField(Manager)
    meta = {
        "collection": "sales",
        "index": [{
            'fields': ['_id', 'phone', "master_belong"],
            'unique': True,
        }]
    }


class Byeer(mongo.Document):
    id = mongo.SequenceField(primary_key=True)
    name = mongo.StringField()
    phone = mongo.StringField(required=True, max_length=11, unique=True)
    email = mongo.StringField()
    password = mongo.StringField(required=True)
    create_tiem = mongo.DateTimeField(default=datetime.datetime.now, required=True)
    ismaster = mongo.BooleanField()
    education = mongo.StringField()
    self_introduction = mongo.StringField()
    meta = {
        "collection": "byeer",
        "index": [{
            'fields': ["_id", 'phone'],
            'unique': True,
        }]
    }


class Cars(mongo.Document):
    id = mongo.SequenceField(primary_key=True)  # 让_id自增
    insert_manager = mongo.ReferenceField(Manager)
    name = mongo.StringField(required=True, unique=True)
    min_price = mongo.FloatField(required=True)
    max_price = mongo.FloatField(required=True)
    introduction = mongo.StringField()
    brand = mongo.StringField(required=True)
    saled_number = mongo.IntField()

    meta = {
        "collection": "cars",
        "index": [{
            'fields': ['_id','name', 'min_price', 'max_price', 'saled_number', 'brand'],
            'unique': True,
        }]
    }


class Bills(mongo.Document):
    id = mongo.SequenceField(primary_key=True)
    car_id = mongo.ReferenceField(Cars)
    saler_id = mongo.ReferenceField(Sales)
    price_saled = mongo.FloatField(required=True)
    date_saled = mongo.DateTimeField(default=datetime.datetime.now, required=True)
    byeer_id = mongo.ReferenceField(Byeer)
    creater = mongo.ReferenceField(Manager)

    meta = {
        "collection": "bills",
        "index": [{
            'fields': ['_id', 'car_id', 'saler_id', "byeer"],
            'unique': True,
        }]
    }
