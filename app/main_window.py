# Copyright (c) 2025 Seychik23
# This software is licensed under the MIT License.
# See the LICENSE file for more details.

import notify2
import os
from PySide6.QtWidgets import ( QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QMenuBar, QMenu, QMessageBox)

from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Slot

from .worker import RecognitionWorker
from .word_manager import load_words_for_current_language

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setMinimumSize(400, 200)
        self.resize(500, 300)

        self.setWindowTitle("Obscene detector (alpha version)")
        self.bad_words = load_words_for_current_language()
        
        # GUI
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        
        self.status_label = QLabel("Нажмите 'Старт' для начала работы")
        self.toggle_button = QPushButton("Старт")
        
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.toggle_button)
        
        self.setCentralWidget(self.central_widget)
        
        # Init
        self.worker = None
        self.is_listening = False
        
        # Connect start button
        self.toggle_button.clicked.connect(self.toggle_listening)

        # Check if notify2 is available
        try:
            import notify2
            notify2.init("Obscene Detector")
        except ImportError:
            print("Warning: notify2 library not found. Notifications will be disabled.")
            pass

        # Menu bar
        self._create_menus()
   
    def _create_menus(self):
        menu_bar=self.menuBar()


        settings_menu = menu_bar.addMenu("Настройки")

        set_lang_file_action = QAction("Выбрать файл языка", self)      
        set_lang_file_action.triggered.connect(self._select_language_file)
        settings_menu.addAction(set_lang_file_action)

        '''
        # For settings qaction
        configure_action = QAction("Настроить...", self)
        configure_action.setEnabled(False) 
        settings_menu.addAction(configure_action)
        
        '''

        help_menu = menu_bar.addMenu("Справка")
        
        # About menu
        about_app_action = QAction("О Obscene Detector", self)
        about_app_action.triggered.connect(self._show_about_dialog)  
        help_menu.addAction(about_app_action)
        
        # Default Qt about dialog
        about_qt_action = QAction("О Qt", self)
        about_qt_action.triggered.connect(lambda: QMessageBox.aboutQt(self))  
        help_menu.addAction(about_qt_action)


    @Slot()
    def _select_language_file(self):
     #todo
        pass

    def _show_about_dialog(self):
        QMessageBox.about(self, "О Obscene Detector",
            "<h3>Obscene Detector</h3>"
            "<p>Простая утилита для обнаружения нецензурной лексики в речи, распознаваемой через микрофон.</p>"
            "<p>Версия: 0.1 (alpha)</p>"
            "<p><b>Альфа-версия!</b>. Только для тестирования!</p>"
            "<hr>"
            "<p>Использует библиотеку: <a href='https://github.com/Uberi/speech_recognition'>SpeechRecognition</a></p>"
            "<p>Лицензия: <a href='https://mit-license.org/'>MIT License</a></p>"      
            "<p>Copyight (c) 2025 Seychik23</p>"
        
        )

    def toggle_listening(self):
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()

    def start_listening(self):
        self.worker = RecognitionWorker()
        
        # Connect signals from the worker to slots in this class
        self.worker.recognized_text.connect(self.handle_recognition)
        self.worker.error_occurred.connect(self.handle_error)
        
        self.worker.start()
        self.is_listening = True
        self.toggle_button.setText("Стоп")
        self.status_label.setText("Слушаю микрофон...")

    def stop_listening(self):
        if self.worker:
            self.worker.stop()
            self.worker.wait() 
        self.is_listening = False
        self.toggle_button.setText("Старт")
        self.status_label.setText("Остановлено. Нажмите 'Старт' для начала.")

    @Slot(str)
    def handle_recognition(self, text):
        self.status_label.setText(f"Распознано: {text}")
        found_words = [word for word in self.bad_words if word in text.lower()]
        
        if found_words:
            print(f"Обнаружено: {', '.join(found_words)}")
            self.send_notification("Обнаружена ненормативная лексика!")
            # Red st
            self.status_label.setStyleSheet("color: red;")
        else:
            self.status_label.setStyleSheet("") # Reset color

    @Slot(str)
    def handle_error(self, error_message):
        self.status_label.setText(f"Ошибка: {error_message}")
        self.status_label.setStyleSheet("color: red;")
        self.stop_listening()

    def send_notification(self, message):
        notification = notify2.Notification("Предупреждение", message)
        notification.show()

    def closeEvent(self, event):
        self.stop_listening()
        event.accept()
