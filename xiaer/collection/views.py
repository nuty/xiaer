# -*- coding: utf-8 -*-
from flask import render_template, jsonify, request
from xiaer.collection.models import User, Entry, Song
from xiaer.collection.tools import truncate_dot
from xiaer.collection.spider import Spider


def loop():
    try:
        uid = int(request.form['uid'])
    except Exception as e:
        return jsonify(ok=False, errors=u"uid")

    try:
        user = User.query.get(uid=self.uid)
    except Exception as e:
        user = None
    if user is not None:
        return jsonify(ok=False, errors=u'用户已存在')
    try:
        spider = Spider(uid=uid)
    except Exception as e:
        return jsonify(ok=False, errors=e)
    try:
        spider.loop()
        return jsonify(ok=True)
    except Exception as e:
        return jsonify(ok=False, errors=e)


def spider():
    user = None
    return render_template('spider.html',
                           user=user)


def collection():
    errors = ''
    user = None
    try:
        uid = int(request.args['uid'])
    except Exception as e:
        errors = u'请输入正确的UID'
    try:
        user = User.query.filter_by(uid=uid)[0]
    except:
        errors = u'你输入的UID不存在'
    if user:
        userid = user.id
    else:
        userid = None
    songs = xiami_items(key='song', page=1, userid=userid)
    album = xiami_items(key='album', page=1, userid=userid)
    artist = xiami_items(key='artist', page=1, userid=userid)
    return render_template('collection.html',
                           user=user,
                           errors=errors,
                           songs=songs,
                           album=album,
                           artist=artist,
                           )


def xiami_items(key, page, userid):
    if not userid:
        return []
    user = User.query.get(userid)
    xiami_list = []
    hits_list = []

    def get_pre_items(key, page):
        if key == 'song':
            items = Song.query.filter_by(
                user_id=userid).paginate(page, 40, False).items
        elif key == 'artist':
            items = Entry.query.filter_by(
                state=1, user_id=userid).paginate(page, 40, False).items
        else:
            items = Entry.query.filter_by(
                state=2, user_id=userid).paginate(page, 40, False).items
        return items
    if page == 1:
        for item in get_pre_items(key, page):
            if item.hits == u'':
                hits = 0
            else:
                hits = int(item.hits)
            data = [truncate_dot(item.name, 20), hits]
            xiami_list.append(data)

    for item in get_pre_items(key, page=2):
        if item.hits == u'':
            hits = 0
        else:
            hits = int(item.hits)
        hits_list.append(hits)
    other = sum(hits_list)
    xiami_list.append(['other', other])

    return xiami_list
