from sre_constants import SUCCESS
from urllib import request
from flask import Flask, render_template, Response
import cv2
import face_recognition
import numpy as np
from pyzbar.pyzbar import decode
import requests
import json



app=Flask(__name__)
camera = cv2.VideoCapture(0)
# Load a sample picture and learn how to recognize it.
# Load a sample picture and learn how to recognize it.
arslan_image = face_recognition.load_image_file("pictures/arslan.jpg")
arslan_face_encoding = face_recognition.face_encodings(arslan_image)[0]

jabbar_image = face_recognition.load_image_file("pictures/jab.jpg")
jabbar_face_encoding = face_recognition.face_encodings(jabbar_image)[0]


#POST API
# headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

# r = requests.post("localhost:3002/api/analytic", headers=headers, data=json.dumps({
#      "testID": "000-000-001",
#     "testcenter": "Public School Sukkur",
#     "detected":"arslan",
#     "gender":"male",
#     "authorized":"true"
# }))



saif_image = face_recognition.load_image_file("pictures/saif.jpg")
saif_face_encoding = face_recognition.face_encodings(saif_image)[0]

ghafoor_image = face_recognition.load_image_file("pictures/ghafoor.png")
ghafoor_face_encoding = face_recognition.face_encodings(ghafoor_image)[0]

tahir_image = face_recognition.load_image_file("pictures/tahir.png")
tahir_face_encoding = face_recognition.face_encodings(tahir_image)[0]


amjad_image = face_recognition.load_image_file("pictures/amjad.png")
amjad_face_encoding = face_recognition.face_encodings(amjad_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    arslan_face_encoding,

    jabbar_face_encoding,
    saif_face_encoding,
    ghafoor_face_encoding,
    tahir_face_encoding,
    amjad_face_encoding
    
]
known_face_names = [
    "Arslan",
    "Jabbar",
    "Saif", 
    "Ghafoor",
    "Tahir",
    "Amjad"
]
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
detected  = []


def face_detect():  
    countCountinue = 0
    detectedAC = False
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
           
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)
            


            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                
                if(name not in detected):

                    prevName = name;

                    if(prevName==name):
                        countCountinue+=1
                        if(countCountinue>=50):
                            countCountinue = 0
                            detectedAC = True
                    
                    if(detectedAC):
                        
                        detected.append(name)
                        print(detected)
                        detectedAC = False
                        
                   
                else:
                    pass

                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            
            detector=cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
            eye_cascade = cv2.CascadeClassifier('Haarcascades/haarcascade_eye.xml')
            faces=detector.detectMultiScale(frame,1.1,7)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
             #Draw the rectangle around each face
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



#QR code generator
with open('myDataFile.txt') as f:
    myDataList = f.read().splitlines()

def qr_code():
    while True:
        success, frame = camera.read()  # read the camera frame
        for barcode in decode(frame):
            myData = barcode.data.decode('utf-8')
            if myData in myDataList:
                Output = "Authorized"
            else:
                Output = "UnAuthorized"
            #detect QR
            pts = np.array([barcode.polygon],np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(frame,[pts],True,(255,0,255),5)

            pts2 = barcode.rect
            cv2.putText(frame,(Output),(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,255),2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/face')
def face():
    return render_template('face_detection.html')

@app.route('/video')
def video():
    return Response(face_detect(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/qrcheck')
def qrcheck():
    return render_template('qr_code.html')

@app.route('/code')
def code():
    return Response(qr_code(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__=='__main__':
    app.run(debug=True)

# app = Flask(__name__)

# camera = cv2.VideoCapture(0)

# def generate_frames():
#     while True:
            
#         ## read the camera frame
#         success,frame=camera.read()
#         if not success:
#             break
#         else:
            
#             detector=cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
#             eye_cascade = cv2.CascadeClassifier('Haarcascades/haarcascade_eye.xml')
#             faces=detector.detectMultiScale(frame,1.1,7)
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#              #Draw the rectangle around each face
#             for (x, y, w, h) in faces:
#                 cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
#                 roi_gray = gray[y:y+h, x:x+w]
#                 roi_color = frame[y:y+h, x:x+w]
#                 eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)

#             ret,buffer=cv2.imencode('.jpg',frame)
#             frame=buffer.tobytes()

#             yield(b'--frame\r\n'
#                         b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video')
# def video():
#     return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__=="__main__":
#     app.run(debug=True)






# from pickletools import markobject
# from flask import Flask, redirect, url_for,render_template

# app = Flask(__name__)


# @app.route('/')
# def welcome():
#     return render_template('index.html')

# @app.route('/members')
# def mem():
#     return 'hello members how are you'


# @app.route('/success/<int:score>')
# def success(score):
#     return "The Person has passed and the mark is "+str(score)
    


# @app.route('/fail/<int:score>')
# def fail(score):
#     return "The person has failed and the mark is " +str(score)

# @app.route('/results/<int:marks>')
# def results(marks):
#     result=""
#     if marks<50:
#         result='fail'
#     else:
#         result='success'
#     return redirect(url_for(result,score=marks))



# if __name__ == '__main__':
#     app.run(debug=True)
