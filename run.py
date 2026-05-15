from app import create_app, db

app1 = create_app()

if __name__ == '__main__':
    with app1.app_context():
        db.create_all()
        app1.run(debug=True)