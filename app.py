# from Flask website
# run, will see output in http://localhost:5000/

#cd C:\Users\Anya\Documents\!School\CISC332\make-website
# to get requirements, cd into there and type "setup.cmd"

from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.mysql import MySQL
from datetime import datetime, date
import random
app = Flask(__name__)
mysql = MySQL()
app.secret_key = 'SUSHI'
from random import randint
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root' # user Anna probably has a password?
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'ktowncarshare2'
app.config['MYSQL_DATABASE_HOST'] = 'localhost' # this machine
mysql.init_app(app)

# #connect to db
conn = mysql.connect()

# #create cursor to query db
cursor = conn.cursor()


@app.route("/") # when someone visits slash http://localhost:5000/ on your webpage, run this method
def hello():
    session['email'] = None
    session['FName'] = None
    session['isAdmin'] = None
    return redirect(url_for('homepage'))

# @app.route("/index/") # when someone visits http://localhost:5000/index/, run this method
# @app.route("/index/<name>")
# def hello2(name="no name given"):
#     #return "<h1>Hello World again!</h1>"
#     return render_template("index.html", name=name)
#     #http://localhost:5000/index/goldfish will print "hello goldfish"

@app.route("/homepage") # when someone visits slash http://localhost:5000/ on your webpage, run this method
def homepage():
    if session['email'] == None:
        return render_template("index_homepage.html", firstName = None)
    elif session['isAdmin'] == 1:
        return redirect(url_for("welcome_admin"))
    elif session['isAdmin'] == 0:
        return redirect(url_for("welcome_member"))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html', firstName = None)
    elif request.method == 'POST':
        email = request.values.get('inputEmail')
        password = request.values.get('inputPassword')

        sql = "SELECT FName, isAdmin from member where email=%s and password=%s"
        cursor.execute(sql, (email, password))
        data = cursor.fetchone() 

        if data == None:
            return render_template('signin.html', errorMessage="Username or password incorrect. Please try again.", firstName = None)
        else:
            # set cookies for email and first name and admin
            session['email'] = email
            session['FName'] = data[0]
            session['isAdmin'] = data[1]

        if session['isAdmin'] == 0:
            return redirect(url_for('welcome_member'))
        else:
            return redirect(url_for('welcome_admin'))



@app.route('/member/welcome')
def welcome_member():
    if session['isAdmin'] == 0:
        return render_template('welcome_member.html', firstName = session['FName'])
    else:
        return render_template('welcome_admin.html', firstName = session['FName'])

@app.route('/admin/welcome')
def welcome_admin():
    if session['isAdmin'] == 0:
        return render_template('welcome_member.html', firstName = session['FName'])
    else:
        return render_template('welcome_admin.html', firstName = session['FName'])

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html', firstName = None)
    elif request.method == 'POST':
        firstName = request.values.get('inputFirstName')
        lastName = request.values.get('inputLastName')
        email = request.values.get('inputEmail')
        address = request.values.get('inputAddress')
        phone = request.values.get('inputPhone')
        driversLicense = request.values.get('inputDriversLicense')
        discountCode = request.values.get('inputDiscountCode')
        password = request.values.get('inputPassword')

        if isValidPassword(password) == False:
            return render_template('signup.html', errorMessage="Invalid password. Please enter a password between 6 to 64 characters in length.", firstName = None)

        if phone.isdigit() == False:
            return render_template('signup.html', errorMessage="Invalid phone number. Phone number should contain only digits", firstName = None)

        sql = "SELECT * from member where email=%s"
        cursor.execute(sql, (email))
        data = cursor.fetchone() 

        if data != None:
            return render_template('signup.html', errorMessage="This email is already registered for kingston carshare. Please sign in or enter a new email.", firstName = None)
        else:
            
            newMemberID = generateNewMemberID()
            monthlyMemberFee = assignMonthlyMemberFee(discountCode)
            isAdmin = checkIfAdmin(discountCode) #0 is false

            # set cookies for email and first name and admin
            session['email'] = email
            session['FName'] = firstName
            session['isAdmin'] = isAdmin

            #sql command to insert new member into database
            sql = "INSERT INTO member VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (newMemberID, firstName, lastName, address, phone, email, driversLicense, monthlyMemberFee, password, isAdmin))
            conn.commit()
            
        if session['isAdmin'] == 0:
            return redirect(url_for('welcome_member'))
        else:
            return redirect(url_for('welcome_admin'))


