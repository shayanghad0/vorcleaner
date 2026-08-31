import os
import shutil
import getpass
import tempfile
import ctypes
import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QLabel, QProgressBar, QTextEdit, QHBoxLayout,
    QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QIcon, QLinearGradient, QColor, QPainter, QPainterPath


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

# ─── Color Palette ────────────────────────────────────────────────────────────
DARK = {
    "bg":          "#0b0b19",
    "surface":     "#12122a",
    "surface2":    "#1a1a35",
    "surface3":    "#222244",
    "border":      "#2a2a50",
    "accent":      "#00d4ff",
    "accent_dim":  "#0099bb",
    "accent_glow": "#00d4ff33",
    "danger":      "#ff4757",
    "danger_dim":  "#cc3040",
    "success":     "#00e676",
    "success_dim": "#00b85c",
    "warning":     "#ffc107",
    "text":        "#e8e8f0",
    "text_dim":    "#8888aa",
    "text_muted":  "#555577",
    "log_bg":      "#0a0a1a",
    "log_text":    "#7ec8e3",
}

LIGHT = {
    "bg":          "#f0f2f5",
    "surface":     "#ffffff",
    "surface2":    "#f7f8fa",
    "surface3":    "#ebedf0",
    "border":      "#d5d8de",
    "accent":      "#2563eb",
    "accent_dim":  "#1d4ed8",
    "accent_glow": "#2563eb22",
    "danger":      "#ef4444",
    "danger_dim":  "#dc2626",
    "success":     "#22c55e",
    "success_dim": "#16a34a",
    "warning":     "#f59e0b",
    "text":        "#1a1a2e",
    "text_dim":    "#64748b",
    "text_muted":  "#94a3b8",
    "log_bg":      "#f8f9fb",
    "log_text":    "#334155",
}


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
            "C:/ProgramData/Microsoft/Windows/Critical/Logs",
            f"C:/Users/{user}/AppData/Local/Discord/Cache",
            f"C:/Users/{user}/AppData/Local/Discord/Code Cache",
            f"C:/Users/{user}/AppData/Local/Slack/Cache",
            f"C:/Users/{user}/AppData/Local/Slack/Service Worker/CacheStorage",
            f"C:/Users/{user}/AppData/Local/WhatsApp/Cache",
            f"C:/Users/{user}/AppData/Local/Telegram Desktop/tdata/cache",
            f"C:/Users/{user}/AppData/Local/Steam/htmlcache",
            f"C:/Users/{user}/AppData/Local/Steam/httpcache",
            "C:/ProgramData/Package Cache",
            "C:/Windows/System32/LogFiles",
            "C:/Windows/System32/LogFiles/WMI",
            "C:/Windows/System32/LogFiles/Scm",
            "C:/Windows/System32/LogFiles/Setup",
            "C:/Windows/System32/LogFiles/SystemRestore",
            "C:/ProgramData/Microsoft/Search/Data/Applications/Windows/Projects",
            f"C:/Users/{user}/AppData/Local/Temp/Rar$EX*",
            f"C:/Users/{user}/AppData/Local/Temp/7z*",
            f"C:/Users/{user}/AppData/Local/Temp/WinRar*",
            "C:/Windows/System32/Config/TxR",
            "C:/ProgramData/Intel/Intel Extreme Tuning Utility/Logs",
            "C:/ProgramData/NVIDIA Corporation/Downloader",
            f"C:/Users/{user}/AppData/Local/Adobe/Lightroom/Caches",
            f"C:/Users/{user}/AppData/Local/Adobe/Photoshop/Caches",
            f"C:/Users/{user}/AppData/Local/Microsoft/Windows/Explorer/ThumbCache",
            f"C:/Users/{user}/AppData/Local/Microsoft/Windows/Explorer/IconCache",
            "C:/Windows/System32/spool/PRINTERS",
            "C:/Windows/System32/spool/TEMP",
            f"C:/Users/{user}/AppData/Local/Jagex/Cache",
            f"C:/Users/{user}/AppData/Local/Battle.net/Cache",
            f"C:/Users/{user}/AppData/Local/EpicGamesLauncher/Saved/webcache",
            f"C:/Users/{user}/AppData/Local/Origin/Cache",
            "C:/ProgramData/USOShared/Logs",
            "C:/ProgramData/Microsoft/Windows/DRM/Cache",
            "C:/Windows/System32/LogFiles/HTTPERR",
            "C:/Windows/System32/LogFiles/Sum",
            f"C:/Users/{user}/AppData/Local/Plex Media Server/Cache",
            f"C:/Users/{user}/AppData/Local/VLC/cache",
            "C:/Windows/Temp/Applog",
            "C:/Windows/Temp/DebugLogs",
            "C:/Windows/Temp/InstallLogs",
            "C:/Windows/Temp/Setup Logs",
            f"C:/Users/{user}/AppData/Local/Google/Chrome/User Data/Default/Code Cache",
            f"C:/Users/{user}/AppData/Local/Google/Chrome/User Data/Default/Service Worker/CacheStorage",
            f"C:/Users/{user}/AppData/Local/Microsoft/Edge/User Data/Default/Code Cache",
            f"C:/Users/{user}/AppData/Local/Mozilla/Firefox/Profiles/*/cache",
            f"C:/Users/{user}/AppData/Local/Mozilla/Firefox/Profiles/*/startupCache",
            f"C:/Users/{user}/AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/Cache",
            f"C:/Users/{user}/AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/Code Cache",
            f"C:/Users/{user}/AppData/Local/Vivaldi/User Data/Default/Cache",
            f"C:/Users/{user}/AppData/Local/Chromium/User Data/Default/Cache",
            "C:/Windows/System32/config/systemprofile/AppData/Local/Microsoft/Windows/INetCache",
            "C:/Windows/System32/config/systemprofile/AppData/Local/Temp",
            "C:/Windows/SysWOW64/config/systemprofile/AppData/Local/Temp",
            "C:/ProgramData/Adobe/Common/Media Cache",
            "C:/ProgramData/Adobe/Common/Media Cache Files",
            "C:/ProgramData/Adobe/SLStore",
            "C:/ProgramData/Microsoft/Windows/WER",
            "C:/ProgramData/Microsoft/Windows/WER/ReportArchive",
            "C:/ProgramData/Microsoft/Windows/WER/ReportQueue",
            "C:/ProgramData/Microsoft/Windows/LiveKernelReports",
            "C:/ProgramData/Microsoft/Search/Data/Temp",
            "C:/ProgramData/Microsoft/Search/Data/Applications/Windows/Temp",
            "C:/ProgramData/VMware/VMware USB Arbitration Service/logs",
            "C:/ProgramData/VMware/VMware Workstation/logs",
            "C:/ProgramData/VirtualBox/HostInterface/logs",
            "C:/ProgramData/Apple/Apple Software Update/logs",
            "C:/ProgramData/Apple/Installer Cache",
            "C:/ProgramData/Microsoft/Windows Defender/Scans/History/Cache",
            "C:/ProgramData/Microsoft/Windows Defender/Scans/History/Store",
            "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Startup/Temp",
            "C:/Windows/System32/LogFiles/Firewall",
            "C:/Windows/System32/LogFiles/SQM",
            "C:/Windows/System32/LogFiles/CloudFiles",
            "C:/Windows/System32/LogFiles/MSDTC",
            "C:/Windows/System32/LogFiles/FAX",
            "C:/Windows/System32/Config/WindowsUpdate",
            "C:/Windows/System32/Config/SoftwareDistribution",
            "C:/Windows/System32/Config/SystemProfile/AppData/Local/Temp",
            "C:/Windows/System32/DriverStore/Temp",
            "C:/Windows/System32/DirectX/D3DSCache",
            "C:/Windows/System32/DirectX/D3DSCache/Temp",
            f"C:/Users/{user}/AppData/Local/Microsoft/Windows/Explorer/Temp",
            f"C:/Users/{user}/AppData/Local/Microsoft/Windows/Caches",
            f"C:/Users/{user}/AppData/Local/Microsoft/Windows/Temporary Internet Files",
            f"C:/Users/{user}/AppData/Local/Microsoft/Windows/History",
            f"C:/Users/{user}/AppData/Local/Microsoft/Windows/PrintDialog",
            f"C:/Users/{user}/AppData/Local/Microsoft/Office/16.0/OfficeFileCache",
            f"C:/Users/{user}/AppData/Local/Microsoft/OneDrive/logs",
            f"C:/Users/{user}/AppData/Local/Microsoft/OneDrive/update",
            f"C:/Users/{user}/AppData/Local/Microsoft/Teams/Temp",
            f"C:/Users/{user}/AppData/Local/Microsoft/Teams/previous",
            f"C:/Users/{user}/AppData/Local/Discord/Cache/Cache_Data",
            f"C:/Users/{user}/AppData/Roaming/Code/Cache",
            f"C:/Users/{user}/AppData/Roaming/Code/CachedData",
            f"C:/Users/{user}/AppData/Roaming/Code/CachedExtensionVSIXs",
            f"C:/Users/{user}/AppData/Roaming/Slack/Cache",
            f"C:/Users/{user}/AppData/Roaming/Slack/Service Worker/CacheStorage",
            f"C:/Users/{user}/AppData/Roaming/Spotify/PersistentCache",
            f"C:/Users/{user}/AppData/Roaming/Spotify/Data",
            f"C:/Users/{user}/AppData/Roaming/Thunderbird/Profiles/*/cache",
            f"C:/Users/{user}/AppData/Roaming/zoom/data/Cache",
            f"C:/Users/{user}/AppData/Roaming/zoom/logs",
            f"C:/Users/{user}/AppData/Local/zoom/data/Cache",
            f"C:/Users/{user}/AppData/Local/zoom/logs",
            f"C:/Users/{user}/AppData/Local/Programs/zoom/data/Cache",
            "C:/inetpub/logs/LogFiles",
            "C:/inetpub/temp",
            "C:/PerfLogs",
            "C:/PerfLogs/System",
            "C:/PerfLogs/Diagnostics",
            "C:/Intel/Logs",
            "C:/AMD/Logs",
            "C:/NVIDIA/Logs",
            "C:/Drivers/Logs",
            "C:/Temp",
            "C:/tmp",
            "C:/Users/Public/Documents/temp",
            "C:/Users/Public/Downloads/temp",
            "C:/ProgramData/Temp",
            "C:/ProgramData/Tmp",
            "C:/ProgramData/Cache",
            "C:/Program Files/Common Files/Temp",
            "C:/Program Files (x86)/Common Files/Temp",
            "C:/MSOCache",
            "C:/Windows/Installation Media Cache",
            "C:/Windows/CSC",
            "C:/Windows/CSC/v2.0/temp",
            "C:/Windows/Offline Web Pages",
            "C:/Windows/Downloaded Program Files",
            "C:/Windows/ServiceProfiles/LocalService/AppData/Local/Temp/Temporary ASP.NET Files",
            "C:/Windows/ServiceProfiles/NetworkService/AppData/Local/Temp/Temporary ASP.NET Files",
            "C:/Windows/Microsoft.NET/Framework/v4.0.30319/Temporary ASP.NET Files",
            "C:/Windows/Microsoft.NET/Framework64/v4.0.30319/Temporary ASP.NET Files",
            "C:/Windows/System32/LogFiles/ClipSVC",
            "C:/Windows/System32/LogFiles/AppXSvc",
            "C:/ProgramData/Microsoft/Windows/AppRepository/Packages",
            "C:/ProgramData/Microsoft/Windows/AppRepository/Temp",
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


