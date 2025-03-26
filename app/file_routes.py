<<<<<<< HEAD
import os
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity

file_bp = Blueprint("file", __name__)
BASE_UPLOAD_FOLDER = 'uploads'
=======
from flask import Blueprint, request, render_template, redirect, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os

file_bp = Blueprint("file", __name__)
UPLOAD_FOLDER = 'uploads'
>>>>>>> ff07861 (feat: Add file upload feature and UI updates)
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

<<<<<<< HEAD
@file_bp.route("/upload", methods=["GET", "POST"])
@jwt_required()
def upload_file():
    username = get_jwt_identity()  # 🔐 Get the current logged-in user's identity

    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file part")
=======
@file_bp.route('/upload', methods=['GET', 'POST'])
@jwt_required()
def upload_file():
    username = get_jwt_identity()  # get current user
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
>>>>>>> ff07861 (feat: Add file upload feature and UI updates)
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
<<<<<<< HEAD
            flash("No selected file")
=======
            flash('No selected file')
>>>>>>> ff07861 (feat: Add file upload feature and UI updates)
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
<<<<<<< HEAD

            # ✅ Create user-specific upload path
            user_folder = os.path.join(BASE_UPLOAD_FOLDER, username)
            os.makedirs(user_folder, exist_ok=True)

=======
            user_folder = os.path.join(UPLOAD_FOLDER, username)
            os.makedirs(user_folder, exist_ok=True)
>>>>>>> ff07861 (feat: Add file upload feature and UI updates)
            file.save(os.path.join(user_folder, filename))
            return render_template("upload.html", message="File uploaded successfully!")

        return render_template("upload.html", message="Invalid file type!")

    return render_template("upload.html")
