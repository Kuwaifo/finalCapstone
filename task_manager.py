# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
import io
import sys

from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

task_dict = {}

def reg_user():
    '''Add a new user to the user.txt file'''
        # - Request input of a new username
    new_username = input("New Username: ")
    check_user(new_username)
        # - Request input of a new password
    new_password = input("New Password: ")

        # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password
            
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))

        # - Otherwise you present a relevant message.
    else:
            print("Passwords do no match")

def add_task():
    '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            pass
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")


    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
    new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

    task_list.append(new_task)
    with open("tasks.txt", "r+") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes;" if t['completed'] else "No;"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''

    for t in task_list:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)
            

def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''
   
    rec_numbers_for_user = []    
    for count, t in enumerate(task_list,1):
        if t['username'] == curr_user:
                task_dict[count] = t
                disp_str = f"  {count}) \t{t['title']}\t"
                disp_str += f"Date Assigned: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\t"
                disp_str += f"Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\t"
                disp_str += f"Assigned to: {t['username']}\n"
                disp_str += f"\t\tDescription: {t['description']}"    
                print(disp_str)    
                rec_numbers_for_user.append(count)                  # Store all the record positions for a user

    loopout = 0
    selection = int(input("\nSelect a task number, or enter -1 to return to menu: "))
    while loopout!= "-1":
        if selection in rec_numbers_for_user:
          
            loopout = select_task(selection)
        
        elif selection == -1:
            break
        else:
            selection = int( input("\nError!! Please enter a valid selection from the menu: "))
    return

    
def writeToFile(content):
   """
   This writes to file tasks.txt
   """
   with open('tasks.txt', 'w+') as task_file:
      for line in content:
        task_file.write(line)



def check_user(name):
    '''
    Reads the user.txt file to see if the user already exists on file or not. 
    This is to prevent duplicate usernames being added and an appropriate message 
    is displayed is it is found to exist on the file.
    '''
    user_list=[]
    while True:
            f=open("user.txt","r")
            for line in f: 
                user_name = line.split(';')[0]
                user_list.append(user_name)
            if name in user_list:
                name = input("This user already exists, try again : ") 
            else:
                return name
    f.close()


def select_task(select_f):
    '''
    This function ensures that a valid option has been made,  
    which would be either a task number or -1 to return to the menu
    '''    
    content = []
    position = select_f - 1 

    selection = int(input("Select: 2-Mark complete, 3-Edit  or -1 to exit: "))
    if selection == 2:                                       # Update the status of this record as completed
        with open('tasks.txt', 'r+') as task_file:
            task_rec = task_file.readlines()
        # reads each line in the file
            rec_count = 0
            for ur in task_rec:
                field = ur.split(';')    
                if position == rec_count:
                    field[5] = field[5].replace("No", "Yes")
                content.append(';'.join(field))
                task_rec = task_file.readline()
                rec_count += 1

        writeToFile(content)
        print("\n**  This task is now completed.  **")

    elif selection == 3:                        # Edit the user name and/or the due date for this record
        user_found = False
        
        with open('tasks.txt', 'r+') as task_file:
                task_rec = task_file.readlines()
            # reads each line in the file
                rec_count = 0
                for ur in task_rec:
                    field = ur.split(';')    
                    if position == rec_count:
                        if field[5] != "Yes":                                
                                eusername = input("Edit Username y/n: ")    
                                if eusername == "y":
                                    edit_username = input("Please enter new username:")
                                    user_file = open("user.txt","r")
                                    for line in user_file:
                                        split_record =line.split(";")
                                        
                                # This record will have a new user assigned that that exists
                                        if edit_username == split_record[0]:
                                                user_found = True    
                                                break
                                        
                                    if user_found is True:
                                        field[0] = field[0].replace(field[0],edit_username)
                                    else:
                                        print("Invalid user entered!  Please try again")
                                        edit_username = input("Invalid user entered!! Please try again: ")
  
                                eduedate = input("Edit Due Date y/n: ") 
                                if eduedate == "y":
                                    while True:
                                        try:
                                            edit_duedate = input("Due date of task (YYYY-MM-DD): ")
                                            due_date_time = datetime.strptime(edit_duedate, DATETIME_STRING_FORMAT)
                                            field[3] = field[3].replace(field[3],edit_duedate)
                                            break
                                        except ValueError:
                                                print("Invalid datetime format. Please use the format specified")
                        else:
                            print("\nvm  ** Task Completed - changes can no longer be made **")
   
                    content.append(';'.join(field))
                    task_rec = task_file.readline()
                    rec_count += 1

                writeToFile(content)
                print("\n**  This record has been modified  **")
    else:
        if selection == -1:
           return "-1"
    
