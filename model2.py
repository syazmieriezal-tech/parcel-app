import sqlite3 as sql

connect_db = 'parsel2.db'

# ================= STAFF =================

def insert_staff(staff_id, name, email, password):
    with sql.connect(connect_db) as db:
        qry = 'INSERT INTO staff (staff_id, name, email, password) VALUES (?, ?, ?, ?)'
        db.execute(qry, (staff_id, name, email, password))

def check_staff_login(staff_id, password):
    with sql.connect(connect_db) as db:
        qry = 'SELECT * FROM staff WHERE staff_id=? AND password=?'
        return db.execute(qry, (staff_id, password)).fetchone()

# ================= CUSTOMER =================
# ================= CUSTOMER =================

def list_customer():
    with sql.connect(connect_db) as db:
        return db.execute('SELECT * FROM customers').fetchall()


def insert_customer(name, phone, email, address):
    with sql.connect(connect_db) as db:
        qry = '''
        INSERT INTO customers (name, phone, email, address)
        VALUES (?, ?, ?, ?)
        '''
        db.execute(qry, (name, phone, email, address))


def get_customer_by_id(customer_id):
    with sql.connect(connect_db) as db:
        qry = 'SELECT * FROM customers WHERE customer_id=?'
        return db.execute(qry, (customer_id,)).fetchone()


def list_customer_with_parcel():
    """
    Untuk LIST CUSTOMER + NO TRACK
    """
    with sql.connect(connect_db) as db:
        qry = '''
        SELECT 
            c.customer_id,
            c.name,
            c.phone,
            c.email,
            c.address,
            p.tracking_number
        FROM customers c
        LEFT JOIN parcels p ON c.customer_id = p.customer_id
        ORDER BY c.customer_id
        '''
        return db.execute(qry).fetchall()



# ================= LOCATION =================

def list_storage_location():
    with sql.connect(connect_db) as db:
        return db.execute('SELECT * FROM storage_location').fetchall()

def insert_storage_location(location_name, description):
    with sql.connect(connect_db) as db:
        qry = 'INSERT INTO storage_location (location_name, description) VALUES (?, ?)'
        db.execute(qry, (location_name, description))

def find_location(location_name):
    with sql.connect(connect_db) as db:
        qry = 'SELECT * FROM storage_location WHERE location_name=?'
        return db.execute(qry, (location_name,)).fetchone()

def update_location(location_id, location_name, description):
    with sql.connect(connect_db) as db:
        qry = '''
        UPDATE storage_location
        SET location_name=?, description=?
        WHERE location_id=?
        '''
        db.execute(qry, (location_name, description, location_id))

def delete_location(location_id):
    with sql.connect(connect_db) as db:
        db.execute('DELETE FROM storage_location WHERE location_id=?', (location_id,))

def get_location_by_id(location_id):
    with sql.connect(connect_db) as db:
        qry = 'SELECT * FROM storage_location WHERE location_id=?'
        return db.execute(qry, (location_id,)).fetchone()

# ================= PARCEL =================

def list_parcel():
    with sql.connect(connect_db) as db:
        qry = '''
        SELECT
            p.parcel_id,
            p.tracking_number,
            p.parcel_type,
            p.date_received,
            p.date_collected,
            c.name AS customer_name,
            l.location_name
        FROM parcels p
        LEFT JOIN customers c ON p.customer_id = c.customer_id
        LEFT JOIN storage_location l ON p.location_id = l.location_id
        ORDER BY p.parcel_id
        '''
        return db.execute(qry).fetchall()

def insert_parcel(customer_id, tracking_number, parcel_type, date_received, date_collected, location_id):
    with sql.connect(connect_db) as db:
        qry = '''
        INSERT INTO parcels
        (customer_id, tracking_number, parcel_type, date_received, date_collected, location_id)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        db.execute(qry, (customer_id, tracking_number, parcel_type, date_received, date_collected, location_id))


def find_parcel(tracking_number):
    with sql.connect(connect_db) as db:
        qry = 'SELECT * FROM parcels WHERE tracking_number=?'
        return db.execute(qry, (tracking_number,)).fetchone()

def update_parcel(parcel_id, tracking_number, parcel_type, date_received, date_collected, location_id):
    with sql.connect(connect_db) as db:
        qry = '''
        UPDATE parcels
        SET tracking_number=?, parcel_type=?, date_received=?, date_collected=?, location_id=?
        WHERE parcel_id=?
        '''
        db.execute(qry, (tracking_number, parcel_type, date_received, date_collected, location_id, parcel_id))

def get_parcel_by_id(parcel_id):
    with sql.connect(connect_db) as db:
        qry = 'SELECT * FROM parcels WHERE parcel_id=?'
        return db.execute(qry, (parcel_id,)).fetchone()


def delete_parcel(parcel_id):
    with sql.connect(connect_db) as db:
        db.execute('DELETE FROM parcels WHERE parcel_id=?', (parcel_id,))

def search_parcel(tracking_number):
    with sql.connect(connect_db) as db:
        qry = '''
        SELECT 
            p.parcel_id,
            p.tracking_number,
            p.parcel_type,
            p.date_received,
            p.date_collected,
            c.name,
            l.location_name
        FROM parcels p
        LEFT JOIN customers c ON p.customer_id = c.customer_id
        LEFT JOIN storage_location l ON p.location_id = l.location_id
        WHERE p.tracking_number LIKE ?
        '''
        return db.execute(qry, ('%' + tracking_number + '%',)).fetchall()
