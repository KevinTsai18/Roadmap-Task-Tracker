import json
import os
import datetime


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
        print("Error: Invalid argument!")


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
 - task-cli update task_ID
 - task-cli delete task_ID
 - task-cli mark todo
 - task-cli mark in-progress
 - task-cli mark done
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
        print(valid_command)
        if (not valid_command):
            print("Error: Invalid input!")
        else:
            command_type = user_input.split()[1]
            match command_type:
                case "add":
                    add_task(user_input, task_list)
                case "exit":
                    exit = True
                case _:
                    print("Error: Invalid command!")
            input("Press enter to continue ")
            os.system("cls" if os.name == "nt" else "clear")
        exit = True
    save_task_list(task_list)
    print("Saving changes...")
    print("App closed successfully!")


if __name__ == "__main__":
    main()
