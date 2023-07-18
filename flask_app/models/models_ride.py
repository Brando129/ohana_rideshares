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
        self.pickup_location = data['pickup_location']
        self.date = data['date']
        self.details =  data['details']
        self.created_at = data['created_at']
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
            "pickup_location": ride_dict['pickup_location'],
            "date": ride_dict['date'],
            "details": ride_dict['details'],
            "created_at": ride_dict['created_at'],
            "updated_at": ride_dict['updated_at']
        }
        # Return the object
        return cls(ride_dict)

    # Classmethod to get all the ooen ride requests
    @classmethod
    def get_open_ride_requests(cls):
        # Query for the ride requests (No driver)
        query = """SELECT * FROM rideshares JOIN users on
                users.id = rider_id WHERE driver_id IS NULL;"""
        results = connectToMySQL(db).query_db(query)
        # List for requests
        requests = []
        # Loop over the DB results
        for row in results:
            # Each time make a user dict from the results.
            user_dict = row.copy()
            # Needs a primary id
            user_dict['id'] = row['rider_id']
            # Make a user object
            user = models_user.User(user_dict)
            # Make a ride dict from the results
            ride_dict = row.copy()
            # Add the user object to the dictionary
            ride_dict['rider'] = user
            ride_dict['driver'] = None
            # Make a ride object
            ride = cls(ride_dict)
            # Add ride to the requests list.
            requests.append(ride)
        return requests

    @classmethod
    def get_booked_rides(cls):
        query = """SELECT * FROM rideshares JOIN users as riders
                on riders.id = rider_id JOIN users as drivers on
                drivers.id = driver_id;"""
        results = connectToMySQL(db).query_db(query)
        # List for requests
        booked_rides = []
        # Loop over the DB results
        for row in results:
            # Each time make a user dict from the results.
            rider_dict = row.copy()
            # Needs a primary id
            rider_dict['id'] = row['rider_id']
            # Make a user object
            rider = models_user.User(rider_dict)
            # Make a driver dict, and a driver (user) object
            driver = {
                "id": row['driver_id'],
                "first_name": row['drivers.first_name'],
                "last_name": row['drivers.last_name'],
                "email": row['drivers.email'],
                "password": row['drivers.password'],
                "created_at": row['drivers.created_at'],
                "updated_at": row['drivers.updated_at']
            }
            # Make a ride dict from the results
            ride_dict = row.copy()
            # Add the user object to the dictionary
            ride_dict['rider'] = rider
            ride_dict['driver'] = driver
            # Make a ride object
            ride = cls(ride_dict)
            # Add ride to the requests list.
            booked_rides.append(ride)
        return booked_rides

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

    # Classmethod for assigning a driver to a ride.
    @classmethod
    def assign_driver_to_ride(cls, driver_id, ride_id):
        query = """UPDATE rideshares SET driver_id = %(driver_id)s
                WHERE id = %(ride_id)s;"""
        data = {
            "ride_id": ride_id,
            "driver_id": driver_id
        }
        result = connectToMySQL(db).query_db(query, data)
        return result

    # Classmethod for a driver to cancel their ride.
    @classmethod
    def cancel_driver_of_ride(cls, ride_id):
        query = """UPDATE rideshares SET driver_id = NULL
                WHERE id = %(ride_id)s;"""
        data = {
            'ride_id': ride_id
        }
        results = connectToMySQL(db).query_db(query, data)
        return results

    # Classmethod for updating the ride details.
    @classmethod
    def update_ride(cls, ride_id):
        print("Updating the ride details...")
        query = """UPDATE rideshares SET pickup_location=%(pickup_location)s, details=%(details)s,
                WHERE id = %(ride_id)s;"""
        data = {
            'ride_id': ride_id
        }
        print("Ride details update successful...")
        return connectToMySQL(db).query_db(query, data)


    # Classmethod for deleting a recipe.
    @classmethod
    def destroy_ride(cls, ride_id):
        print("Deleting the ride...")
        query = "DELETE FROM rideshares WHERE id = %(ride_id)s;"
        data = {
            'ride_id': ride_id
        }
        print("Deletion successful...")
        return connectToMySQL(db).query_db(query, data)

    # Staticmethod for validating a created ride.
    @staticmethod
    def validate_ride(ride):
        is_valid = True
        if len(ride['destination']) < 3:
            is_valid = False
            flash("Destination must be at least 3 characters", "ride")
        if len(ride['pickup_location']) < 3:
            is_valid = False
            flash("Pick up location must be at least 3 characters", "ride")
        if ride['date'] == "":
            is_valid = False
            flash("Invalid date", "ride")
        if len(ride['details']) < 1:
            is_valid = False
            flash("Please give some details", "ride")
        return is_valid

    # Staticmethod for validating an update of a created ride.
    @staticmethod
    def validate_update_ride(update_ride):
        is_valid = True
        if len(update_ride['pickup_location']) < 3:
            is_valid = False
            flash("Pick up location must be at least 3 characters", "update_ride")
        if len(update_ride['details']) < 3:
            is_valid = False
            flash("Please give some details about the ride", "update_ride")
        return is_valid
