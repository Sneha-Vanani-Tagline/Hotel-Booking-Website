from app import create_app, db
from app.extensions import socketio

app1 = create_app()

if __name__ == '__main__':
    with app1.app_context():
        db.create_all()
        socketio.run(app1, debug=True)