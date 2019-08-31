from flask import Flask, request
import urllib, os
import random 
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import json
from urllib.parse import urlparse

db_connect = create_engine('sqlite:///filedownload.sqlite')
app = Flask(__name__)
api = Api(app)

class Download(Resource):
    def post(self,url):
        if not urlparse(url).scheme:
            url = 'http://' + url
        site = urllib.request.urlopen(url)
        size = site.headers['content-length']
        uniqueId = int(random.random()* 10000000)
        conn = db_connect.connect()
        statement = "insert into file(UniqueId, Url, Size) values({},'{}',{})"
        query = statement.format(uniqueId,url,size)
        conn.execute(query)
        return uniqueId

class Status(Resource):
    def get(self,id):
        conn = db_connect.connect()
        query = conn.execute("select id, uniqueid, url, size from file where uniqueid={};".format(id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return  json.dumps(result)

api.add_resource(Download, '/download/<url>')
api.add_resource(Status, '/status/<id>')


if __name__ == '__main__':
     app.run(port='5002')