from tkinter import *
import customtkinter as ctk
import tkintermapview 
import mysql.connector
from tkinter import messagebox
import tksheet as sheet
from datetime import datetime
import random

# Database Connection
# AdminPassword = input("Enter password to access the app: ")

AdminPassword_db = "lakshay24" # For testing purposes

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=AdminPassword_db,
    database="thecabco"
)

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("Cabco.")

app.resizable(False, False)

app_width = 600
app_height = 800

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x = (screen_width/2) - (app_width/2)
y = (screen_height/2) - (app_height/2)

app.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

bg = PhotoImage(file ="images/bg.png")
bg_label = Label(app, image = bg)
bg_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

#Booking Form
BookingFrame = ctk.CTkFrame(app,width=400, height=400,corner_radius=25,background_corner_colors=["#FAF8F5","#FAF8F5","#FAF8F5","#FAF8F5"],border_width=7,bg_color="#FFD33F",fg_color="#323231",border_color="#FFD33F")
BookingFrame.place(x=103, y=309)

logo = PhotoImage(file ="images/logo.png")
logo_label = Label(BookingFrame, image = logo)
logo_label.place(relx = 0.5, rely = 0.15, anchor = CENTER)
LoginLabel = ctk.CTkLabel(BookingFrame, text="User Login", font=('Poppins', 30, 'bold'), fg_color="#323231", text_color="#FFFFFF") 
LoginLabel.place(relx = 0.5, rely = 0.3, anchor = CENTER)

UserNameEntry = ctk.CTkEntry(master=BookingFrame, width=300,height=42,corner_radius=7, border_width=1,placeholder_text="Username")
UserNameEntry.place(relx=0.5, rely=0.48, anchor=CENTER)

PassEntry = ctk.CTkEntry(BookingFrame, width=300,height=42,corner_radius=7, border_width=1,placeholder_text="Password")
PassEntry.place(relx=0.5, rely=0.62, anchor=CENTER)

def bookacab():
    app.destroy()
    main = ctk.CTk()
    main.title("Cabco. - Book a Cab")

    main_width = 600
    main_height = 800

    screen_width = main.winfo_screenwidth()
    screen_height = main.winfo_screenheight()

    x = (screen_width/2) - (main_width/2)
    y = (screen_height/2) - (main_height/2)

    main.geometry(f"{main_width}x{main_height}+{int(x)}+{int(y)}")

    map_widget = tkintermapview.TkinterMapView(main, width=600, height=750, corner_radius=20)

    map_widget.place(relx=0.5, rely=0.7,anchor='center')
    
    map_widget.set_position(28.5459, 77.2732)

    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    def pickupPlaceMarker():
        map_widget.set_address(pickup.get())
        currentpickpos = map_widget.get_position()
        marker1 = map_widget.set_marker(currentpickpos[0],currentpickpos[1])
        return currentpickpos,marker1.position
        
    def dropPlaceMarker():
        map_widget.set_address(drop.get())
        currentdroppos = map_widget.get_position()
        marker2 = map_widget.set_marker(currentdroppos[0],currentdroppos[1])
        return currentdroppos,marker2.position

    def setpath():
        print(pickupPlaceMarker()[0],dropPlaceMarker()[0])
        map_widget.set_path([pickupPlaceMarker()[1],dropPlaceMarker()[1],pickupPlaceMarker()[0],dropPlaceMarker()[0]])

    booktext = ctk.CTkLabel(main, text="Book your Cab", font=('Poppins', 25, 'bold'), text_color="#FFD33F")
    booktext.place(relx=0.5, rely=0.05, anchor=CENTER)

    pickup = ctk.CTkEntry(master=main, width=360,height=40,corner_radius=7, border_width=1,placeholder_text="Pickup Location")
    pickup.place(relx=0.45, rely=0.12, anchor=CENTER)

    def pickupDestget():
        mysqlcursor = mydb.cursor()
        mysqlcursor.execute("Insert into booking (pickup_location,destination_location) values (%s,%s)",(pickup.get(),drop.get(),))
        return pickup.get(),drop.get()

    pickupEnter = ctk.CTkButton(main, text="Go",font=('Poppins',13,'bold'), width=70,height= 40,corner_radius=7, border_width=1,fg_color="#FFC500",text_color="#323231",hover_color="#FFD33F",command= lambda : [pickupPlaceMarker()])
    pickupEnter.place(relx=0.83, rely=0.12, anchor=CENTER)

    drop = ctk.CTkEntry(master=main, width=360,height=40,corner_radius=7, border_width=1,placeholder_text="Drop Location")
    drop.place(relx=0.45, rely=0.185, anchor=CENTER)

    dropEnter = ctk.CTkButton(main, text="Go",font=('Poppins',13, 'bold'), width=70,height= 40,corner_radius=7, border_width=1,fg_color="#FFC500",text_color="#323231",hover_color="#FFD33F",command=lambda : [dropPlaceMarker(),setpath(),pickupDestget()])

    dropEnter.place(relx=0.83, rely=0.185, anchor=CENTER)
    
    confirmbooking = ctk.CTkButton(main, text="Confirm Booking",font=('Poppins',15,'bold'), width=600,height=42,corner_radius=0, border_width=1,fg_color="#FFC500",text_color="#323231",hover_color="#FFD33F",command=  Userdetails)
    confirmbooking.place(relx=0.5, rely=0.975, anchor=CENTER)

    main.mainloop()

