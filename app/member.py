from datetime import datetime
from db import addMember, getAllMembers, getMemberByEmail, addHealthMetric, getMetricsForMember, updateMemberProfile, getAllClasses, countRegistrations, registerForClass

def registerMember():
    print("\n== Member Registration ==")
    full_name = input("Full name: ").strip()
    email = input("Email: ").strip()
    dob_str = input("Date of Birth (YYYY-MM-DD): ").strip()
    gender = input("Gender: ").strip()
    phone = input("Phone: ").strip()
    
    dob = None
    if dob_str:
        try:
            datetime.strptime(dob_str, "%Y-%m-%d")
            dob = dob_str
        except ValueError:
            print("Invalid Date")
    
    try:
        new_id = addMember(full_name, email, dob, gender, phone)
        print(f"Member registered with ID: {new_id}")
    except Exception as e:
        print("Failed to register member (email may exists already)")
        print("Error:", e)


def listMembers():
    print("\n== All Members ==")
    rows = getAllMembers()
    if not rows:
        print("No members found.")
        return
    
    for row in rows:
        member_id, full_name, email = row
        print(f"{member_id}: {full_name} <{email}>")
        

def findMemberByEmail():
    print("\n== Find Member by Email ==")
    email = input("Email: ").strip()
    row = getMemberByEmail(email)
    
    if row is None:
        print("No member found with that email.")
    else:
        member_id, full_name, email, *_ = row
        print(f"Found: {member_id}: {full_name} <{email}>")


def addHealthMetricMenu():
    print("\n== Add Health Metric ==")
    email = input("Member email: ").strip()
    row = getMemberByEmail(email)
    
    if row is None:
        print("No member found with that email.")
        return
    
    member_id, full_name, email, *_ = row
    
    metric_type = input("Metric type (eg. weight, heart rate): ").strip()
    value_str = input("Metric value (eg. 72.5): ").strip()
    
    try:
        value = float(value_str)
    except ValueError:
        print("Invalid number for metric value")
        return
    
    try:
        metric_id = addHealthMetric(member_id, metric_type, value)
        print(f"Metric #{metric_id} for {full_name}.")
    except Exception as e:
        print("Failed to add health metric")
        print("Error:", e)

def viewHealthHistory():
    print("\n== View Health History ==")
    email = input("Member email: ").strip()
    row = getMemberByEmail(email)
    
    if row is None:
        print("No member found with that email.")
        return
    
    member_id, full_name, email, *_= row
    metrics = getMetricsForMember(member_id)
    
    if not metrics:
        print(f"No health metrics for {full_name}.")
        return
    
    print(f"\nHealth metrics for {full_name}:")
    for metric_id, metric_type, metric_value, recorded_at in metrics:
        print(f"- [{recorded_at}] {metric_type}: {metric_value}")
    
def updateMemberProfileMenu():
    print("\n== Update Member Profile ==")
    email = input("Member email: ").strip()
    row = getMemberByEmail(email)
    
    if row is None:
        print("No member found with that email.")
        return
    
    member_id, current_name, current_email, current_dob, current_gender, current_phone, current_goal = row

    
    full_name = input("New full name (leave blank to keep current): ").strip()
    if not full_name:
        full_name = current_name
    
    new_email = input("New email (leave blank to keep current): ").strip()
    if not new_email:
        new_email = current_email
    
    dob_str = input("New Date of Birth (YYYY-MM-DD, leave blank to keep current): ").strip()
    date_of_birth = None
    if dob_str:
        try:
            datetime.strptime(dob_str, "%Y-%m-%d")
            date_of_birth = dob_str
        except ValueError:
            print("Invalid Date") 
            date_of_birth = current_dob
    else:
        date_of_birth = current_dob
    
    
    gender = input("New gender (leave blank to keep current): ").strip()
    if gender == "":
        gender = current_gender
        
    phone = input("New phone (leave blank to keep current): ").strip()
    if phone == "":
        phone = current_phone
        
    fitness_goal = input("New fitness goal (leave blank to keep current): ").strip()
    if fitness_goal == "":
        fitness_goal = current_goal
    
    updated_rows = updateMemberProfile(member_id, full_name, new_email, date_of_birth, gender, phone, fitness_goal)
    
    if updated_rows == 0:
        print("No profile was updated")
    else:
        print("Profile updated successfully")
        
        updated = getMemberByEmail(new_email)
        
        if updated is None:
            print("Warning: could not reload updated profile (email may have changed)")
            return
        
        print("\n--UPDATED INFO--")
        print(f"\nID: {updated[0]}")
        print(f"\nFull Name: {updated[1]}")
        print(f"\nEmail: {updated[2]}")
        print(f"\nDate of Birth: {updated[3]}")
        print(f"\nGender: {updated[4]}")
        print(f"\nPhone: {updated[5]}")
        print(f"\nFitness Goal: {updated[6]}")

def registerForClassMenu():
    print("\n== Class Registration ==")
    email = input("Member email: ").strip()
    row = getMemberByEmail(email)
    
    if row is None:
        print("No member found with that email.")
        return
    
    member_id, _, email, *_= row
    
    classes = getAllClasses()
    
    if not classes:
        print("\nNo classes are currently scheduled.")
        return
    
    print("\nAvailable Classes:")
    for class_id, name, time, cap in classes:
        print(f"{class_id}, {name} at {time} (Capacity {cap})")
    
    try:
        class_id = int(input("\nEnter class ID to register: ").strip())
    except ValueError:
        print("Invalid ID")
        return
    
    current = countRegistrations(class_id)
    
    class_cap = None
    for c in classes:
        if c[0] == class_id:
            class_cap = c[3]
    
    if class_cap is None:
        print("Class does not exist.")
        return
    
    if current >= class_cap:
        print("Class is full. Cannot register.")
        return
    
    result = registerForClass(member_id, class_id)
    
    if result is None:
        print("You already registered for this class.")
    else:
        print("Registration successful!")    
          
        

def memberMenu():
    while True:
        print ("\n== Member Menu ==")
        print("1. Register new member")
        print("2. Add health metric")
        print("3. View health history")
        print("4. Update member profile")
        print("5. Register for class")
        print("0. Back to main menu")
        
        choice = input("Select: ").strip()
        
        if choice == "1":
            registerMember()
        elif choice == "2":
            addHealthMetricMenu()
        elif choice == "3":
            viewHealthHistory()
        elif choice == "4":
            updateMemberProfileMenu()
        elif choice == "5":
            registerForClassMenu()
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again.")
