import os
from flask import current_app, render_template, request, jsonify
from werkzeug.utils import secure_filename
from ..extensions import db
from ..models import File
from . import main
import time

@main.route('/', methods=['POST','GET'])
def home():
    if request.method=='POST':
        if 'file' not in request.files:
            return jsonify({'error':'No file'}),400
        file = request.files['file']
        if file.filename=='':
            return jsonify({'error':'No file selected'}),400

        filename = f'{int(time.time())}{secure_filename(file.filename)}'
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'],filename)
        file.save(filepath)

        uploaded_file = File(
            filename = filename,
            filepath = filepath,
            mimetype = file.mimetype,
            size = os.path.getsize(filepath)
        )
        db.session.add(uploaded_file)
        db.session.commit()

        return jsonify({'message':'Sucess'},200)
        
    else:
        return render_template('index.html')