from flask import Flask
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)

class hello(restful.Resource):
    def get(self):
        return {'hhi': 'man'}

api.add_resource(hello, '/')

if __name__ == '__main__':
    app.run(debug=True)
