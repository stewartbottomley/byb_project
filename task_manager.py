import os
from datetime import datetime, date

# Constant representing the format of the date and time used in the program
DATETIME_STRING_FORMAT = "%Y-%m-%d"

def reg_user():
    """Register a new user"""
    new_username = input("Enter new username: ")

    # Check if the username already exists
    if new_username in username_password:
        print("Username already exists. Please choose a different username.")
        return
    # User has to input the new password twice to confirm it
    while True:
        new_password = input("Enter new password: ")
        confirm_password = input("Confirm new password: ")

        if new_password == confirm_password:
            break
        else:
            print("Passwords do not match. Please try again.")

    # Add the new user to the username_password dictionary
    username_password[new_username] = new_password

    # Write the new user details to the user.txt file
    with open("user.txt", "a") as user_file:
        user_file.write("\n" + new_username + ";" + new_password)

    print("User registered successfully!")


def add_task():
    """Add a new task"""
    assigned_username = input("Enter username of the person the task is assigned to: ")

    # Check if the assigned username exists in the username_password dictionary
    if assigned_username not in username_password:
        print("Username does not exist.")
        return

    task_title = input("Enter task title: ")
    task_description = input("Enter task description: ")
    due_date_str = input("Enter due date (YYYY-MM-DD): ")

    # Validate and convert the due date string to a datetime object
    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
        return

    # Get the current date and time
    assigned_date = datetime.now()

    # Create a new task dictionary
    new_task = {
        'username': assigned_username,
        'title': task_title,
        'description': task_description,
        'due_date': due_date,
        'assigned_date': assigned_date,
        'completed': False  # The task is initially marked as incomplete
    }

    # Add the new task to the task_list
    task_list.append(new_task)

    # Write the new task details to the tasks.txt file
    with open("tasks.txt", "a") as task_file:
        task_file.write(f"{assigned_username};{task_title};{task_description};{due_date.strftime(DATETIME_STRING_FORMAT)};{assigned_date.strftime(DATETIME_STRING_FORMAT)};No\n") #change the \n to beginning?

    print("Task added successfully!")

# Function to load tasks from the tasks.txt file
def load_tasks():
    """Load tasks from the tasks.txt file"""
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as task_file:
            for line in task_file:
                task_data = line.strip().split(";")
                assigned_username = task_data[0]
                task_title = task_data[1]
                task_description = task_data[2]
                due_date = datetime.strptime(task_data[3], "%Y-%m-%d").date()
                assigned_date = datetime.strptime(task_data[4], "%Y-%m-%d").date()  # Updated line
                completed = task_data[5] == 'Yes'
                
                new_task = {
                    'username': assigned_username,
                    'title': task_title,
                    'description': task_description,
                    'due_date': due_date,
                    'assigned_date': assigned_date,
                    'completed': completed
                }
                
                task_list.append(new_task)
    
    print("Tasks loaded successfully!")

def view_all():
    """View all tasks"""
    print("All Tasks:")
    for task in task_list:
        print("------------------------------")
        print(f"Title: {task['title']}")
        print(f"Assigned to: {task['username']}")
        print(f"Description: {task['description']}")
        print(f"Due Date: {task['due_date'].strftime('%Y-%m-%d')}")
        print(f"Assigned Date: {task['assigned_date'].strftime('%Y-%m-%d')}")
        print(f"Status: {'Completed' if task['completed'] else 'Incomplete'}")
    print("------------------------------")

def view_mine():
    """View tasks assigned to the currently logged-in user"""
    logged_in_user = input("Enter your username: ")

    # Check if the logged-in user exists in the username_password dictionary
    if logged_in_user not in username_password:
        print("Username does not exist.")
        return

    print("Tasks assigned to you:")
    for index, task in enumerate(task_list):
        if task['username'] == logged_in_user:
            print(f"Task {index+1}:")
            print(f"Title: {task['title']}")
            print(f"Description: {task['description']}")
            print(f"Due Date: {task['due_date'].strftime('%Y-%m-%d')}")
            print(f"Assigned Date: {task['assigned_date'].strftime('%Y-%m-%d')}")
            print(f"Completed: {'Yes' if task['completed'] else 'No'}")
            print()

            action = input("Enter 'c' to mark the task as complete, 'e' to edit the task, or any other key to continue: ")
            if action == 'c':
                task['completed'] = True
                print("Task marked as complete.")
            elif action == 'e':
                new_title = input("Enter new task title: ")
                new_description = input("Enter new task description: ")
                new_due_date_str = input("Enter new due date (YYYY-MM-DD): ")

                # Validate and convert the new due date string to a datetime object
                try:
                    new_due_date = datetime.strptime(new_due_date_str, "%Y-%m-%d").date()
                except ValueError:
                    print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
                    return

                task['title'] = new_title
                task['description'] = new_description
                task['due_date'] = new_due_date

                print("Task updated successfully.")

            print()


