# 🔐 Keylogger Project

A Python-based keylogger application with a modern GUI interface built using Tkinter. This project logs keyboard events, stores them in JSON format, and provides functionality to convert logs to readable text files.

## Demo Video --> https://drive.google.com/file/d/13T-MxqjFM7_-FOMzUJPZ8OFN9CKLzw17/view?usp=drive_link

## PPTX --> https://docs.google.com/presentation/d/1SpEHlm2ZyTEyQFc-JwTisq9qmosJPNBb/edit?usp=drive_link&ouid=112011770901139299951&rtpof=true&sd=true

## ✨ Features

- 🖥️ **Modern GUI Interface** - Clean and intuitive Tkinter-based interface
- ⌨️ **Real-time Keystroke Logging** - Captures all keyboard events
- 💾 **JSON Storage** - Stores keystrokes in structured JSON format with timestamps
- 📄 **TXT Conversion** - Convert JSON logs to human-readable text format
- 👁️ **Log Viewer** - View recent activity directly in the GUI
- 🗑️ **Clear Logs** - Easy log management
- 📊 **Live Counter** - Real-time keystroke count display

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Setup

1. Clone this repository:
```bash
git clone https://github.com/SatyamPandey-07/keylogger-project.git
cd keylogger-project
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## 📖 Usage

Run the application:
```bash
python keylogger.py
```

### GUI Controls

- **▶ Start Logging** - Begin recording keystrokes
- **⏹ Stop Logging** - Stop recording keystrokes
- **📄 Convert to TXT** - Convert JSON log to readable text file
- **👁 View Logs** - Display recent keystrokes in the interface
- **🗑 Clear Logs** - Delete all recorded logs

### Files Generated

- `keylog.json` - Stores all keystrokes in JSON format
- `keylog.txt` - Human-readable log file (after conversion)

## 🛠️ Technical Details

### Dependencies
- `pynput` - For keyboard event monitoring
- `tkinter` - For GUI interface (comes with Python)

### Data Structure

Keystrokes are stored in JSON format:
```json
{
    "keystrokes": [
        {
            "event": "press",
            "key": "a",
            "timestamp": "2025-12-24 10:30:45.123456"
        }
    ]
}
```

## ⚠️ Disclaimer

This project is created for **educational purposes only**. Users must comply with all applicable laws and regulations. Unauthorized use of keyloggers may be illegal in many jurisdictions. Always obtain proper consent before monitoring keyboard activity.

## 📝 License

This project is open-source and available for educational purposes.

## 👤 Author

**Satyam Pandey**
- GitHub: [@SatyamPandey-07](https://github.com/SatyamPandey-07)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

**Note:** Use this software responsibly and ethically. The author is not responsible for any misuse of this application.
