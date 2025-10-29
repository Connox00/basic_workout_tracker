import tkinter as tk
from tkinter import *
from tkinter import ttk
from db import *
from logic.workouts import *
from logic.exercise import *

frames = {}    

def start_gui(mydb):
    ### GUI-Fenster
    root = Tk()
    root.title("Workout Tracker")
    # root.geometry("640x480")
    # root.resizable(False, False)
    # Root-Fenster dehnbar machen
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    ### Hauptmenü-Buttons
    menu_frame = Frame(root)
    frames["menu"] = menu_frame
    frames["menu"].grid_columnconfigure(0, weight=1)
    frames["menu"].grid_rowconfigure([0,1,2,3,4,5,6], weight=1)
    frames["menu"].grid(row=0, column=0, sticky="nsew")

    button_frame = Frame(frames["menu"])
    frames["buttons"] = button_frame
    frames["buttons"].grid(row=2, column=0)
    frames["buttons"].grid_columnconfigure(0, weight=1)
    frames["buttons"].grid_columnconfigure(1, weight=1)

    add_workout_frame = Frame(root)
    frames["add_workout"] = add_workout_frame
    frames["add_workout"].grid(row=0, column=0, sticky="nsew")
    ### Logik für das Fenster Workout-Eintrag

    # Eingabefelder
    Label(frames["add_workout"], text="Datum (YYYY-MM-DD)").grid(row=0)
    Label(frames["add_workout"], text="Name").grid(row=1)
    Label(frames["add_workout"], text="Dauer (Minuten)").grid(row=2)
    Label(frames["add_workout"], text="Notiz").grid(row=3)

    e_date = Entry(frames["add_workout"])
    e_name = Entry(frames["add_workout"])
    e_duration = Entry(frames["add_workout"])
    e_notes = Entry(frames["add_workout"])

    e_date.grid(row=0, column=1)
    e_name.grid(row=1, column=1)
    e_duration.grid(row=2, column=1)
    e_notes.grid(row=3, column=1)

    # Button zum Speichern
    Button(frames["add_workout"], text="Workout speichern", command=lambda: add_workout(mydb, e_date.get(), e_name.get(), int(e_duration.get()), e_notes.get())).grid(row=4, column=1)
    Button(frames["add_workout"], text="Zurück", command=frames["menu"].tkraise).grid(row=4, column=0)

    add_exercise_frame = Frame(root)
    frames["add_exercise"] = add_exercise_frame
    frames["add_exercise"].grid(row=0, column=0, sticky="nsew")

    ### Logik fuer das Fenster 'Uebung eintragen'

    # Eingabefelder
    Label(frames["add_exercise"], text="Name").grid(row=0)
    Label(frames["add_exercise"], text="Muskelgruppe").grid(row=1)
    Label(frames["add_exercise"], text="Equipment").grid(row=2)

    exercise_name = Entry(frames["add_exercise"])
    exercise_muscles = Entry(frames["add_exercise"])
    exercise_equipment = Entry(frames["add_exercise"])

    exercise_name.grid(row=0, column=1)
    exercise_muscles.grid(row=1, column=1)
    exercise_equipment.grid(row=2, column=1)

    # Button zum Speichern und zurueck
    Button(frames["add_exercise"], text="Uebung speichern", command=lambda: submit_exercise(name=exercise_name, muscles=exercise_muscles, equipment=exercise_equipment, db=mydb)).grid(row=3, column=1)
    Button(frames["add_exercise"], text="Zurück", command=frames["menu"].tkraise).grid(row=3, column=0)    

    add_exercise_for_workout_frame = Frame(root)
    add_exercise_for_workout_frame.grid(row=0, column=0, sticky="nsew")

    show_workouts_frame = Frame(root)
    frames["workouts"] = show_workouts_frame
    frames["workouts"].grid(row=0, column=0, sticky="nsew")

    ### Logik fuer das Fenster 'Workouts anzeigen'
    workout_list = Text(frames["workouts"], width=50, height=10)
    workout_list.grid()
    Button(frames["workouts"], text="Zurück", command=frames["menu"].tkraise).grid()

    show_exercise_for_workout_frame = Frame(root)
    frames["exercises_for_workout"] = show_exercise_for_workout_frame
    frames["exercises_for_workout"].grid(row=0, column=0, sticky="nsew")

    ### Logik fuer das Fenster 'Exercises anzeigen'

    top_frame = Frame(frames["exercises_for_workout"])
    top_frame.pack(side='top')
    bottom_frame = Frame(frames["exercises_for_workout"])
    bottom_frame.pack(side='bottom', fill='both')

    bottom_left_frame = Frame(bottom_frame)
    bottom_left_frame.pack(side="left", fill='both', expand=True)
    bottom_right_frame = Frame(bottom_frame)
    bottom_right_frame.pack(side="right", fill='both', expand=True)

    exercise_for_workout_list = Text(top_frame, width=50, height=10)
    exercise_for_workout_list.pack(side='top')

    all_workouts = load_workouts_as_list(mydb)
    workouts = all_workouts
    display_list = [str(w[1]) + ' ' + str(w[2]) for w in workouts]

    entry = tk.Entry(bottom_left_frame)
    entry.pack(side="top", anchor='center')
    entry.bind("<KeyRelease>", filter_workout_list_box)

    listbox = tk.Listbox(bottom_left_frame, height=5)
    listbox.bind("<ButtonRelease-1>", lambda event: load_exercises_for_workout(workouts, exercise_for_workout_list, listbox, mydb))
    for val in display_list:
            listbox.insert(tk.END, val)
    listbox.pack(side="top", anchor='center')

    Button(bottom_right_frame, text="Zurück", command=frames["menu"].tkraise).pack(anchor='center', pady=45)


    show_exercise_frame = Frame(root)
    frames["exercises"] = show_exercise_frame
    frames["exercises"].grid(row=0, column=0, sticky="nsew")

    ### Logik fuer das Fenster 'Exercises anzeigen'
    exercise_list = Text(frames["exercises"], width=50, height=10)
    exercise_list.pack()

    Button(frames["exercises"], text="Zurück", command=frames["menu"].tkraise).pack()

    # Menü-Buttons
    Button(menu_frame, text="Workout eintragen", command=frames["add_workout"].tkraise).grid(row=0, column=0, pady=5)
    Button(menu_frame, text="Übung hinzufügen", command=frames["add_exercise"].tkraise).grid(row=1, column=0, pady=5)
    Button(button_frame, text="Workouts", command=lambda: (frames["workouts"].tkraise(), load_workouts_as_textlist(workout_list, mydb))).grid(row=0, column=0, pady=5)
    Button(button_frame, text="Übungen", command=lambda: (frames["exercises"].tkraise(), load_exercises(exercise_list, mydb))).grid(row=0, column=1, pady=5)
    Button(menu_frame, text="Übungen für Workout eintragen", command=frames["menu"].tkraise).grid(row=4, column=0, pady=5)
    Button(menu_frame, text="Übungen für Workout anzeigen", command=frames['exercises_for_workout'].tkraise).grid(row=5, column=0, pady=5)
    Button(menu_frame, text="Beenden", command=root.quit).grid(row=6, column=0, pady=5)

    frames["menu"].tkraise()
    root.mainloop()

