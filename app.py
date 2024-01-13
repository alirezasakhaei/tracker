import json
import datetime
import argparse
import texttable


feasable_kinds = ["record", "routine"]
feasable_commands = ["quit", "add", "remove", "insert"]

def create():
    print("Creating")
    database = {}

    # Get today's date
    today = datetime.date.today()

    # Get the end date of 2024
    end_date = datetime.date(2024, 12, 31)

    # Iterate over each day from today until the end of 2024
    current_date = today
    while current_date <= end_date:
        # Create a dictionary for each day
        day_data = {}
        day_data["routine"] = {}
        day_data["record"] = {}
        # Set the value for the current date key in the main dictionary
        database[str(current_date)] = day_data

        # Increment the current date by one day
        current_date += datetime.timedelta(days=1)

    # Print the created database
    print(database)

    # Save the database to a JSON file
    with open("data.json", "w") as file:
        json.dump(database, file, indent=4)

def get_last_date(database):
    last_date = None
    for date in database:
        current_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        if last_date is None or current_date > last_date:
            last_date = current_date
    return last_date

def insert(user_input):

    # Load the database
    with open("data.json", "r") as file:
        database = json.load(file)

    # Get the last date from the database
    last_date = get_last_date(database)

    # Get the date to insert the record or routine
    date = user_input.split(" ")[1]
    if date == "today":
        date = datetime.date.today()
    elif date == "yesterday":
        date = datetime.date.today() - datetime.timedelta(days=1)
    else:
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

    # Check if the date is valid
    if date < datetime.date.today() or date > last_date:
        print("Invalid date")
        return

    # Get the kind of the record or routine
    kind = user_input.split(" ")[2]
    if not kind in feasable_kinds:
        print("Invalid kind")
        return

    # Get the name of the record or routine
    name = user_input.split(" ")[3]
    if not name in list(database[str(date)][kind].keys()):
        print(f"Invalid {kind}")
        return
    
    # Get the value of the record or routine
    if kind == "record":
        try:
            value = int(user_input.split(" ")[4])
        except:
            print("Invalid value")
            return
    elif kind == "routine":
        try:
            value = bool(user_input.split(" ")[4])
        except:
            print("Invalid value")
            return

    # Insert the record or routine to the database
    database[str(date)][kind][name] = value

    # Save the updated database to the JSON file
    with open("data.json", "w") as file:
        json.dump(database, file, indent=4)

def add(user_input):
    today = datetime.date.today()
    kind = user_input.split(" ")[1] # record or routine
    if not kind in feasable_kinds:
        print("Invalid kind")
        return
    name = user_input.split(" ")[2]
    if kind == "record":
        default_value = 0
    elif kind == "routine":
        default_value = False
    
    # Load the database
    with open("data.json", "r") as file:
        database = json.load(file)
    
    # Get the last date from the database
    last_date = get_last_date(database)
    
    # Add the new record or routine to each day in the database
    current_date = today   
    while current_date <= last_date:
        database[str(current_date)][kind][name] = default_value
        current_date += datetime.timedelta(days=1)
    
    # Save the updated database to the JSON file
    with open("data.json", "w") as file:
        json.dump(database, file, indent=4)

def remove(user_input):
    today = datetime.date.today()
    kind = user_input.split(" ")[1] # record or routine
    if not kind in feasable_kinds:
        print("Invalid kind")
        return
    name = user_input.split(" ")[2]
    with open("data.json", "r") as file:
        database = json.load(file)
    last_date = get_last_date(database)
    current_date = today

    # remove the record or routine from each day in the database
    while current_date <= last_date:
        database[str(current_date)][kind].pop(name)
        current_date += datetime.timedelta(days=1)

    # save the updated database to the JSON file    
    with open("data.json", "w") as file:
        json.dump(database, file, indent=4)

    print(f'{name} {kind} removed from all days in the database. If you want to add it again, use "add {kind} {name}')

def help():
    print('''
    add record <name>
    add routine <name>
    insert <date> record <name> <value>
    insert <date> routine <name> <value>
    remove <record/routine> <name>
    report <date>
    report today
    report yesterday
    report
    quit
    ''')

def shortcut(user_input):
    # Load the database
    with open("data.json", "r") as file:
        database = json.load(file)
    
    # Check if only one routine or record starts with the first word
    first_word = user_input.split(" ")[0]
    count = 0

    selected_kind = None
    selected_name = None

    today = str(datetime.date.today())
    for kind in database[today].keys():
        for name in database[today][kind].keys():
            if name.startswith(first_word):
                count += 1
                selected_kind = kind
                selected_name = name
    
    if count == 1:
        try:
            value = user_input.split(" ")[1]
        except:
            if selected_kind == "routine":
                value = True
        
        if not isinstance(value, bool):
        
            if selected_kind == "record":
                value = int(value)
            elif selected_kind == "routine":
                if value.lower() in ['true', '1']:
                    value = True
                elif value.lower() in ['false', '0']:
                    value = False
                else:
                    raise Exception('invalid value')

    else:
        print("Invalid shortcut")
        return
    
    database[today][selected_kind][selected_name] = value
    
    # Save the updated database to the JSON file
    with open("data.json", "w") as file:
        json.dump(database, file, indent=4)



# ...

def report(user_input):
    try:
        date = user_input.split(" ")[1]
        if date == "today":
            date = datetime.date.today()
        elif date == "yesterday":
            date = datetime.date.today() - datetime.timedelta(days=1)
        else:
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    except:
        date = datetime.date.today()
    
    # Load the database
    with open("data.json", "r") as file:
        database = json.load(file)
    
    # Check if the date is valid
    if date < datetime.date.today() or date > get_last_date(database):
        print("Invalid date")
        return
    
    # Create a table for the report
    table = texttable.Texttable()
    table.set_cols_align(["l", "r"])
    table.set_cols_valign(["t", "m"])
    table.add_row(["Report for", str(date)])
    
    for kind in database[str(date)].keys():
        table.add_row([f"{kind}s:", ""])
        for name in database[str(date)][kind].keys():
            table.add_row([f"  {name}:", str(database[str(date)][kind][name])])
    
    # Print the formatted table
    print(table.draw())




def run():
    print("Welcome to the tracker app Alireza!")
    print("I wish you a productive and happy day :)")
    
    while True:
        try:
            user_input = input("Enter command: ")
            command = user_input.split(" ")[0]

            if command == "add":
                add(user_input)
            elif command == "insert":
                insert(user_input)
            elif command == "quit":
                break
            elif command == "report":
                report(user_input)
            elif command == 'remove':
                remove(user_input)
            elif command == 'help':
                help()
            else:
                shortcut(user_input)
        except Exception as e:
            print(e)
            print("Invalid command")
            continue

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--create", action="store_true", help="create or run")
    args = parser.parse_args()
    if args.create:
        create()
    else:
        run()



if __name__ == '__main__':
    main()