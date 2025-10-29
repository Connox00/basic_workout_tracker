import mysql.connector

def connect_to_db():
    # Verbindung ohne Datenbank, um zu prüfen ob sie existiert
    base_connection = mysql.connector.connect(
        host="127.0.0.1",
        user="lutz",
        password="11"
    )
    cursor = base_connection.cursor()
    cursor.execute("SHOW DATABASES")
    databases = [db[0] for db in cursor.fetchall()]
    cursor.close()
    base_connection.close()

    # Datenbank erstellen, falls sie fehlt
    if 'mydatabase' not in databases:
        base_connection = mysql.connector.connect(
            host="127.0.0.1",
            user="lutz",
            password="11"
        )
        cursor = base_connection.cursor()
        cursor.execute("CREATE DATABASE mydatabase")
        base_connection.commit()
        cursor.close()
        base_connection.close()
        print("Database 'mydatabase' created.")

    # Verbindung zur Ziel-Datenbank herstellen
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="lutz",
        password="11",
        database="mydatabase"
    )
    print("Connected to 'mydatabase'.")
    return mydb

def initialize_tables(mydb):
    cursor = mydb.cursor()
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    if 'workouts' in tables:
        print("Table 'workouts' already exists.")
    else:
        cursor.execute("""CREATE TABLE workouts (
                         id INT PRIMARY KEY AUTO_INCREMENT,
                         date DATE,
                         name VARCHAR(255),
                         duration_minutes INT,
                         notes TEXT)""")
        print("Table 'workouts' created.")

    if 'exercises' in tables:
        print("Table 'exercises' already exists.")
    else:
        cursor.execute("""CREATE TABLE exercises (
                         id INT PRIMARY KEY AUTO_INCREMENT,
                         name VARCHAR(255),
                         muscle_group VARCHAR(255),
                         equipment VARCHAR(255))""")
        print("Table 'exercises' created.")

    if 'workout_exercises' in tables:
        print("Table 'workout_exercises' already exists.")
    else:
        cursor.execute("""CREATE TABLE workout_exercises (
                         id INT PRIMARY KEY AUTO_INCREMENT,         -- Eindeutige ID für jede Zeile
                         workout_id INT NOT NULL,                   -- Verweis auf das zugehörige Workout
                         exercise_id INT NOT NULL,                  -- Verweis auf die Übung
                         sets TINYINT UNSIGNED,                     -- Anzahl der Sätze (kleine Ganzzahl)
                         reps TINYINT UNSIGNED,                     -- Wiederholungen pro Satz
                         weight FLOAT,                              -- Gewicht in kg (Kommazahl erlaubt)
                         notes TEXT,                                -- Optionales Feld für Feedback, z.B. „Grip war schwach“
                         completed BOOLEAN DEFAULT FALSE,           -- Optional: Wurde die Übung abgeschlossen?
                         created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Zeitstempel für die Eintragung
                         FOREIGN KEY (workout_id) REFERENCES workouts(id),
                         FOREIGN KEY (exercise_id) REFERENCES exercises(id))""")
        print("Table 'workout_exercises' created.")

    cursor.close()
    return 'All tables initialized!'
