import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import os
import face_recognition as fr
import mediapipe as mp
import numpy as np
#############################################
import serial
import time
from pyModbusTCP.client import ModbusClient
#############################################


class FaceRecognitionAndBlinkApp:
    def __init__(self, root, esp32_ip, esp32_port):
        self.root = root
        self.root.title("Face Recognition and Blink Verification")
        self.root.geometry("800x600")

        # Initialize camera
        self.cap = cv2.VideoCapture(0)

        # Face recognition data
        self.known_face_encodings, self.known_face_names = self.load_database()

        # Face Mesh initialization for blink detection
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

        # Blink detection variables
        self.blink_count = 0
        self.blink_verification_active = False
        self.user_verified = False
        self.ratio_list = []
        self.counter_time = 0
        # self.User_i = 0  # variable de la clase


        # UI elements
        self.label = tk.Label(root)
        self.label.pack()
        self.btn_verify_blink = tk.Button(root, text="Start Blink Verification", command=self.activate_blink_verification)
        self.btn_verify_blink.pack()

        #############################################
        # ESP32 communication setup
        self.esp32_ip = esp32_ip
        self.esp32_port = esp32_port
        self.esp32_modbus = ModbusClient(host=self.esp32_ip, port=self.esp32_port, auto_open=True)
        time.sleep(2)  # Allow time for ESP32 to initialize
        #############################################

        # Update frame
        self.update_frame()

    def load_database(self):
        known_face_encodings = []
        known_face_names = []

        # Path to the face database
        database_path = "database"

        for filename in os.listdir(database_path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(database_path, filename)
                face_image = fr.load_image_file(image_path)
                face_encoding = fr.face_encodings(face_image)[0]

                known_face_encodings.append(face_encoding)
                known_face_names.append(os.path.splitext(filename)[0])

        return known_face_encodings, known_face_names

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Face recognition
            face_locations = fr.face_locations(rgb_frame)
            face_encodings = fr.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = fr.compare_faces(self.known_face_encodings, face_encoding)
                name = "Desconocido"
                
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]
                    self.user_verified = True
                    print(f"User Verified: {name}")  # Debugging print
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
                    break  # Break after first match
                else:
                    self.user_verified = False
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
                    break

            # Blink detection if activated
            if self.blink_verification_active:
                self.process_blink_detection(frame)

            # Display the frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.label.config(image=self.photo)

        self.root.after(10, self.update_frame)

    def process_blink_detection(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                self.mp_drawing.draw_landmarks(frame, face_landmarks, self.mp_face_mesh.FACE_CONNECTIONS)
                landmarks = np.array([(landmark.x, landmark.y) for landmark in face_landmarks.landmark])
                
                # Define the landmarks for the left eye
                left_up = landmarks[159]
                left_down = landmarks[23]
                left_left = landmarks[130]
                left_right = landmarks[243]

                # Calculate distances
                length_ver = np.linalg.norm(left_up - left_down)
                length_hor = np.linalg.norm(left_left - left_right)

                ratio = (length_ver / length_hor) * 100
                self.ratio_list.append(ratio)

                # Blink detection logic
                # Asegurarse de que hay suficientes elementos en self.ratio_list antes de calcular el promedio
                if len(self.ratio_list) >= 2:
                    # Si el ratio anterior estaba por debajo del umbral y el actual está por encima, cuenta un parpadeo
                    if self.ratio_list[-2] < 36 and self.ratio_list[-1] >= 35:
                        self.blink_count += 1

                # Agrega el ratio actual a la lista
                self.ratio_list.append(ratio)
                if len(self.ratio_list) > 2:
                    self.ratio_list.pop(0)  # Mantiene solo los últimos dos ratios
                    
                if self.blink_count >= 2:
                    self.blink_verification_active = False
                    # self.User_i = 1
                    #############################################
                    self.esp32_modbus.write_single_coil(0, 1)
                    print("Enviando valor 1")
                    # messagebox.showinfo("Verification Complete", "Blink verification complete!")
                    self.esp32_modbus.write_single_coil(0, 0)
                    self.blink_count = 0
                else:
                    self.esp32_modbus.write_single_coil(0, 0) 
                    print("Enviando valor 0") 
                #############################################
    

    def activate_blink_verification(self):
        if self.user_verified:
            self.blink_verification_active = True
            self.blink_count = 0
            messagebox.showinfo("Vrification started", "Quitese los lentes si tiene, pestañee detenidamente")
        else:
            messagebox.showinfo("Info", "User not verified")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.cap. release()
            self.root.destroy()
            #############################################
            self.esp32_modbus.close()  # Close the Modbus connection
            #############################################
        

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionAndBlinkApp(root,'10.1.17.48',502)    #IP ASOCIADO
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


