from sqlalchemy import inspect, event
from app.models import User_cred, Audit_logs
from app.extensions import db
from flask_login import current_user
from app.extensions import socketio

@event.listens_for(User_cred, 'before_update')
def after_register(mapper, connection, target):

    state = inspect(target)

    for attr in state.attrs:
        history = attr.history

        if history.has_changes():

            if not(attr.key == 'last_seen' or attr.key == 'is_online'):
                # print('\nAudit Profile Changes in : ', attr.key)
                # print(f'\nOld : {history.deleted}')
                # print(f'\nNew : {history.added}')

                connection.execute(
                    Audit_logs.__table__.insert(),
                    {
                        'action' : 'UPDATE',
                        'user_id' : target.id,
                        'record_id' : target.id,
                        'table_name' : 'user_cred',
                        'field' : attr.key,
                        'old_value' : history.deleted,
                        'new_value' : history.added
                    }
                )

                # print(f'\nAudit: Profile Updated- {target.id}\n')

@event.listens_for(User_cred, 'after_update')
def after_profile_update(mapper, connection, target):
    
    # print('\nBefore : Audit Emit in after_update')
    socketio.emit('update_actionLogs', to='super_admin')
    # print('After : Audit Emit\n')


