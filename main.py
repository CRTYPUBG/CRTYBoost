import sys
import os
import threading
import urllib.request
import shutil

from flask import Flask
from flask_cors import CORS

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

# Flask app
app = Flask(__name__, static_folder='static')
CORS(app)

DOWNLOAD_FOLDER = r"C:\crtytooldownload"

BOOST_URL = "https://raw.githubusercontent.com/CRTYPUBG/mylicensesystem/refs/heads/main/boost_script.ps1"
RESET_URL = "https://raw.githubusercontent.com/CRTYPUBG/12_ahk-_99_teeen_anti/refs/heads/main/reset_script.ps1"

def download_script(url, filename):
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    urllib.request.urlretrieve(url, file_path)
    return file_path

@app.route('/')
def index():
    # Ana sayfaya static/ui.html dosyasını servis et
    return app.send_static_file('ui.html')

@app.route('/boost')
def boost():
    script_path = download_script(BOOST_URL, "boost_script.ps1")
    os.system(f'powershell -ExecutionPolicy Bypass -File "{script_path}"')
    return "✔ FPS BOOST uygulandı!"

@app.route('/reset')
def reset():
    script_path = download_script(RESET_URL, "reset_script.ps1")
    os.system(f'powershell -ExecutionPolicy Bypass -File "{script_path}"')
    return "✔ Ayarlar geri alındı!"

def clean_download_folder():
    if os.path.exists(DOWNLOAD_FOLDER):
        shutil.rmtree(DOWNLOAD_FOLDER)

def run_flask():
    app.run(port=5000)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRTY FPS BOOST TOOL")
        self.resize(900, 600)
        self.browser = QWebEngineView()
        self.browser.load(QUrl("http://127.0.0.1:5000/"))
        self.setCentralWidget(self.browser)

    def closeEvent(self, event):
        # Uygulama kapanınca geçici dosyaları temizle
        clean_download_folder()
        event.accept()

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    app_qt = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app_qt.exec_())
