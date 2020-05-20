#!/usr/bin/env python
# coding=utf-8

from . import mongo


class BasePerson(mongo.Document):
    # id_ = mongo.StringField(required=True, max_length=50, unique=True, primary_key=True)
    name = mongo.StringField()
    phone = mongo.StringField(required=True, max_length=11, unique=True)
    email = mongo.StringField()
    password = mongo.StringField(required=True)
    creater = mongo.StringField(required=True)
    create_tiem = mongo.DateTimeField()
    ismaster = mongo.IntField()
    education = mongo.StringField()
    master_belong = mongo.StringField()
    self_introduction = mongo.StringField()

    meta = {
        "allow_inheritance": True
    }


class Manager(BasePerson):
    # BasePerson.meta["collection"] = "manager"
    meta = {
        "collection": "manager",
        "index": [{
            'fields': ['phone'],
            'unique': True,
        }]
    }


class Sales(BasePerson):
    meta = {
        "collection": "sales",
        "index": [{
            'fields': ['phone', "master_belong"],
            'unique': True,
        }]
    }


class Byeer(BasePerson):
    meta = {
        "collection": "byeer",
        "index": [{
            'fields': ['phone'],
            'unique': True,
        }]
    }


class Cars(mongo.Document):
    name = mongo.StringField(required=True, unique=True)
    min_price = mongo.FloatField(required=True)
    max_price = mongo.FloatField(required=True)
    introduction = mongo.StringField()
    brand = mongo.StringField(required=True)
    saled_number = mongo.IntField()

    meta = {
        "collection": "cars",
        "index": [{
            'fields': ['name', 'min_price', 'max_price', 'saled_number', 'brand'],
            'unique': True,
        }]
    }


class Bills(mongo.Document):
    car_id = mongo.StringField(required=True)
    id = mongo.IntField(required=True, unique=True)
    person_saled = mongo.StringField(required=True)
    price_saled = mongo.FloatField(required=True)
    date_saled = mongo.DateTimeField(required=True)
    byeer = mongo.StringField(required=True)

    meta = {
        "collection": "bills",
        "index": [{
            'fields': ['car_id', 'person_saled', "byeer"],
            'unique': True,
        }]
    }
