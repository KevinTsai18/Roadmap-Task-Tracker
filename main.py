import json
import os


def add_task(command, list):


def load_task_list():
    file = open("tasklist.json", "r")
    task_list = json.load(file)
    file.close()
    return task_list


def check_valid_command(text):
    # First, we evaluate if the text the user inputed contains "task-cli" as its first word
    first_word = text.split(" ", 1)[0]
    # print(first_word)
    if (first_word != "task-cli" or len(text.split()) == 1):
        return ("invalid")
    else:
        valid_commands = ["add", "update", "delete", "mark", "list", "exit"]
        command = text.split(" ")[1]
        if (command in valid_commands):
            return command
        else:
            return ("invalid")


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
        task_list = load_task_list()
        print("Successfully loaded task list")
    except FileNotFoundError:
        print("Task list file not found! Creating a new file...")
        task_list = []
    display_title("Task Tracker")
    exit = False
    while not exit:
        display_menu()
        user_input = input().lower()
        valid_command = check_valid_command(user_input)
        # print(valid_command)
        if (valid_command == "invalid"):
            print("Error: Invalid command!")
        else:
            if valid_command.startswith("add"):
                add_task(valid_command, task_list)
        exit = True


if __name__ == "__main__":
    main()
