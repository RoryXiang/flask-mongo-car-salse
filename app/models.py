#!/usr/bin/env python
# coding=utf-8

from . import mongo


class BasePerson(mongo.Document):
    id = mongo.SequenceField(primary_key=True)
    name = mongo.StringField()
    phone = mongo.StringField(required=True, max_length=11, unique=True)
    email = mongo.StringField()
    password = mongo.StringField(required=True)
    create_tiem = mongo.DateTimeField()
    ismaster = mongo.BooleanField()
    education = mongo.StringField()
    self_introduction = mongo.StringField()

    meta = {
        "allow_inheritance": True
    }


class Manager(BasePerson):
    meta = {
        "collection": "manager",
        "index": [{
            'fields': ['_id', 'phone'],
            'unique': True,
        }]
    }


class Sales(BasePerson):
    master_belong = mongo.IntField(required=True)
    creater = mongo.ReferenceField(Manager)
    meta = {
        "collection": "sales",
        "index": [{
            'fields': ['_id', 'phone', "master_belong"],
            'unique': True,
        }]
    }


class Byeer(BasePerson):
    meta = {
        "collection": "byeer",
        "index": [{
            'fields': ["_id", 'phone'],
            'unique': True,
        }]
    }


class Cars(mongo.Document):
    id = mongo.SequenceField(primary_key=True)  # 让_id自增
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
    date_saled = mongo.DateTimeField(required=True)
    byeer = mongo.ReferenceField(Byeer)

    meta = {
        "collection": "bills",
        "index": [{
            'fields': ['_id', 'car_id', 'saler_id', "byeer"],
            'unique': True,
        }]
    }
