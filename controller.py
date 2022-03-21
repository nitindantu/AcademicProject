from flask import Flask, render_template, request,Response
from werkzeug.utils import secure_filename
import os
import cv2

UPLOAD_FOLDER = 'static'

  
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


  
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return render_template('index.html')
@app.route('/imguploader', methods = ['GET', 'POST'])
# ‘/’ URL is bound with hello_world() function.
def imguploader():
    if request.method == 'POST':
      file = request.files['file']
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      #f.save(secure_filename(f.filename))
      fname = "/static/" + file.filename
      print("stored as:" + filename)
      return render_template("imgupload.html", uploaded_image=fname)
      

@app.route('/viduploader', methods = ['GET', 'POST'])
# ‘/’ URL is bound with hello_world() function.
def viduploader():
    if request.method == 'POST':
      file = request.files['file']
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      #f.save(secure_filename(f.filename))
      fname = "C:/Users/nitin/Desktop/FacialRecognition_FYP/static/" + file.filename
      print("stored as:" + fname)
    global camera
    camera = cv2.VideoCapture(fname)  # use 0 for web camera
    return render_template("vdupload.html")
      
 
@app.route('/camloader', methods = ['GET', 'POST'])
# ‘/’ URL is bound with hello_world() function.
def camloader():
    if request.method == 'POST':
        global camera
        camera = cv2.VideoCapture(0)  # use 0 for web camera
        return render_template('camera.html') 
       

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        global frame
        success, frame = camera.read()  # read the camera frame

        #faces = face_cascade.detectMultiScale(frame)
        #for (x, y, w, h) in faces:
               # cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)

        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame1 = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n')  # concat frame one by one and show result


@app.route("/myvideo_feed")
def myvideo_feed():

    # return the response generated along with the specific media
    # type (mime type)
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    
  
# main driver function
if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)