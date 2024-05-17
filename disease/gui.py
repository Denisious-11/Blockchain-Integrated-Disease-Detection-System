
import tkinter as tk
from tkinter import *
from tkinter import messagebox as msg
import numpy as np
from tensorflow.keras.models import load_model
import pickle
# Load the saved model
model_saved = load_model('prediction_model.h5')
with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# Function to make prediction
def predict():
    # Get the input data from the entry field
    input_entry = entry1.get()

    # Split the input data string by commas and convert it into a list of integers
    input= [int(x) for x in input_entry.split(',')]

    # Convert the list into a NumPy array and reshape it
    processed_data = np.array(input).reshape(1, 131, 1)

    # Make predictions using the model
    predictions = model_saved.predict(processed_data)

    # Get the predicted class index
    predicted_class_index = np.argmax(predictions)
    class_name = label_encoder.inverse_transform([predicted_class_index])[0]


    # Display the predicted class
    
    symptoms_text.delete(1.0, END)
    symptoms_text.insert(END, "Steps Behind the Scene:\n")
    symptoms_text.insert(END, "1. Input feature: {}\n".format(input))
    #symptoms_text.insert(END, "2. Processed Data: {}\n".format(processed_data))
    symptoms_text.insert(END, "3. Prediction_probabilities: {}\n".format(predictions))
    symptoms_text.insert(END, "4. Predicted_class_index: {}\n".format(predicted_class_index))
    symptoms_text.insert(END, "5. Prediction_classname: {}\n".format(class_name))
    


    # Show prediction result in a message box
    msg.showinfo("Prediction ", f"The predicted class is: {class_name}")

# GUI
top = tk.Tk()
top.configure(bg='light blue')
top.resizable(0, 0)
top.geometry('1200x650')
top.title('Disease prediction')

label1 = tk.Label(top, text="Disease Prediction", font=('Arial', 32, 'bold'), bg="light blue", fg="red")
label1.place(x=425, y=60)

# Open the image file
image = PhotoImage(file="desease.png")

# Resize the image using subsampling
width, height = 150, 150  # Set the desired width and height
resized_image = image.subsample(int(image.width() / width), int(image.height() / height))

image_label = Label(top, image=resized_image, bg="light blue")
image_label.place(x=240, y=30)

label2 = tk.Label(top, text="Symptoms", font=('Arial', 22, 'bold'), bg="light blue", fg="black")
label2.place(x=300, y=290)

entry1 = tk.Entry(top, width=30, font=("Arial", 20, 'bold'))
entry1.place(x=180, y=340)

symptoms_text = Text(top, height=15, width=40, font=('Arial', 14), bg="black", fg="white")
symptoms_text.place(x=690, y=190)

predict = tk.Button(top, text="Predict", width=20, bg="black", font=('Arial', 12, 'bold'), fg="white",
                    command=predict)
predict.place(x=290, y=420)
top.mainloop()

