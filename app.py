# from Flask website
# run, will see output in http://localhost:5000/

#cd C:\Users\Anya\Documents\!School\CISC332\make-website
# to get requirements, cd into there and type "setup.cmd"

from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.mysql import MySQL
app = Flask(__name__)
mysql = MySQL()
app.secret_key = 'SUSHI'
 
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
	return redirect(url_for('homepage'))

# @app.route("/index/") # when someone visits http://localhost:5000/index/, run this method
# @app.route("/index/<name>")
# def hello2(name="no name given"):
#     #return "<h1>Hello World again!</h1>"
#     return render_template("index.html", name=name)
#     #http://localhost:5000/index/goldfish will print "hello goldfish"

@app.route("/homepage") # when someone visits slash http://localhost:5000/ on your webpage, run this method
def homepage():
	return render_template("index_homepage.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	if request.method == 'GET':
		return render_template('signin.html')
	elif request.method == 'POST':
		email = request.values.get('inputEmail')
		password = request.values.get('inputPassword')

		sql = "SELECT FName, isAdmin from member where email=%s and password=%s"
		cursor.execute(sql, (email, password))
		data = cursor.fetchone() 

		if data == None:
			return render_template('signin.html', errorMessage="Username or password incorrect. Please try again.")
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
		return render_template('signup.html')
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
			return render_template('signup.html', errorMessage="Invalid password. Please enter a password between 6 to 64 characters in length.")

		if phone.isdigit() == False:
			return render_template('signup.html', errorMessage="Invalid phone number. Phone number should contain only digits")

		sql = "SELECT * from member where email=%s"
		cursor.execute(sql, (email))
		data = cursor.fetchone() 

		if data != None:
			return render_template('signup.html', errorMessage="This email is already registered for kingston carshare. Please sign in or enter a new email.")
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
    session.pop('email', None)
    return redirect(url_for('homepage'))

@app.route('/member/reserve', methods=['GET', 'POST'])
def reservationPage():
        if request.method == 'GET':
		return render_template('reservation.html')
	elif request.method == 'POST':
		print(str(request.args))
		VIN = request.values.get('inputVIN')
		startingDay = request.values.get('inputDay')
		numberOfDays = request.values.get('inputNumDays')
		userID = request.values.get('inputID')
                errorFlag = False

		if isCar == False:
                        errorFlag = True
		elif isReserved(startingDay,numberOfDays,VIN) == True:
                        errorFlag = True
                elif isUser == False:
                        errorFlag = True                        




		if errorFlag == False:
			newReservationID = createNewReservationID()
			newEntryCode = createNewEntryCode()
			sql = "INSERT INTO reservations VALUES (%s, %s, %s, %s, %s, %s)"
			cursor.execute(sql, (newReservationID, userID, VIN, startingDay, newEntryCode, numberOfDays))
			conn.commit()
			return str("Reservation complete? Check db")
	    #do a check if admin


def createNewReservationID():
        notRandom = True
        while notRandom:
                randomInt = randint(1,10000)
                sql = "SELECT reservationID FROM reservations WHERE reservationID=%s"
                cursor.execute(sql, (randomInt))
                data = cursor.fetchone()
                print data
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
                print data
                if data == None:
                        notRandom = False
        return randomInt	

def isReserved(startDate,numDays,VIN):
        sql = "SELECT VIN FROM reservations WHERE %s > DATEDIFF(%s,reservations.rentalDate) AND DATEDIFF(%s,reservations.rentalDate) > 0 AND VIN=%s"
        cursor.execute(sql, (numDays, startDate, startDate, VIN))
        data = cursor.fetchone()
        if data != None:
                return True
        else:
                return False

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
                sql = "SELECT parkingAddress FROM parking_locations"
                cursor.execute(sql)
                Addresses = cursor.fetchall()
                print Addresses
                return render_template('locations2.html', theThing=Addresses)
        elif request.method == 'POST':
        	return

@app.route('/member/pickup_dropoff')
def pickup_dropoff():
	return render_template('pickup_dropoff.html')

@app.route('/member/rental_history')
def rental_history():
	return render_template('rental_history.html')

@app.route('/admin/comments')
def comments_admin():
	return render_template('comments_admin.html')

@app.route('/admin/reservations')
def reservations_admin():
	return render_template('reservations_admin.html')

@app.route('/admin/cars')
def cars_admin():
	return render_template('cars_admin.html')

@app.route('/admin/car_history')
def car_history():
	return render_template('car_history.html')

@app.route('/admin/add_car')
def add_car():
	return render_template('add_car.html')

@app.route('/admin/invoice')
def invoice():
	return render_template('invoice.html')

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

