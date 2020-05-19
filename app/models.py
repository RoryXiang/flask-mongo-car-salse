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
        "allow_inheritance": True,
        "index": [{
            'fields': ['phone'],
            'unique': True,
            }]
    } 


class Manager(BasePerson):
    meta = {"collection":"manager"}


class Sales(BasePerson):
    meta = {"collection": "sales"}


class Byeer(BasePerson):
    meta = {"collection": "byeer"}


class Cars(mongo.Document):
    name = mongo.StringField()
    min_price = mongo.StringField()
    max_price = mongo.StringField()
    introdution = mongo.StringField()
    saled_bumber = mongo.StringField()
    
    meta = {"collection": "cars"}


class Bills(mongo.Document):
    car_id = mongo.StringField()
    person_saled = mongo.StringField()
    price_saled = mongo.StringField()
    date_saled = mongo.StringField()
    byeer = mongo.StringField()
    
    meta = {"collection": "cars"}

