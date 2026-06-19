from app import db, cache
from app.models import User_cred, Hotels, Rooms, Room_facilities, Room_Image, Facilities,Bookings, Chat_message, Conversation,Audit_logs
from datetime import datetime
from flask_login import current_user

# -------------- Hotel table ----------------------

def getHotelDataById(hid):
    data = Hotels.query.filter_by(id = hid).first()
    return data

def getAllHotels():
    data = Hotels.query.all()
    return data
    

def updateHotelData(id, data):
    hotel = Hotels.query.get(id)

    if 'name' in data:
        hotel.name = data['name']

    if data.get('type', None) != None:
        hotel.type = data['type']

    if 'desc' in data:
        hotel.description = data['desc']

    if 'city' in data:
        hotel.city = data['city']

    if 'location' in data:
        hotel.location = data['location']

    if data.get('image', None) != None:
        hotel.images = data['image']

    db.session.commit()

def createHotel(**data):
    hotel = {}

    if data.get('images', None) != None:
        hotel = Hotels(name=data['name'], description = data['description'], type = data['type'], city = data['city'], location = data['location'], images = data['images'], host_id = data['host_id'])
    else:
        hotel = Hotels(name=data['name'], description = data['description'], type = data['type'], city = data['city'], location = data['location'], host_id = data['host_id'])

    db.session.add(hotel)
    db.session.commit()
    print('Hotel Added')


def deleteHotel(hid):
    # after bookings module, delete booking details here also
    hotel = getHotelDataById(hid)
    rooms = getRoomsByHotelId(hid)

    # can not delete all records at once, so created loop and delete one by one
    for r in rooms:
        deleteRoomById(r.id)

    db.session.delete(hotel)
    db.session.commit()


# ----------------------- Rooms --------------

# add room
def addRoom(**data):
    room = {}

    room = Rooms(category=data['category'], bedrooms=data['bedrooms'], beds=data['beds'], person_capacity=data['person'], price_per_night=data['price'], no_rooms=data['rooms'], hotel_id=data['hid'])
    db.session.add(room)
    db.session.commit()

    for i in data['images']:
        addRoomImage(room.id, i)

    for fid in data['facility']:
        addRoomFacilityByRoomId_FacilityId(room.id, fid)

# edit room
def editRoom(rid, data):
    room = Rooms.query.get(rid)
    # roomImgs = getRoomImageById(rid)
    # roomFacility = getRoomFacilityByRoomId(rid)

    if data.get('category', None) != None:
        room.category = data['category'] 

    if data.get('bedrooms', None) != None:
        room.bedrooms = data['bedrooms']

    if data.get('beds', None) != None:
        room.beds = data['beds']

    if data.get('person_capacity', None) != None:
        room.person_capacity = data['person_capacity']

    if data.get('price_per_night', None) != None:
        room.price_per_night = data['price_per_night']

    if data.get('no_rooms', None) != None:
        room.no_rooms = data['no_rooms']

    if data.get('deleteImages', None) != None:
        print('room edit service: delete images')
        for id in data['deleteImages']:
            deleteImageByImageId(id)

    if data.get('newImages', None) != None:
        print('room edit service: add images')

        # if fid has multiple name, so we can access one by one using loop
        for img in data['newImages']:
            addRoomImage(rid, img)
        
    if data.get('newFacilities', None) != None:
        print('room edit service: add facility')
       
        # if fid has multiple id, so we can access id one by one using loop
        for fid in data['newFacilities']:
            addRoomFacilityByRoomId_FacilityId(rid, fid)
    
    if data.get('deleteFacilities', None) != None:
        print('room edit service: remove facility')

        for fid in data['deleteFacilities']:
            deleteRoomFacilityByRoomId_FacilityId(rid, fid)

    db.session.commit()

def getRoomsByHotelId(hid):
    rooms = Rooms.query.join(Hotels).filter(Rooms.hotel_id == hid).all()
    return rooms

def getRoomById(id):
    room = Rooms.query.filter(Rooms.id == id).first()
    return room

def getAllRooms():
    rooms = Rooms.query.all()
    return rooms

def deleteRoomById(rid):
    # after bookings module, delete booking details here also
    room = getRoomById(rid)

    rImage = getRoomImageById(rid)
    deleteRoomImagesByObject(rImage)

    rFacility = getRoomFacilityByRoomId(rid)
    deleteRoomFacilityByObject(rFacility)

    db.session.delete(room)
    db.session.commit()


# ----------------------- Facilities -----------------------
def getAllFacility():
    f = Facilities.query.all()
    return f

def getFacilityByName(name):
    f = Facilities.query.filter(Facilities.name == name).first()
    return f

# ----------------------- Room_Facilities -----------------------
def addRoomFacilityByRoomId_FacilityId(rid, fid):
    facility = Room_facilities(room_id=rid, facility_id = fid)
    db.session.add(facility)
    db.session.commit()

def getAllRoomFacility():
    f = Room_facilities.query.all()
    return f

def getRoomFacilityByRoomId(rid):
    f = Room_facilities.query.filter(Room_facilities.room_id == rid).all()
    return f

def deleteRoomFacilityByObject(facilities):
    for f in facilities:
        db.session.delete(f)
    db.session.commit()

def deleteRoomFacilityByRoomId_FacilityId(rid, fid):
    f = Room_facilities.query.filter(Room_facilities.room_id == rid, Room_facilities.facility_id == fid).first()
    # print(f)
    db.session.delete(f)
    db.session.commit()

