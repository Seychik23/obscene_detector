# Copyright (c) 2025 Seychik23
# This software is licensed under the MIT License.
# See the LICENSE file for more details.

import speech_recognition as sr
from PySide6.QtCore import QThread, Signal

class RecognitionWorker(QThread):
    
    # Signals for connection with main_window
    recognized_text = Signal(str)
    error_occurred = Signal(str)
    
    # Init speech recogition and mic
    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_running = True

    def run(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source) 

        print("Worker thread started, beginning to listen...")
        while self.is_running:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=5)
                
                try:
                    text = self.recognizer.recognize_google(audio, language='ru-RU') # used google speech recogition (temp)
                    self.recognized_text.emit(text)
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    self.error_occurred.emit(f"API Error: {e}")
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                self.error_occurred.emit(f"Mic Error: {e}")
                self.is_running = False

    def stop(self):
        self.is_running = False
        print("Command to stop the thread received...")
        self.quit() 
        self.wait() 