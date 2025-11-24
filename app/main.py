from member import memberMenu

def main_menu():
    while True:
        print("\n=== Health & Fitness Club System ===")
        print("1. Member")
        print("0. Exit")
        
        choice = input("Select: ").strip()
        
        if choice == "1":
            memberMenu()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main_menu()
