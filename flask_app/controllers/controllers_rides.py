from flask_app import app
from flask import render_template, redirect, request, session, flash
# Class imports
from flask_app.models import models_user, models_ride

# Get Routes
# Route for rendering the new_ride HTML page.
@app.route ('/rides/new')
def new_ride():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('new_ride.html')

# Post Routes