def submit_exercise(name, muscles, equipment, db):
    name = name.get()
    muscles = muscles.get()
    equipment = equipment.get()
    add_exercise(db, name, muscles, equipment)
    print('Uebung gespeichert!')

def submit_exercise_for_workout(e_workout_id, e_exercise_id, e_sets, e_reps, e_weight, e_notes, mydb):
    workout_id = e_workout_id.get()
    exercise_id = e_exercise_id.get()
    sets = e_sets.get()
    reps = e_reps.get()
    weight = e_weight.get()
    notes = e_notes.get()
    add_workout_exercise(mydb, workout_id, exercise_id, sets, reps, weight, notes)
    print(f"Uebung fuer workout {workout_id} gespeichert!")

def load_workouts_as_textlist(workout_list, mydb):
        workout_list.delete("1.0", END)  # vorherige Inhalte löschen
        cursor = mydb.cursor()
        cursor.execute("SELECT id, date, name, duration_minutes, notes FROM workouts ORDER BY date DESC")
        rows = cursor.fetchall()
        for row in rows:
            date_str = row[1].strftime("%d.%m.%Y")
            workout_list.insert(END, f"{date_str} – {row[2]} ({row[3]} min) | ID: {row[0]}\n")
            if row[4]:
                workout_list.insert(END, f"  Notiz: {row[4]}\n")
            workout_list.insert(END, "\n")
        cursor.close()

