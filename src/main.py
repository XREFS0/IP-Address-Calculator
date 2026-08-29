import sys
from PySide6.QtWidgets import QApplication
from calculator.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("IP Address Calculator")
    app.setApplicationVersion("1.0.0")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
