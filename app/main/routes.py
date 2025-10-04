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
        print (request.form)
        if not('file' in request.files or "existingFile" in request.form) or 'description' not in request.form:
            return jsonify({'error':'Missing fields'}),400
        if "existingFile" in request.form:
            resume_id = request.form["existingFile"]
            text = Resume.query.get(resume_id).parsed_text
            print ('text',text)
        else:
            file = request.files['file']
            if file.filename=='':
                return jsonify({'error':'No file selected'}),400
            filename = f'{int(time.time())}{secure_filename(file.filename)}'
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'],filename)
            file.save(filepath)
            text = ""
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            uploaded_resume = Resume(
                filename = filename,
                filepath = filepath,
                mimetype = file.mimetype,
                size = os.path.getsize(filepath),
                parsed_text = text
            )
            db.session.add(uploaded_resume)

        description = request.form['description']
        title = request.form['job_title']
        company = request.form['company']       

        model = SentenceTransformer('all-MiniLM-L6-v2')
        resume_embeddings = model.encode(text, convert_to_tensor=True)
        job_desc_embeddings = model.encode(description, convert_to_tensor=True)

        similarity = util.cos_sim(resume_embeddings, job_desc_embeddings)

        score = similarity.item()
        
        job_details = Job(
            title=title,
            content=description,
            company=company
        )

        db.session.add(job_details)

        db.session.commit()
        print ('score',score)
        return render_template('index.html', score=score)
        
    else:
        resumes = Resume.query.all()
        print (resumes)
        res = []
        for resume in resumes:
            res.append({"id":resume.id, "filename":resume.filename})
        return render_template('index.html',resumeList=res)