def isValidPassword(password):
    if len(password) <= 5 or len(password) >=65:
        return False
    else:
        return True

# not best way to this, make more efficient if time permits
def generateNewMemberID():
    memberID = 1000000
    data = "not null"

    while data != None:
        memberID += 1
        sql = "SELECT * from member where memberID=%s"
        cursor.execute(sql, (str(memberID)))
        data = cursor.fetchone() 

    return str(memberID)

def checkIfAdmin(discountCode):
    if discountCode != None:
        discountCode = discountCode.upper() # discount code not case sensitive
    if discountCode == "MAKEMEADMIN":
        return 1
    else:
        return 0

def assignMonthlyMemberFee(discountCode):
    if discountCode != None:
        discountCode = discountCode.upper()
    if discountCode == "20-OFF":
        return "55"
    else:
        return "75"

@app.route('/logout')
def logout():
    # remove the email from the session if it's there
    # session.pop('email', None)
    # session.pop('FName', None)
    # session.pop('isAdmin', None)
    session['email'] = None
    session['FName'] = None
    session['isAdmin'] = None
    return redirect(url_for('homepage'))




@app.route('/member/pickup_dropoff', methods=['GET', 'POST'])
def pickup_dropoff():


    #get user's memberID
    sql = "SELECT memberID FROM member WHERE email=\"" + session['email'] + "\""
    cursor.execute(sql)
    memberID = cursor.fetchone()[0]

    if request.method == 'GET':
        today = date.today()
        # day = today.day
        # month = today.month
        # year = today.year

        #get dates for all the user's reservations
        sql = "SELECT rentalDate, reservationID, VIN, reservationNumDays FROM reservations WHERE memberID=" + memberID + " AND rentalDate=\"" + str(today) + "\""
        cursor.execute(sql)
        reservations = cursor.fetchall()

        carsNotPickedUpYet = []
        for res in reservations:
            resID = res[1]
            # car will only be in car_rental_history if it has already been picked up
            sql = "SELECT * FROM car_rental_history WHERE reservationID=" + resID
            cursor.execute(sql)
            i = cursor.fetchone()
            if i == None:
                carsNotPickedUpYet.append(res)

        carsReadyForDropoff = []
        sql = "SELECT * FROM car_rental_history WHERE memberID=" + memberID + " AND dropOffKm=0"
        cursor.execute(sql)
        carsForDropoff = cursor.fetchall()

        # for reservation in reservations:
        #   #date = datetime.strptime(str(reservation[0]), "%Y-%m-%d")
        #   reservationDate = str(reservation[0])

        return render_template('pickup_dropoff.html', firstName = session['FName'], reservationsPickup = carsNotPickedUpYet, carsForDropoff = carsForDropoff)

    elif request.method == 'POST':
        
        reservationID = request.values.get('inputReservationID')
        inputKm = request.values.get('inputKm')
        inputStatus = request.values.get('inputStatus')
        pickup = request.values.get('pickup') == "pickup" #otherwise action is dropoff
        currentTime = datetime.today()
        currentTime = currentTime.strftime('%Y-%m-%d %H:%M:%S')

        if pickup == True:
            print ("submitted car for pick-up")

            #sql = "UPDATE car_rental_history SET `statusOnReturn` = 'not running!' WHERE `car_rental_history`.`reservationID` = 'Reserve2345'
            #UPDATE `car_rental_history` SET `statusOnReturn` = 'not running!', `pickUpTime` = '2017-04-03 07:00:00' WHERE `car_rental_history`.`reservationID` = 'Reserve2345'
            
            # sql = "UPDATE car_rental_history SET pickUpTime=%s, pickUpKm=%s, statusOnPickup=%s WHERE car_rental_history.reservationID=%s"
            # cursor.execute(sql, (currentTime, inputKm, pickupStatus, reservationID))
            sql = "SELECT * FROM reservations WHERE reservationID=" + reservationID
            cursor.execute(sql)
            res = cursor.fetchone()
            print(res)
            for item in res:
                print(item)

            if res != None:
                print ("here")
                sql = "INSERT INTO car_rental_history VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (res[0], res[1], str(inputKm), str(0), inputStatus, "", currentTime, currentTime, res[2]))
                conn.commit()

                sql = "INSERT INTO member_rental_history VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (res[0], res[1], res[2], str(res[3]), res[4], res[5]))
                conn.commit()

        else: # submitted for dropoff
            print ("car submitted for dropoff")

            sql = "UPDATE car_rental_history SET dropOffTime=%s, dropOffKm=%s, statusOnReturn=%s WHERE car_rental_history.reservationID=%s"
            cursor.execute(sql, (currentTime, inputKm, inputStatus, reservationID))
            conn.commit()


        return redirect(url_for('homepage'))


