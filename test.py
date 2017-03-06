"""Test File to check possibilty"""
import sys
import json
import os
from pathlib import Path
import uuid
import time
from terminaltables import AsciiTable

DATA = []


def init():
    """init function"""

    datafile = Path("data.json")
    if not datafile.is_file():
        print(
            "File data.json doesnt exist. Creating a new data.json for future use"
        )
        empty = []
        with open('data.json', 'x') as data_file:
            json.dump(empty, data_file)

    datafile = Path("completed.json")
    if not datafile.is_file():
        print(
            "File completed.json doesnt exist. Creating a new data.json for future use"
        )
        empty = []
        with open('completed.json', 'x') as data_file:
            json.dump(empty, data_file)

    if os.stat("data.json").st_size == 0:
        print("Data file empty")
        print("Entering emtpy array as data in the file for future use")
        empty = []
        with open('data.json', 'w') as data_file:
            json.dump(empty, data_file)

    with open('data.json', 'r') as data_file:
        DATA.extend(json.load(data_file))

    if len(DATA) == 0:
        print("No previous task")


def createtask():
    """creates new task"""

    #generate an empty task dict
    task = {}
    #generating a uuid for each task. uuid4 generates a random uuid
    task['id'] = str(uuid.uuid4())
    task['name'] = input("\nEnter the task name\n")
    task['description'] = input("\nEnter the description\n")
    task['priority'] = -1
    while task['priority'] < 0:
        task['priority'] = int(input("\nEnter the priority\n"))
        if task['priority'] < 0:
            print("Enter a non negatvie priority")
    task['start_time'] = time.asctime(time.localtime(time.time()))
    task['end_date'] = ""
    #append the task dict to DATA array
    DATA.append(task)


def writetofile():
    """writes back to the data file by removing previous content and entering new one"""

    with open('data.json', 'w') as data_file:
        json.dump(DATA, data_file)


def displaycurrentlist():
    """displays the list of incomplete task"""
    table_data = [["Priority", "Description", "Name", "Start Time"]]
    DATA.sort(key=lambda tuple: tuple["priority"])
    for task in DATA:
        table_row = [
            task["priority"], task["description"], task["name"],
            task["start_time"]
        ]
        table_data.append(table_row)
    table = AsciiTable(table_data)
    print(table.table)


def order(param1, param2):
    """replaces the task at priority param1 with task at priority param2"""
    for task in DATA:
        if task['priority'] == param1:
            task['priority'] = param2
        elif task['priority'] == param2:
            task['priority'] = param1
    writetofile()


def setcomplete(param):
    """sets the task of priority param as complete and saves the task in the file"""
    temptask = 0
    for task in DATA:
        if task['priority'] == param:
            temptask = task
            DATA.remove(task)
    writetofile()

    temptask["end_data"] = time.asctime(time.localtime(time.time()))
    completed = []
    with open('data.json', 'r') as data_file:
        completed.extend(json.load(data_file))
    completed.append(temptask)
    with open('completed.json', 'w') as data_file:
        json.dump(DATA, data_file)


if __name__ == '__main__':
    init()
    if sys.argv[1] == "list":
        displaycurrentlist()
    elif sys.argv[1] == "create":
        createtask()
        writetofile()
        displaycurrentlist()
    elif sys.argv[1] == "order":
        order(int(sys.argv[2]), int(sys.argv[3]))
    elif sys.argv[1] == "complete":
        setcomplete(int(sys.argv[2]))
