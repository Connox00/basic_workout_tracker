import tkinter as tk
from tkinter import *
from tkinter import ttk
from db import *
from logic.workouts import *
from logic.exercise import *
from gui.gui_tkinter import *

import unittest

def main():
    mydb = connect_to_db()
    print(initialize_tables(mydb))
    cursor = mydb.cursor()

    while True:
        print('\nExpense Tracker')
        print('1. Add an exercise')
        print('2. List all exercises')
        print('3. Add a workout')
        print('4. Show all workouts')
        print('5. Add an exercise to workout')
        print('6. Show all exercises for a workout')
        print('7. Delete an exercise')
        print('10. Exit')
       
        choice = input('Enter your choice: ')

        if choice == '1':
            name = input('Enter name: ')
            muscle_group = input('Enter muscle_group: ')
            equipment = input('Enter equipment used: ')            
            add_exercise(mydb, name, muscle_group, equipment)

        elif choice == '2':
            print_exercises(mydb)

        elif choice == '3':
            name = input('Enter name: ')
            date = input('Enter date: ')
            duration = input('Enter duration(minutes): ')
            notes = input('Enter notes: ')
            add_workout(mydb, date, name, duration, notes)

        elif choice == '4':
            print_workouts(mydb)

        elif choice == '5':
            workout_id = input('Enter workout id: ')
            exercise_id = input('Enter exercise id: ')
            sets = input('Add number of sets: ')
            reps = input('Add number of reps: ')
            weight = input('Add weight(kg): ')
            notes = input('Add notes: ')
            add_workout_exercise(mydb, workout_id, exercise_id, sets, reps, weight, notes)

        elif choice == '6':
            workout_id = input('Enter workout id: ')
            print_exercises_of_workout(mydb, workout_id)

        elif choice == '10':
            mydb.commit()
            print('Exiting the program.')
            break

    cursor.close()
    mydb.close()

def addition():
    return 2+2

### Verbindung zur Datenbank
mydb = connect_to_db()
print(initialize_tables(mydb))

### GUI starten
start_gui(mydb)

# main()

class SimpleTestCase(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
   
    def tearDown(self):
        """Call after every test case."""
   
    def testA(self):
        """Test case A. note that all test method names must begin with 'test.'"""
        assert addition() == 4, "bar() not calculating values correctly"
   
if __name__ == "__main__":
    unittest.main() # run all tests