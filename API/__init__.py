from flask import Flask
from flask_restful import Resource, reqparse
# import jsonify

# Creating an instance of Flask
app = Flask(__name__)


class Coefficients(Resource):
    def get(self):
        # Do something
        return {"message": "I did it"}

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('identifier', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('device_type', required=True)
        parser.add_argument('controller_gateway', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        print(args)
        return {'message': 'Device registered', 'data': args}, 201

@app.route('/')
def hello():
    return jsonify({'res': 'JJLHFKJHJ JFKDSKJ'})


if __name__ == '__main__':
    app.run(debug=True)
