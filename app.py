# from Flask website
# run, will see output in http://localhost:5000/

#cd C:\Users\Anya\Documents\!School\CISC332\make-website
# to get requirements, cd into there and type "setup.cmd"

from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.mysql import MySQL
app = Flask(__name__)
mysql = MySQL()
app.secret_key = 'SUSHI'
from random import randint
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root' # user Anna probably has a password?
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'carshare_sushi_v2'
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
			return redirect(url_for('welcome_user'))
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
                print carToRent
                sql = "SELECT memberID FROM member WHERE email=%s"
                cursor.execute(sql, session['email'])
                data = cursor.fetchone()
                print data[0]
                reservationID = createNewReservationID()
                print reservationID
                entryCode = createNewEntryCode()
                print entryCode
                print session['startingDay']
                print session['numberOfDays']
                sql = "INSERT INTO reservations VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (reservationID, data, carToRent, session['startingDay'], entryCode, session['numberOfDays']))
                conn.commit()
                session['day'] = "Success"
                return render_template('reservation.html', firstName = session['FName'], errorMessage = "Reservation Successful", dateSelected=session['day'])


def createNewReservationID():
        notRandom = True
        while notRandom:
                randomInt = randint(1,10000)
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
                randomInt = randint(1,10000)
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
                print whichLot
                sql = "SELECT carTypeID, vin FROM car WHERE parkingAddress=%s"
                cursor.execute(sql, whichLot)
                data = cursor.fetchall()
                print data
                session['ch'] = True
                return render_template('locations2.html', theLocation=data, locationSelected=True, firstName = session['FName'])
            else:
                whichCar = request.values.get("cars")
                sql = "SELECT * FROM car_rental_history WHERE VIN=%s"
                cursor.execute(sql, whichCar)
                rentals = cursor.fetchall()
                print whichCar
                return render_template('locations2.html', firstName = session['FName'], locationSelected="3", rentals=rentals)
 
@app.route('/member/pickup_dropoff')
def pickup_dropoff():
	return render_template('pickup_dropoff.html', firstName = session['FName'])

@app.route('/member/rental_history')
def rental_history():
	print(session['email'])
	sql = "SELECT memberID FROM member WHERE email=\"" + session['email'] + "\""
	print(sql)
	cursor.execute(sql)
	memberID = cursor.fetchone()[0]
	print(memberID)


	sql = "SELECT * FROM member_rental_history WHERE memberID=" + memberID
	cursor.execute(sql)
	rentals = cursor.fetchall()

	return render_template('rental_history.html', firstName = session['FName'], rentals=rentals)

@app.route('/admin/comments')
def comments_admin():
	return render_template('comments_admin.html', firstName = session['FName'])

@app.route('/admin/reservations')
def reservations_admin():
	return render_template('reservations_admin.html', firstName = session['FName'])

@app.route('/admin/cars')
def cars_admin():
	return render_template('cars_admin.html', firstName = session['FName'])

@app.route('/admin/car_history', methods=['GET','POST'])
def car_history():
        if request.method == 'GET':
            sql = "SELECT VIN FROM car"
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
	    sql = "INSERT INTO car VALUES (%s, %s, %s)"
	    cursor.execute(sql, (VIN, Type, Address))
	    conn.commit()
	    return render_template('add_car.html', firstName = session['FName'],errorMessage = "Success!")
            

@app.route('/admin/invoice', methods=['GET','POST'])
def invoice():
        Members = False
	if request.method == 'GET':
                sql = "SELECT memberID FROM member"
                cursor.execute(sql)
                Members = cursor.fetchall()
                return render_template('invoice.html', theThing=Members, firstName = session['FName'])
        elif request.method == 'POST':
                sql = "SELECT memberID FROM member"
                cursor.execute(sql)
                Members = cursor.fetchall()
                fuckery = request.values.get('selected')
                sql = "SELECT monthlyMemberFee FROM member WHERE memberID=%s"
                cursor.execute(sql, fuckery)
                data = cursor.fetchone()
                returnSentence = "User " + fuckery + "'s monthly invoice totals " + str(data[0]) + " dollars"
               	return render_template('invoice.html', invoiceResult=returnSentence, theThing=Members, firstName = session['FName'])

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

