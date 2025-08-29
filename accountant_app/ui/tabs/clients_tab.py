from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from sqlalchemy.orm import Session

from ...db import get_session
from ...models import Client
from ..dialogs.client_dialog import ClientDialog


class ClientsTab(QWidget):
	def __init__(self) -> None:
		super().__init__()
		layout = QVBoxLayout()

		self.table = QTableWidget(0, 4)
		self.table.setHorizontalHeaderLabels(["Name", "Email", "Phone", "Billing Rate"])
		layout.addWidget(self.table)

		buttons = QHBoxLayout()
		self.add_btn = QPushButton("Add")
		self.edit_btn = QPushButton("Edit")
		self.delete_btn = QPushButton("Delete")
		buttons.addWidget(self.add_btn)
		buttons.addWidget(self.edit_btn)
		buttons.addWidget(self.delete_btn)
		buttons.addStretch(1)
		layout.addLayout(buttons)

		self.setLayout(layout)

		self.add_btn.clicked.connect(self._on_add)
		self.edit_btn.clicked.connect(self._on_edit)
		self.delete_btn.clicked.connect(self._on_delete)

		self._reload()

	def _reload(self) -> None:
		self.table.setRowCount(0)
		with get_session() as session:
			clients = session.query(Client).order_by(Client.name.asc()).all()
		for c in clients:
			self._append_row(c)

	def _append_row(self, client: Client) -> None:
		row = self.table.rowCount()
		self.table.insertRow(row)
		self.table.setItem(row, 0, QTableWidgetItem(client.name))
		self.table.setItem(row, 1, QTableWidgetItem(client.email or ""))
		self.table.setItem(row, 2, QTableWidgetItem(client.phone or ""))
		self.table.setItem(row, 3, QTableWidgetItem(f"{client.default_hourly_rate:.2f}" if client.default_hourly_rate is not None else ""))
		self.table.setVerticalHeaderItem(row, QTableWidgetItem(client.id))

	def _selected_client_id(self) -> str | None:
		row = self.table.currentRow()
		if row < 0:
			return None
		hdr = self.table.verticalHeaderItem(row)
		return hdr.text() if hdr else None

	def _on_add(self) -> None:
		d = ClientDialog(self)
		if d.exec() == d.Accepted:
			values = d.get_values()
			if not values["name"]:
				QMessageBox.warning(self, "Missing Name", "Name is required")
				return
			with get_session() as session:
				client = Client(**values)
				session.add(client)
				session.commit()
				self._append_row(client)

	def _on_edit(self) -> None:
		client_id = self._selected_client_id()
		if not client_id:
			QMessageBox.information(self, "Select", "Select a client to edit")
			return
		with get_session() as session:
			client = session.get(Client, client_id)
			if not client:
				return
			d = ClientDialog(self, name=client.name, email=client.email or "", phone=client.phone or "", rate=str(client.default_hourly_rate or ""))
			if d.exec() == d.Accepted:
				values = d.get_values()
				if not values["name"]:
					QMessageBox.warning(self, "Missing Name", "Name is required")
					return
				client.name = values["name"]
				client.email = values["email"]
				client.phone = values["phone"]
				client.default_hourly_rate = values["default_hourly_rate"]
				session.commit()
				self._reload()

	def _on_delete(self) -> None:
		client_id = self._selected_client_id()
		if not client_id:
			QMessageBox.information(self, "Select", "Select a client to delete")
			return
		with get_session() as session:
			client = session.get(Client, client_id)
			if not client:
				return
			session.delete(client)
			session.commit()
			self._reload()