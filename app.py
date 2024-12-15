import sqlite3
import csv

USERS = {
    "u1@test.com": {"password": "1234", "role": "user"},
    "m1@test.com": {"password": "1234", "role": "manager"},
    "a1@test.com": {"password": "1234", "role": "super-admin"},
}


def setup_database():
    conn = sqlite3.connect("competency_tracking.db")
    cursor = conn.cursor()

    with open("schema.sql", "r") as schema_file:
        schema = schema_file.read()
        cursor.executescript(schema)

    USERS = {
        "u1@test.com": {"password": "1234", "role": "user"},
        "m1@test.com": {"password": "1234", "role": "manager"},
        "a1@test.com": {"password": "1234", "role": "super-admin"},
    }

    for email, details in USERS.items():
        cursor.execute(
            "INSERT OR IGNORE INTO users (email, password, role) VALUES (?, ?, ?)",
            (email, details["password"], details["role"]),
        )

    conn.commit()
    print("Database setup complete.")
    conn.close()


def add_user():
    email = input("Enter the new user's email: ")
    password = input("Enter the new user's password: ")
    role = input("Enter the new user's role (user/manager/super-admin): ").lower()

    if role not in ["user", "manager", "super-admin"]:
        print("Invalid role. Please enter one of the following: user, manager, super-admin.")
        return

    hashed_password = password

    conn = sqlite3.connect("competency_tracking.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (email, password, role) VALUES (?, ?, ?)", (email, hashed_password, role))
        conn.commit()
        print(f"User {email} with role {role} has been added successfully.")
    except sqlite3.IntegrityError:
        print("Error: User with this email already exists.")

    conn.close()


def grade_user():
    email = input("Enter the email of the user you want to grade: ")
    grade = input("Enter the grade (0-100): ")

    if not grade.isdigit() or not (0 <= int(grade) <= 100):
        print("Invalid grade. Please enter a number between 0 and 100.")
        return

    conn = sqlite3.connect("competency_tracking.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if user:
        user_id = user[0]
        cursor.execute("INSERT INTO grades (user_id, grade) VALUES (?, ?)", (user_id, grade))
        conn.commit()
        print(f"Grade {grade} has been assigned to {email}.")
    else:
        print(f"Error: User with email {email} not found.")

    conn.close()


def login(email, password):
    conn = sqlite3.connect("competency_tracking.db")
    cursor = conn.cursor()

    cursor.execute("SELECT email, password, role FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    conn.close()

    if user and user[1] == password:
        return {"success": True, "role": user[2]}
    else:
        return {"success": False, "message": "Invalid email or password"}


def display_all_users():
    try:
        conn = sqlite3.connect("competency_tracking.db")
        cursor = conn.cursor()

        cursor.execute("SELECT email, role FROM users")

        users = cursor.fetchall()

        if users:
            for user in users:
                print(f"Email: {user[0]}, Role: {user[1]}")
        else:
            print("No users found.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def display_menu(role):
    if role == "user":
        print("\nUser Menu:")
        print("1. View Competencies")
        print("2. Log Out")
    elif role == "manager":
        print("\nManager Menu:")
        print("1. View Competencies")
        print("2. Manage Team")
        print("3. Add a New User")
        print("4. Grade a User")
        print("5. Log Out")
    elif role == "super-admin":
        print("\nSuper Admin Menu:")
        print("1. View Competencies")
        print("2. Manage Users")
        print("3. Manage Projects")
        print("4. Log Out")


def manage_team(role):
    while True:
        print("\nManage Team Options:")
        print("1. View All Users")
        print("2. Add a New User")
        print("3. Grade a User")
        print("4. Back to Menu")

        choice = input("\nChoose an option: ")

        if choice == "1":
            print("\nDisplaying all users...")
        elif choice == "2":
            add_user()
        elif choice == "3":
            grade_user()
        elif choice == "4":
            break
        else:
            print("Invalid option. Please try again.")


def main():
    setup_database()

    while True:
        print("\nWelcome to the Competency Tracking System!")
        email = input("Email: ")
        password = input("Password: ")

        result = login(email, password)
        if result["success"]:
            role = result["role"]
            print(f"\nLogin successful! Welcome, {role.capitalize()}.")

            while True:
                display_menu(role)
                choice = input("\nChoose an option: ")

                if choice == "1":
                    print("\nView Competencies")
                elif choice == "2":
                    if role == "user":
                        print("\nYou have been logged out.")
                        break
                    elif role in ["manager", "super-admin"]:
                        manage_team(role)
                elif choice == "5":
                    print("\nLogging out...")
                    break
        else:
            print(result["message"])


if __name__ == "__main__":
    main()
