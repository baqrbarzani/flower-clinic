def initialize_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diseases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease_name TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    # Proceed with the rest of your application
