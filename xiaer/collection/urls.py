from xiaer.collection.views import spider, loop, collection
from xiaer.app import app


app.add_url_rule('/', view_func=spider, methods=['GET'])
app.add_url_rule('/collection', view_func=collection, methods=['GET'])
app.add_url_rule('/loop', view_func=loop, methods=['GET','POST'])
