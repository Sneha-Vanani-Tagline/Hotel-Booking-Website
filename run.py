from app import create_app

app1 = create_app()

if __name__ == '__main__':
    app1.run(debug=True)