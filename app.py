
from flask import Flask, render_template, request, redirect, flash, url_for, render_template_string
import urllib.request
from werkzeug.utils import secure_filename
from main_image import getPrediction
import os
import numpy as np
import cv2
from bot import get_response

cattle_app = Flask(__name__)

@cattle_app.route("/")
@cattle_app.route("/home")
def home():
    return render_template("index.html")


@cattle_app.route('/skin_diease_form',  methods=['GET'])
def skin_diease_form():
    return render_template('predict.html', predicted=False)


@cattle_app.route('/predict_skin_diease_image', methods=['POST'])
def predict_skin_diease_image():
    print(request.url)
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.referrer)
        file = request.files['image']
        if file:
            # convert string of image data to uint8
            nparr = np.fromstring(request.files['image'].read(), np.uint8)
            # decode image
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            label1, acc1, label2, acc2, label3, acc3, doctor = getPrediction(img)
            flash(label1)
            flash(acc1)
            flash(label2)
            flash(acc2)
            flash(label3)
            flash(acc3)
            f1=acc1.find('e')
            f2=acc2.find('e')
            f3=acc3.find('e')
            if(f1!=-1):
                acc1="0"
            if(f2!=-1):
                acc2="0"
            if(f3!=-1):
                acc3="0"

            return render_template("predict.html", predicted=True, label1=label1, label2=label2, label3=label3, acc1=acc1, acc2=acc2, acc3=acc3, doctor=doctor)

@cattle_app.route('/social_page')
def social_page():
    return render_template('social.html')


@cattle_app.route("/bot")
def bot():
	return render_template("chatbot.html")

@cattle_app.route("/chatbot_response", methods=["GET","POST"])
def chatbot_response():
    msg = request.form["msg"]
    response = get_response(msg)
    return str(response)

@cattle_app.route("/skin_diease_camera", methods=["GET","POST"])
def skin_diease_camera():
    return render_template_string('''
<video id="video" width="640" height="480" autoplay style="background-color: grey"></video>
<button id="send">Take & Send Photo</button>
<canvas id="canvas" width="640" height="480" style="background-color: grey"></canvas>

<script>

// Elements for taking the snapshot
var video = document.getElementById('video');
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');

// Get access to the camera!
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Not adding `{ audio: true }` since we only want video now
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        //video.src = window.URL.createObjectURL(stream);
        video.srcObject = stream;
        video.play();
    });
}

// Trigger photo take
document.getElementById("send").addEventListener("click", function() {
    context.drawImage(video, 0, 0, 640, 480); // copy frame from <video>
    canvas.toBlob(upload, "image/jpeg");  // convert to file and execute function `upload`
});

function upload(file) {
    // create form and append file
    var formdata =  new FormData();
    formdata.append("image", file);
    
    // create AJAX requests POST with file
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "{{ url_for('predict_skin_diease_image') }}", true);
    xhr.onload = function() {
        if(this.status = 200) {
            document.write(this.response);
        } else {
            console.error(xhr);
        }
    };
    xhr.send(formdata);
}

</script>
''')

if __name__ == "__main__":
    cattle_app.secret_key = 'super secret key'
    cattle_app.run(debug=True)
    