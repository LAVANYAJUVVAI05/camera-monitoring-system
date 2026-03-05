import sqlite3


def get_db():
    conn = sqlite3.connect("camera.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cameras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        place_name TEXT,
        camera_name TEXT,
        camera_mode TEXT
    )
    """)

    cur.execute("INSERT OR IGNORE INTO users VALUES (1,'admin','admin123')")

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