from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QMenuBar, QAction, QStatusBar, QInputDialog, QMainWindow, 
    QScrollArea, QTextBrowser
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.bot import Query, Reply
import pyttsx3




class MyHealthCareBot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.query = Query()
    
        
        self.patient_name = None
        self.patient_age = None
        # ✅ Initialize Text-to-Speech (TTS) Engine inside the class
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty("rate", 150)  # Adjust speech speed
        self.tts_engine.setProperty("volume", 1.5)  # Set volume level
        

    def initUI(self):
        self.setWindowTitle('🩺 AI-Powered HealthCare Chatbot')
        self.setGeometry(100, 100, 700, 500)

        # Create widgets
        self.label = QLabel('Enter Patient Name:')
        self.input_text = QLineEdit()
        self.submit_button = QPushButton('Submit')
        self.output_browser = QTextBrowser()
        self.output_browser.setOpenExternalLinks(True)

        # Style widgets
        self.label.setStyleSheet('font-size: 18px; font-weight: bold; color: #2C3E50; padding: 5px;')
        self.input_text.setStyleSheet('padding: 10px; color:white; border-radius: 5px; border: 2px solid #007BFF; font-size: 14px;')
        self.submit_button.setStyleSheet('''
            QPushButton { padding: 10px; background-color: #007BFF; color: white; font-size: 14px; font-weight: bold; border: none; border-radius: 5px; }
            QPushButton:hover { background-color: #0056b3; }
        ''')
        self.output_browser.setStyleSheet('''
            QTextBrowser { font-size: 14px; background-color: #2C3E50; border: 1px solid #7a7c7d; padding: 10px; border-radius: 5px; }
        ''')
        self.output_browser.setFont(QFont("Arial", 12))
        self.output_browser.setAlignment(Qt.AlignTop)

        # Create scrollable output area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.output_browser)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_text)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.scroll_area)

        # Create central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect button click event to function
        self.submit_button.clicked.connect(self.collect_patient_info)
        

    def collect_patient_info(self):
        """
        Step 1: Collect Name and Age before asking for Symptoms
        """
        if not self.patient_name:
            self.patient_name = self.input_text.text().strip()
            if not self.patient_name:
                self.output_browser.setText("<b>Please enter your name.</b>")
                return
            self.label.setText(f'Hello {self.patient_name}! Please Enter your Age:')
            self.input_text.clear()
            return

        if not self.patient_age:
            try:
                self.patient_age = int(self.input_text.text().strip())
                if self.patient_age < 0 or self.patient_age > 100:
                    self.output_browser.setText("<b>Please enter a valid age (0-100).</b>")
                    self.patient_age = None
                    return
            except ValueError:
                self.output_browser.setText("<b>Please enter a valid number for age.</b>")
                return

            # Move to symptom collection
            self.label.setText(f'Thank you, {self.patient_name} (Age: {self.patient_age})! Tell me about your symptoms:')
            self.input_text.clear()
            return

        # If name & age are already collected, process symptoms
        self.process_input()

    def process_input(self):
        """
        Step 2: Get Symptoms and Send to AI
        """
        user_input = self.input_text.text().strip()
        if not user_input:
            self.output_browser.setText("<b>Please enter your symptoms.👆</b>")
            return

        # Update query with user details
        self.query.set_param("name", self.patient_name)
        self.query.set_param("age", self.patient_age)
        self.query.set_message(user_input)

        # Call chatbot API
        bot_output = Reply(self.query.create_message()).send(interactive=True)
        print("DEBUG: bot_output =", bot_output)

        bot_output = str(bot_output)  # Ensure it's a string


        
        # Process bot_output separately before inserting into f-string
        formatted_bot_output = bot_output.replace(":**", "</b>:").replace("**", "<b>").replace("*", "-").replace("\n", "<br>")

        formatted_output = f"""
        <p><b>Patient Name:</b> {self.patient_name}</p>
        <p><b>Patient Age:</b> {self.patient_age}</p>
        <p><b>Symptoms:</b> {user_input}</p>
        <hr>
        <p><b>Dr. Lili:</b></p>
        <pre style="white-space: pre-wrap; font-size: 14px; font-family: Arial; line-height: 1.5;">
        {formatted_bot_output}
        </pre>
        """


        # call the output formatS

        # Update the output QTextBrowser with formatted text
        self.output_browser.setHtml(formatted_output)

        # Auto-scroll to the bottom
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )
        # self.tts_engine.say(formatted_bot_output)
        # self.tts_engine.runAndWait()
        
		
        
		
