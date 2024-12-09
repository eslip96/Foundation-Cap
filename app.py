USERS = {
    "user1@test.com": {"password": "1234", "role": "user"},
    "manager1@test.com": {"password": "1234", "role": "manager"},
    "admin1@test.com": {"password": "1234", "role": "super-admin"},
}


def login(email, password):
    user = USERS.get(email)
    if user and user["password"] == password:
        return {"success": True, "role": user["role"]}
    else:
        return {"success": False, "message": "Invalid email or password"}


def display_menu(role):
    match role:
        case "user":
            print("\nUser Menu:")
            print("1. View Competencies")
            print("2. Log Out")

        case "manager":
            print("\nManager Menu:")
            print("1. View Competencies")
            print("2. Manage Team")
            print("3. Log Out")

        case "super-admin":
            print("\nSuper Admin Menu:")
            print("1. View Competencies")
            print("2. Manage Users")
            print("3. Manage Projects")
            print("4. Log Out")


def main():
    while True:
        print("\nWelcome to the Competency Tracking System!")
        print("Please log in to continue.")

        email = input("Email: ")
        password = input("Password: ")

        result = login(email, password)

        if result["success"]:
            role = result["role"]
            print(f"\nLogin successful! Welcome, {role.capitalize()}.")

            while True:
                display_menu(role)
                choice = input("\nChoose an option: ")

                match (choice, role):
                    case ("1", _):
                        print("\nYOURE FIRED")

                    case ("2", "user"):
                        print("\nYou have been logged out.")
                        break

                    case ("2", "manager"):
                        print("\nNOT BUILT OUT YET")
                    case ("3", "manager"):
                        print("\nYou have been logged out.")
                        break

                    case ("2", "super-admin"):
                        print("\nNOT BUILT OUT YET")
                    case ("3", "super-admin"):
                        print("\nNOT BUILT OUT YET")
                    case ("4", "super-admin"):
                        print("\nNOT BUILT OUT YET")
                        break

                    case _:
                        print("Invalid option. Please try again.")
        else:
            print(result["message"])


if __name__ == "__main__":
    main()