def load_exercises(exercise_list, mydb):
    exercise_list.delete("1.0", END)  # vorherige Inhalte löschen
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM exercises ORDER BY id ASC")
    rows = cursor.fetchall()
    for row in rows:
        exercise_list.insert(END, f"{row[1]}: \n  musclegroup: {row[2]}\n  equipment: {row[3]}\n\n")
    cursor.close()

def load_exercises_for_workout(workouts, exercise_for_workout_list, listbox, mydb):
        exercise_for_workout_list.delete("1.0", END)  # vorherige Inhalte löschen
        cursor = mydb.cursor()
        
        cursor.execute("SELECT * FROM workout_exercises WHERE workout_id = %s", [workouts[listbox.curselection()[0]][0]])

        rows = cursor.fetchall()
        for row in rows:
            # exercise_for_workout_list.insert(END, f"{row}\n")

            date_str = row[8].strftime("%d.%m.%Y – %H:%M")
            exercise_for_workout_list.insert(END, f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[7]} | {date_str}\n")
            if row[6]:
                exercise_for_workout_list.insert(END, f"  Notiz: {row[6]}\n")
            exercise_for_workout_list.insert(END, "\n")
        cursor.close()

def load_workouts_as_list(mydb):
        cursor = mydb.cursor()
        cursor.execute("SELECT id, date, name, duration_minutes, notes FROM workouts ORDER BY date DESC")
        rows = cursor.fetchall()
        cursor.close()
        return rows

def filter_workout_list_box(event):
        global workouts
        workouts = all_workouts
        listbox.delete(0, tk.END)        
        input = entry.get().lower()
        filtered_list = {index: display_string for index, display_string in enumerate(display_list) if input in display_string.lower()}
        filtered_workouts = [workout for index, workout in enumerate(workouts) if index in filtered_list]
        workouts = filtered_workouts
        for val in list(filtered_list.values()):
            listbox.insert(tk.END, val)
        listbox.pack()    

def add_exercise_for_workout_gui(add_exercise_for_workout_frame):
    ### Logik fuer das Fenster 'Uebung fuer workout eintragen'

    # Eingabefelder : workout_id, exercise_id, sets, reps, weight, notes
    Label(add_exercise_for_workout_frame, text="workout_id").grid(row=0)
    Label(add_exercise_for_workout_frame, text="exercise_id").grid(row=1)
    Label(add_exercise_for_workout_frame, text="sets").grid(row=2)
    Label(add_exercise_for_workout_frame, text="reps").grid(row=3)
    Label(add_exercise_for_workout_frame, text="weight").grid(row=4)
    Label(add_exercise_for_workout_frame, text="notes").grid(row=5)
    Label(add_exercise_for_workout_frame, text="workout_id").grid(row=6)

    e_workout_id = tk.Entry(add_exercise_for_workout_frame)
    e_exercise_id = Entry(add_exercise_for_workout_frame)
    e_sets = Entry(add_exercise_for_workout_frame)
    e_reps = Entry(add_exercise_for_workout_frame)
    e_weight = Entry(add_exercise_for_workout_frame)
    e_notes = Entry(add_exercise_for_workout_frame)

    e_workout_id.grid(row=0, column=1)
    e_exercise_id.grid(row=1, column=1)
    e_sets.grid(row=2, column=1)
    e_reps.grid(row=3, column=1)
    e_weight.grid(row=4, column=1)
    e_notes.grid(row=5, column=1)

    # Button zum Speichern und zurueck
    Button(add_exercise_for_workout_frame, text="Uebung speichern", command=submit_exercise_for_workout).grid(row=7, column=1)
    Button(add_exercise_for_workout_frame, text="Zurück", command=frames["menu"].tkraise).grid(row=7, column=0)   