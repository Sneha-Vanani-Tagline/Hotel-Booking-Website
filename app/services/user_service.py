from app.extensions import cache
from app import db
from app.models import User_cred, Hotels, Rooms, Room_facilities, Room_Image, Facilities,Bookings, Audit_logs
from datetime import datetime, timezone

# get User
def getUserByMail(mail):
    user = User_cred.query.filter_by(email=mail).first()
    return user 

def getUserById(id):
    user = User_cred.query.filter_by(id = id).first()
    return user

# update column: set is_verified = true
def updateVerifyMail(user):
    user.is_verified = True
    db.session.commit()

# need recheck for registration
# Insert User record
def insertUser(**data):
    user = {}
    if data.get('image', None) == None:
        user = User_cred(name=data['name'], email=data['email'], password=data['psw'], role=data['role'])
    else:
        user = User_cred(name=data['name'], email=data['email'], image=data['image'], password=data['psw'], role=data['role'])
    
    db.session.add(user)
    db.session.flush()

    row = Audit_logs(user_id = user.id, action = 'REGISTRATION', record_ir = user.id, table_name = 'user_cred')
    db.session.add(row)

    db.session.commit()

    print('User Added.')
    print(f'\nAudit: {user.id} Registered\n')


# Update User record
def updateUser(data, uid):
    user = User_cred.query.get(uid)
    
    if 'name' in data:
        user.name = data['name']

    if data.get('image', None) != None:
        user.image = data['image']
  
    db.session.commit()

def getUserBooking(id):
    bookings = Bookings.query.join(User_cred).filter(Bookings.user_id == id).all()
    return bookings

def resetPass(uid, new):
    user = User_cred.query.get(uid)

    if user:
        user.password = new
        db.session.commit()
        return True
    else:
        return False
    
def makeUser_online(uid):
    user = User_cred.query.get(uid)
    user.is_online = True
    print('in makeUser_online function', user)

    db.session.commit()

def makeUser_offline(uid):
    print('in makeUser_offline function')
    user = User_cred.query.get(uid)
    user.is_online = False
    db.session.commit()

def update_lastSeen(uid):
    user = User_cred.query.get(uid)
    user.last_seen = datetime.now()
    db.session.commit()

def login_audit(uid, action):

    if uid and action:
        row = Audit_logs(action = action.upper(), user_id = uid)
        db.session.add(row)

        db.session.commit()

        return True
    
    return False

def logout_audit(uid, action):

    audit = ''
    if uid and action:
        row = Audit_logs(action = action.upper(), user_id = uid)
        db.session.add(row)

        db.session.commit()

        return True
    return False

    


    