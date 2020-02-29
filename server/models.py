# -*- coding: utf-8 -*-
from server import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(10), nullable = False)
    password = db.Column(db.String(30), nullable = False)


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(30), nullable = False)
    status = db.Column(db.Integer, nullable = False, default = 0)
    time = db.Column(db.String(10), nullable = False,
                     default = str(datetime.now().strftime('%Y-%m-%d')))
    ownerId = db.Column(db.Integer, db.ForeignKey('user.id'))

    owner = db.relationship('User', backref = db.backref('tasks'))


class Other(db.Model):
    __tablename__ = 'other'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    advice = db.Column(db.String(200), nullable = True)
    time = db.Column(db.String(10), nullable = False,
                     default = str(datetime.now().strftime('%Y-%m-%d')))
    ownerId = db.Column(db.Integer, nullable = False)


class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    content = db.Column(db.String(100), nullable = False)
    ownerId = db.Column(db.Integer, db.ForeignKey('user.id'))

    owner = db.relationship('User', backref = db.backref('logs'))


class MailConfig(db.Model):
    __tablename__ = 'mailconfig'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    fromName = db.Column(db.String(10), nullable = False)
    toName = db.Column(db.String(10), nullable = False)
    fromEmail = db.Column(db.String(50), nullable = False)
    fromEmailKey = db.Column(db.String(30), nullable = False)
    toEmail = db.Column(db.String(50), nullable = False)
    ownerId = db.Column(db.Integer, db.ForeignKey('user.id'))

    owner = db.relationship('User', backref = db.backref('mailconfigs'))
