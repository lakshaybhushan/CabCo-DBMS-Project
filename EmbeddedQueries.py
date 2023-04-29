import mysql.connector
from prettytable import PrettyTable

db_connection = mysql.connector.connect(
  host = "localhost",
  user = "root",
  passwd = "lakshay24",
  database = "thecabco"
  )
FLAG = True # Creating a flag variable to run the program in a loop

print('''

            _____ _  _ ___    ___   _   ___    ___ ___             
  ___ ___  |_   _| || | __|  / __| /_\ | _ )  / __/ _ \    ___ ___ 
 |___|___|   | | | __ | _|  | (__ / _ \| _ \ | (_| (_) _  |___|___|
             |_| |_||_|___|  \___/_/ \_|___/  \___\___(_)          
                                             
''')

if db_connection.is_connected():
    print(">> Status >> : Database is successfully connected\n")
mycursor = db_connection.cursor()

while FLAG:

  print("Select the query you want to run: \n")
  print("Query 1: To Show details of the bookings made by customers who have a first name starting with the letter '_' and a fare greater than or equal to ____:\n")
  print("Query 2: To show the details of all drivers who have completed at least one ride with a rating Greater than __:\n")
  print("Query 3: OLAP QUERIES:\n")
  print("Query 4: Check Triggers:\n")

  query = int(input("Enter the query number: "))

  if query == 1:
    name = input("Enter the first letter from first name of the customer: ")
    fare = input("Enter the fare: ")
    mycursor.execute("SELECT Booking.*, Customer.First_Name, Customer.Last_Name FROM Booking JOIN Customer ON Booking.Customer_Id = Customer.User_ID WHERE Customer.First_Name LIKE %s AND Booking.fare >= %s", (name+'%', fare))
    table = PrettyTable()
    table.field_names = [i[0] for i in mycursor.description]
    for row in mycursor:
      table.add_row(row)
    print(table)

  elif query == 2:
    rating = float(input("Enter the minimum rating: "))
    if rating > 5:
      print("Invalid rating. Please enter a rating between 0 and 5.")
    else:
      mycursor.execute("SELECT Driver.First_Name, Driver.Last_Name, AVG(Ride.Rating) AS Avg_Rating FROM Driver INNER JOIN Booking ON Driver.Driver_ID = Booking.Driver_ID INNER JOIN Ride ON Booking.Booking_ID = Ride.Booking_ID GROUP BY Driver.Driver_ID HAVING AVG(Ride.Rating) > %s", (rating,))
      table = PrettyTable()
      table.field_names = ["First Name", "Last Name", "Average Rating"]
      for row in mycursor:
        table.add_row(row)
      print(table)
    
  elif query == 3:
      print("1. To retrieve the total amount paid by each customer who has made a payment, sorted in descending order of the total amount, and filtered by payment status.")

      print("2. To calculate the average rating received by each driver based on their ride history.")

      print("3. To show the total fare earned by each driver who has accepted cash or UPI payment, grouped by payment mode.")

      print("4. To show the total distance traveled by each customer based on their ride history, grouped by customer.")

      print("Enter the OLAP query number: ")

      olap_query = int(input())
      
      if olap_query == 1:
        mycursor.execute("SELECT Customer.User_ID, Customer.First_Name, Customer.Last_Name, Payment.Status, SUM(Payment.Amount) AS Total_Amount FROM Customer JOIN Booking ON Customer.User_ID = Booking.User_ID JOIN Ride ON Booking.Booking_ID = Ride.Booking_ID JOIN Payment ON Ride.Ride_ID = Payment.Ride_ID WHERE Payment.Status = 1 GROUP BY Customer.User_ID, Customer.First_Name, Customer.Last_Name, Payment.Status with rollup ORDER BY Total_Amount DESC;")

        table = PrettyTable()
        table.field_names = [i[0] for i in mycursor.description]
        for row in mycursor:
          table.add_row(row)
        print(table)

      elif olap_query == 2:
        mycursor.execute("SELECT Driver.Driver_ID, AVG(Ride.Rating) AS Avg_Rating FROM Driver INNER JOIN Ride ON Driver.Driver_ID = Ride.Driver_ID GROUP BY Driver.Driver_ID with rollup;")

        table = PrettyTable()
        table.field_names = [i[0] for i in mycursor.description]
        for row in mycursor:
          table.add_row(row)
        print(table)

      elif olap_query == 3:
        mycursor.execute("SELECT Driver.First_Name, Driver.Last_Name, Modes_of_Payment.Payment_ID, SUM(Booking.Fare) AS Total_Fare FROM Driver JOIN Booking ON Driver.Driver_ID = Booking.Driver_ID JOIN Modes_of_Payment ON Booking.Booking_ID = Modes_of_Payment.Booking_ID WHERE Modes_of_Payment.Cash = 1 OR Modes_of_Payment.Upi = 1 GROUP BY Driver.First_Name, Driver.Last_Name, Modes_of_Payment.Payment_ID with rollup;")

        table = PrettyTable()
        table.field_names = [i[0] for i in mycursor.description]
        for row in mycursor:
          table.add_row(row)
        print(table)

      elif olap_query == 4:
        mycursor.execute("SELECT Customer.First_Name, Customer.Last_Name, SUM(Ride.Distance) AS Total_Distance FROM Customer JOIN Booking ON Customer.User_ID = Booking.User_Id JOIN Ride ON Booking.Booking_ID = Ride.Booking_ID GROUP BY Customer.First_Name, Customer.Last_Name with rollup;")

        table = PrettyTable()
        table.field_names = [i[0] for i in mycursor.description]
        for row in mycursor:
          table.add_row(row)
        print(table)

  elif query == 4:
    print("1. A trigger named Ride_Rating which enforces a constraint on ride rating to be between 0 and 5.")
    print("2. A trigger named Check_payment_mode which ensures atleast one payment mode is selected.")

    print("Enter the trigger number: ")

    trigger_query = int(input())

    if trigger_query == 1:

      checktrigger = int(input())


      if checktrigger == 1:
        print("If you enter a rating greater than 5, the trigger will set the value to 5.")

        mycursor.execute("INSERT INTO Ride (Rating, Start_Time, End_Time, Distance, Booking_ID) VALUES (7, '2023-03-26 10:00:00', '2023-03-26 11:00:00', 10.44, 338);")

        mycursor.execute("SELECT * FROM Ride WHERE Ride_ID = 338;")
        table = PrettyTable()
        table.field_names = [i[0] for i in mycursor.description]
        for row in mycursor:
          table.add_row(row)
        print(table)

      elif checktrigger == 2:
        print("If you enter a rating less than 0, the trigger will set the value to 0.")

        mycursor.execute("INSERT INTO Ride (Rating, Start_Time, End_Time, Distance, Booking_ID) VALUES (-5, '2023-04-21 01:12:23', '2023-04-21 07:34:35', 34.33, 339);")

        mycursor.execute("SELECT * FROM Ride WHERE Ride_ID = 339;")

        table = PrettyTable()
        table.field_names = [i[0] for i in mycursor.description]
        for row in mycursor:
          table.add_row(row)
        print(table)

    elif trigger_query == 2:
      print(" If you do not select any payment mode, the trigger will set the value of Cash to 1.")
      mycursor.execute("INSERT INTO Modes_of_Payment (Booking_ID, Cash, Upi, NetBanking, Debit_Credit) VALUES (6, 0, 1, 0, 0);")
      mycursor.execute("SELECT * FROM Modes_of_Payment WHERE Payment_ID = 6;")
      table = PrettyTable()
      table.field_names = [i[0] for i in mycursor.description]
      for row in mycursor:
        table.add_row(row)
      print(table)

  # An Update Query (if time permits)
  else:
    print("Invalid query number.. Please Try Again !!")
  
  ask = input("Do you want to continue? (Y/N): ")
  if ask.lower() != "y":
    break 