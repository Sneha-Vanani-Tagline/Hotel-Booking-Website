from app import db
from app.models import User_cred, Hotels, Rooms, Room_facilities, Room_Image, Facilities,Bookings

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

# Insert User record
def insertUser(**data):
    user = {}
    if data.get('image', None) == None:
        user = User_cred(name=data['name'], email=data['email'], password=data['psw'], role=data['role'])
    else:
        user = User_cred(name=data['name'], email=data['email'], image=data['image'], password=data['psw'], role=data['role'])
    db.session.add(user)
    db.session.commit()
    print('User Added.')

# Update User record
def updateUser(**data):
    user = getUserById(data['id'])
    user.name = data['name']

    if data.get('image', None) != None:
        user.image = data['image']
    
    db.session.commit()

def getUserBooking(id):
    bookings = Bookings.query.join(User_cred).filter(Bookings.user_id == id).all()
    return bookings

def resetPass(uid, new):
    user = User_cred.query.get(uid)
    # print(user, uid, type(uid))
    if user:
        # print('user found in password reset')
        user.password = new
        db.session.commit()
        return True
    else:
        # print('user not found in password reset')
        return False