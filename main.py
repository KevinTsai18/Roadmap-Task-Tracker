import json
import os
import datetime


def print_tasks(task_list):
    print("TASK_LIST")
    for task in task_list:
        print(f"""{task[0]} - {task[1]} - {task[3]}
* {task[2]}
* Creation Date: {task[4]}
* Last Update: {task[5]}
""")


def list_tasks(command, task_list):
    if (len(task_list) == 0):
        print("The task list is empty!")
    else:
        if command == "task-cli list":
            print_tasks(task_list)
        else:
            argument = command.removeprefix("task-cli list ")
            if len(argument.split()) != 1:
                print("Error: Incorrect number of parameters!")
            else:
                filtered_list = []
                for task in task_list:
                    if task[3] == argument:
                        filtered_list.append(task)
                print_tasks(filtered_list)


def mark_task(command, task_list):
    argument = command.removeprefix("task-cli mark ")
    if len(argument.split()) != 2:
        print("Error: Incorrect number of parameters!")
    else:
        if ((argument.split()[0] == "in-progress") or (argument.split()[0] == "done")):
            try:
                id = int(argument.split()[1])
            except:
                print("Error: Invalid ID type!")
            id_found = False
            for task in task_list:
                if task[0] == id:
                    id_found = True
                    task[3] = argument.split()[0]
                    print("Task marked successfully!")
                    task[5] = datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S")
            if (not id_found):
                print("Error: ID not found!")
        else:
            print("Error: Invalid mark command")


def delete_task(command, task_list):
    argument = command.removeprefix("task-cli delete ")
    try:
        argument = int(argument)
    except:
        print("Error: Invalid argument for ID!")
    id_found = False
    for task in task_list:
        if task[0] == argument:
            id_found = True
            task_list.remove(task)
            print("Task deleted successfully!")
    if id_found == False:
        print("Error: ID not found!")


def update_task(command, task_list):
    argument = command.removeprefix("task-cli update ")
    if (len(argument.split()) != 2):
        print("Error: Incorrect number of parameters!")
    else:
        new_description = argument.split(" ", 1)[1]
        if ((new_description[0] == '"' and new_description[-1] == '"') or (new_description[0] == "'" and new_description[-1] == "'")):
            new_description = new_description[1:-1]
            id_found = False
            try:
                task_id = int(argument.split(" ", 1)[0])
            except:
                print("Error: You've entered an invalid ID!")
            for task in task_list:
                if task[0] == task_id:
                    id_found = True
                    task[2] = new_description
                    print("Description updated successfully!")
                    task[5] = datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S")
            if (not id_found):
                print("Error: ID not found!")
        else:
            print("Error: Invalid argument format!")


def save_task_list(task_list):
    file = open("task_list.json", "w")
    json.dump(task_list, file)
    file.close()


def get_last_id(task_list):
    id = 0
    for task in task_list:
        if task[0] > id:
            id = task[0]
    return id


def add_task(command, task_list):
    argument = command.removeprefix("task-cli add ")
    if ((argument[0] == '"' and argument[-1] == '"') or (argument[0] == "'" and argument[-1] == "'")):
        task_name = argument[1:-1]
        if len(task_list) == 0:
            task_id = 1
        else:
            task_id = get_last_id(task_list)+1
        task_description = input("Please add the task's description: ")
        task_status = "todo"
        task_creation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task_update_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task = [task_id, task_name, task_description,
                task_status, task_creation_date, task_update_date]
        task_list.append(task)
    else:
        print("Error: Invalid argument format!")


def load_task_list():
    file = open("task_list.json", "r")
    task_list = json.load(file)
    file.close()
    return task_list


def check_valid_command(text):
    # First, we evaluate if the text the user inputed starts with "task-cli"
    first_word = text.split(" ", 1)[0]
    # print(first_word)
    if (first_word != "task-cli" or len(text.split()) == 1):
        # We also make sure that it also includes more than one word
        return False
    else:
        valid_commands = ["add", "update", "delete", "mark", "list", "exit"]
        command = text.split(" ")[1]
        # Lastly, we make sure that the second word is included in the allowed commands
        if (command in valid_commands):
            return True
        else:
            return False


def display_menu():
    # Prints the command list
    print("*** Command List ***")
    print(""" - task-cli add "task_name"
 - task-cli update task_ID "new description"
 - task-cli delete task_ID
 - task-cli mark in-progress task_ID
 - task-cli mark done task_ID
 - task-cli list
 - task-cli list done
 - task-cli list todo
 - task-cli list in-progress
 - task-cli exit
          """)


def display_title(title):
    # Prints title between asterisk rows
    print(("*" * (len(title)+4)).center(100))
    print(("* " + title + " *").center(100))
    print(("*" * (len(title)+4)).center(100))


def main():
    try:
        # First, we try to load the task list JSON file
        task_list = load_task_list()
        print("Successfully loaded task list")
    except FileNotFoundError:
        # If it's not foumnd, we create a new file
        print("Task list file not found! Creating a new file...")
        task_list = []
    display_title("Task Tracker")
    exit = False
    while not exit:
        display_menu()
        user_input = input().lower()
        # We check if the user input is valid
        valid_command = check_valid_command(user_input)
        # print(valid_command)
        if (not valid_command):
            print("Error: Invalid input!")
        else:
            # command_type is the part of the commando that indicates the function. It removes "task-cli" and the other arguments from the user's input
            command_type = user_input.split()[1]
            match command_type:
                case "add":
                    add_task(user_input, task_list)
                case "update":
                    update_task(user_input, task_list)
                case "delete":
                    delete_task(user_input, task_list)
                case "mark":
                    mark_task(user_input, task_list)
                case "list":
                    list_tasks(user_input, task_list)
                case "exit":
                    exit = True
                case _:
                    print("Error: Invalid command!")
            input("Press enter to continue ")
            os.system("cls" if os.name == "nt" else "clear")
        # exit = True
    save_task_list(task_list)
    print("Saving changes...")
    print("App closed successfully!")


if __name__ == "__main__":
    main()
