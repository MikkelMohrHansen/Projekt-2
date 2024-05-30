# Connecting to mysql database
import mysql.connector
import matplotlib.pyplot as plt

mydb = mysql.connector.connect(
                                host="localhost",
                                port="3306",   
                                user="user", 
                                password="PASSWORD", 
                                database="LogunitDB")

mycursor = mydb.cursor()

# Fetching data from mysql to python
mycursor.execute("SELECT studentID, lokaleID, checkIn FROM Checkind")
result = mycursor.fetchall()

lokaleID = []
studentID = []
checkIn = []

for i in result:
    lokaleID.append(i[0])
    studentID.append(i[1])
    checkIn.append(i[2])

# Figure and axis
fig, ax = plt.subplots()

# Hide axes
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.set_frame_on(False)

# Create table
table_data = list(zip(lokaleID, studentID, checkIn))
column_labels = ["Student ID", "Lokale ID", "Check ind tidspunkt: "]

# Add table to the figure
table = ax.table(cellText=table_data, colLabels=column_labels, cellLoc='center', loc='center')

# Adjust table scale
table.scale(1, 1.5)

# Set the title
plt.title("Studerende info")

# Show plot
plt.savefig('checkind/data.png')