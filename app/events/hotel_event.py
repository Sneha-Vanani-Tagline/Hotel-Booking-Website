from app.extensions import db
from sqlalchemy.event import listens_for
from sqlalchemy import inspect
from app.models import Audit_logs, Hotels
from flask_login import current_user
from app.extensions import socketio

# INSERT
@listens_for(Hotels, 'after_insert')
def after_hotel_insert(mapper, connection, target):
    # print('Inserted row : ', target)        # Inserted row :  Testing Hotel (gives name)

    connection.execute(
        Audit_logs.__table__.insert(),
        {
            'action' : 'INSERT',
            'user_id' : current_user.id,
            'record_id' : target.id,
            'table_name' : 'hotels'
        }
    )
    socketio.emit('update_actionLogs', to='super_admin')
    # print(f'\nAudit : New Hotel Inserted {target.id}\n')


# UPDATE
@listens_for(Hotels, 'before_update')
def before_hotel_update(mapper, connection, target):

    state = inspect(target)

    for attr in state.attrs:
        history = attr.history

        if history.has_changes():
            # print(f'\nChanes in Hotels : {attr.key}')
            # print(f'old : {history.deleted}')
            # print((f'new : {history.added}\n'))

            connection.execute(
                Audit_logs.__table__.insert(),
                {
                    'action' : 'UPDATE',
                    'user_id' : current_user.id,
                    'record_id' : target.id,
                    'table_name' : 'hotels',
                    'field' : attr.key,
                    'old_value' : history.deleted,
                    'new_value' : history.added
                }
            )
            socketio.emit('update_actionLogs', to='super_admin')

            # print(f'\nAudit : Hotel Updated {target.id}\n')

# DELETE
@listens_for(Hotels, 'before_delete')
def before_hotel_delete(mapper, connection, target):
    # print('deleted row : ', target)     

    connection.execute(
        Audit_logs.__table__.insert(),
        {
            'action' : 'DELETE',
            'user_id' : current_user.id,
            'record_id' : target.id,
            'table_name' : 'hotels',
        }
    )

    socketio.emit('update_actionLogs', to='super_admin')
    # print(f'\nAudit : Hotel Deleted {target.id}\n')

