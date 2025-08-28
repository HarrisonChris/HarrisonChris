import sys
from PySide6.QtWidgets import QApplication
from .ui.main_window import MainWindow
from .db.init_db import initialize_database


def main() -> None:
	app = QApplication(sys.argv)
	initialize_database()
	window = MainWindow()
	window.show()
	sys.exit(app.exec())