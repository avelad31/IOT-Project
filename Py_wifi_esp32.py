import face_recognition
import cv2
import os
import numpy as np
import serial
import time
from pyModbusTCP.client import ModbusClient

class FaceRecognition:
    def __init__(self, esp32_ip='192.168.18.116', esp32_port=502):  ##PONER EL IP
        self.known_face_encodings, self.known_face_names = self.load_database()
        self.video_capture = cv2.VideoCapture(0)  # 0 or 1 according to the computer's camera

        # ESP32 communication setup
        self.esp32_ip = esp32_ip
        self.esp32_port = esp32_port
        self.esp32_modbus = ModbusClient(host=self.esp32_ip, port=self.esp32_port, auto_open=True)
        time.sleep(2)  # Allow time for ESP32 to initialize

    def load_database(self):
        known_face_encodings = []
        known_face_names = []

        # Database path
        database_path = "database"

        for filename in os.listdir(database_path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(database_path, filename)
                face_image = face_recognition.load_image_file(image_path)
                face_encoding = face_recognition.face_encodings(face_image)[0]

                known_face_encodings.append(face_encoding)
                known_face_names.append(os.path.splitext(filename)[0])

        return known_face_encodings, known_face_names

    def run_recognition(self):
        while True:
            # Capture frame from the camera
            ret, frame = self.video_capture.read()

            # Convert the image from BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Find all faces in the frame
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            confidence = 0
            
            # Iterate over each face in the frame
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Compare with known faces
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Desconocido"

                # If there are matches, use the closest one
                if True in matches:
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = matches.index(True)
                    confidence = (1 - face_distances[best_match_index] + 0.15) * 100
                    name = self.known_face_names[best_match_index]
                else:
                    confidence=0

                # Draw rectangle, display the name, and confidence %
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                label = f"{name} ({confidence:.2f}%)"
                cv2.putText(frame, label, (left + 6, bottom - 6), font, 0.5, (0, 255, 0), 2)
 
            print("Confidencia: ", confidence)
            # Write '0' or '1' to Modbus registers based on confidence
            if confidence >= 75:
                self.esp32_modbus.write_single_coil(0, 1)
                print("Enviando valor 1")  
            else:
                self.esp32_modbus.write_single_coil(0, 0) 
                print("Enviando valor 0") 
                
            cv2.imshow('Video', frame)

            # Exit with 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release resources
        self.video_capture.release()
        cv2.destroyAllWindows()
        self.esp32_modbus.close()  # Close the Modbus connection

if __name__ == "__main__":
    recognizer = FaceRecognition()
    recognizer.run_recognition()
