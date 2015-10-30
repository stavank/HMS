import datetime
from flask import Blueprint, redirect, render_template, request, url_for, session
from flask_login import current_user
from datab import Session
from sqlalchemy import asc
from models.roles import Roles
from models.user_roles import UserRoles
from models.patients import Patients
from app import app

mod = Blueprint('managepatients', __name__)


@mod.route('/manage-patients')
def list_patients():
    if session['logged_in'] and ('Read patients' in session or 'Edit patients' in session):
        q_session = Session()
        query = q_session.query(
            Patients
        ).order_by(
            asc(Patients.name)
        ).all()
        if query:
            return render_template('managepatients.html', patients=query)
        else:
            errormsg = 'No patient found. Please add a patient.'
            return render_template('managepatients.html', error=errormsg)
    else:
        session['no-access'] = True
        session['tried'] = 'Patients'
        return redirect(url_for('login'))


@mod.route('/create-patient', methods=['POST'])
def create_patient():
    if session['logged_in'] and ('Read patients' in session or 'Edit patients' in session):
        name = request.form['patientname']
        category = request.form['patientcategory']
        ptype = request.form['patienttype']
        age = request.form['patientage']
        sex = request.form['patientsex']
        contact = request.form['patientcontact']
        email = request.form['patientemail']
        address = request.form['patientaddress']
        reg_no = request.form['patientreg']
        ref_no = request.form['patientref']
        mlc_no = request.form['patientmlc']
        q_session = Session()
        record = Patients(
            name=name,
            category=category,
            type=ptype,
            age=age,
            sex=sex,
            contact=contact,
            email=email,
            address=address,
            reg_no=reg_no,
            ref_no=ref_no,
            mlc_no=mlc_no
        )
        q_session.add(record)
        q_session.commit()
        msg = str(datetime.datetime.now()) + ': Created patient with name = ' + name + ' and ref_no = ' + ref_no + \
            ' by ' + current_user.email
        app.logger.info(msg)
        return redirect(url_for('.list_patients'))
    else:
        session['no-access'] = True
        session['tried'] = 'Patients'
        return redirect(url_for('login'))


@mod.route('/modify-patients', methods=['POST'])
def modify_patients():
    if session['logged_in'] and ('Read patients' in session or 'Edit patients' in session):
        if request.form['submit'] == 'save':
            patid = request.form['patientid']
            name = request.form['patientname']
            category = request.form['patientcategory']
            pattype = request.form['patienttype']
            age = request.form['patientage']
            sex = request.form['patientsex']
            contact = request.form['patientcontact']
            email = request.form['patientemail']
            address = request.form['patientaddress']
            reg_no = request.form['patientreg']
            ref_no = request.form['patientref']
            mlc_no = request.form['patientmlc']
            q_session = Session()
            query = q_session.query(
                Patients
            ).filter(
                Patients.id == patid
            ).update(
                {
                    'name': name,
                    'category': category,
                    'type': pattype,
                    'age': age,
                    'sex': sex,
                    'contact': contact,
                    'email': email,
                    'address': address,
                    'reg_no': reg_no,
                    'ref_no': ref_no,
                    'mlc_no': mlc_no
                }
            )
            q_session.commit()
            msg = str(datetime.datetime.now()) + ': Modified patient with id = ' + patid + ' and name = ' + name + \
                ' by ' + current_user.email
            app.logger.info(msg)
        if request.form['submit'] == 'delete':
            patid = request.form['patientid']
            name = request.form['patientname']
            q_session = Session()
            query = q_session.query(
                Patients
            ).filter(
                Patients.id == patid
            ).delete()
            q_session.commit()
            msg = str(datetime.datetime.now()) + ': Deleted patient with id = ' + patid + ' and name = ' + name + \
                ' by ' + current_user.email
            app.logger.info(msg)

        return redirect(url_for('.list_patients'))
    else:
        session['no-access'] = True
        session['tried'] = 'Patients'
        return redirect(url_for('login'))
