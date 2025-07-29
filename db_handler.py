import sqlite3

DB_NAME = "database.db"

# ---------------- Create Main Materials Table ----------------
def create_tables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Table for Materials
    c.execute('''CREATE TABLE IF NOT EXISTS materials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    category TEXT,
                    supplier TEXT,
                    location TEXT,
                    project_area TEXT,
                    quantity INTEGER,
                    unit_price REAL,
                    total_cost REAL,
                    order_date TEXT,
                    delivered INTEGER DEFAULT 0,
                    notes TEXT
                )''')

    conn.commit()
    conn.close()


# ---------------- Insert Functions ----------------
def insert_material(data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT INTO materials 
                (name, category, supplier, location, project_area, quantity, unit_price, total_cost, order_date, delivered, notes) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
    conn.commit()
    conn.close()


def insert_delivery(data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO deliveries (material_id, material_name, location, quantity_delivered, delivery_date, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['material_id'],
        data['material_name'],
        data['location'],
        data['quantity_delivered'],
        data['delivery_date'],
        data['notes'],
        data['created_at']
    ))
    conn.commit()
    conn.close()


# ---------------- Fetch Functions ----------------
def fetch_materials():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM materials")
    rows = c.fetchall()
    conn.close()
    return rows


def get_all_materials():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM materials")
    rows = c.fetchall()
    conn.close()

    materials = []
    for r in rows:
        materials.append({
            'id': r[0],
            'name': r[1],
            'category': r[2],
            'supplier': r[3],
            'location': r[4],
            'project_area': r[5],
            'quantity': r[6],
            'unit_price': r[7],
            'total_cost': r[8],
            'order_date': r[9],
            'delivered': r[10],
            'total_ordered': r[6],  # Using quantity as total_ordered
            'status': "Pending Delivery" if r[10] == 0 else "Partially Delivered" if r[10] < r[6] else "Fully Delivered",
            'notes': r[11] if len(r) > 11 else "",
            'created_at': ""
        })
    return materials


# ---------------- Update Functions ----------------
def update_delivery(material_id, delivered_quantity):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        UPDATE materials 
        SET delivered = delivered + ?
        WHERE id = ?
    """, (delivered_quantity, material_id))
    conn.commit()
    conn.close()


# ---------------- Extra Tables ----------------
def create_extra_tables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Deliveries Table
    c.execute("""
    CREATE TABLE IF NOT EXISTS deliveries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        material_id INTEGER,
        material_name TEXT,
        location TEXT,
        quantity_delivered INTEGER,
        delivery_date TEXT,
        notes TEXT,
        created_at TEXT
    )
    """)

    # Cash Transactions Table
    c.execute("""
    CREATE TABLE IF NOT EXISTS cash_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        amount REAL,
        category TEXT,
        location TEXT,
        payment_method TEXT,
        transaction_date TEXT,
        reference TEXT,
        description TEXT,
        created_at TEXT
    )
    """)

    # Receivables Table
    c.execute("""
    CREATE TABLE IF NOT EXISTS receivables (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT,
        amount REAL,
        due_date TEXT,
        status TEXT,
        notes TEXT,
        created_at TEXT
    )
    """)

    # Payables Table
    c.execute("""
    CREATE TABLE IF NOT EXISTS payables (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendor_name TEXT,
        amount REAL,
        due_date TEXT,
        status TEXT,
        notes TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


# ---------------- Fetch Extra Tables ----------------
def get_all_deliveries():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM deliveries")
    rows = c.fetchall()
    conn.close()
    return rows


def get_all_cash():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM cash_transactions")
    rows = c.fetchall()
    conn.close()
    return rows


def get_all_receivables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM receivables")
    rows = c.fetchall()
    conn.close()
    return rows


def get_all_payables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM payables")
    rows = c.fetchall()
    conn.close()
    return rows


# ---------------- Init Database ----------------
def init_db():
    create_tables()
    create_extra_tables()
