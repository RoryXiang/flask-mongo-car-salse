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
    create_tiem = mongo.Document()
    ismaster = mongo.StringField()
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
    name = mongo.StringField(required=True)
    min_price = mongo.StringField(required=True)
    max_price = mongo.StringField(required=True)
    introdution = mongo.StringField()
    saled_bumber = mongo.StringField()

    meta = {
        "collection": "cars",
        "index": [{
            'fields': ['name'],
            'unique': True,
        }]
    }


class Bills(mongo.Document):
    car_id = mongo.StringField(required=True)
    id = mongo.StringField(required=True, unique=True)
    person_saled = mongo.StringField(required=True)
    price_saled = mongo.StringField(required=True)
    date_saled = mongo.StringField(required=True)
    byeer = mongo.StringField(required=True)

    meta = {
        "collection": "bills",
        "index": [{
            'fields': ['car_id', 'person_saled', "byeer"],
            'unique': True,
        }]
    }