@app.route('/member/reserve', methods=['GET', 'POST'])
def reservationPage():
    if request.method == 'GET':
        session['startingDay'] = False
        session['numberOfDays'] = False
        session['day'] = False
        return render_template('reservation.html', firstName = session['FName'], dateSelected=session['day'] )
    elif request.method == 'POST':
        if session['day'] == False:
            session['startingDay'] = request.values.get('inputDay')
            session['numberOfDays'] = request.values.get('inputNumDays')
            session['day'] = True
            sql = "SELECT VIN, carTypeID FROM car WHERE VIN NOT IN (SELECT VIN FROM reservations WHERE %s >= DATEDIFF(%s,reservations.rentalDate) AND DATEDIFF(%s,reservations.rentalDate) >= 0)"
            cursor.execute(sql, (session['numberOfDays'], session['startingDay'], session['startingDay']))
            data = cursor.fetchall()
            return render_template('reservation.html', firstName = session['FName'], dateSelected=session['day'], theThing=data)
        else:
            carToRent = request.values.get('selected')
            print (carToRent)
            sql = "SELECT memberID FROM member WHERE email=%s"
            cursor.execute(sql, session['email'])
            data = cursor.fetchone()
            print (data[0])
            reservationID = createNewReservationID()
            print (reservationID)
            entryCode = createNewEntryCode()
            print (entryCode)
            print (session['startingDay'])
            print (session['numberOfDays'])
            sql = "INSERT INTO reservations VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (reservationID, data, carToRent, session['startingDay'], entryCode, session['numberOfDays']))
            conn.commit()
            sql = "SELECT monthlyMemberFee FROM member WHERE email=%s"
            cursor.execute(sql, session['email'])
            data1 = cursor.fetchone()[0]
            print (data1)
            sql = "SELECT carTypeID FROM car WHERE VIN=%s"
            cursor.execute(sql, carToRent)
            data2 = cursor.fetchone()
            print (data2)
            sql = "SELECT dailyRentalFee FROM car_type WHERE carTypeID=%s"
            cursor.execute(sql, data2)
            data3 = cursor.fetchone()[0]
            sql = "UPDATE member SET monthlyMemberFee=%s WHERE email=%s"
            updatedFee = int(data1) + int(data3)*int(session['numberOfDays'])
            cursor.execute(sql, (updatedFee, session['email']))
            session['day'] = "Success"
            conn.commit()
            return render_template('reservation.html', firstName = session['FName'], errorMessage = "Reservation Successful", dateSelected=session['day'])


def createNewReservationID():
        notRandom = True
        while notRandom:
                randomInt = random.randint(1,10000)
                sql = "SELECT reservationID FROM reservations WHERE reservationID=%s"
                cursor.execute(sql, (randomInt))
                data = cursor.fetchone()
                if data == None:
                        notRandom = False
        return randomInt

