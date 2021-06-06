from flask import Blueprint, json, render_template, request, flash, jsonify,redirect, url_for
from flask.wrappers import JSONMixin
from flask_login import login_required, current_user
from . import db
from .models import Appointment, User, Pet


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    return render_template("home.html", user=current_user)

@views.route('/delete-appointment', methods=['POST'])
def delete_appointment():
    appt = json.loads(request.data)
    apptID = appt['apptID']

    appt = Appointment.query.get(apptID)
    db.session.delete(appt)
    db.session.commit()

    return jsonify({})

