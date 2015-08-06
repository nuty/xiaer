# -*- coding: utf-8 -*-
import datetime
from xiaer import db

ENTRY_CHOICES = {
    1:'Artist',
    2:'Album'
}

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, unique=True)
    username = db.Column(db.String(length=100), nullable=True)
    desc = db.Column(db.String(length=100), nullable=True)
    avatar = db.Column(db.String(length=100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __unicode__(self):
        return self.username

    def __repr__(self):
        return '<User %r>' % self.username
    
    def _json(self):
        rv = {
            'username': self.username,
            'uid': self.uid,
        }
        return rv



class Entry(db.Model):
    __tablename__ = 'entry'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    # user = db.relationship('User',backref=db.backref('entries', lazy='dynamic'))
    name = db.Column(db.String(length=100), nullable=True)
    hits = db.Column(db.Integer, default=0, nullable=True)
    state = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Entry %r>' % self.name
    
    def _json(self):
        rv = {
            'name':self.name,
            'hits':self.hits,
            'state':self.state
        }
        return rv

class Song(db.Model):
    __tablename__ = 'song'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    # user = db.relationship('User',backref=db.backref('entries', lazy='dynamic'))
    name = db.Column(db.String(length=100), default='')
    artist = db.Column(db.String(length=100), default='')
    hits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Song %r>' % self.name
    
    def _json(self):
        rv = {
            'name':self.name,
            'artist':self.artist,
            'hits':self.hits
        }
        return rv