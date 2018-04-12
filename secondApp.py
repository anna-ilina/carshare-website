# from Flask website
# run, will see output in http://localhost:5000/

#cd C:\Users\Anya\Documents\!School\CISC332\make-website
# to get requirements, cd into there and type "setup.cmd"
from random import randint
from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.mysql import MySQL
app = Flask(__name__)
mysql = MySQL()
app.secret_key = 'SUSHI'
 
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
	cursor.execute('SELECT * FROM car')
	return str(cursor.fetchall()) # or .fetchone()
    #return "Hello World!"

@app.route("/index/") # when someone visits http://localhost:5000/index/, run this method
@app.route("/index/<name>")
def hello2(name="no name given"):
    #return "<h1>Hello World again!</h1>"
    return render_template("index.html", name=name)
    #http://localhost:5000/index/goldfish will print "hello goldfish"

@app.route("/homepage") # when someone visits slash http://localhost:5000/ on your webpage, run this method
def hello3():
	return render_template("index_homepage.html")

# @app.route('/showSignUp', methods=['GET'])
# def showSignUp():
#     return render_template('signup.html')

# @app.route('/signUp', methods=['GET', 'POST'])
# def signUp():
# 	if request.method == 'GET':
# 		return render_template('signup.html')
# 	elif request.method == 'POST':

# 	    # create user code will be here !!
# 	    # read the posted values from the UI
# 	    _name = request.form['inputName']
# 	    _email = request.form['inputEmail']
# 	    _password = request.form['inputPassword']

# 	    # validate the received values
# 	    if _name and _email and _password:
# 	        return json.dumps({'html':'<span>All fields good !!</span>'})
# 	    else:
# 	        return json.dumps({'html':'<span>Enter the required fields</span>'})

# @app.route("/Authenticate")
# def Authenticate():
#     username = request.args.get('UserName')
#     password = request.args.get('Password')
#     cursor = mysql.connect().cursor()
#     cursor.execute("SELECT * from member where Username='" + username + "' and Password='" + password + "'")
#     data = cursor.fetchone()
#     if data is None:
#      return "Username or Password is wrong"
#     else:
#      return str("Logged in successfully" + str(data))
    #do a check if admin

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
		discountCode = request.values.get('discountCode')
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
			# set cookies for email and first name
			session['email'] = email
			session['FName'] = firstName

			#sql command to insert new member into database
			newMemberID = generateNewMemberID()
			monthlyMemberFee = assignMonthlyMemberFee(discountCode)
			isAdmin = checkIfAdmin(discountCode) #0 is false
			sql = "INSERT INTO member VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			cursor.execute(sql, (newMemberID, firstName, lastName, address, phone, email, driversLicense, monthlyMemberFee, password, isAdmin))
			conn.commit()
			return redirect(url_for('hello'))
	    #do a check if admin

def isValidPassword(password):
	if len(password) <= 5 or len(password) >=65:
		return False
	else:
		return True

# not best way to this, make more efficient if time permits
def generateNewMemberID():
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

def checkIfAdmin(discountCode):
	if discountCode == "makeMeAdmin":
		return "1"
	else:
		return "0"

def assignMonthlyMemberFee(discountCode):
	#todo: have a field where they can enter a discount code ("20-OFF"), use here
	if discountCode == "20-OFF":
		return "55"
	else:
		return "75"
	
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

@app.route('/reserve', methods=['GET', 'POST'])
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

@app.route('/locations', methods=['GET','POST'])
def locationsPage():
        if request.method == 'GET':
                sql = "SELECT parkingAddress FROM parking_locations"
                cursor.execute(sql)
                Addresses = cursor.fetchall()
                print Addresses
                return render_template('locations2.html', theThing=Addresses)
        elif request.method == 'POST':
                

if __name__ == "__main__":
        app.run(threaded=True, debug=True) # threaded=True help ctrl+c work in command line to close it
