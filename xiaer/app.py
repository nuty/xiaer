import sys
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import Configuration

app = Flask("xiaer")
app.config.from_object(Configuration)
app.template_folder = Configuration.APP_ROOT + "/templates"
app.static_folder = Configuration.APP_ROOT + "/static"

app.debug = True

app.config['SECRET_KEY'] = Configuration.SECRET_KEY

db = SQLAlchemy(app)

 
# def init_db(db):
#     """Add a save() function to db.Model"""
#     def save(model):
#         db.session.add(model)
#         db.session.commit()
#         db.Model.save = save
     
     
# db = SQLAlchemy()
# init_db(db)

def init_db():
    from collection import models
    left = db.engine.table_names()
    db.metadata.create_all(bind=db.engine)
    right = db.engine.table_names()
    if not left:
        res = right
    else:
        res = list(set(right).difference(set(left)))
    for r in res:
        sys.stdout.write('table %s created'% r)
        print ""

