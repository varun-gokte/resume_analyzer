import os
from flask import current_app, render_template, request, jsonify
from werkzeug.utils import secure_filename
from ..extensions import db
from ..models import Resume, Job
from . import main
import time
import pdfplumber
from sentence_transformers import SentenceTransformer, util

@main.route('/', methods=['POST','GET'])
def home():
    if request.method=='POST':
        if 'file' not in request.files or 'description' not in request.form:
            return jsonify({'error':'Missing fields'}),400
        file = request.files['file']
        if file.filename=='':
            return jsonify({'error':'No file selected'}),400
        description = request.form['description']
        title = request.form['job_title']
        company = request.form['company']

        filename = f'{int(time.time())}{secure_filename(file.filename)}'
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'],filename)
        file.save(filepath)

        text = ""
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        model = SentenceTransformer('all-MiniLM-L6-v2')
        resume_embeddings = model.encode(text, convert_to_tensor=True)
        job_desc_embeddings = model.encode(description, convert_to_tensor=True)

        similarity = util.cos_sim(resume_embeddings, job_desc_embeddings)

        score = similarity.item()

        uploaded_resume = Resume(
            filename = filename,
            filepath = filepath,
            mimetype = file.mimetype,
            size = os.path.getsize(filepath),
            parsed_text = text
        )
        
        job_details = Job(
            title=title,
            content=description,
            company=company
        )

        db.session.add(uploaded_resume)
        db.session.add(job_details)

        db.session.commit()
        print ('score',score)
        return render_template('index.html', score=score)
        
    else:
        return render_template('index.html')