class GlassPanel(QFrame):
    """A semi-transparent card panel with rounded corners and subtle border."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("glassPanel")


class CacheCleanerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vorcleaner")
        self.setGeometry(100, 100, 540, 520)
        self.setMinimumSize(480, 480)
        self.setWindowIcon(QIcon("vorcleaner.ico"))
        self.updates_disabled = False
        self.current_theme = "dark"
        self.initUI()
        self.apply_dark_theme()

    def _make_shadow(self, widget, blur=24, offset_y=4, color="#000000"):
        shadow = QGraphicsDropShadowEffect(widget)
        shadow.setBlurRadius(blur)
        shadow.setOffset(0, offset_y)
        shadow.setColor(QColor(color))
        widget.setGraphicsEffect(shadow)

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 16)
        main_layout.setSpacing(0)

        # ── HEADER ────────────────────────────────────────────────────────────
        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(0)

        title_block = QVBoxLayout()
        title_block.setSpacing(2)

        self.title = QLabel("Vorcleaner")
        self.title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        self.title.setObjectName("appTitle")

        subtitle = QLabel("System Cache & Junk Cleaner")
        subtitle.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        subtitle.setFont(QFont("Segoe UI", 9))
        subtitle.setObjectName("appSubtitle")
        title_block.addWidget(self.title)
        title_block.addWidget(subtitle)

        header.addLayout(title_block)
        header.addStretch()

        self.dark_mode_btn = QPushButton("  DARK  ")
        self.dark_mode_btn.setObjectName("themeBtnDark")
        self.dark_mode_btn.setFixedHeight(30)
        self.dark_mode_btn.setCursor(Qt.PointingHandCursor)
        self.dark_mode_btn.clicked.connect(self.apply_dark_theme)

        self.light_mode_btn = QPushButton("  LIGHT  ")
        self.light_mode_btn.setObjectName("themeBtnLight")
        self.light_mode_btn.setFixedHeight(30)
        self.light_mode_btn.setCursor(Qt.PointingHandCursor)
        self.light_mode_btn.clicked.connect(self.apply_light_theme)

        self.close_btn = QPushButton("X")
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.clicked.connect(self.close)

        header.addWidget(self.dark_mode_btn)
        header.addSpacing(6)
        header.addWidget(self.light_mode_btn)
        header.addSpacing(10)
        header.addWidget(self.close_btn)

        main_layout.addLayout(header)
        main_layout.addSpacing(20)

        # ── STATUS CARD ───────────────────────────────────────────────────────
        self.status_card = GlassPanel()
        status_layout = QVBoxLayout(self.status_card)
        status_layout.setContentsMargins(20, 16, 20, 16)
        status_layout.setSpacing(6)

        self.status_icon = QLabel("●")
        self.status_icon.setObjectName("statusIcon")
        self.status_icon.setAlignment(Qt.AlignCenter)
        self.status_icon.setFont(QFont("Segoe UI", 18))

        self.status = QLabel("Ready to clean")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setFont(QFont("Segoe UI", 11))
        self.status.setObjectName("statusText")

        status_layout.addWidget(self.status_icon)
        status_layout.addWidget(self.status)

        self._make_shadow(self.status_card, blur=20, offset_y=4, color="#000000")
        main_layout.addWidget(self.status_card)
        main_layout.addSpacing(16)

        # ── ACTION BUTTONS ────────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self.clean_btn = QPushButton("  CLEAN NOW  ")
        self.clean_btn.setObjectName("cleanBtn")
        self.clean_btn.setFixedHeight(48)
        self.clean_btn.setCursor(Qt.PointingHandCursor)
        self.clean_btn.clicked.connect(self.handle_clean)

        self.disable_btn = QPushButton("  DISABLE UPDATE  ")
        self.disable_btn.setObjectName("updateBtn")
        self.disable_btn.setFixedHeight(48)
        self.disable_btn.setCursor(Qt.PointingHandCursor)
        self.disable_btn.clicked.connect(self.toggle_windows_update)

        btn_row.addWidget(self.clean_btn)
        btn_row.addWidget(self.disable_btn)

        main_layout.addLayout(btn_row)
        main_layout.addSpacing(16)

        # ── PROGRESS BAR ──────────────────────────────────────────────────────
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setTextVisible(True)
        self.progress.setFixedHeight(22)
        self.progress.setObjectName("mainProgress")
        main_layout.addWidget(self.progress)
        main_layout.addSpacing(14)

        # ── LOG PANEL ─────────────────────────────────────────────────────────
        log_header = QLabel("Activity Log")
        log_header.setObjectName("logHeader")
        log_header.setFont(QFont("Segoe UI", 9, QFont.Bold))
        main_layout.addWidget(log_header)
        main_layout.addSpacing(6)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setObjectName("logOutput")
        self.log_output.setFixedHeight(160)
        main_layout.addWidget(self.log_output)
        main_layout.addSpacing(12)

        # ── FOOTER ────────────────────────────────────────────────────────────
        footer = QLabel("Created by Shayan Ghadamian")
        footer.setAlignment(Qt.AlignCenter)
        footer.setFont(QFont("Segoe UI", 8))
        footer.setObjectName("footerText")
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

    # ── Actions ───────────────────────────────────────────────────────────────
    def handle_clean(self):
        self.status_icon.setText("◌")
        self.status_icon.setStyleSheet("color: #00d4ff;")
        self.status.setText("Scanning & cleaning system junk...")
        self.clean_btn.setEnabled(False)
        self.disable_btn.setEnabled(False)
        self.progress.setValue(0)
        self.log_output.clear()

        self.cleaner = CleanerThread()
        self.cleaner.progress.connect(self.progress.setValue)
        self.cleaner.done.connect(self.on_clean_done)
        self.cleaner.log_signal.connect(self.log)
        self.cleaner.start()

    def on_clean_done(self, total_deleted):
        c = DARK if self.current_theme == "dark" else LIGHT
        self.status_icon.setText("●")
        self.status_icon.setStyleSheet(f"color: {c['success']};")
        self.status.setText(f"Done — {total_deleted:,} files removed")
        self.clean_btn.setEnabled(True)
        self.disable_btn.setEnabled(True)
        self.send_notification(f"Cache cleaner completed.\nDeleted {total_deleted} files.")

    def log(self, message):
        self.log_output.append(message)

    def send_notification(self, message):
        try:
            notification.notify(
                title="Vorcleaner",
                message=message,
                app_name="Vorcleaner",
                timeout=5,
            )
        except Exception as e:
            print(f"Notification error: {e}")

    def toggle_windows_update(self):
        c = DARK if self.current_theme == "dark" else LIGHT
        if not self.updates_disabled:
            command = (
                'sc stop wuauserv & sc config wuauserv start= disabled & '
                'sc stop bits & sc config bits start= disabled & '
                'sc stop dosvc & sc config dosvc start= disabled & '
                'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\WaaSMedicSvc" /v Start /t REG_DWORD /d 4 /f'
            )
            self.log("Windows Update disabled")
            self.disable_btn.setText("  ENABLE UPDATE  ")
            self.disable_btn.setObjectName("updateBtnActive")
        else:
            command = (
                'sc config wuauserv start= auto & sc start wuauserv & '
                'sc config bits start= delayed-auto & sc start bits & '
                'sc config dosvc start= delayed-auto & sc start dosvc & '
                'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\WaaSMedicSvc" /v Start /t REG_DWORD /d 3 /f'
            )
            self.log("Windows Update enabled")
            self.disable_btn.setText("  DISABLE UPDATE  ")
            self.disable_btn.setObjectName("updateBtn")

        subprocess.call(f'cmd /c {command}', shell=True)
        self.updates_disabled = not self.updates_disabled
        self._refresh_styles()

    # ── Themes ────────────────────────────────────────────────────────────────
    def _refresh_styles(self):
        if self.current_theme == "dark":
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

    def apply_dark_theme(self):
        self.current_theme = "dark"
        c = DARK
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {c['bg']};
                color: {c['text']};
                font-family: 'Segoe UI';
            }}

            /* ── App Title ── */
            #appTitle {{
                color: {c['text']};
                font-size: 20px;
                font-weight: bold;
                padding: 0;
            }}
            #appSubtitle {{
                color: {c['text_dim']};
                font-size: 9px;
                padding: 0;
            }}

            /* ── Glass Panels ── */
            #glassPanel {{
                background-color: {c['surface']};
                border: 1px solid {c['border']};
                border-radius: 12px;
            }}

            /* ── Status ── */
            #statusIcon {{
                color: {c['accent']};
                font-size: 18px;
                background: transparent;
                border: none;
            }}
            #statusText {{
                color: {c['text']};
                font-size: 11px;
                background: transparent;
                border: none;
            }}

            /* ── Buttons ── */
            QPushButton {{
                border: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 11px;
                letter-spacing: 0.5px;
            }}

            /* Clean Now — primary CTA */
            #cleanBtn {{
                background-color: {c['accent']};
                color: #000000;
                font-size: 13px;
                font-weight: 700;
                border-radius: 10px;
                padding: 0 24px;
            }}
            #cleanBtn:hover {{
                background-color: #33ddff;
            }}
            #cleanBtn:pressed {{
                background-color: {c['accent_dim']};
            }}
            #cleanBtn:disabled {{
                background-color: {c['surface3']};
                color: {c['text_muted']};
            }}

            /* Update button — secondary */
            #updateBtn {{
                background-color: {c['surface2']};
                color: {c['text']};
                border: 1px solid {c['border']};
                font-size: 11px;
            }}
            #updateBtn:hover {{
                background-color: {c['surface3']};
                border-color: {c['text_muted']};
            }}
            #updateBtn:pressed {{
                background-color: {c['border']};
            }}

            /* Update button — active/disabled state */
            #updateBtnActive {{
                background-color: {c['danger']};
                color: #ffffff;
                border: 1px solid {c['danger']};
                font-size: 11px;
                border-radius: 8px;
            }}
            #updateBtnActive:hover {{
                background-color: #ff6b7a;
            }}
            #updateBtnActive:pressed {{
                background-color: {c['danger_dim']};
            }}

            /* Theme toggle buttons */
            #themeBtnDark {{
                background-color: {c['surface2']};
                color: {c['text']};
                border: 1px solid {c['border']};
                border-radius: 6px;
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 1px;
            }}
            #themeBtnDark:hover {{
                background-color: {c['surface3']};
            }}

            #themeBtnLight {{
                background-color: transparent;
                color: {c['text_dim']};
                border: 1px solid transparent;
                border-radius: 6px;
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 1px;
            }}
            #themeBtnLight:hover {{
                background-color: {c['surface2']};
                border-color: {c['border']};
                color: {c['text']};
            }}

            /* Close button */
            #closeBtn {{
                background-color: transparent;
                color: {c['text_dim']};
                border: none;
                font-size: 12px;
                font-weight: 700;
                border-radius: 6px;
            }}
            #closeBtn:hover {{
                background-color: {c['danger']};
                color: #ffffff;
            }}

            /* ── Progress Bar ── */
            #mainProgress {{
                background-color: {c['surface2']};
                border: 1px solid {c['border']};
                border-radius: 11px;
                text-align: center;
                color: {c['text']};
                font-size: 9px;
                font-weight: 600;
            }}
            #mainProgress::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {c['accent_dim']}, stop:1 {c['accent']});
                border-radius: 10px;
            }}

            /* ── Log Panel ── */
            #logHeader {{
                color: {c['text_dim']};
                background: transparent;
                border: none;
                font-size: 9px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }}
            #logOutput {{
                background-color: {c['log_bg']};
                color: {c['log_text']};
                border: 1px solid {c['border']};
                border-radius: 8px;
                padding: 8px;
                font-family: 'Cascadia Code', 'Consolas', monospace;
                font-size: 10px;
                selection-background-color: {c['accent']};
                selection-color: #000000;
            }}

            /* ── Footer ── */
            #footerText {{
                color: {c['text_muted']};
                font-size: 8px;
                background: transparent;
                border: none;
            }}
        """)
        self._apply_button_shadow()

    def apply_light_theme(self):
        self.current_theme = "light"
        c = LIGHT
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {c['bg']};
                color: {c['text']};
                font-family: 'Segoe UI';
            }}

            /* ── App Title ── */
            #appTitle {{
                color: {c['text']};
                font-size: 20px;
                font-weight: bold;
                padding: 0;
            }}
            #appSubtitle {{
                color: {c['text_dim']};
                font-size: 9px;
                padding: 0;
            }}

            /* ── Glass Panels ── */
            #glassPanel {{
                background-color: {c['surface']};
                border: 1px solid {c['border']};
                border-radius: 12px;
            }}

            /* ── Status ── */
            #statusIcon {{
                color: {c['accent']};
                font-size: 18px;
                background: transparent;
                border: none;
            }}
            #statusText {{
                color: {c['text']};
                font-size: 11px;
                background: transparent;
                border: none;
            }}

            /* ── Buttons ── */
            QPushButton {{
                border: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 11px;
                letter-spacing: 0.5px;
            }}

            /* Clean Now — primary CTA */
            #cleanBtn {{
                background-color: {c['accent']};
                color: #ffffff;
                font-size: 13px;
                font-weight: 700;
                border-radius: 10px;
                padding: 0 24px;
            }}
            #cleanBtn:hover {{
                background-color: #3b82f6;
            }}
            #cleanBtn:pressed {{
                background-color: {c['accent_dim']};
            }}
            #cleanBtn:disabled {{
                background-color: {c['surface3']};
                color: {c['text_muted']};
            }}

            /* Update button — secondary */
            #updateBtn {{
                background-color: {c['surface']};
                color: {c['text']};
                border: 1px solid {c['border']};
                font-size: 11px;
            }}
            #updateBtn:hover {{
                background-color: {c['surface3']};
                border-color: {c['text_muted']};
            }}
            #updateBtn:pressed {{
                background-color: {c['border']};
            }}

            /* Update button — active/disabled state */
            #updateBtnActive {{
                background-color: {c['danger']};
                color: #ffffff;
                border: 1px solid {c['danger']};
                font-size: 11px;
                border-radius: 8px;
            }}
            #updateBtnActive:hover {{
                background-color: #f87171;
            }}
            #updateBtnActive:pressed {{
                background-color: {c['danger_dim']};
            }}

            /* Theme toggle buttons */
            #themeBtnDark {{
                background-color: transparent;
                color: {c['text_dim']};
                border: 1px solid transparent;
                border-radius: 6px;
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 1px;
            }}
            #themeBtnDark:hover {{
                background-color: {c['surface3']};
                border-color: {c['border']};
                color: {c['text']};
            }}

            #themeBtnLight {{
                background-color: {c['surface']};
                color: {c['text']};
                border: 1px solid {c['border']};
                border-radius: 6px;
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 1px;
            }}
            #themeBtnLight:hover {{
                background-color: {c['surface3']};
            }}

            /* Close button */
            #closeBtn {{
                background-color: transparent;
                color: {c['text_dim']};
                border: none;
                font-size: 12px;
                font-weight: 700;
                border-radius: 6px;
            }}
            #closeBtn:hover {{
                background-color: {c['danger']};
                color: #ffffff;
            }}

            /* ── Progress Bar ── */
            #mainProgress {{
                background-color: {c['surface3']};
                border: 1px solid {c['border']};
                border-radius: 11px;
                text-align: center;
                color: {c['text']};
                font-size: 9px;
                font-weight: 600;
            }}
            #mainProgress::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {c['accent_dim']}, stop:1 {c['accent']});
                border-radius: 10px;
            }}

            /* ── Log Panel ── */
            #logHeader {{
                color: {c['text_dim']};
                background: transparent;
                border: none;
                font-size: 9px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }}
            #logOutput {{
                background-color: {c['log_bg']};
                color: {c['log_text']};
                border: 1px solid {c['border']};
                border-radius: 8px;
                padding: 8px;
                font-family: 'Cascadia Code', 'Consolas', monospace;
                font-size: 10px;
                selection-background-color: {c['accent']};
                selection-color: #ffffff;
            }}

            /* ── Footer ── */
            #footerText {{
                color: {c['text_muted']};
                font-size: 8px;
                background: transparent;
                border: none;
            }}
        """)
        self._apply_button_shadow()

    def _apply_button_shadow(self):
        self._make_shadow(self.clean_btn, blur=20, offset_y=3,
                          color="#00d4ff" if self.current_theme == "dark" else "#2563eb")
        self._make_shadow(self.status_card, blur=16, offset_y=4, color="#000000")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("vorcleaner.ico"))

    # Apply base font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    win = CacheCleanerApp()
    win.show()
    sys.exit(app.exec_())
