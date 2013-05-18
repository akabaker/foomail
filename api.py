from flask import Flask
from flask.ext import restful
from foomail import run

app = Flask(__name__)
api = restful.Api(app)

class foomail(restful.Resource):
    def get(self):
        return run()

api.add_resource(foomail, '/')

if __name__ == '__main__':
    app.run(debug=True)
