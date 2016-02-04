from webpage import app

@app.route('/')
def index():
    print('Hi')
    return 'Hello app'
