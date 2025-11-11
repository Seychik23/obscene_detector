# Obscene Detector
Obscene Detector is a simple tool designed to identify inappropriate language in speech recognized through a microphone input.

## Features
- Real-time detection of inappropriate language.
- Built using the [SpeechRecognition](https://github.com/Uberi/speech_recognition) library.
- Utilizes **[PySide6](https://pyside.org/)** for the user interface.
- Multi-language support.
- Desktop notifications.

## Note
This is an alpha version of the software. Feedback and bug reports are welcome. Please note that this is a very early development version.

## Installation
To get started, clone the repository and install the required dependencies:

### Prerequisites

#### System Dependencies

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install portaudio19-dev python3-dev alsa-utils
```

**Fedora Linux/RHEL:**
```bash
sudo dnf install portaudio-devel python3-devel alsa-lib-devel
```

**Arch Linux:**
```bash
sudo pacman -S portaudio python-base
```

## Preparing steps

### Option 1: Using `uv` (recommended)
```bash
git clone https://github.com/Seychik23/obscene_detector.git
cd obscene_detector
uv sync
python -m app
```

### Option 2: Using `pip`
```bash
git clone https://github.com/Seychik23/obscene_detector.git
cd obscene_detector
pip install -e .
python -m app
```

## Usage

After installation, you can run the application using:
```bash
python -m app
```

## Project Structure
```
obscene_detector/
├── app/                 # Main application package
│   ├── __main__.py     # Application entry point
│   ├── main_window.py   # GUI main window
│   ├── worker.py       # Background worker
│   ├── conf_manager.py  # Configuration manager
│   ├── word_manager.py  # Word list manager
│   └── locale/         # Translation files
├── data/               # Data files
├── detector.conf       # Configuration file
└── pyproject.toml      # Project dependencies
```

## Install with development dependencies
```bash
uv sync --dev
```

## Troubleshooting

### PyAudio Installation Fails:
- Ensure system dependencies are installed (see Prerequisites section).
- On Windows(not tested yet), try:
  ```bash
  pip install pipwin && pipwin install pyaudio
  ```

### No Microphone Detected:
- Check microphone permissions.
- Ensure the microphone is not being used by another application.
- On Linux, verify ALSA is working:
  ```bash
  alsamixer
  ```

## License

This project is licensed under the MIT License.
