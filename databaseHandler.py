import os
import cx_Oracle as cx

#getting the instant client
currentpath = os.path.dirname(os.path.abspath(__file__))
clientpath = os.path.join(currentpath, "instantclient_19_11")
cx.init_oracle_client(lib_dir=clientpath)
# easy connect string
connect_string = "tcps://adb.uk-london-1.oraclecloud.com/t3ulea4zs7iolax_db202008251748_high.atp.oraclecloud.com?wallet_location=/Users/georg/Downloads/Wallet&retry_count=20&retry_delay=3"
username = "ADMIN"
userpwd = "MTR86pWL7GaShTE"

def dbConnect():
    con = cx.connect("Admin", "MTR86pWL7GaShTE", "db202008251748_high", encoding="UTF-8" )
    return con

global con
con = dbConnect()

def loadAccounts(username):
    cur = con.cursor() #create a cursor object from the connection object
    cmd = "SELECT * FROM accounts WHERE username = '{}'".format(username)
    cur.execute(cmd) #execute the sql comamnd
    accountsArr = []
    data = cur.fetchall()
    for i in range(0, len(data)): #adding data in cur to an array
	    row = data[i]
	    accountsArr.append(row)
    return accountsArr #the array of valid accounts is returned

def createAccount(username, password): 
#function to add a new account to the database]
	cur = con.cursor()
	cmd = '''INSERT INTO accounts (user_id, username, password) VALUES (seq_userid.nextval, '{}', '{}')'''.format(username, password)
    #using the seq_userid sequence 
	cur.execute(cmd)
	con.commit()

def insertSolarSystem(name, date, objectCount, userID):
    cur = con.cursor()
    cmd = '''INSERT INTO solarsystems VALUES (seq_solarsystem.nextval, '{}', '{}', '{}')'''.format(name, date, objectCount)
    cur.execute(cmd)
    cmd = '''INSERT INTO user_solarsystems VALUES (seq_usersolarsystem.nextval, '{}', seq_solarsystem.currval)'''.format(userID)
    cur.execute(cmd)
    con.commit()

def getNewSolarSystem():
    cur = con.cursor()
    cmd = '''SELECT seq_solarsystem.currval FROM solarsystems'''
    cur.execute(cmd)
    ID = cur.fetchall()
    con.commit()
    return ID 

def getSolarSystem(ID):
    cur = con.cursor()
    cmd = """SELECT * FROM solarsystems WHERE solarsystem_id = '{}'""".format(ID)
    cur.execute(cmd)
    solarsystem = cur.fetchall()
    con.commit()
    return solarsystem 

def getUserSolarSystems(userID):
    solarSystemArray = []
    cur = con.cursor()
    cmd = '''SELECT * FROM SolarSystems 
		   INNER JOIN user_solarsystems ON 
		   solarsystems.solarsystem_id = user_solarsystems.solarsystem_id 
		   WHERE user_solarsystems.user_id = 1''' 
		   #Loads the default solar systems (the userID for the default user is 1)
    cur.execute(cmd)
    data = cur.fetchall()
    for i in range(len(data)):
        solarSystemArray.append(data[i]) #adds selected solar systems to array
    if userID != 1: #if the user is not a Guest
        cmd = """SELECT * FROM solarsystems 
        INNER JOIN user_solarsystems ON 
        solarsystems.solarsystem_id = user_solarsystems.solarsystem_id 
        WHERE user_solarsystems.user_id = '{}'""".format(userID)
        #Loads the user's solar systems, if the user is not a Guest
        cur.execute(cmd)
        data = cur.fetchall()
        for i in range(len(data)):
            solarSystemArray.append(data[i])
    return solarSystemArray

def getNumberOfObjects(solarsystemID):
    cur = con.cursor()
    cmd = """SELECT * FROM objects WHERE solarsystem_id = '{}'""".format(solarsystemID)
    cur.execute(cmd)
    data = cur.fetchall()
    return len(data)

    #loading the objects from a specified solar system
def loadObjects(solarSystemID):
	objectData = []
	cur = con.cursor()
	cmd = """SELECT * FROM objects where solarsystem_id = '{}'""".format(solarSystemID)
	cur.execute(cmd) #Loads the objects from the solar system
	data = cur.fetchall()
	for i in range(len(data)):
		objectData.append(data[i]) #adds selected solar systems to array
	return objectData

#procedure to update the database with the new objectData
def updateObjectsDatabase(objectData):
    cur = con.cursor() #create a cursor instance
    for i in range(0, len(objectData)): #for every object
        row = objectData[i]
        if row[0] == 0: #if it's a new object, add a row to the database	
            cmd = """INSERT INTO objects VALUES (seq_object_id.nextval, '{}')""".format("', '"
            .join(str(row[item]) for item in range(1, len(row))))
            #the object_id will be automatically incremented by SQL
        else: #if it's an existing object, update the existing row in the database
            if row[3] == None: #if the object was deleted
                cmd = """DELETE FROM objects WHERE object_id = '{}'""".format(row[0])
            else:
                cmd = """UPDATE objects SET solarsystem_id = '{}', 
                        parent_id = '{}', solarsystem_object_id = '{}', 
                        name = '{}', x_coord = '{}', y_coord = '{}',
                        x_velocity = '{}', y_velocity = '{}', 
                        mass = '{}', red = '{}', green = '{}', 
                        blue = '{}' WHERE object_id = '{}'""".format(row[1], row[2], row[3], row[4], row[5], row[6], 
                        row[7], row[8], row[9], row[10], row[11], row[12], row[0])
        cur.execute(cmd)
    con.commit()

#updates a solar system with new information
def updateSolarSystem(date, objectCount, solarsystemID): 
    cmd = """UPDATE solarsystems SET last_date = '{}', object_count = '{}'
             WHERE solarsystem_id = '{}'""".format(date, objectCount, solarsystemID)
    cur = con.cursor()
    cur.execute(cmd)
    con.commit()

#getting all the interactive lessons
def loadLessons():
    cur = con.cursor() #create a cursor object from the connection object
    cmd = "SELECT * FROM lessons"
    cur.execute(cmd) #execute the sql comamnd
    lessonsArr = []
    data = cur.fetchall()
    for i in range(0, len(data)): #adding data in cur to an array
	    row = data[i]
	    lessonsArr.append(row)
    return lessonsArr #the array of lessons is returned

#getting all the stages from a given lesson
def loadLessonStages(lessonID):
    cur = con.cursor() #create a cursor object from the connection object
    cmd = "SELECT * FROM lessonstages WHERE lesson_id = '{}'".format(lessonID)
    cur.execute(cmd) #execute the sql comamnd
    lessonStagesArr = []
    data = cur.fetchall()
    for i in range(0, len(data)): #adding data in cur to an array
	    row = data[i]
	    lessonStagesArr.append(row)
    return lessonStagesArr #the array of lesson stages is returned


