from sqlalchemy.event import listens_for
from sqlalchemy import inspect
from app.models import Audit_logs, Rooms, Room_Image, Room_facilities
from flask_login import current_user
from app.extensions import socketio

# ROOM INSERT
@listens_for(Rooms, 'after_insert')
def after_room_insert(mapper, connection, target):
    # print('Roon Creating..', target)

    connection.execute(
        Audit_logs.__table__.insert(),
        {
            'action' : 'INSERT',
            'user_id' : current_user.id,
            'record_id' : target.id,
            'table_name' : 'rooms'
        }
    )
    socketio.emit('update_actionLogs', to='super_admin')
    # print(f'\nAudit : Room Inserted-{target.id}\n')

# ROOM UPDATE
@listens_for(Rooms, 'before_update')
def before_room_update(mapper, connection, target):
    # print('Roon Updating..', target)
    
    state = inspect(target)

    for attr in state.attrs:
            history = attr.history

            if history.has_changes():
                print('\nAudit room Changes in : ', attr.key)
                print(f'old : {history.deleted}')
                print(f'new : {history.added}\n')

                connection.execute(
                    Audit_logs.__table__.insert(),
                    {
                        'action' : 'UPDATE',
                        'user_id' : current_user.id,
                        'record_id' : target.id,
                        'table_name' : 'rooms',
                        'field' : attr.key,
                        'old_value' : history.deleted,
                        'new_value' : history.added
                    }
                )

                socketio.emit('update_actionLogs', to='super_admin')
                # print(f'\nAudit : Room Updated-{target.id}\n')

# ROOM DELETE
@listens_for(Rooms, 'before_delete')
def before_room_delete(mapper, connection, target):
    # print('Roon Deleting..', target)

    connection.execute(
        Audit_logs.__table__.insert(),
        {
            'action' : 'DELETE',
            'user_id' : current_user.id,
            'record_id' : target.id,
            'table_name' : 'rooms'
        }
    )
    socketio.emit('update_actionLogs', to='super_admin')
    # print(f'\nAudit : Room Deleted-{target.id}\n')

      
