import sqlite3
import csv


def setup_database():
    conn = sqlite3.connect("competency_tracking.db")
    cursor = conn.cursor()

    with open("schema.sql", "r") as schema_file:
        schema = schema_file.read()
        cursor.executescript(schema)

    USERS = {
        "u1@test.com": {"password": "1234", "role": "user", "first_name": "test", "last_name": "user"},
        "m1@test.com": {"password": "1234", "role": "manager", "first_name": "test", "last_name": "manager"},
        "a1@test.com": {"password": "1234", "role": "super-admin", "first_name": "test", "last_name": "super-admin"},
    }

    for email, details in USERS.items():
        cursor.execute(
            """
            INSERT OR IGNORE INTO users (email, password, role, first_name, last_name) 
            VALUES (?, ?, ?, ?, ?)
            """,
            (email, details["password"], details["role"], details["first_name"], details["last_name"]),
        )

    conn.commit()
    print("Database setup complete.")
    conn.close()


def login(email, password):
    conn = sqlite3.connect("competency_tracking.db")
    cursor = conn.cursor()

    cursor.execute("SELECT email, password, role FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    conn.close()

    if user:
        stored_email, stored_password, role = user
        if stored_password == password:
            return {"success": True, "role": role}
        else:
            return {"success": False, "message": "Incorrect password"}
    else:
        return {"success": False, "message": "User not found"}


def add_user():
    email = input("Enter the new user's email: ")
    password = input("Enter the new user's password: ")
    role = input("Enter the new user's role (user/manager/super-admin): ").lower()
    first_name = input("Enter the new user's first name: ")
    last_name = input("Enter the new user's last name: ")

    if role not in ["user", "manager", "super-admin"]:
        print("Invalid role. Please enter one of the following: user, manager, super-admin.")
        return

    hashed_password = password

    conn = sqlite3.connect("competency_tracking.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (email, password, role, first_name, last_name) 
            VALUES (?, ?, ?, ?, ?)
            """,
            (email, hashed_password, role, first_name, last_name),
        )
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
        print(f"User with email {email} not found.")

    conn.close()


def check_user(email):
    conn = sqlite3.connect('competency_tracking.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    conn.close()

    return user


def search_user_by_name():
    name = input("Enter the first or last name to search: ").strip()

    conn = sqlite3.connect("competency_tracking.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT first_name, last_name, email, role 
        FROM users 
        WHERE first_name LIKE ? OR last_name LIKE ?
    """, (f"%{name}%", f"%{name}%"))

    results = cursor.fetchall()

    if results:
        print("\nSearch Results:")
        for row in results:
            first_name, last_name, email, role = row
            print(f"Name: {first_name} {last_name}, Email: {email}, Role: {role}")
    else:
        print("No users found with that name.")

    conn.close()


def export_competency_report():
    conn = sqlite3.connect("competency_tracking.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT users.email, competencies.name, assessments.score
        FROM users
        JOIN assessments ON users.id = assessments.user_id
        JOIN competencies ON assessments.assessment_id = competencies.id
    """)

    report_data = cursor.fetchall()

    with open("competency_report.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["User Email", "Competency", "Score"])
        for row in report_data:
            writer.writerow(row)

    print("Competency report exported successfully.")
    conn.close()


def export_user_competency_report(user_email):
    conn = sqlite3.connect("competency_tracking.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT competencies.name, assessments.score
        FROM users
        JOIN assessments ON users.id = assessments.user_id
        JOIN competencies ON assessments.assessment_id = competencies.id
        WHERE users.email = ?
    """, (user_email,))

    report_data = cursor.fetchall()

    with open(f"{user_email}_competency_report.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Competency", "Score"])
        for row in report_data:
            writer.writerow(row)

    print(f"Competency report for {user_email} exported successfully.")
    conn.close()


