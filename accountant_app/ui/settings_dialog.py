import json
import os
from pathlib import Path
from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox

CONFIG_DIR = Path.home() / ".accountant_app"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config() -> dict:
	if CONFIG_FILE.exists():
		with open(CONFIG_FILE, "r", encoding="utf-8") as f:
			return json.load(f)
	return {}


def save_config(data: dict) -> None:
	CONFIG_DIR.mkdir(parents=True, exist_ok=True)
	with open(CONFIG_FILE, "w", encoding="utf-8") as f:
		json.dump(data, f, indent=2)


class SettingsDialog(QDialog):
	def __init__(self, parent=None) -> None:
		super().__init__(parent)
		self.setWindowTitle("Settings")

		self._config = load_config()

		layout = QVBoxLayout()
		form = QFormLayout()

		self.db_url = QLineEdit(self._config.get("db_url", ""))
		self.smtp_host = QLineEdit(self._config.get("smtp_host", ""))
		self.smtp_port = QLineEdit(str(self._config.get("smtp_port", "")))
		self.smtp_user = QLineEdit(self._config.get("smtp_user", ""))
		self.smtp_password = QLineEdit(self._config.get("smtp_password", ""))
		self.smtp_password.setEchoMode(QLineEdit.Password)

		form.addRow("DB URL", self.db_url)
		form.addRow("SMTP Host", self.smtp_host)
		form.addRow("SMTP Port", self.smtp_port)
		form.addRow("SMTP User", self.smtp_user)
		form.addRow("SMTP Password", self.smtp_password)

		layout.addLayout(form)

		buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)
		layout.addWidget(buttons)

		self.setLayout(layout)

	def accept(self) -> None:
		data = {
			"db_url": self.db_url.text().strip(),
			"smtp_host": self.smtp_host.text().strip(),
			"smtp_port": int(self.smtp_port.text()) if self.smtp_port.text().strip() else None,
			"smtp_user": self.smtp_user.text().strip(),
			"smtp_password": self.smtp_password.text(),
		}
		save_config(data)
		super().accept()