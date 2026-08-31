# Vorcleaner

**Vorcleaner** is a modern and user-friendly Windows cache cleaner built with **PyQt5**, designed to improve performance, free up space, and optionally **disable Windows Updates** with a single click because it is **AI Based**

> Created with love by [Shayan Ghadamian](#)

---

## Features

- **Deep Cache Cleaning** -- Deletes junk files from:
  - Windows Temp, Prefetch, Installer, Recycle Bin
  - AI Based
  - Chrome, Edge, Firefox cache
  - Teams, Spotify, Adobe, and more
- **Fast and Safe** -- Smart file handling, avoids files in use
- **Light/Dark Mode** -- Toggle beautiful OLED-inspired themes with green accent
- **Disable/Enable Windows Update** -- Includes advanced controls:
  - Disables `wuauserv`, `bits`, `dosvc`, `UsoSvc`, `WaaSMedicSvc`
  - Disables update tasks like `Schedule Scan` and `Scheduled Start`
- **System Notifications** -- Completion alerts via system tray
- **Live Logs** -- See real-time cleaning progress

---

## Requirements

- Python 3.8+
- Admin privileges (auto-prompts if needed)

### Install dependencies

```bash
pip install PyQt5 plyer
```

**`requirements.txt`**
```
PyQt5==5.15.11
plyer==2.1
```

---

## How to Run

```bash
python main.py
```

Make sure you are running with **Administrator privileges** to allow cleaning protected directories and managing services.

---

## Windows Update Toggle (Important)

The "Disable Update" button:
- **First click**: Disables all core update services and tasks
- **Second click**: Re-enables everything back to normal

Make sure to **run as administrator**, or the update toggle will not function properly.

---

## Tested On

- Windows 10 (21H2+)
- Windows 11 (22H2+)

---

## Directory Structure

```
Vorcleaner/
├── main.py
├── vorcleaner.ico
├── requirements.txt
├── README.md
└── ui/
    ├── __init__.py
    ├── main_window.py
    ├── styles.py
    └── widgets.py
```

---

## UI Architecture

The UI is split into modular components under the `ui/` directory:

| Module | Purpose |
|--------|---------|
| `ui/styles.py` | Theme definitions (Dark OLED + Light) with semantic color tokens |
| `ui/widgets.py` | Reusable UI components (buttons, progress, log, footer) |
| `ui/main_window.py` | Main window layout and theme switching |

---

## Credits

Created by **Shayan Ghadamian**

> Open to contributions, feedback, and ideas!

## License

This project is licensed under the [MIT License](LICENSE).
