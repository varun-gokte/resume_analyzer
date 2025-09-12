from flask import Blueprint, render_template, request

main = Blueprint('main',__name__)

@main.route('/', methods=['POST','GET'])
def home():
    if request.method=='POST':
        print (request.files)
        file = request.files['file']
        
    else:
        return render_template('index.html')