import mysql.connector as mysql
from datetime import datetime, timedelta

class StudentTable:
    def __init__(self):
        self.db = mysql.connect(
            host="79.171.148.163",
            user="user",
            passwd="MaaGodt*7913!",
            database="LogunitDB"
        )
        self.mycursor = self.db.cursor(dictionary=True)
        print("Connected to database")

    def get_attend_table(self, uddannelses_Hold_ID):
        # Get today's date
        today_date = datetime.now().date()

        # Combined query to get all required data
        query = """
        SELECT s.navn, s.opstartsDato, 
               COUNT(c.studentID) AS antal,
               MAX(CASE WHEN DATE(c.checkin) = %s THEN c.checkin ELSE NULL END) AS checked_in_today_timestamp
        FROM Students s
        LEFT JOIN Checkind c ON s.studentID = c.studentID
        WHERE s.uddannelseID = %s
        GROUP BY s.studentID, s.navn, s.opstartsDato
        """
        self.mycursor.execute(query, (today_date, uddannelses_Hold_ID))
        result = self.mycursor.fetchall()

        today = datetime.now().date()
        attendance_table = []

        for row in result:
            navn = row['navn']
            start_date = row['opstartsDato']
            antal = row['antal']
            checked_in_today_timestamp = row['checked_in_today_timestamp']
            days_difference = self.count_weekdays(start_date, today)
            attendance_percentage = (days_difference - antal) / days_difference * 100 if days_difference > 0 else 0
            checked_in_today = 1 if checked_in_today_timestamp is not None else 0

            attendance_table.append({
                'navn': navn,
                'attendance_percentage': attendance_percentage,
                'checked_in_today': checked_in_today,
                'checked_in_today_timestamp': checked_in_today_timestamp.time() if checked_in_today_timestamp else None
            })

        return attendance_table

    def count_weekdays(self, start_date, end_date):
        # Ensure start_date is before end_date
        if start_date > end_date:
            return 0

        weekdays_count = 0

        # Loop through each day from start_date to end_date
        while start_date <= end_date:
            # Check if start_date is a weekday (Monday to Friday)
            if start_date.weekday() < 5:
                weekdays_count += 1

            # Move to the next day
            start_date += timedelta(days=1)

        return weekdays_count

# Example usage
if __name__ == "__main__":
    table = StudentTable()
    uddannelses_Hold_ID = 1  # Replace with the desired educational group ID

    # Get the attendance table
    attendance_table = table.get_attend_table(uddannelses_Hold_ID)

    # Print the attendance table
    print("Attendance Table:")
    for entry in attendance_table:
        print(f"Navn: {entry['navn']}, Attendance Percentage: {entry['attendance_percentage']:.2f}%, Checked In Today: {entry['checked_in_today']}, Checked In Today Timestamp: {entry['checked_in_today_timestamp']}")
