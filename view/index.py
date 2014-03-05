from view import app
from view.util.render import render

@app.route('/')
def index():
    return render('index.html')