def Userdetails():

    userapp = ctk.CTk()
    userapp.title("Cabco. - User Mode")

    userapp_width = 600
    userapp_height = 800

    screen_width = userapp.winfo_screenwidth()
    screen_height = userapp.winfo_screenheight()

    x = (screen_width/2) - (userapp_width/2)
    y = (screen_height/2) - (userapp_height/2)

    userapp.geometry(f"{userapp_width}x{userapp_height}+{int(x)}+{int(y)}")
    
    paytext = ctk.CTkLabel(userapp, text="Payment Details", font=('Poppins', 30, 'bold'), text_color="#FFD33F")
    paytext.place(relx=0.5, rely=0.05, anchor=CENTER)

    payframe = ctk.CTkFrame(userapp,width=500, height=400,corner_radius=20,background_corner_colors=["#252424","#252424","#252424","#252424"],border_width=7,bg_color="#FFD33F",fg_color="#323231",border_color="#FFD33F")

    payframe.place(relx=0.5, rely=0.35, anchor=CENTER)

    amounttext = ctk.CTkLabel(payframe, text="Amount to be paid", font=('Poppins', 30, 'bold'), text_color="#FFFFFF")
    amounttext.place(relx=0.5, rely=0.1, anchor=CENTER)

    randmoney= round(random.uniform(30,999),2)

    setamount = ctk.CTkLabel(payframe, text=("INR",randmoney), font=('Poppins', 20), text_color="#A0FF55")
    setamount.place(relx=0.5, rely=0.2, anchor=CENTER)

    amountentry = ctk.CTkEntry(master=payframe, width=400,height=40,corner_radius=7, border_width=1,placeholder_text=randmoney,border_color="#FFD33F")
    amountentry.place(relx=0.5, rely=0.35, anchor=CENTER)

    radio_var = IntVar(value=0)

    choosebttn = ctk.CTkRadioButton(payframe, text="Cash", font=('Poppins', 15), text_color="#FFFFFF",variable=radio_var, value=0,hover_color="#FFD33F",fg_color="#FFD33F")
    choosebttn.place(relx=0.25, rely=0.48, anchor=CENTER)

    choosebttn2 = ctk.CTkRadioButton(payframe, text="UPI", font=('Poppins', 15), text_color="#FFFFFF",variable=radio_var, value=1,hover_color="#FFD33F",fg_color="#FFD33F")
    choosebttn2.place(relx=0.45, rely=0.48, anchor=CENTER)

    choosebttn3 = ctk.CTkRadioButton(payframe, text="Credit/Debit Card", font=('Poppins', 15), text_color="#FFFFFF",variable=radio_var, value=2,hover_color="#FFD33F",fg_color="#FFD33F")
    choosebttn3.place(relx=0.68, rely=0.48, anchor=CENTER)

    methodDetails = ctk.CTkEntry(master=payframe, width=400,height=40,corner_radius=7, border_width=1,placeholder_text="UPI ID | Credit/Debit Card Number | Cash Details",border_color="#FFD33F")
    methodDetails.place(relx=0.5, rely=0.62, anchor=CENTER)

    contactDetails = ctk.CTkEntry(master=payframe, width=400,height=40,corner_radius=7, border_width=1,placeholder_text="Phone No.| Email Address",border_color="#FFD33F")
    contactDetails.place(relx=0.5, rely=0.75, anchor=CENTER)

    def getamount():
        mysqlcursor = mydb.cursor()
        mysqlcursor.execute("Insert into BOOKING (fare) values (%s)",(amountentry.get(),))
        mysqlcursor.execute("Insert into payment (amount,date,payment_details,status) values (%s,%s,%s,%s)",(amountentry.get(),datetime.now(),methodDetails.get(),1))
        mysqlcursor.execute("Insert into customer (contact_details) values (%s)",(contactDetails.get(),))
        mydb.commit()
        return amountentry.get()

    def finalconfirmations():
        finalbooking = ctk.CTkToplevel(userapp)
        finalbooking.geometry("500x300")
        finalbooking.resizable(False, False)
        finalbooking.title("Cabco. - Booking Confirmed")
        cnfmlabel = ctk.CTkLabel(finalbooking, text="Booking Confirmed", font=('Poppins', 40, 'bold'), text_color="#FFD33F")

        cnfmlabel.place(relx=0.5, rely=0.2, anchor=CENTER)

        cnfmlabel2 = ctk.CTkLabel(finalbooking, text="Your booking has been confirmed. \nThank you for choosing Cabco.", font=('Poppins', 15), text_color="#FFFFFF")

        cnfmlabel2.place(relx=0.5, rely=0.5, anchor=CENTER)

        exitbttn = ctk.CTkButton(finalbooking, text="Exit",font=('Poppins',15,'bold'), width=400,height=42,corner_radius=7, border_width=1,fg_color="#FFC500",text_color="#323231",hover_color="#FFD33F",command = finalbooking.destroy)

        exitbttn.place(relx=0.5, rely=0.89, anchor=CENTER)

    confirmbooking = ctk.CTkButton(payframe, text="Book Now",font=('Poppins',15,'bold'), width=400,height=42,corner_radius=7, border_width=1,fg_color="#00CD82",text_color="#323231",hover_color="#009B62",command= lambda : [finalconfirmations(),print(getamount()),getamount()]) 
    confirmbooking.place(relx=0.5, rely=0.89, anchor=CENTER)


    # --------------------------------- Other Options ---------------------------------
    def aboutpg():
        aboutus = ctk.CTkToplevel(userapp)
        aboutus.title("About Us")
        aboutus.geometry("500x300")
        aboutus.resizable(False, False)
        aboutus.configure(bg="#323231")
        
        aboutuslabel = ctk.CTkLabel(aboutus, text="About Us", font=('Poppins', 30, 'bold'), text_color="#FFD33F")
        aboutuslabel.place(relx=0.5, rely=0.1, anchor=CENTER)

        aboutusframe = ctk.CTkFrame(aboutus,width=480, height=200,corner_radius=20,background_corner_colors=["#252424","#252424","#252424","#252424"],border_width=7,bg_color="#FFD33F",fg_color="#323231",border_color="#FFD33F")
        aboutusframe.place(relx=0.5, rely=0.57, anchor=CENTER)

        aboutusdata = ctk.CTkLabel(aboutusframe, text="About Page for Cabco., DBMS Group Project (179)", font=('Poppins',17), text_color="#FFFFFF")

        aboutusdata1 = ctk.CTkLabel(aboutusframe, text="Please Give us Five Stars for this project", font=('Poppins',17), text_color="#FFFFFF")

        aboutusdata.place(relx=0.5, rely=0.3, anchor=CENTER)
        aboutusdata1.place(relx=0.5, rely=0.5, anchor=CENTER)
        aboutus.mainloop()

