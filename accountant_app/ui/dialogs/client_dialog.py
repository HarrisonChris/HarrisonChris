from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox
from PySide6.QtCore import Qt


class ClientDialog(QDialog):
	def __init__(self, parent=None, *, name: str = "", email: str = "", phone: str = "", rate: str = "") -> None:
		super().__init__(parent)
		self.setWindowTitle("Client")

		layout = QVBoxLayout()
		form = QFormLayout()

		self.name_edit = QLineEdit(name)
		self.email_edit = QLineEdit(email)
		self.phone_edit = QLineEdit(phone)
		self.rate_edit = QLineEdit(rate)

		form.addRow("Name", self.name_edit)
		form.addRow("Email", self.email_edit)
		form.addRow("Phone", self.phone_edit)
		form.addRow("Billing Rate", self.rate_edit)
		layout.addLayout(form)

		buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)
		layout.addWidget(buttons)

		self.setLayout(layout)

	def get_values(self) -> dict:
		name = self.name_edit.text().strip()
		email = self.email_edit.text().strip() or None
		phone = self.phone_edit.text().strip() or None
		try:
			rate = float(self.rate_edit.text().strip()) if self.rate_edit.text().strip() else None
		except ValueError:
			rate = None
		return {
			"name": name,
			"email": email,
			"phone": phone,
			"default_hourly_rate": rate,
		}