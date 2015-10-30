import datetime
from flask import Blueprint, redirect, render_template, request, url_for, session
from flask_login import current_user
from sqlalchemy import asc
from datab import Session
from models.tests import Tests
from app import app

mod = Blueprint('managetests', __name__)


@mod.route('/manage-tests')
def list_tests():
    if session['logged_in'] and ('Read tests' in session or 'Edit tests' in session):
        q_session = Session()
        tests = q_session.query(
            Tests
        ).order_by(
            asc(Tests.name)
        ).all()
        if tests:
            return render_template('managetests.html', tests=tests)
        else:
            errormsg = "No tests found. Please add a test."
            return render_template('managetests.html', error=errormsg)
    else:
        session['no-access'] = True
        session['tried'] = 'Tests'
        return redirect(url_for('login'))


@mod.route('/create-test', methods=["POST"])
def create_test():
    if session['logged_in'] and ('Read tests' in session or 'Edit tests' in session):
        name = request.form['testname']
        if len(request.form.getlist('testavail')) > 0:
            avail = True
        else:
            avail = False
        price = request.form['testprice']
        category = request.form['testcategory']
        testtype = request.form['testtype']
        code = request.form['testcode']
        desc = request.form['testdesc']
        q_session = Session()
        record = Tests(
            name=name,
            available=avail,
            price=price,
            category=category,
            type=testtype,
            code=code,
            description=desc
        )
        q_session.add(record)
        q_session.commit()
        msg = str(datetime.datetime.now()) + ': Created test with code = ' + code + ' by ' + current_user.email
        app.logger.info(msg)
        return redirect(url_for('.list_tests'))
    else:
        session['no-access'] = True
        session['tried'] = 'Tests'
        return redirect(url_for('login'))


@mod.route('/modify-test', methods=["POST"])
def modify_tests():
    if session['logged_in'] and ('Read tests' in session or 'Edit tests' in session):
        if request.form['submit'] == 'save':
            name = request.form['testname']
            if len(request.form.getlist('testavail')) > 0:
                avail = True
            else:
                avail = False
            price = request.form['testprice']
            category = request.form['testcategory']
            testtype = request.form['testtype']
            code = request.form['testcode']
            desc = request.form['testdesc']
            q_session = Session()
            query = q_session.query(
                Tests
            ).filter(
                Tests.code == code
            ).update(
                {
                    'name': name,
                    'available': avail,
                    'price': price,
                    'category': category,
                    'code': code,
                    'type': testtype,
                    'description': desc
                }
            )
            q_session.commit()
            msg = str(datetime.datetime.now()) + ': Modified test with code = ' + code + ' by ' + current_user.email
            app.logger.info(msg)
        if request.form['submit'] == 'delete':
            code = request.form['testcode']
            q_session = Session()
            query = q_session.query(
                Tests
            ).filter(
                Tests.code == code
            ).delete()
            q_session.commit()
            msg = str(datetime.datetime.now()) + ': Deleted test with code = ' + code + ' by ' + current_user.email
            app.logger.info(msg)
        return redirect(url_for('.list_tests'))
    else:
        session['no-access'] = True
        session['tried'] = 'Tests'
        return redirect(url_for('login'))
