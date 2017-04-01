# from Flask website
# run, will see output in http://localhost:5000/

#cd C:\Users\Anya\Documents\!School\CISC332\make-website
# to get requirements, cd into there and type "setup.cmd"

from flask import Flask, render_template, request
from flask.ext.mysql import MySQL
app = Flask(__name__)
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root' # user Anna probably has a password?
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'carshare_sushi_v2'
app.config['MYSQL_DATABASE_HOST'] = 'localhost' # this machine
mysql.init_app(app)

# #connect to db
# conn = mysql.connect()

# #create cursor to query db
# cursor = conn.cursor()


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
		print(str(request.args))
		firstName = request.values.get('inputFirstName')
		lastName = request.values.get('inputLastName')
		email = request.values.get('inputEmail')
		address = request.values.get('inputAddress')
		phone = request.values.get('inputPhone')
		driversLicense = request.values.get('inputDriversLicense')
		discountCode = request.values.get('discountCode')
		password = request.values.get('inputPassword')

		#todo: check that password is valid, otherwise ask to try again? somehow?

		cursor = mysql.connect().cursor()
		sql = "SELECT * from member where email=%s"

		cursor.execute(sql, (email))
		data = cursor.fetchone() 


		if data != None:
			return "This email is already registered for kingston carshare. Please sign in or enter a new email."
		else:
			newMemberID = createNewMemberID()
			monthlyMemberFee = assignMonthlyMemberFee(discountCode)
			isAdmin = checkIfAdmin(discountCode) #0 is false
			sql = "INSERT INTO member VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			cursor.execute(sql, (newMemberID, firstName, lastName, address, phone, email, driversLicense, monthlyMemberFee, password, isAdmin))
			conn.commit()
			return str("Signed up successfully? Check db")
	    #do a check if admin

#todo: add checks for valid address and phone number etc

def createNewMemberID():
	return "1000000"

def checkIfAdmin(discountCode):
	if discountCode == "makeMeAdmin":
		return 1
	else:
		return 0

def assignMonthlyMemberFee(discountCode):
	#todo: have a field where they can enter a discount code ("20-OFF"), use here
	if discountCode == "20-OFF":
		return 55
	return 75

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

