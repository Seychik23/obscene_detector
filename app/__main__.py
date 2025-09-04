# Copyright (c) 2025 Seychik23
# This software is licensed under the MIT License.
# See the LICENSE file for more details.

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from .main_window import MainWindow

try:
    import notify2
    notify2.init("Obscene Detector")
    _notify_available = True
    print("Successfully initialized notify2 for notifications.")
except ImportError:
    _notify_available = False
    print("Notify2 module not found. Notifications will be disabled.")
except Exception as e:
    _notify_available = False
    print("Failed to initialize notify2. Notifications will be disabled.")


def main():
    app = QApplication(sys.argv)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, 'icons', 'icon.png')

    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    else:
        print(f'Warning! Icon file not found at: {icon_path}')

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()