#AlterToRandomCharactersIfTimePermits
def createNewEntryCode():
        notRandom = True
        while notRandom:
                randomInt = random.randint(1,10000)
                sql = "SELECT reservationID FROM reservations WHERE reservationID=%s"
                cursor.execute(sql, (randomInt))
                data = cursor.fetchone()
                if data == None:
                        notRandom = False
        return randomInt    

def isCar(VIN):
        sql = "SELECT vin FROM car WHERE vin=%s"
        cursor.execute(sql, (VIN))
        data = cursor.fetchone()
        if data != None:
                return True
        else:
                return False

def isUser(ID):
        sql = "SELECT memberID FROM member WHERE memberID=%s"
        cursor.execute(sql, (ID))
        data = cursor.fetchone()
        if data != None:
                return True
        else:
                return False

@app.route('/member/locations', methods=['GET','POST'])
def locationsPage():
        if request.method == 'GET':
                session['ch'] = False
                sql = "SELECT parkingAddress FROM parking_locations"
                cursor.execute(sql)
                Addresses = cursor.fetchall()
                return render_template('locations2.html', theThing=Addresses, locationSelected=False, firstName = session['FName'])
        elif request.method == 'POST':
            if session['ch'] == False:
                whichLot = request.values.get("sites")
                print (whichLot)
                sql = "SELECT carTypeID, vin FROM car WHERE parkingAddress=%s"
                cursor.execute(sql, whichLot)
                data = cursor.fetchall()
                print (data)
                session['ch'] = True
                return render_template('locations2.html', theLocation=data, locationSelected=True, firstName = session['FName'])
            else:
                whichCar = request.values.get("cars")
                sql = "SELECT * FROM car_rental_history WHERE VIN=%s"
                cursor.execute(sql, whichCar)
                rentals = cursor.fetchall()
                print (rentals)
                print (whichCar)
                return render_template('locations2.html', firstName = session['FName'], locationSelected="3", rentals=rentals)

@app.route('/member/rental_history')
def rental_history():
    #print(session['email'])
    sql = "SELECT memberID FROM member WHERE email=\"" + session['email'] + "\""
    #print(sql)
    cursor.execute(sql)
    memberID = cursor.fetchone()[0]
    #print(memberID)


    sql = "SELECT * FROM member_rental_history WHERE memberID=" + memberID
    cursor.execute(sql)
    rentals = cursor.fetchall()

    return render_template('rental_history.html', firstName = session['FName'], rentals=rentals)

@app.route('/admin/comments', methods=['GET','POST'])
def comments_admin():
    if request.method == 'GET':
        sql = "SELECT * FROM rental_comments"
        cursor.execute(sql)
        data = cursor.fetchall()
        sql = "SELECT * FROM admin_reply"
        cursor.execute(sql)
        data2 = cursor.fetchall()
    return render_template('comments_admin.html', firstName = session['FName'], comments=data, adminReplies=data2)
    if request.method == 'POST':
        thingOne = request.values.get('inputComment')
        thingTwo = request.values.get('inputResponse')
        newID = generateAdminCommentID()
        sql = "INSERT INTO admin_reply VALUES (%s, %s, %s)"
        cursor.execute(sql, (newID, thingOne, thingTwo))
        conn.commit()
        sql = "SELECT * FROM rental_comments"
        cursor.execute(sql)
        data = cursor.fetchall()
        sql = "SELECT * FROM admin_reply"
        cursor.execute(sql)
        data2 = cursor.fetchall()
    return render_template('comments_admin.html', firstName = session['FName'], comments=data, adminReplies=data2)

@app.route('/admin/reservations', methods=['GET','POST'])
def reservations_admin():
    if request.method == 'GET':
        return render_template('reservations_admin.html', firstName = session['FName'])
    if request.method == 'POST':
        dayToCheck = request.values.get('inputDay')
        sql = "SELECT * FROM reservations WHERE rentalDate=%s"
        cursor.execute(sql, dayToCheck)
        data = cursor.fetchall()
        print (data)
        return render_template('reservations_admin.html', firstName = session['FName'], dateSelected=True, rentals=data)