def gen_task_rep():
    '''
    This function writes to the Task Overview file called task_overview.txt. 

        It will summary of statistice of file task.txtI  
    '''    
    curr_date = date.today()
    completed_tasks = 0
    incomplete_tasks = 0
    total_tasks=0
    incomplete_od = 0

    # Open files 
    tasks = open("tasks.txt","r")
    tasks_ov = open("task_overview.txt","w")

    for line in tasks:             
        total_tasks += 1                                # Accumulate total number of all records in task.txt
        status = line.split(';')[5]                     # Retrieve status of record - if completed or not    
        name_user = line.split(';')[0] 
        if status == 'Yes':
            completed_tasks += 1                        # Accumulate the number of completed tasks
        else: 
            incomplete_tasks +=  1                      # Accumulate the number of incomplete tasks

            # Retrieve and format the due date
            date_split = line.split(";")[3]
            date_split_n = date_split.split("-")
            new_date_fmt = date(int(date_split_n[0]), int(date_split_n[1]), int(date_split_n[2]))

            if  new_date_fmt < curr_date:
                incomplete_od += 1                      # Accumulate the number of incomplete tasks overdue

    incomplete_pc = (incomplete_tasks/total_tasks) * 100        # Calculate percentage of incomplete tasks
    overdue_pc = (incomplete_od/total_tasks) * 100             # Calculate percentage of overdue tasks 

    task_list = [total_tasks,completed_tasks,incomplete_tasks,incomplete_od,f"{incomplete_pc:,.1f}",f"{overdue_pc:,.1f}"]
    string_list = ";".join(str(var) for var in task_list)

    tasks_ov.write(string_list)                   # Write to file task_overview.txt

    tasks.close()
    tasks_ov.close()
    
def gen_user_rep():
    '''
    This function writes to the User Overview file called user_overview.txt. 
    It will summary of statistice of file user.txtI  
    '''    
    curr_date = date.today()
    completed_tasks = 0
    incomplete_tasks = 0
    total_tasks=0
    incomplete_od = 0
    no_of_users = 0
    user_list = []

    # Open files 
    users = open("user.txt","r")
    users_ov = open("user_overview.txt","w")
    file_name ='tasks.txt'
    num_of_tasks = count_tasks(file_name)
    for line_user in users: 
        no_of_users += 1                                    # Accumulate total number of users
        name_user = line_user.split(';')[0] 
        user_list.append(name_user)
    
    for name_user in user_list:                 # Loop through all the users in a list
        tasks = open("tasks.txt","r")
        total_tasks_user = 0
        completed_tasks = 0
        incomplete_tasks = 0
        total_tasks_user_pc = 0
        completed_tasks_pc = 0
        incomplete_pc = 0
        overdue_pc = 0
        incomplete_od = 0

        for line_task in tasks:                           # Summarize all the tasks for a specific user  
            name_task = line_task.split(';')[0] 

            if name_user == name_task:
                total_tasks += 1
                total_tasks_user += 1
                status = line_task.split(";")[5]                     # Retrieve status of record - if completed or not    
                if status == 'Yes':
                    completed_tasks += 1                        # Accumulate the number of completed tasks
                else: 
                    incomplete_tasks +=  1                      # Accumulate the number of incomplete tasks
                    task = line_task
                    # Retrieve and format the due date
                    date_split = line_task.split(";")[3]
                    date_split_n = date_split.split("-")
                    new_date_fmt = date(int(date_split_n[0]), int(date_split_n[1]), int(date_split_n[2]))
                    if  new_date_fmt < curr_date:
                        incomplete_od += 1                      # Accumulate the number of incomplete tasks overdue

        total_tasks_user_pc = (total_tasks_user/num_of_tasks) * 100        # Total % of tasks assigned to user
        if total_tasks_user!=0:
            completed_tasks_pc = (completed_tasks/total_tasks_user) * 100        # % of completed tasks for user
            incomplete_pc = (incomplete_tasks/total_tasks_user) * 100        # Calculate % of incomplete tasks
            overdue_pc = (incomplete_od/total_tasks_user) * 100             # Calculate % of overdue tasks
        else: 
            print("Error!! Total users task is 0 - You cannot divide by 0")
        
   
        task_list = [name_user,no_of_users,num_of_tasks,total_tasks_user,f"{total_tasks_user_pc:,.1f}",f"{completed_tasks_pc:,.1f}",f"{incomplete_pc:,.1f}",f"{overdue_pc:,.1f}", "\n"]
        string_list = ";".join(str(var) for var in task_list)
             
        users_ov.write(string_list )                   # Write to file users_overview.txt
    tasks.close
    users.close()
    users_ov.close()

