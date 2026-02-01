import sqlite3 as sql
from model2 import *
from flask import Flask, render_template, request, redirect, session, flash
from model2 import search_parcel


app = Flask(__name__)
app.secret_key = "tailor123"

# ================= LOGIN =================

@app.route('/')
def home():
    return redirect('/login_staff')

@app.route('/login_staff')
def login_staff():
    return render_template('login_staff.html')


@app.route('/do_login_staff', methods=['POST'])
def do_login_staff():
    staff_id = request.form['staff_id']
    password = request.form['password']

    user = check_staff_login(staff_id, password)
    if user:
        session['role'] = 'staff'
        session['user_id'] = staff_id
        return redirect('/staff_home')
    else:
        flash('Login gagal')
        return redirect('/login_staff')


@app.route('/register_staff')
def register_staff():
    return render_template('register_staff.html')


@app.route('/register_staff_save', methods=['POST'])
def register_staff_save():
    staff_id = request.form['staff_id']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    try:
        insert_staff(staff_id, username, email, password)
        flash('Staff berjaya didaftarkan')
        return redirect('/login_staff')
    except:
        flash('Staff ID sudah wujud')
        return redirect('/register_staff')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
# ================= DASHBOARD =================

@app.route('/staff_home')
def staff_home():
    if session.get('role') != 'staff':
        return redirect('/login_staff')
    return render_template('home_staff.html')

# ================= PARCEL =================

@app.route('/list_parcel')
def list_parcel_route():
    if session.get('role') != 'staff':
        return redirect('/')
    rows = list_parcel()
    return render_template('list_parcel.html', rows=rows)

@app.route('/new_parcel')
def new_parcel():
    customers = list_customer()
    locations = list_storage_location()
    return render_template('form_parcel.html', status='0', customers=customers, locations=locations)

@app.route('/save_parcel', methods=['POST'])
def save_parcel():
    if session.get('role') != 'staff':
        return redirect('/')

    customer_id = request.form['customer_id']
    tracking_number = request.form['tracking_number']
    parcel_type = request.form['parcel_type']
    date_received = request.form['date_received']
    date_collected = request.form.get('date_collected')
    location_id = request.form['location_id']

    if request.form['status'] == '0':
        insert_parcel(customer_id, tracking_number, parcel_type, date_received, date_collected, location_id)
        flash("Parcel berjaya ditambah")
    else:
        parcel_id = request.form['parcel_id']
        update_parcel(parcel_id, tracking_number, parcel_type, date_received, date_collected, location_id)
        flash("Parcel berjaya dikemaskini")

    return redirect('/list_parcel')

@app.route('/edit_parcel/<int:parcel_id>')
def edit_parcel(parcel_id):
    if session.get('role') != 'staff':
        return redirect('/login_staff')

    parcel = get_parcel_by_id(parcel_id)
    customers = list_customer()
    locations = list_storage_location()

    return render_template(
        'form_parcel.html',
        status='1',
        parcel=parcel,
        customers=customers,
        locations=locations
    )


@app.route('/delete_parcel/<int:parcel_id>')
def delete_parcel_route(parcel_id):
    delete_parcel(parcel_id)
    flash("Parcel dipadam")
    return redirect('/list_parcel')

@app.route('/search_parcel', methods=['GET'])
def search_parcel_route():
    if session.get('role') != 'staff':
        return redirect('/login_staff')

    keyword = request.args.get('keyword')
    parcels = []

    if keyword:
        parcels = search_parcel(keyword)

    return render_template(
        'search_parcel.html',
        parcels=parcels,
        keyword=keyword
    )



# ================= LOCATION =================

@app.route('/list_location')
def list_location_route():
    if session.get('role') != 'staff':
        return redirect('/login_staff')

    rows = list_storage_location()
    return render_template('list_location.html', rows=rows)


@app.route('/new_location')
def new_location():
    if session.get('role') != 'staff':
        return redirect('/login_staff')

    return render_template('form_location.html', status='0')


@app.route('/edit_location/<int:location_id>')
def edit_location(location_id):
    if session.get('role') != 'staff':
        return redirect('/login_staff')

    location = get_location_by_id(location_id)
    return render_template(
        'form_location.html',
        status='1',
        location=location
    )


@app.route('/save_location', methods=['POST'])
def save_location():
    if session.get('role') != 'staff':
        return redirect('/login_staff')

    location_name = request.form['location_name']
    description = request.form['description']

    if request.form['status'] == '0':
        insert_storage_location(location_name, description)
        flash('Location berjaya ditambah')
    else:
        location_id = request.form['location_id']
        update_location(location_id, location_name, description)
        flash('Location berjaya dikemaskini')

    return redirect('/list_location')


@app.route('/delete_location/<int:location_id>')
def delete_location_route(location_id):
    if session.get('role') != 'staff':
        return redirect('/login_staff')

    delete_location(location_id)
    flash('Location berjaya dipadam')
    return redirect('/list_location')

# ================= CUSTOMER =================

@app.route('/list_customer')
def list_customer_route():
    if session.get('role') != 'staff':
        return redirect('/login_staff')

    rows = list_customer_with_parcel()
    return render_template('list_customer.html', rows=rows)


@app.route('/new_customer')
def new_customer():
    if session.get('role') != 'staff':
        return redirect('/login_staff')

    return render_template('form_customer.html')


@app.route('/save_customer', methods=['POST'])
def save_customer():
    if session.get('role') != 'staff':
        return redirect('/login_staff')

    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    address = request.form['address']

    insert_customer(name, phone, email, address)
    flash('Customer berjaya ditambah')

    return redirect('/list_customer')




if __name__ == "__main__":
    import os
    app.secret_key = os.environ.get("SECRET_KEY", "dev")

    app.run()