@app.route('/admin/cars_at_location', methods=['POST'])
def cars_at_location_admin():
    location = request.values.get("site")
    sql = "SELECT vin, carTypeID FROM car WHERE parkingAddress=\"" + location + "\""
    cursor.execute(sql)
    cars = cursor.fetchall()
    return render_template('cars_at_location.html', firstName = session['FName'], cars=cars, location=location)

@app.route('/admin/cars_by_km', methods=['POST'])
def cars_by_km_admin():
    minKm = request.values.get("minKm")
    maxKm = request.values.get("maxKm")
    sql = "SELECT vin, dropOffKm, statusOnReturn FROM car_rental_history WHERE dropOffKm>=%s AND dropOffKm<=%s ORDER BY dropOffKm"
    cursor.execute(sql, (minKm, maxKm))
    cars = cursor.fetchall()
    return render_template('cars_by_km.html', firstName = session['FName'], cars=cars, minKm=minKm, maxKm=maxKm)

@app.route('/admin/cars_by_rentals', methods=['POST'])
def cars_by_rentals_admin():
    sql = "SELECT VIN, COUNT(VIN) AS timesRented, SUM(reservationNumDays) AS totalDaysRented FROM reservations GROUP BY VIN"
    cursor.execute(sql)
    cars = cursor.fetchall()
    return render_template('cars_by_rentals.html', firstName = session['FName'], cars=cars)

@app.route('/admin/cars_by_damage', methods=['POST'])
def cars_by_damage_admin():
    sql = "SELECT VIN, statusOnReturn, MAX(dropOffTime) AS latestRental FROM car_rental_history WHERE statusOnReturn != \"good\" AND statusOnReturn != \"okay\" GROUP BY VIN"
    cursor.execute(sql)
    cars = cursor.fetchall()
    return render_template('cars_by_damage.html', firstName = session['FName'], cars=cars)

@app.route('/admin/cars', methods=['GET', 'POST'])
def cars_admin():
    if request.method == 'GET':
        #session['ch'] = False
        sql = "SELECT parkingAddress FROM parking_locations"
        cursor.execute(sql)
        Addresses = cursor.fetchall()
        return render_template('cars_admin.html', locations=Addresses, locationSelected=False, firstName = session['FName'])
    elif request.method == 'POST':
        return render_template('cars_admin.html', locationSelected=True, firstName = session['FName'])

    #view all cars
    #return render_template('cars_admin.html', firstName = session['FName'], locationSelected="False")

@app.route('/admin/car_history', methods=['GET','POST'])
def car_history():
        if request.method == 'GET':
            sql = "SELECT VIN, carTypeID FROM car"
            cursor.execute(sql)
            cars = cursor.fetchall()
            return render_template('car_history.html', carSelected=False, firstName = session['FName'], theThing=cars)
        if request.method == 'POST':
            VIN = request.values.get("cars")
            sql = "SELECT * FROM car_rental_history WHERE VIN=" + VIN
            cursor.execute(sql)
            vals = cursor.fetchall()
            return render_template('car_history.html', carSelected=True, rentals=vals, firstName = session['FName'])

@app.route('/admin/add_car', methods=['GET','POST'])
def add_car():
        if request.method == 'GET':
            return render_template('add_car.html', firstName = session['FName'])
        if request.method == 'POST':
            VIN = request.values.get('inputVIN')
            Type = request.values.get('inputType')
            Address = request.values.get('inputAddress')
            sql = "SELECT parkingAddress FROM parking_locations WHERE parkingAddress=%s"
            cursor.execute(sql, Address)
            data = cursor.fetchone()
            print (data)
            if data == None:
                sql = "INSERT INTO parking_locations VALUES (%s, %s)"
                cursor.execute(sql, (Address, "10"))
                conn.commit()
            sql = "SELECT carTypeID FROM car_type WHERE carTypeID=%s"
            cursor.execute(sql, Type)
            data = cursor.fetchone()
            if data == None:
                return render_template('add_car.html', firstName = session['FName'], errorMessage = "Tried to add car of invalid type. Please try again")
            sql = "INSERT INTO car VALUES (%s, %s, %s)"
            cursor.execute(sql, (VIN, Type, Address))
            conn.commit()
            return render_template('add_car.html', firstName = session['FName'],errorMessage = "Success!")
            

