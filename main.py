import os
import shutil
import getpass
import tempfile
import ctypes
import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QLabel, QProgressBar, QTextEdit, QHBoxLayout
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from plyer import notification


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, ' '.join(sys.argv), None, 1
    )
    sys.exit()

class CleanerThread(QThread):
    progress = pyqtSignal(int)
    done = pyqtSignal(int)
    log_signal = pyqtSignal(str)

    def is_file_in_use(self, file_path):
        try:
            os.rename(file_path, file_path)
            return False
        except OSError:
            return True

    def delete_temp_folder(self, folder_path):
        deleted = 0
        total = sum(len(files) for _, _, files in os.walk(folder_path))
        processed = 0

        for root, dirs, files in os.walk(folder_path, topdown=False):
            for name in files:
                try:
                    file_path = os.path.join(root, name)
                    processed += 1
                    if not self.is_file_in_use(file_path):
                        os.remove(file_path)
                        deleted += 1
                except:
                    continue
                if total:
                    self.progress.emit(min(100, int((processed / total) * 100)))
            for name in dirs:
                try:
                    shutil.rmtree(os.path.join(root, name), ignore_errors=True)
                except:
                    continue
        return deleted

    def run(self):
        user = getpass.getuser()
        locations = [
            tempfile.gettempdir(),
            f"C:/Users/{user}/AppData/Local/Temp",
            "C:/Windows/Temp",
            "C:/Windows/Prefetch",
            f"C:/Users/{user}/AppData/Local/Google/Chrome/User Data/Default/Cache",
            f"C:/Users/{user}/AppData/Local/Microsoft/Edge/User Data/Default/Cache",
            f"C:/Users/{user}/AppData/Local/Mozilla/Firefox/Profiles/*/cache2",
            f"C:/Users/{user}/AppData/Roaming/Microsoft/Windows/Recent",
            f"C:/Users/{user}/AppData/Roaming/Microsoft/Teams",
            f"C:/Users/{user}/AppData/Local/Spotify/Storage",
            f"C:/Users/{user}/AppData/Roaming/Adobe/Common/Media Cache Files",
            "C:/Windows/SoftwareDistribution/Download",
            f"C:/Users/{user}/AppData/Local/CrashDumps",
            f"C:/Users/{user}/AppData/Local/Temp/Temp1",
            f"C:/Users/{user}/AppData/LocalLow/Temp",
            f"C:/Users/{user}/AppData/LocalLow/Microsoft/CryptnetUrlCache",
            f"C:/Users/{user}/AppData/Local/Microsoft/CLR_v4.0",
            f"C:/Users/{user}/AppData/Local/Microsoft/Windows/WebCache",
            f"C:/Users/{user}/AppData/Local/Microsoft/Windows/Notifications",
            f"C:/Users/{user}/AppData/Local/ConnectedDevicesPlatform",
            f"C:/Users/{user}/AppData/Roaming/Spotify/Browser",
            f"C:/Users/{user}/AppData/Local/Opera Software/Opera Stable/Cache",
            f"C:/Users/{user}/AppData/Local/Yandex/YandexBrowser/User Data/Default/Cache",
            "C:/Windows/Temp/WPR_initiated_DiagTrack",
            "C:/Windows/Temp/perflogs",
            "C:/Windows/inf/logs",
            "C:/Windows/Logs/WindowsUpdate",
            "C:/Windows/ServiceProfiles/NetworkService/AppData/Local/Temp",
            "C:/Windows/ServiceProfiles/LocalService/AppData/Local/Temp",
            "C:/Windows/System32/config/systemprofile/AppData/Local/Temp",
            "C:/Windows/Minidump",
            "C:/Windows/Memory.dmp",
            "C:/Windows/Logs/CBS",
            "C:/$Recycle.Bin",
            "C:/$WINDOWS.~BT",
            "C:/$WINDOWS.~WS",
            "C:/Windows/Installer",
            "C:/ProgramData/Microsoft/Windows/DeliveryOptimization",
            "C:/Windows/System32/DriverStore/FileRepository",
            f"C:/Users/{user}/AppData/Local/Packages",
            "C:/Windows/System32/SysWow64/Tasks",
            f"C:/Users/{user}/AppData/Roaming/Local/Temp",
            f"C:/Users/{user}/AppData/Local/Packages/Temp",
            f"C:/Users/{user}/AppData/Local/Microsoft/Windows/INetCache",
            "C:/Windows/Logs/Diagnostic",
            "C:/Windows/Logs/WMI",
            "C:/ProgramData/Microsoft/Windows/Critical/Logs"
        ]
        total_deleted = 0
        total_locations = len(locations)
        for i, loc in enumerate(locations):
            if os.path.exists(loc):
                self.log_signal.emit(f"Deleting {loc}... {int(((i + 1) / total_locations) * 100)}%")
                total_deleted += self.delete_temp_folder(loc)
            self.progress.emit(int(((i + 1) / total_locations) * 100))

        try:
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x0007)
        except:
            pass

        self.done.emit(total_deleted)


class CacheCleanerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧹 Vorcleaner")
        self.setGeometry(100, 100, 520, 440)
        self.setWindowIcon(QIcon("vorcleaner.ico"))
        self.updates_disabled = False
        self.initUI()
        self.apply_light_theme()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        # HEADER
        header_layout = QHBoxLayout()
        self.dark_mode_btn = QPushButton("🌙")
        self.dark_mode_btn.clicked.connect(self.apply_dark_theme)
        self.light_mode_btn = QPushButton("☀️")
        self.light_mode_btn.clicked.connect(self.apply_light_theme)
        self.close_btn = QPushButton("❌")
        self.close_btn.clicked.connect(self.close)
        self.title = QLabel("Welcome To VorCleaner")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Segoe UI", 14, QFont.Bold))

        header_layout.addWidget(self.dark_mode_btn)
        header_layout.addWidget(self.light_mode_btn)
        header_layout.addWidget(self.title, 1)
        header_layout.addWidget(self.close_btn)

        # BODY
        self.disable_btn = QPushButton("Disable Update")
        self.disable_btn.clicked.connect(self.toggle_windows_update)
        self.clean_btn = QPushButton("Clean Now")
        self.clean_btn.clicked.connect(self.handle_clean)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.disable_btn)
        buttons_layout.addWidget(self.clean_btn)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setTextVisible(True)

        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignCenter)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFixedHeight(120)

        # FOOTER
        footer = QLabel("Create By Shayan Ghadamian")
        footer.setAlignment(Qt.AlignCenter)
        footer.setFont(QFont("Segoe UI", 9))
        footer.setStyleSheet("color: gray; padding-top: 8px;")

        # COMBINE
        main_layout.addLayout(header_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.progress)
        main_layout.addWidget(self.status)
        main_layout.addWidget(self.log_output)
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

    def handle_clean(self):
        self.status.setText("Cleaning in progress...")
        self.clean_btn.setEnabled(False)
        self.progress.setValue(0)
        self.log_output.clear()

        self.cleaner = CleanerThread()
        self.cleaner.progress.connect(self.progress.setValue)
        self.cleaner.done.connect(self.on_clean_done)
        self.cleaner.log_signal.connect(self.log)
        self.cleaner.start()

    def on_clean_done(self, total_deleted):
        self.status.setText(f"✅ Deleted {total_deleted} files (and emptied Recycle Bin).")
        self.clean_btn.setEnabled(True)
        self.send_notification(f"Cache cleaner completed.\nDeleted {total_deleted} files.")

    def log(self, message):
        self.log_output.append(message)

    def send_notification(self, message):
        try:
            notification.notify(
                title='🧹 Vorcleaner',
                message=message,
                app_name='Vorcleaner',
                timeout=5
            )
        except Exception as e:
            print(f"Notification error: {e}")

    def toggle_windows_update(self):
        if not self.updates_disabled:
            command = (
                'sc stop wuauserv & sc config wuauserv start= disabled & '
                'sc stop bits & sc config bits start= disabled & '
                'sc stop dosvc & sc config dosvc start= disabled & '
                'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\WaaSMedicSvc" /v Start /t REG_DWORD /d 4 /f'
            )
            self.log("🔻 Disabling Windows Update...")
            self.disable_btn.setText("Enable Update")
        else:
            command = (
                'sc config wuauserv start= auto & sc start wuauserv & '
                'sc config bits start= delayed-auto & sc start bits & '
                'sc config dosvc start= delayed-auto & sc start dosvc & '
                'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\WaaSMedicSvc" /v Start /t REG_DWORD /d 3 /f'
            )
            self.log("✅ Enabling Windows Update...")
            self.disable_btn.setText("Disable Update")

        subprocess.call(f'cmd /c {command}', shell=True)
        self.updates_disabled = not self.updates_disabled

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: #f0f0f0;
                font-family: 'Segoe UI';
            }
            QPushButton {
                background-color: #2e2e3f;
                color: white;
                padding: 8px 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3c3c50;
            }
            QProgressBar {
                background: #2e2e3f;
                border: 1px solid #555;
                height: 20px;
                border-radius: 10px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #00e676;
                width: 10px;
                border-radius: 10px;
            }
            QTextEdit {
                background-color: #2a2a3d;
                color: #ccc;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 6px;
            }
        """)

    def apply_light_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                color: #212121;
                font-family: 'Segoe UI';
            }
            QPushButton {
                background-color: #e3e3e3;
                color: #212121;
                padding: 8px 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QProgressBar {
                background: #e0e0e0;
                border: 1px solid #bbb;
                height: 20px;
                border-radius: 10px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2196f3;
                width: 10px;
                border-radius: 10px;
            }
            QTextEdit {
                background-color: #ffffff;
                color: #212121;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 6px;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("vorcleaner.ico"))
    win = CacheCleanerApp()
    win.show()
    sys.exit(app.exec_())
