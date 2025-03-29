import os
import sqlite3

datasetPath = "dataset-resized"

# list all items in the dataset from the path
trashnetClasses = [item for item in os.listdir(datasetPath) if os.path.isdir(os.path.join(datasetPath, item))]

# map all the items in the files to their respective bins, compost will have to be done another way
mapping = {
    "cardboard": "Recycling",
    "compost": "Compost",
    "glass": "Recycling",  
    "metal": "Recycling",
    "paper": "Recycling",
    "plastic": "Recycling",
    "trash": "Garbage",
}

# connect and make a cursor for the dataset
conn = sqlite3.connect("wasteItems.db")
cursor = conn.cursor()

# create the table 
cursor.execute('''
CREATE TABLE IF NOT EXISTS wasteItems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    itemName TEXT UNIQUE,
    bin TEXT
)
''')

# insert the data into the table
for className in trashnetClasses:
    # get the bin type from the hashmap
    binType = mapping.get(className.lower(), "Unknown")
    # insert the className and binType into the database if it doesn't already exist in that order
    cursor.execute("INSERT OR IGNORE INTO wasteItems (itemName, bin) VALUES (?,?)", (className, binType))
    print(f"Added {className} to {binType} bin")

# commit the changes and close the connection
conn.commit()
conn.close()

print("finished creating the database")