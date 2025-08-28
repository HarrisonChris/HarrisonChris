from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget


class ProjectsTab(QWidget):
	def __init__(self) -> None:
		super().__init__()
		layout = QVBoxLayout()

		self.table = QTableWidget(0, 4)
		self.table.setHorizontalHeaderLabels(["Client", "Project Name", "Hourly Rate", "Active"])
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