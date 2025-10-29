def add_exercise(mydb, name, muscle_group, equipment):
    cursor = mydb.cursor()
    sql = "INSERT INTO exercises (name, muscle_group, equipment) VALUES (%s, %s, %s)"
    val = (name, muscle_group, equipment)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    print("Added exercise!")

def print_exercises(mydb):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM exercises")
    exercises = cursor.fetchall()
    for exercise in exercises:
        print(exercise)
    cursor.close()