def import_assessment_results():
    conn = sqlite3.connect("competency_tracking.db")
    cursor = conn.cursor()

    with open("assessment_results.csv", "r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            user_id, competency_id, score, date_taken = row
            cursor.execute(
                "INSERT INTO assessments (user_id, competency_id, score, date_taken) VALUES (?, ?, ?, ?)",
                (user_id, competency_id, score, date_taken),
            )
    conn.commit()
    conn.close()
    print("Assessment results imported successfully.")


def delete_assessment_result():
    assessment_id = input("Enter the assessment result ID to delete: ")

    conn = sqlite3.connect("competency_tracking.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM assessment_results WHERE id = ?", (assessment_id,))
    result = cursor.fetchone()

    if result:
        cursor.execute("DELETE FROM assessment_results WHERE id = ?", (assessment_id,))
        conn.commit()
        print(f"Assessment result with ID {assessment_id} has been deleted.")
    else:
        print(f"No assessment result found with ID {assessment_id}.")

    conn.close()


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


def display_all_users_and_grades():
    conn = sqlite3.connect("competency_tracking.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT users.first_name, users.last_name, users.email, users.role, grades.grade
        FROM users
        LEFT JOIN grades ON users.id = grades.user_id
    """)

    users = cursor.fetchall()

    if users:
        print("\nAll Users and their Grades:")
        for user in users:
            first_name, last_name, email, role, grade = user
            print(f"Name: {first_name} {last_name}, Email: {email}, Role: {role}, Grade: {grade if grade is not None else 'No grade assigned'}")
    else:
        print("No users found.")

    conn.close()


def view_user_competencies(user_email):
    conn = sqlite3.connect("competency_tracking.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT competencies.name, assessments.score
        FROM users
        JOIN assessments ON users.id = assessments.user_id
        JOIN competencies ON assessments.assessment_id = competencies.id
        WHERE users.email = ?
    """, (user_email,))

    competencies = cursor.fetchall()

    if competencies:
        print("\nYour Competencies and Grades:")
        for competency in competencies:
            name, score = competency
            print(f"Competency: {name}, Grade: {score}")
    else:
        print("No grade assigned.")

    conn.close()


def delete_user_grade(user_email):
    conn = sqlite3.connect("competency_tracking.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE email = ?", (user_email,))
    user = cursor.fetchone()

    if user:
        user_id = user[0]
        cursor.execute("DELETE FROM grades WHERE user_id = ?", (user_id,))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"Grade for user '{user_email}' has been deleted.")
        else:
            print(f"No grade found for user '{user_email}'.")
    else:
        print(f"User with email '{user_email}' not found.")

    conn.close()


def manage_team(role):
    while True:
        print("\nManage Team Options:")
        print("1. View All Users and Grades")
        print("2. Add a New User")
        print("3. Grade a User")
        print("4. Search User by Name")
        print("5. Delete User Grade")
        print("6. Export Competency Report")
        print("7. Back to Menu")

        choice = input("\nChoose an option: ")

        if choice == "1":
            display_all_users_and_grades()
        elif choice == "2":
            add_user()
        elif choice == "3":
            grade_user()
        elif choice == "4":
            search_user_by_name()
        elif choice == "5":
            email = input("Enter the user's email to delete their grade: ")
            delete_user_grade(email)
        elif choice == "6":
            export_competency_report()
        elif choice == "7":
            break
        else:
            print("Invalid option. Please try again.")


def display_menu(role, email):
    print("\nMenu:")
    print("1. View Competencies")
    if role == "manager" or role == "super-admin":
        print("2. Manage Team")
    print("3. log out")

    choice = input("\nChoose an option: ")

    if choice == "1":
        view_user_competencies(email)


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
                display_menu(role, email)
                choice = input("\nChoose an option: ")

                if choice == "1":
                    print("\nView Competencies")
                elif choice == "2":
                    if role == "manager" or role == "super-admin":
                        manage_team(role)
                elif choice == "3":
                    print("\nYou have been logged out.")
                    break
                else:
                    print("Invalid option. Please try again.")
        else:
            print(f"\nLogin failed: {result['message']}")


if __name__ == "__main__":
    main()
