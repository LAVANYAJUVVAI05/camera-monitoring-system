import sqlite3

DB_NAME = "camera.db"

def get_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    # Cameras table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cameras(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        place_name TEXT,
        camera_name TEXT,
        camera_mode TEXT
    )
    """)

    # Default admin login
    cur.execute(
        "INSERT OR IGNORE INTO users (id, username, password) VALUES (1,'admin','admin123')"
    )

    # Insert camera data if table empty
    cur.execute("SELECT COUNT(*) FROM cameras")
    count = cur.fetchone()[0]

    if count == 0:
        camera_data = [
            ("Vuyyur", "NVR", "online"),
            ("Kanuru", "SIM", "offline"),
            ("Gannavaram", "MATRIX", "online"),
            ("Kankipadu", "NVR", "online"),
            ("Ibrahimpatnam", "SIM", "offline"),
            ("Penamaluru", "MATRIX", "online"),
            ("Pamarru", "NVR", "offline"),
            ("Veeravalli", "SIM", "online"),
            ("Bapulapadu", "MATRIX", "online"),
            ("Agiripalli", "NVR", "online"),
            ("Musunuru", "SIM", "offline"),
            ("Chandarlapadu", "MATRIX", "online"),
            ("Tiruvuru", "NVR", "offline"),
            ("A.Konduru", "SIM", "online"),
            ("Reddigudem", "MATRIX", "offline"),
            ("Nandigama", "NVR", "online"),
            ("Jaggaiahpet", "SIM", "online"),
            ("Mylavaram", "MATRIX", "offline"),
            ("Unguturu", "NVR", "online")
        ]

        cur.executemany("""
        INSERT INTO cameras (place_name, camera_name, camera_mode)
        VALUES (?, ?, ?)
        """, camera_data)

    conn.commit()
    conn.close()