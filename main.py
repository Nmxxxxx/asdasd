from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog, QTextEdit
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import torch
from transformers import pipeline


class VideoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ видео")
        self.setGeometry(100, 100, 400, 300)

        # Элементы интерфейса
        self.upload_button = QPushButton("Загрузить видео")
        self.extract_audio_button = QPushButton("Извлечь звук")
        self.audio_to_text_button = QPushButton("Перевести звук в текст")
        self.analyze_text_button = QPushButton("Анализ текста")
        self.result_text = QTextEdit()

        self.upload_button.clicked.connect(self.upload_video)
        self.extract_audio_button.clicked.connect(self.extract_audio)
        self.audio_to_text_button.clicked.connect(self.audio_to_text)
        self.analyze_text_button.clicked.connect(self.analyze_text)

        layout = QVBoxLayout()
        layout.addWidget(self.upload_button)
        layout.addWidget(self.extract_audio_button)
        layout.addWidget(self.audio_to_text_button)
        layout.addWidget(self.analyze_text_button)
        layout.addWidget(self.result_text)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.video_path = ""
        self.audio_path = ""
        self.text = ""

    def upload_video(self):
        file_dialog = QFileDialog()
        self.video_path, _ = file_dialog.getOpenFileName(self, "Выберите видеофайл", "", "Video Files (*.mp4 *.avi)")
        if self.video_path:
            self.result_text.setText(f"Видео загружено: {self.video_path}")

    def extract_audio(self):
        if not self.video_path:
            self.result_text.setText("Сначала загрузите видео.")
            return
        video = VideoFileClip(self.video_path)
        self.audio_path = "audio.wav"
        video.audio.write_audiofile(self.audio_path)
        self.result_text.setText("Звук извлечен из видео.")

    def audio_to_text(self):
        if not self.audio_path:
            self.result_text.setText("Сначала извлеките звук.")
            return
        recognizer = sr.Recognizer()
        with sr.AudioFile(self.audio_path) as source:
            audio = recognizer.record(source)
            self.text = recognizer.recognize_google(audio, language="ru-RU")
            self.result_text.setText(f"Текст из аудио: {self.text}")

    def analyze_text(self):
        if not self.text:
            self.result_text.setText("Сначала переведите звук в текст.")
            return
        classifier = pipeline("sentiment-analysis", model="cointegrated/rubert-tiny")
        result = classifier(self.text)
        self.result_text.setText(f"Анализ текста: {result}")


app = QApplication([])
window = VideoApp()
window.show()
app.exec()
