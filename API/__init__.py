from flask import Flask
from flask_restful import Resource, reqparse, Api
# import jsonify

# Creating an instance of Flask
app = Flask(__name__)
# Create the API
api = Api(app)


@app.route("/")
def index():
    """Present some documentation"""

    # Open the README file
    return 'sdklfh jkdhfjk'


class Coefficients(Resource):
    def get(self):
        # Do something
        return {"message": "I did it"}, 200

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


class TeamCoefficient(Resource):
    def get(self, hometeam, awayteam):
        # if not in list of available teams
            # return {"Message": "was not found"}, 404
        return {"message": f"I did it. Return res of {hometeam} vs {awayteam}"}, 200


api.add_resource(TeamCoefficient,
                 '/coeffs/<string:hometeam>/<string:awayteam>')

if __name__ == '__main__':
    app.run(debug=True)
