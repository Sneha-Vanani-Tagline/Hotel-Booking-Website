from app import create_app, db

# print(type(current_app))

# with current_app.app_context():
#     db.create_all()
#     print('table loaded')

app1 = create_app()

with app1.app_context():
    db.create_all()
    print('loaded')

