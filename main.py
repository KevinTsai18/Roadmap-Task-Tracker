import json
import os


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
 - task-cli exit""")


def display_title(title):
    # Prints title between asterisk rows
    print(("*" * (len(title)+4)).center(100))
    print(("* " + title + " *").center(100))
    print(("*" * (len(title)+4)).center(100))


def main():
    display_title("Task Tracker")
    exit = False
    while not exit:
        display_menu()
        exit = True


if __name__ == "__main__":
    main()
