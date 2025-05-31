#  Vorcleaner

**Vorcleaner** is a modern and user-friendly Windows cache cleaner built with 

**PyQt5**, designed to improve performance, free up space, and optionally **disable Windows Updates** with a single click becuase is **AI Based**
> Created with love by [Shayan Ghadamian](#)

---

## 🚀 Features

- ✅ **Deep Cache Cleaning** – Deletes junk files from:
  - Windows Temp, Prefetch, Installer, Recycle Bin
  - Ai Based
  - Chrome, Edge, Firefox cache
  - Teams, Spotify, Adobe, and more
- ⚡ **Fast & Safe** – Smart file handling, avoids files in use
- 🌗 **Light/Dark Mode** – Toggle beautiful themes easily
- 🔻 **Disable/Enable Windows Update** – Includes advanced controls:
  - Disables `wuauserv`, `bits`, `dosvc`, `UsoSvc`, `WaaSMedicSvc`
  - Disables update tasks like `Schedule Scan` and `Scheduled Start`
- 🔔 **System Notifications** – Completion alerts via system tray
- 💬 **Live Logs** – See real-time cleaning progress

---

## 🖼️ Preview

![Vorcleaner Screenshot Light](https://your-screenshot-link-here)
![Vorcleaner Screenshot Dark](https://your-screenshot-link-here)

---

## 📦 Requirements

- Python 3.8+
- Admin privileges (auto-prompts if needed)

### 🔧 Install dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt`**
```
PyQt5
plyer
```

---

## ▶️ How to Run

```bash
python main.py
```

Make sure you're running with **Administrator privileges** to allow cleaning protected 

directories and managing services.

---

## 🛑 Windows Update Toggle (Important)

The "Disable Update" button:
- **First click**: Disables all core update services and tasks
- **Second click**: Re-enables everything back to normal

Make sure to **run as administrator**, or the update toggle won’t function properly.

---

## 🧪 Tested On

- ✅ Windows 10 (21H2+)
- ✅ Windows 11 (22H2+)

---

## 📁 Directory Structure

```
Vorcleaner/
├── main.py
├── vorcleaner.ico
├── requirements.txt
└── README.md
```

---

## ❤️ Credits

Created by **Shayan Ghadamian**

> Open to contributions, feedback, and ideas!



## 📜 License

This project is licensed under the [MIT License](LICENSE).
