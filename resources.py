from flask_restful import Resource, reqparse
from models import User, Location, Zone
from flask import jsonify


class addUserLocation(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', help = 'This field cannot be blank', required = True, location='headers')
        parser.add_argument('datetime', help = 'This field cannot be blank', required = True, location='headers')
        parser.add_argument('lat', help = 'This field cannot be blank', required = True, location='headers')
        parser.add_argument('lng', help = 'This field cannot be blank', required = True, location='headers')
        data = parser.parse_args()

        if not User.find_by_id(data['id']):
            return {'message': 'User {} doesn\'t exists'.format(data['id'])}

        new_location = Location(
            latitude = data['lat'],
            longitude = data['lng'],
            dateTime = data['datetime'],
            userId = data['id']
        )

        try:
            new_location.save_to_db()
            return {'message': 'Location was saved!'}
        except:
            return {'message': 'Something went wrong {}'.format(data)}, 500

class getUserLocation(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', help = 'This field cannot be blank', required = True, location='headers')
        data = parser.parse_args()

        if not User.find_by_id(data['id']):
            return {'message': 'User {} doesn\'t exists'.format(data['id'])}

        return Location.get_recent_location(data['id'])

class getAllUserZones(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', help = 'This field cannot be blank', required = True, location='headers')
        data = parser.parse_args()

        if not User.find_by_id(data['id']):
            return {'message': 'User {} doesn\'t exists'.format(data['id'])}

        return jsonify(zones=[i.serialize for i in User.find_by_id(data['id']).zones])


class getLocationByDate(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', help = 'This field cannot be blank', required = True, location='headers')
        parser.add_argument('date', help = 'This field cannot be blank', required = True, location='headers')
        data = parser.parse_args()

        if not User.find_by_id(data['id']):
            return {'message': 'User {} doesn\'t exists'.format(data['id'])}

        return jsonify(locations=[i.serialize for i in Location.get_locations_by_date(data['date'], data['id'])])

class setZone(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', help = 'This field cannot be blank', required = True, location='headers')
        parser.add_argument('latitude', help = 'This field cannot be blank', required = True, location='headers')
        parser.add_argument('longitude', help = 'This field cannot be blank', required = True, location='headers')
        parser.add_argument('radius', help = 'This field cannot be blank', required = True, location='headers')
        parser.add_argument('userId', help = 'This field cannot be blank', required = True, location='headers')
        data = parser.parse_args()

        if not User.find_by_id(data['userId']):
            return {'message': 'User {} doesn\'t exists'.format(data['userId'])}

        new_zone = Zone(
            name = data['name'],
            latitude = data['latitude'],
            longitude = data['longitude'],
            radius = data['radius'],
            userId = data['userId'],
        )


        try:
            new_zone.save_to_db()
            return {'message': 'Zone was saved!'}
        except:
            return {'message': 'Something went wrong {}'.format(data)}, 500