def count_tasks(filename):
    """
    This function retrieve the number of records on in a file
    """       
    with open(filename,'r') as file:
        no_of_tasks = sum(1 for _ in file)
    return no_of_tasks

if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
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
        gen_task_rep()    
        gen_user_rep()
                
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        
        gen_task_rep()          # Generate the Tasks Overview file
        gen_user_rep()          # Generate the Users Overview file

        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")  

        tasks_ov = open("task_overview.txt","r")
        for line in tasks_ov:
            total_tasks = line.split(";")[0]    
            completed_tasks = line.split(";")[1]
            incomplete_tasks = line.split(";")[2]
            incomplete_od = line.split(";")[3]    
            incomplete_pc = line.split(";")[4]
            overdue_pc = line.split(";")[5]
        tasks_ov.close()

       # print("-----------------------------------")   
        print("      Tasks Overview               ")
        print("-----------------------------------")
        print(f"Number of total tasks: \t\t {total_tasks}")
        print(f"Completed tasks: \t\t {completed_tasks}")
        print(f"Uncompleted tasks: \t\t {incomplete_tasks}")
        print(f"Incomplete and O/D: \t\t {incomplete_od}")
        print(f"% of incomplete tasks: \t\t {incomplete_pc}")
        print(f"% of overdue tasks: \t\t {overdue_pc}")
        print("-----------------------------------")   
        print("      Users Overview               ")
        print("------------------------------------")
        print("User\t", "User\t","% Assigned\t","% completed\t","% incomplete\t","% overdue\t\t" )
        print("         Tasks\t","tasks\t\t","tasks \t\t","tasks\t\t","tasks: \t\t" )
        users_ov = open("user_overview.txt","r")
        for line in users_ov:
            name_user = line.split(";")[0]    
            total_tasks_user = line.split(";")[3]
            total_tasks_user_pc = line.split(";")[4]
            completed_tasks_pc = line.split(";")[5]    
            incomplete_pc = line.split(";")[6]
            overdue_pc = line.split(";")[7]
            print(f"{name_user}\t",f"{total_tasks_user}\t",f"{total_tasks_user_pc}\t\t",f"{completed_tasks_pc}\t\t",f"{incomplete_pc}\t\t"f" {overdue_pc}\t\t")
      #  print(f"% of task assigned to user: \t\t {total_tasks_user_pc}")
      # print(f"% of completed tasks by user: \t\t {completed_tasks_pc}")
      #  print(f"% of incomplete tasks: \t\t {incomplete_pc}")
       # print(f"% of overdue tasks: \t\t {overdue_pc}")
        users_ov.close()
     
      
        print("-----------------------------------")    


    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")