#----------
    def previousrides():
        prevrides = ctk.CTkToplevel(userapp)
        prevrides.title("Previous Rides")

        prevrides.geometry("1180x720")

        prevrides.configure(bg="#323231")
            
        prevrideslabel = ctk.CTkLabel(prevrides, text="Previous Rides", font=('Poppins', 35, 'bold'), text_color="#FFD33F")
        prevrideslabel.place(relx=0.5, rely=0.1, anchor=CENTER)

        rideUserID = ctk.CTkEntry(master=prevrides, width=700,height=42,corner_radius=7, border_width=1,placeholder_text="Enter USER-ID",border_color="#FFD33F")
        rideUserID.place(relx=0.35, rely=0.2, anchor=CENTER)

        tksheet = sheet.Sheet(prevrides,theme="dark")
        tksheet.place(relx=0.5, rely=0.28,relheight=1,relwidth=0.95,anchor="n")

        def getdata():
            mycursor = mydb.cursor()

            if int(rideUserID.get()) >=100:
                Message.showinfo("Error","Invalid Username")
            else:
                mycursor.execute("SELECT r.Start_Time, b.Fare,b.Pickup_Location,b.Destination_Location,b.status_of_booking as Status_of_Booking, r.Distance, r.Rating FROM ride r LEFT JOIN booking b ON r.Booking_ID = b.Booking_ID WHERE r.User_ID = %s", (rideUserID.get(),))

                myresult = mycursor.fetchall()
                column_names = [i[0] for i in mycursor.description]
                tksheet.headers(column_names)
                tksheet.set_sheet_data(myresult)

        rideUsername_Entrybutton = ctk.CTkButton(prevrides,text="Enter",font=('Poppins',15,'bold'), width=250,height=42,corner_radius=7, border_width=1,fg_color="#FFE000",text_color="#323231",hover_color="#FECB1E",command=lambda: [getdata(),print(rideUserID.get())]) 
        rideUsername_Entrybutton.place(relx=0.8, rely=0.2, anchor=CENTER)

        prevrides.mainloop()

    otheropt = ctk.CTkLabel(userapp, text="Other Options", font=('Poppins', 30, 'bold'), text_color="#FFD33F")
    otheropt.place(relx=0.5, rely=0.65, anchor=CENTER)

    otheroptframe = ctk.CTkFrame(userapp,width=500, height=200,corner_radius=20,background_corner_colors=["#252424","#252424","#252424","#252424"],border_width=7,bg_color="#FFD33F",fg_color="#323231",border_color="#FFD33F")
    otheroptframe.place(relx=0.5, rely=0.82, anchor=CENTER)

    prevrides = ctk.CTkLabel(otheroptframe, text="Previous Rides", font=('Poppins', 20, 'bold'), text_color="#FFFFFF")
    prevrides.place(relx=0.27, rely=0.23, anchor=CENTER)

    prevridesbttn = ctk.CTkButton(otheroptframe, text="View Rides",font=('Poppins',15,'bold'), width=200,height=42,corner_radius=7, border_width=1,fg_color="#FFE000",text_color="#323231",hover_color="#FECB1E",command=previousrides) 
    prevridesbttn.place(relx=0.68, rely=0.23, anchor=CENTER)

    cancelride = ctk.CTkLabel(otheroptframe, text="Cancel Ride", font=('Poppins', 20, 'bold'), text_color="#FFFFFF")
    cancelride.place(relx=0.27, rely=0.48, anchor=CENTER)

    cancelridebttn = ctk.CTkButton(otheroptframe, text="Cancel",font=('Poppins',15,'bold'), width=200,height=42,corner_radius=7, border_width=1,fg_color="#FFE000",text_color="#323231",hover_color="#FECB1E",command=userapp.destroy)
    cancelridebttn.place(relx=0.68, rely=0.48, anchor=CENTER)

    aboutus = ctk.CTkLabel(otheroptframe, text="About Us", font=('Poppins', 20, 'bold'), text_color="#FFFFFF")
    aboutus.place(relx=0.27, rely=0.73, anchor=CENTER)
    
    aboutusbttn = ctk.CTkButton(otheroptframe, text="About",font=('Poppins',15,'bold'), width=200,height=42,corner_radius=7, border_width=1,fg_color="#FFE000",text_color="#323231",hover_color="#FECB1E",command=aboutpg)
    aboutusbttn.place(relx=0.68, rely=0.73, anchor=CENTER)

    userapp.mainloop()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def adminpg():
    app.destroy()
    adminpg = ctk.CTk()
    adminpg.title("Admin Page")
    adminpg_width = 500
    adminpg_height = 450
    screen_width = adminpg.winfo_screenwidth()
    screen_height = adminpg.winfo_screenheight()

    x = (screen_width / 2) - (adminpg_width / 2)
    y = (screen_height / 2) - (adminpg_height /2)

    adminpg.geometry("%dx%d+%d+%d" % (adminpg_width, adminpg_height, x, y))

    adminpglabel = ctk.CTkLabel(adminpg, text="Admin Page", font=('Poppins', 35, 'bold'), text_color="#FF6262")
    adminpglabel.place(relx=0.5, rely=0.07, anchor=CENTER)

    exitbttnadmin = ctk.CTkButton(adminpg, text="Exit",font=('Poppins',18,'bold'), width=250,height=45,corner_radius=6, border_width=1,fg_color="#FF4545",text_color="#FFFFFF",hover_color="#FF7F7F",command=adminpg.destroy)
    exitbttnadmin.place(relx=0.5, rely=0.93, anchor=CENTER)

    adminpgframe = ctk.CTkFrame(adminpg,width=450, height=300,corner_radius=20,background_corner_colors=["#252424","#252424","#252424","#252424"],border_width=7,bg_color="#FF6262",fg_color="#323231",border_color="#FF6262")


    adminpgframe.place(relx=0.5, rely=0.5, anchor=CENTER)

    def customerdetails():
        mycursor = mydb.cursor()
        customerdet = Toplevel(adminpg)
        customerdet.title("Customer Details")
        customerdet.geometry("1920x1080")
        customerdet.resizable(False, False)
        tksheet = sheet.Sheet(customerdet,theme='dark')

        tksheet.enable_bindings(("single_select", "row_select", "column_width_resize","copy","cut","paste","auto_resize_default_column_index","multi_select"))

        tksheet.pack(fill="both", expand=True)

        mycursor.execute("SELECT c.First_Name AS Customer_firstName, c.Last_Name AS Customer_lastName, c.Contact_Details AS Customer_PhoneNo, c.Address AS Customer_Address, d.First_Name AS Driver_firstName, d.Last_Name AS Driver_lastName,v.Registration_Number AS Vehicle_Reg_No, v.Type AS Vehicle_Type, v.Capacity AS Vehicle_Capacity, v.Model AS Vehicle_Model,b.Pickup_Location AS Pickup_Location, b.Destination_Location AS Destination_Location,b.fare as Trip_Fare FROM customer c JOIN booking b ON c.User_ID = b.User_ID JOIN driver d ON b.Driver_ID = d.Driver_ID JOIN vehicle v ON d.Driver_ID = v.Driver_ID")

        myresult = mycursor.fetchall()
        column_names = [i[0] for i in mycursor.description]
        tksheet.headers(column_names)
        tksheet.set_sheet_data(myresult)

        customerdet.mainloop()
    
    def ridedetails():
        mycursor = mydb.cursor()
        ridedet = Toplevel(adminpg)
        ridedet.title("Ride Details")
        ridedet.geometry("1920x1080")
        ridedet.resizable(False, False)
        tksheet = sheet.Sheet(ridedet,theme='dark')

        tksheet.enable_bindings(("single_select", "row_select", "column_width_resize","copy","cut","paste","auto_resize_default_column_index","multi_select"))

        tksheet.pack(fill="both", expand=True)

        mycursor.execute("SELECT r.Ride_ID, r.Start_Time, r.End_Time, r.Distance, r.Rating, b.Pickup_Location, b.Destination_Location, c.First_Name AS Customer_First_Name, c.Last_Name AS Customer_Last_Name, d.First_Name AS Driver_First_Name, d.Last_Name AS Driver_Last_Name FROM Ride r JOIN Booking b ON r.Booking_ID = b.Booking_ID JOIN Customer c ON r.User_ID = c.User_ID JOIN Driver d ON r.Driver_ID = d.Driver_ID;")

        myresult = mycursor.fetchall()
        column_names = [i[0] for i in mycursor.description]
        tksheet.headers(column_names)
        tksheet.set_sheet_data(myresult)

        ridedet.mainloop()

    def driverdetails():
        mycursor = mydb.cursor()
        driverdet = Toplevel(adminpg)
        driverdet.title("Driver Details")
        driverdet.geometry("1920x1080")
        driverdet.resizable(False, False)
        tksheet = sheet.Sheet(driverdet,theme='dark')

        tksheet.enable_bindings(("single_select", "row_select", "column_width_resize","copy","cut","paste","auto_resize_default_column_index","multi_select"))

        tksheet.pack(fill="both", expand=True)

        mycursor.execute("SELECT d.First_Name AS Driver_First_Name, d.Last_Name AS Driver_Last_Name, v.Registration_Number AS Vehicle_RegNo, v.Type AS Vehicle_Type, v.Capacity AS Vehicle_Capacity, v.Model AS Vehicle_Model FROM Driver d JOIN Vehicle v ON d.Driver_ID = v.Driver_ID;")

        myresult = mycursor.fetchall()
        column_names = [i[0] for i in mycursor.description]
        tksheet.headers(column_names)
        tksheet.set_sheet_data(myresult)

        driverdet.mainloop()


    def customquery():
        mycursor = mydb.cursor()
        customquerydet = Toplevel(adminpg)
        customquerydet.title("Custom Query")
        customquerydet.geometry("800x720")
        customquerydet.resizable(True, False)

        textbox = ctk.CTkTextbox(customquerydet, width=750, height=120, corner_radius=10, border_width=1, bg_color="#323231", fg_color="#323231", border_color="#FFFFFF", text_color="#FFE000", font=('Poppins', 15))
        textbox.insert(INSERT, "Enter your query here")
        textbox.bind("<Button-1>", lambda e: textbox.delete('1.0', END))
        textbox.place(relx=0.5, rely=0.1, anchor=CENTER)

        def customqueryexecute():
            qry = textbox.get("1.0",END)
            mycursor.execute(qry)
            myresult = mycursor.fetchall()
            column_names = [i[0] for i in mycursor.description]
            tksheet.headers(column_names)
            tksheet.set_sheet_data(myresult)

        tksheet = sheet.Sheet(customquerydet,theme='dark')

        tksheet.enable_bindings(("single_select", "row_select", "column_width_resize","copy","cut","paste","auto_resize_default_column_index","multi_select"))

        tksheet.place(x=0, y=220, relwidth=1, relheight=1)

        executebttn = ctk.CTkButton(customquerydet, text="Execute Query",font=('Poppins',15,'bold'), width=250,height=42,corner_radius=7, border_width=1,fg_color="#FFE000",text_color="#323231",hover_color="#FECB1E",command=lambda : [customqueryexecute()])
        executebttn.place(relx=0.5, rely=0.25, anchor=CENTER)

        customquerydet.mainloop()

    viewCustomerbttn = ctk.CTkButton(adminpgframe, text="View Customer Details",font=('Poppins',15,'bold'), width=300,height=44,corner_radius=7, border_width=1,fg_color="#FFE000",text_color="#323231",hover_color="#FECB1E",command=customerdetails)
    viewCustomerbttn.place(relx=0.5, rely=0.21, anchor=CENTER)

    viewRidesbttn = ctk.CTkButton(adminpgframe, text="View Ride Details",font=('Poppins',15,'bold'), width=300,height=44,corner_radius=7, border_width=1,fg_color="#FFE000",text_color="#323231",hover_color="#FECB1E",command=ridedetails)
    viewRidesbttn.place(relx=0.5, rely=0.38, anchor=CENTER)

    viewDriverbttn = ctk.CTkButton(adminpgframe, text="View Driver Details",font=('Poppins',15,'bold'), width=300,height=44,corner_radius=7, border_width=1,fg_color="#FFE000",text_color="#323231",hover_color="#FECB1E",command=driverdetails)
    viewDriverbttn.place(relx=0.5, rely=0.55, anchor=CENTER)

    customQuerybttn = ctk.CTkButton(adminpgframe, text="Custom Query",font=('Poppins',15,'bold'), width=300,height=44,corner_radius=7, border_width=1,fg_color="#FFE000",text_color="#323231",hover_color="#FECB1E",command=customquery)
    customQuerybttn.place(relx=0.5, rely=0.72, anchor=CENTER)

    adminpg.mainloop()

def login():
    if UserNameEntry.get() == "lakshay" and PassEntry.get() == "123" or UserNameEntry.get() == "user" or PassEntry.get() == "123" or UserNameEntry.get() == "alex" or PassEntry.get() == "biden69":
        print("Login Successful")
        UserNameEntry.delete(0,'end')
        PassEntry.delete(0,'end')
        bookacab()

    
    elif UserNameEntry.get() == "admin" or PassEntry.get() == "admin":
        print("Login Successful")
        UserNameEntry.delete(0,'end')
        PassEntry.delete(0,'end')
        adminpg()

    else:
        print("Login Failed")
        messagebox.showerror("Error", "Invalid Username or Password")

LoginButton = ctk.CTkButton(BookingFrame, text="Login", width=300,height=44,corner_radius=7, border_width=1,command=login,font=('Poppins',13, 'bold'),fg_color="#FFE000",text_color="#323231",hover_color="#FECB1E")
LoginButton.place(relx=0.5, rely=0.8, anchor=CENTER)

app.mainloop()