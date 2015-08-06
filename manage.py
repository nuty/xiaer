from flask.ext.script import Server, Manager
from xiaer.app import app, init_db
from xiaer import *
manager = Manager(app)

#manager.add_command("initdb", init_db())

manager.add_command("runserver", Server('0.0.0.0',port=5050))


if __name__ == "__main__":
    manager.run()
