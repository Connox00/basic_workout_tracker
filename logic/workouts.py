def add_workout(mydb, date, name, duration, notes=None):
    cursor = mydb.cursor()
    sql = 'INSERT INTO workouts (date, name, duration_minutes, notes) VALUES (%s, %s, %s, %s)'
    val = (date, name, duration, notes)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    print("Added workout!")

def print_workouts(mydb):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM workouts")
    workouts = cursor.fetchall()
    for workout in workouts:
        formatted_date = workout[1].strftime("%d.%m.%Y")
        print(f'{workout[0]} | {formatted_date} | {workout[2]} | {workout[3]} min')
    cursor.close()

def add_workout_exercise(mydb, workout_id, exercise_id, sets, reps, weight, notes=None):
    cursor = mydb.cursor()
    sql = "INSERT INTO workout_exercises (workout_id, exercise_id, sets, reps, weight, notes) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (workout_id, exercise_id, sets, reps, weight, notes)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    print(f"Added exercise to workout {workout_id}")

def print_exercises_of_workout(mydb, workout_id):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM workout_exercises")
    exercises = cursor.fetchall()
    for exercise in exercises:
        print(exercise)
