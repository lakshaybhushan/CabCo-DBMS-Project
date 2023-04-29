USE thecabco;

-- TRIGGER 1 --
DELIMITER $$
CREATE TRIGGER TR_Ride_Rating
BEFORE INSERT ON Ride
FOR EACH ROW
BEGIN
    IF NEW.Rating < 0 THEN
        SET NEW.Rating = 0;
    ELSEIF NEW.Rating > 5 THEN
        SET NEW.Rating = 5;
    END IF;
END$$
DELIMITER ;

-- QUERIES TO CHECK WHETHER THE TRIGGER IS WORKING OR NOT --
INSERT INTO Ride (Rating, Start_Time, End_Time, Distance, Booking_ID)
VALUES (7, '2023-03-26 10:00:00', '2023-03-26 11:00:00', 10.44, 338);

INSERT INTO Ride (Rating, Start_Time, End_Time, Distance, Booking_ID)
VALUES (-5, '2023-04-21 01:12:23', '2023-04-21 07:34:35', 34.33, 339);

-- TRIGGER 2 -- 
DELIMITER $$
CREATE TRIGGER check_payment_mode
BEFORE INSERT ON Modes_of_Payment
FOR EACH ROW
BEGIN
    IF NOT (NEW.NetBanking = 1 OR NEW.UPI = 1 OR NEW.Debit_Credit = 1) THEN
        SET NEW.Cash = 1;
    END IF;
END $$
DELIMITER ;

-- QUERY TO CHECK WHETHER THE TRIGGER IS WORKING OR NOT --
INSERT INTO Modes_of_Payment (Booking_ID, Cash, Upi, NetBanking, Debit_Credit) 
VALUES (6, 0, 1, 0, 0);

-- OLAP Queries -- 

-- # 1 --
-- To retrieve the total amount paid by each customer who has made a payment, sorted in descending order of the total amount, and filtered by payment status.
SELECT Customer.User_ID, Customer.First_Name, Customer.Last_Name, Payment.Status, SUM(Payment.Amount) AS Total_Amount
FROM Customer
JOIN Booking ON Customer.User_ID = Booking.User_ID
JOIN Ride ON Booking.Booking_ID = Ride.Booking_ID
JOIN Payment ON Ride.Ride_ID = Payment.Ride_ID
WHERE Payment.Status = 1
GROUP BY Customer.User_ID, Customer.First_Name, Customer.Last_Name, Payment.Status with rollup
ORDER BY Total_Amount DESC;

-- # 2 -- 
-- To calculate the average rating received by each driver based on their ride history
SELECT Driver.Driver_ID, AVG(Ride.Rating) AS Avg_Rating
FROM Driver
INNER JOIN Ride ON Driver.Driver_ID = Ride.Driver_ID
GROUP BY Driver.Driver_ID with rollup;

-- # 3 -- 
-- To show the total fare earned by each driver who has accepted cash or UPI payment, grouped by payment mode.
SELECT Driver.First_Name, Driver.Last_Name, Modes_of_Payment.Payment_ID, SUM(Booking.Fare) AS Total_Fare
FROM Driver
JOIN Booking ON Driver.Driver_ID = Booking.Driver_ID
JOIN Modes_of_Payment ON Booking.Booking_ID = Modes_of_Payment.Booking_ID
WHERE Modes_of_Payment.Cash = 1 OR Modes_of_Payment.Upi = 1
GROUP BY Driver.First_Name, Driver.Last_Name, Modes_of_Payment.Payment_ID with rollup;

-- # 4 -- 
-- to show the total distance traveled by each customer based on their ride history, grouped by customer.
SELECT Customer.First_Name, Customer.Last_Name, SUM(Ride.Distance) AS Total_Distance
FROM Customer
JOIN Booking ON Customer.User_ID = Booking.User_Id
JOIN Ride ON Booking.Booking_ID = Ride.Booking_ID
GROUP BY Customer.First_Name, Customer.Last_Name with rollup;



drop trigger check_payment_mode;
drop trigger TR_Ride_Rating;

