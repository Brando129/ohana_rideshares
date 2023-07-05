from flask_app import app
from flask import render_template, redirect, request, session, flash
# Class imports
from flask_app.models import models_user, models_ride

# Get Routes
# Route for rendering the new_ride HTML page.
@app.route('/rides/new')
def new_ride():
    print("Rendering new ride route...")
    if 'user_id' not in session:
        return redirect('/')
    return render_template('new_ride.html')

# Route for rendering the edit_ride HTML page.
@app.route('/rides/edit/<ride_id>')
def edit_ride(ride_id):
    if 'user_id' not in session:
        return redirect('/')
    print(f"Rendering edit ride route...{ride_id}")
    return render_template('edit_ride.html')

# Route for rendering the details_page HTML page.
@app.route('/rides/<ride_id>')
def details_ride(ride_id):
    if 'user_id' not in session:
        return redirect('/')
    print(f"Rendering deatils ride route...{ride_id}")
    # Will need to ge the ride to render.
    return redirect('/homepage')

# Route for deleting a ride.
@app.route('/rides/delete/<ride_id>')
def destroy_ride(ride_id):
    if 'user_id' not in session:
        return redirect('/')
    print(f"Deleting a ride route...{ride_id}")
    return redirect('/homepage')

# Route for "I can drive".
@app.route('/rides/assign/<ride_id>')
def assign_driver(ride_id):
    if 'user_id' not in session:
        return redirect('/')
    print(f"Assign driver route...{ride_id}")
    # assign driver to the request.
    return redirect('/homepage')

# Route for the driver to cancel his/her ability to drive.
@app.route('/rides/cancel/<ride_id>')
def cancel_ride(ride_id):
    if 'user_id' not in session:
        return redirect('/')
    print(f"Cancel ride route...{ride_id}")
    return redirect('/homepage')



# Post Routes
# Route for updating a ride.
@app.route('/rides/update', methods=['POST'])
def update_ride():
    if 'user_id' not in session:
        return redirect('/')
    print(f"Update ride route: {request.form}")
    return redirect('/homepage')

# Route for creating a ride.
@app.route('/rides', methods=['POST'])
def create_ride():
    if 'user_id' not in session:
        return redirect('/')
    print(f"Create ride route: {request.form}")
    models_ride.Ride.save_ride(request.form)
    # if valid input.
        # save the new ride.
        # redirect to the homepage.
    return redirect('/rides/new')