def edit_task(task):
    """Edit a task"""
    task_title = input("Enter updated task title: ")
    task_description = input("Enter updated task description: ")
    due_date_str = input("Enter updated due date (YYYY-MM-DD): ")

    # Validate and convert the due date string to a datetime object
    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        task['title'] = task_title
        task['description'] = task_description
        task['due_date'] = due_date
        print("Task updated successfully!")
    except ValueError:
        print("Invalid date format. Task not updated.")

def complete_task(task):
    """Mark a task as complete"""
    task['completed'] = True
    print("Task marked as complete!")


def generate_reports():
    # Generate task report
    total_tasks = len(task_list)
    completed_tasks = sum(task['completed'] for task in task_list)
    uncompleted_tasks = total_tasks - completed_tasks
    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    overdue_tasks = sum(
        not task['completed'] and task['due_date'] < date.today() for task in task_list
    )
    overdue_percentage = (overdue_tasks / uncompleted_tasks) * 100 if uncompleted_tasks > 0 else 0

    with open("task_overview.txt", "w") as task_report_file:
        task_report_file.write(f"Total Tasks: {total_tasks}\n")
        task_report_file.write(f"Completed Tasks: {completed_tasks}\n")
        task_report_file.write(f"Incomplete Tasks: {uncompleted_tasks}\n")
        task_report_file.write(f"Overdue Tasks: {overdue_tasks}\n")
        task_report_file.write(f"Percentage of Incomplete Tasks: {incomplete_percentage:.2f}%\n")
        task_report_file.write(f"Percentage of Overdue Tasks: {overdue_percentage:.2f}%\n")

    # Generate user report
    total_users = len(username_password)
    user_report = f"Total Users: {total_users}\n"
    user_report += f"Total Tasks: {total_tasks}\n"

    for username in username_password:
        user_tasks = sum(task['username'] == username for task in task_list)
        user_assigned_percentage = (user_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        user_completed_percentage = (sum(
            task['username'] == username and task['completed'] for task in task_list
        ) / user_tasks) * 100 if user_tasks > 0 else 0
        user_uncompleted_percentage = (sum(
            task['username'] == username and not task['completed'] for task in task_list
        ) / user_tasks) * 100 if user_tasks > 0 else 0
        user_overdue_percentage = (sum(
            task['username'] == username and not task['completed'] and task['due_date'] < date.today()
            for task in task_list
        ) / user_tasks) * 100 if user_tasks > 0 else 0

        user_report += f"\nUser: {username}\n"
        user_report += f"Tasks Assigned: {user_tasks}\n"
        user_report += f"Percentage of Tasks Assigned: {user_assigned_percentage:.2f}%\n"
        user_report += f"Percentage of Completed Tasks: {user_completed_percentage:.2f}%\n"
        user_report += f"Percentage of Uncompleted Tasks: {user_uncompleted_percentage:.2f}%\n"
        user_report += f"Percentage of Overdue Tasks: {user_overdue_percentage:.2f}%\n"

    with open("user_overview.txt", "w") as user_report_file:
        user_report_file.write(user_report)

    print("Reports generated successfully.")


# Check if the user.txt file exists and create it with a default admin user if it doesn't exist
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as user_file:
        user_file.write("admin;admin\n")

# Read the user data from the user.txt file and store it in the username_password dictionary
username_password = {}
with open("user.txt", "r") as user_file:
    for line in user_file:
        line = line.strip() # removes any whitespace before splitting the line into 'username' and 'password'
        if line: 
            username, password = line.split(";")
            username_password[username] = password
            # Extra 'if' to check and skip any empty lines, defensive against errors

logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")

    # Check if the entered username exists and the password is correct
    if curr_user not in username_password:
        print("User does not exist")
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
    else:
        print("Login Successful!")
        logged_in = True


# List to store task dictionaries
task_list = []
load_tasks()

def display_statistics():
    """Display statistics from reports"""
    # Check if the task_overview.txt file exists
    if not os.path.exists("task_overview.txt"):
        generate_reports()

    # Read and display the task report
    with open("task_overview.txt", "r") as task_overview_file:
        task_overview = task_overview_file.read()
        print(task_overview)

    # Check if the user_overview.txt file exists
    if not os.path.exists("user_overview.txt"):
        generate_reports()

    # Read and display the user report
    with open("user_overview.txt", "r") as user_overview_file:
        user_overview = user_overview_file.read()
        print(user_overview)

# Update the menu loop
while True:
    print()
    menu = input('''Select one of the following options:
    r - Register a user
    a - Add a task
    va - View all tasks
    vm - View my tasks
    gr - Generate reports
    ds - Display statistics
    e - Exit
    : ''').lower()

    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == 'gr':
        generate_reports()
    elif menu == 'ds':
        generate_reports() # reports are always created first so that the 'ds' option has the most up to date statistics. 
        display_statistics() 
    elif menu == 'e':
        break
    else:
        print("Invalid input. Please select a valid option.")

print("Program exited.")

