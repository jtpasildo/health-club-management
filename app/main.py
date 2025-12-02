from member import memberMenu
from trainer import trainerMenu
from admin import adminMenu

# Main menu for navigating between roles
def main_menu():
    while True:
        print("\n=== Health & Fitness Club System ===")
        print("1. Member")
        print("2. Trainer")
        print("3. Admin")
        print("0. Exit")
        
        choice = input("Select: ").strip()
        
        if choice == "1":
            memberMenu()
        elif choice == "2":
            trainerMenu()
        elif choice == "3":
            adminMenu()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main_menu()
