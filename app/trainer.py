from datetime import datetime
from db import getTrainerByEmail, addTrainerAvailability, getAvailabilityForTrainer, searchMembersByName, getLatestMetric

def setAvailabilityMenu(trainer_id):
    print("\n== Set Availability ==")
    print("Enter time in format: YYYY-MM-DD HH:MM")
    
    start_str = input("Start time: ").strip()
    end_str = input("End time: ").strip()
    
    try:
        start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(end_str, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Invalid date and time format")
        return
    
    if end_time <= start_time:
        print("End time must be after start time")
        return
    
    existing = getAvailabilityForTrainer(trainer_id)
    
    for avail_id, ex_start, ex_end in existing:
        if start_time < ex_end and end_time > ex_start:
            print("WARNING: This time overlaps with existing availability")
            print(f"[{ex_start} - {ex_end}] (ID {avail_id})")
            return
    
    try:
        availability_id = addTrainerAvailability(trainer_id, start_time, end_time)
        print(f"Availability saved with ID: {availability_id}")
    except Exception as e:
        print("Failed to save avalability")
        print("Error:", e)
        
def viewAvailabilityMenu(trainer_id):
    print("\n== My Availability ==")
    slots = getAvailabilityForTrainer(trainer_id)
    
    if not slots:
        print("No availability set")
        return
        
    for avail_id, start_time, end_time in slots:
        print(f"- ID {avail_id}: {start_time} to {end_time}")


def memberLookupMenu():
    print("\n== Member Lookup ==")
    name_query = input("Enter member name: ").strip()
    
    matches = searchMembersByName(name_query)
    if not matches:
        print("No member with that name.")
        return
    
    print("\nMatching member(s): ")
    for member_id, full_name, email, fitness_goal in matches:
        latest = getLatestMetric(member_id)
        goal_display = fitness_goal if fitness_goal else "(no goal set)" 
        
        print(f"-- {full_name} --")
        print(f"Email: {email}")
        print(f"Goal: {goal_display}")
        
        if latest:
            metric_type, metric_value, recorded_at = latest
            print(f"Last Metric: [{recorded_at}] {metric_type}: {metric_value}")
        else:
            print("Last Metric: (none)")
            
    
def trainerMenu():
    print("\n== Trainer Login ==")
    email = input ("Trainer email: ").strip()
    trainer = getTrainerByEmail(email)
    
    if trainer is None:
        print("No trainer found with that email.")
        return
    
    trainer_id, full_name, _ = trainer
    print(f"Welcome, {full_name}!")
    while True:
        print ("\n== Trainer Menu ==")
        print("1. Set availability")
        print("2. View my availability")
        print("3. Lookup Member")
        print("0. Back to main menu")
        
        choice = input("Select: ").strip()
        
        if choice == "1":
            setAvailabilityMenu(trainer_id)
        elif choice == "2":
            viewAvailabilityMenu(trainer_id)
        elif choice == "3":
            memberLookupMenu()
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again.")
