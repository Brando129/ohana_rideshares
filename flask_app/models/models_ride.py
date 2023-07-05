from flask_app.config.mysqlconnection import connectToMySQL
# Flash messages import
from flask import flash

# Database name
db = "ohana_rideshares_schema"

# Class name
class Ride:
    def __init__(self, data):
        self.id = data['id']
        self.destination = data['destination']
        self.date = data['date']
        self.details =  data['details']
        self.created_at = data['creadted_at']
        self.updated_at = data['updated_at']
        self.rider = data['rider']
        self.driver = data['driver']

    @classmethod
    def get_one_ride(cls, ride_id):
        pass

    @classmethod
    def get_all_rides(cls):
        pass

    # Classmethod for saving a new ride.
    @classmethod
    def save_ride(cls, data):
        print("Saving new ride...")
        query = """INSERT INTO rideshares
        (rider_id, destination, pickup_location, date, details)
        VALUES (%(rider_id)s, %(destination)s, %(pickup_location)s, %(date)s, %(details)s);"""
        result = connectToMySQL(db).query_db(query, data)
        print("Ride succesfully saved...")
        return result

    @classmethod
    def update_ride(cls, data):
        pass

    @classmethod
    def delete(cls, ride_id):
        pass