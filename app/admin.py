from datetime import datetime
from db import getAllRooms, getAllClasses, getBookingsForRoom, createRoomBooking, getAllEquipment, addEquipment, reportEquipmentIssue, getOpenIssues, resolveIssue

# Handles the flow of booking a room for a class
def roomBookingMenu():
    print("\n== Room Booking ==")
    
    # Fetch all rooms available
    rooms = getAllRooms()
    
    if not rooms:
        print("No rooms found.")
        return
    
    print("\nAvailable Rooms:")
    for room_id, room_name in rooms:
        print(f"{room_id}: {room_name}")
    
    # Select room ID    
    try:
        room_id = int(input("\nEnter room ID to book: ").strip())
    except ValueError:
        print("Invalid room ID.")
        return
    
    # Validate room exists
    room_ids = [r[0] for r in rooms]
    if room_id not in room_ids:
        print("No such room.")
        return
    
    # Fetch available classes
    classes = getAllClasses()
    
    if not classes:
        print("No classes available to assign.")
        return
    
    print("\nAvailable Classes:")
    for class_id, class_name, class_time, cap in classes:
        print(f"{class_id}: {class_name} at {class_time} (Capacity {cap})")
    
    # Select class ID  
    try:
        class_id = int(input("\nEnter class ID to assign to this room: ").strip())
    except ValueError:
        print("Invalid class ID.")
        return
    
    class_ids = [c[0] for c in classes]
    if class_id not in class_ids:
        print("No such class.")
        return
    
    # Collect booking window
    print("\nEnter booking time window (YYYY-MM-DD HH:MM): ")
    start_str = input("Start time: ").strip()
    end_str = input("End time: ").strip()
    
    # Convert to datetime objects
    try:
        start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(end_str, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Invalid date and time format")
        return
    
    # Validate time order
    if end_time <= start_time:
        print("End time must be after start time")
        return
    
    # Get existing bookings to check conflict
    existing = getBookingsForRoom(room_id)
    
    if existing:
        print("\nExisting Bookings:")
        for booking_id, ex_class_id, ex_start, ex_end in existing:
            print(f"- Booking #{booking_id}: Class {ex_class_id} [{ex_start} - {ex_end}] ")
    else:
        print("\nExisting Bookings: None")
    
    # Check if new booking overlaps with existing    
    for booking_id, ex_class_id, ex_start, ex_end in existing:
        if start_time < ex_end and end_time > ex_start:
            print("WARNING: This time overlaps with existing booking")
            print(f"Existing book #{booking_id}: Class {ex_class_id} [{ex_start} - {ex_end}]")
            return
    
    # Insert booking into database
    try:
        booking_id = createRoomBooking(room_id, class_id, start_time, end_time)
        print(f"Room booked successfully with booking ID: {booking_id}")
    except Exception as e:
        print("Failed to create room booking")
        print("Error:", e)
   
        
# Display all equipment and where it is located
def listEquipment():
    equipment = getAllEquipment()
    
    if not equipment:
        print("No equipment found.")
        return
        
    for eq_id, name, room_name in equipment:
        room_label = room_name if room_name else "Unassigned"
        print(f"- ID {eq_id}: {name} (Room: {room_label})")


# Flow for adding new gym equipment
def addEquipmentFlow():
    print("\n== Add Equipment ==")
    name = input("Equipment Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    
    rooms = getAllRooms()
    
    # If no rooms exist, add equipment without assignment
    if not rooms:
        print("No rooms found. Equipment will be added without a room.")
        room_id = None
    else:
        print("\nAvailable Rooms:")
        for room_id, room_name in rooms:
            print(f"{room_id}: {room_name}")
        
        room_input = input("Enter room ID to assign: ").strip()
        if room_input == "":
            room_id = None
        else:
            try:
                room_id = int(room_input)
            except ValueError:
                print("Invalid room ID. Equipment will be added without a room.")
                room_id = None
            
    # Save equipment record
    eq_id = addEquipment(name, room_id)
    print(f"Equipment added with ID: {eq_id}")
    

# Flow to report an issue with equipment
def reportIssueFlow():
    print("\n== Report Equipment Issue ==")
    
    equipment = getAllEquipment()

    if not equipment:
        print("No equipment found. Add equipment first.")
        return
     
    print("\nEquipment:")
    for eq_id, name, room_name in equipment:
        room_label = room_name if room_name else "Unassigned"
        print(f"{eq_id}: {name} (Room: {room_label})")
    
    # Select equipment ID
    try:
        eq_id = int(input("Enter equipment ID: ").strip())
    except ValueError:
        print("Invalid equipment ID.")
        return
    
    valid_ids = [e[0] for e in equipment]
    if eq_id not in valid_ids:
        print("No such equipment.")
        return
    
    issue = input("Describe the issue: ").strip()
    if not issue:
        print("Description cannot be empty.")
        return
    
    log_id = reportEquipmentIssue(eq_id, issue)
    print(f"Issue logged with ID: {log_id}")

        
# Show all unresolved maintenance issues
def viewOpenIssues():
    open_issues = getOpenIssues()
    
    if not open_issues:
        print("\nNo open issues.")
        return
    
    print("\nOpen Maintenance Issues:")
    for log_id, eq_id, name, issue, reported_at in open_issues:
        print(f"- Log #{log_id}: {name} (ID {eq_id})")
        print(f"    Reported at: {reported_at}")
        print(f"    Issue: {issue}")
    
        
# Resolve a maintenance issue by marking it closed        
def resolveIssueFlow():
    print("\n== Resolve Issue ==")
    open_issues = getOpenIssues()
    
    if not open_issues:
        print("No open issues to resolve.")
        return
     
    print("\nOpen Issues:")
    for log_id, eq_id, name, issue, reported_at in open_issues:
        print(f"{log_id}: {name} (ID {eq_id}) - {issue} [{reported_at}]")
    
    # Select issue to resolve
    try:
        log_id = int(input("Enter log ID to resolve: ").strip())
    except ValueError:
        print("Invalid log ID.")
        return
    
    updated = resolveIssue(log_id)
    if updated:
        print("Issue marked as resolved.")
    else:
        print("No such log ID.")

# Menu for equipment maintenance
def equipmentMenu():
    while True:
        print("\n== Equipment Maintenance ==")
        print("1. List Equipment")
        print("2. Add Equipment")
        print("3. Report Equipment Issue")
        print("4. View Open Issues")
        print("5. Resolve Issue")
        print("0. Back to Admin Menu")
        
        choice = input("Select: ").strip()
        
        if choice == "1":
            listEquipment()
        elif choice == "2":
            addEquipmentFlow()
        elif choice == "3":
            reportIssueFlow()
        elif choice == "4":
            viewOpenIssues()
        elif choice == "5":
            resolveIssueFlow()
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again.")
 
   
# Main admin menu
def adminMenu():
    while True:
        print ("\n== Admin Menu ==")
        print("1. Room Booking")
        print("2. Equipment Maintenance")
        print("0. Back to main menu")
        
        choice = input("Select: ").strip()
        
        if choice == "1":
            roomBookingMenu()
        elif choice == "2":
            equipmentMenu()
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again.")

    