def getRoomFacility_nameList(facilities):
    room_facility = []
    for f in facilities:
        room_facility.append(f.facility.name)

    return room_facility

# ----------------------- Rooms images -----------------------
def addRoomImage(rid, imageName):
    image = Room_Image(room_id=rid, image = imageName)
    db.session.add(image)
    db.session.commit()
    
def getAllRoomImages():
    images = Room_Image.query.all()
    return images

def getRoomImageById(rid):
    images = Room_Image.query.filter(Room_Image.room_id == rid).all()
    return images

def deleteRoomImagesByObject(images):
    for i in images:
        db.session.delete(i)
    db.session.commit()

def deleteRoomImageByRoomId_ImageName(rid, imgName):
    image = Room_Image.query.filter(Room_Image.room_id == rid, Room_Image.image == imgName).first()
    db.session.delete(image)
    db.session.commit()

def deleteImageByImageId(id):
    image = Room_Image.query.filter(Room_Image.id == id).first()
    db.session.delete(image)
    db.session.commit()

# takes multiple images record in argugemt
def getRoomImageName_list(images_obj):
    room_img = []
    for img in images_obj:
        room_img.append(img.image)
        
    return room_img

# ----------------------- Bookings -----------------------
def addBooking(data):
    if checkAvailability(rid = data['rid'], checkin = data['checkin'], checkout= data['checkout']):
        
        b = Bookings(date_of_arrival = data['checkin'], date_of_departure = data['checkout'], nights = data['nights'], bedrooms = data['bedrooms'], guest = data['guest'], total_price = data['totalPrice'], room_id = data['rid'], user_id = data['uid'], status = 'confirmed', hotel_id = data['hid'])
        db.session.add(b)
        db.session.flush()

        log = Audit_logs(action = 'BOOKING_CREATED', user_id = data['uid'], record_id = b.id, table_name = 'bookings')
        db.session.add(log)

        db.session.commit()

        print(f'\nAudit : Booking Created-{b.id}\n')

        return b.id
    
    else:
        return False
    
def getAllBookings_ByUserId(uid):
    bookings = Bookings.query.filter(Bookings.user_id == uid).all()
    return bookings

def getAllBookings():
    bookings = Bookings.query.all()
    return bookings

def getBooking_ById(bid):
    booking = Bookings.query.get(bid)
    return booking

def cancelBooking(bid, reason, cancelledBy):
    booking = Bookings.query.get(bid)

    if booking.status != 'cancelled':
        booking.status = 'cancelled'
        booking.cancel_reason = reason
        booking.cancelled_by = cancelledBy
        booking.cancelled_at = datetime.now()
        db.session.flush()

        log = Audit_logs(action='BOOKING_CANCELLED', user_id = current_user.id, record_id = bid, table_name = 'bookings')
        db.session.add(log)

        db.session.commit()

        print(f'\nAudit : Booking Cancelled-{bid}\n')
 

def checkAvailability(rid, checkin, checkout):
    
    room = Rooms.query.get(rid)

    bookedRooms = Bookings.query.join(Rooms).filter(
        Bookings.room_id == rid,
        
        ~(
            (Bookings.date_of_departure <= checkin) |
            (Bookings.date_of_arrival >= checkout)
        )
    ).count()

    available = room.no_rooms - bookedRooms

    if available > 0:
        return True
    else:
        return False
    

# --------------------- chat ---------------------------

def getUser_Conversations(id):
    user = User_cred.query.get(id)

    if user.role == 'host':
        conversations = Conversation.query.filter(Conversation.host_id == id)
    elif user.role == 'user':
        conversations = Conversation.query.filter(Conversation.user_id == id)

    return conversations

def getUser_Chat(id):
    user = User_cred.query.get(id)

    if user.role == 'host':
        chats = Chat_message.query.join(Conversation).filter(Conversation.host_id == id)
    elif user.role == 'user':
        chats = Chat_message.query.join(Conversation).filter(Conversation.user_id == id)

    return chats

def save_ChatMsg(cid, sender, msg):
    msg = Chat_message(conversation_id = cid, sender = sender, message = msg)
    db.session.add(msg)
    db.session.commit()

    cache.delete_memoized(checkUnreadMessages)

    return msg

def getConversation_byId(cid):
    conversation = Conversation.query.get(cid)
    return conversation


def create_Conversation(user_id, host_id, hotel_id):
    existing_conversation = Conversation.query.filter(Conversation.user_id == user_id, Conversation.hotel_id == hotel_id, Conversation.host_id == host_id).first()

    if(existing_conversation):
        return existing_conversation.id
    else:
        new = Conversation(user_id=user_id, host_id=host_id, hotel_id=hotel_id)
        db.session.add(new)
        db.session.commit()

        return new.id
    

def markAll_msg_Read(cid, sender):
    Chat_message.query.filter_by(
        conversation_id = cid,
        sender = sender,
        is_read = False
    ).update({
        'is_read' : True
    })
    
    db.session.commit()

@cache.memoize(60)
def checkUnreadMessages(uid, role):
    if role == 'user':
        messages = Chat_message.query.join(Conversation).filter(Conversation.user_id == uid, Chat_message.sender != role, Chat_message.is_read == False).count()
    
    elif role == 'host':
        messages = Chat_message.query.join(Conversation).filter(Conversation.host_id == uid, Chat_message.sender != role, Chat_message.is_read == False).count()

    
    return messages
    

# --------------------- Audit logs ---------------------------

def getAuditLogs():
    logs = Audit_logs.query.all()

    return logs
