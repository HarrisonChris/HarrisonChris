from PySide6.QtWidgets import QMainWindow, QWidget, QTabWidget, QToolBar, QMessageBox
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt

from .tabs.clients_tab import ClientsTab
from .tabs.projects_tab import ProjectsTab
from .tabs.time_entries_tab import TimeEntriesTab
from .tabs.invoices_tab import InvoicesTab
from .settings_dialog import SettingsDialog


class MainWindow(QMainWindow):
	def __init__(self) -> None:
		super().__init__()
		self.setWindowTitle("Accountant Time & Invoicing")
		self.resize(1100, 700)

		self._tab_widget = QTabWidget()
		self._tab_widget.addTab(ClientsTab(), "Clients")
		self._tab_widget.addTab(ProjectsTab(), "Projects")
		self._tab_widget.addTab(TimeEntriesTab(), "Time Entries")
		self._tab_widget.addTab(InvoicesTab(), "Invoices")
		self.setCentralWidget(self._tab_widget)

		self._toolbar = QToolBar()
		self._toolbar.setMovable(False)
		self.addToolBar(Qt.TopToolBarArea, self._toolbar)

		self._settings_action = QAction(QIcon(), "Settings", self)
		self._settings_action.triggered.connect(self._open_settings)
		self._toolbar.addAction(self._settings_action)

	def _open_settings(self) -> None:
		dialog = SettingsDialog(self)
		if dialog.exec() == dialog.Accepted:
			QMessageBox.information(self, "Settings Saved", "Settings have been saved. Restart app to apply DB changes.")