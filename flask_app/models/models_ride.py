from flask_app.config.mysqlconnection import connectToMySQL
# Flash messages import
from flask import flash
from flask_app.models import models_user

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
    def get_one_ride_by_id(cls, ride_id):
        # Query for the ride.
        query = """SELECT * FROM rideshares WHERE
                id = %(ride_id)s"""
        data = {
            "ride_id": ride_id
        }
        ride_list = connectToMySQL(db).query_db(query, data)
        ride_dict = ride_list[0]
        # Make an object for the rider,
        rider  = models_user.User.get_by_id({"id": ride_dict['rider_id']})
        # and the driver (if the driver exists)
        driver = None
        if ride_dict['driver_id'] != None:
            driver = models_user.User.get_by_id({"id": ride_dict['driver_id']})
        # Associate the rider (&driver)
        # with a ride object (need dictionary first)
        ride_dict = {
            "id": ride_dict['id'],
            "rider": rider,
            "driver": driver,
            "destination": ride_dict['destination'],
            "date": ride_dict['date'],
            "details": ride_dict['details'],
            "created_at": ride_dict['created_at'],
            "updated_at": ride_dict['updated_at']
        }
        # Return the object
        return cls(ride_dict)

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