@app.route('/admin/invoice', methods=['GET','POST'])
def invoice():
    Members = False
    if request.method == 'GET':
                sql = "SELECT memberID, FName, LName FROM member"
                cursor.execute(sql)
                Members = cursor.fetchall()
                return render_template('invoice.html', theThing=Members, firstName = session['FName'])
    elif request.method == 'POST':
                sql = "SELECT memberID, FName, LName FROM member"
                cursor.execute(sql)
                Members = cursor.fetchall()
                fuckery = request.values.get('selected')
                sql = "SELECT monthlyMemberFee FROM member WHERE memberID=%s"
                cursor.execute(sql, fuckery)
                data = cursor.fetchone()
                returnSentence = "User " + fuckery + "'s annual invoice totals " + str(data[0]) + " dollars"
                return render_template('invoice.html', invoiceResult=returnSentence, theThing=Members, firstName = session['FName'])

@app.route('/comments', methods=['GET', 'POST'])
def comments():
    if request.method == 'GET':
        sql = "SELECT * FROM rental_comments"
        cursor.execute(sql)
        data = cursor.fetchall()
        sql = "SELECT * FROM admin_reply"
        cursor.execute(sql)
        data2 = cursor.fetchall()
    return render_template('comments.html', firstName = session['FName'], comments=data, adminReplies=data2)
    if request.method == 'POST':
        newID = generateCommentID()
        commentText = request.values.get('inputComment')
        rating = request.values.get('inputRating')
        reservationNumber = request.values.get('inputReservationNum')
        sql = "SELECT memberID FROM member WHERE email=%s"
        cursor.execute(sql, session['email'])
        memID = cursor.fetchone()[0]
        if memID == None:
            return render_template('comments.html', errorMessage="We are sorry, please log in before leaving a comment")
        sql = "SELECT VIN from reservations WHERE reservationID=%s"
        cursor.execute(sql, reservationNumber)
        vehicle = cursor.fetchone()
        sql = "SELECT commentID FROM rental_comments WHERE reservationID=%s"
        cursor.execute(sql, reservationNumber)
        data = cursor.fetchone()
        if data != None:
            return render_template('comments.html', firstName = session['FName'], errorMessage="We are sorry, but this reservation already has a comment")
        sql = "INSERT INTO rental_comments VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (newID, memID, reservationNumber, vehicle, rating, commentText))
        conn.commit()
        sql = "SELECT * FROM rental_comments"
        cursor.execute(sql)
        data = cursor.fetchall()
    return render_template('comments.html', firstName = session['FName'], comments=data, errorMessage="Comment posted successfully")

def generateCommentID():
        notRandom = True
        while notRandom:
                randomInt = random.randint(1,10000)
                sql = "SELECT commentID FROM rental_comments WHERE commentID=%s"
                cursor.execute(sql, (randomInt))
                data = cursor.fetchone()
                if data == None:
                        notRandom = False
        return str(randomInt)

def generateAdminCommentID():
        notRandom = True
        while notRandom:
                randomInt = random.randint(1,10000)
                sql = "SELECT adminReplyID FROM admin_reply WHERE adminReplyID=%s"
                cursor.execute(sql, (randomInt))
                data = cursor.fetchone()
                if data == None:
                        notRandom = False
        return str(randomInt)
        

# @app.route('/showEmployee')
# def db():
#     db = MySQLdb.connect("localhost","myusername","mypassword","mydbname" )

#     cursor = db.cursor()

#     cursor.execute("SELECT * from p_user")

#     rows = []

#     for row in cursor:
#         rows.append(row)
#         print(row)

#     return rows

if __name__ == "__main__":
    app.run(threaded=True, debug=True) # threaded=True help ctrl+c work in command line to close it
