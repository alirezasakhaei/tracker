import json
import os


def main():
    while True:
    user_input = input("Enter a command: ")
    command = user_input.split()[0]

    if command == "add":
      word = user_input.split()[1]
      # Load existing data from JSON file
      if os.path.exists("data.json"):
        with open("data.json", "r") as file:
          data = json.load(file)
      else:
        data = []

      # Add the word to the data list
      data.append(word)

      # Save the updated data to JSON file
      with open("data.json", "w") as file:
        json.dump(data, file)

    
  
