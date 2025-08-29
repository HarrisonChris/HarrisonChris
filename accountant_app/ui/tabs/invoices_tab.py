from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget


class InvoicesTab(QWidget):
	def __init__(self) -> None:
		super().__init__()
		layout = QVBoxLayout()

		self.table = QTableWidget(0, 6)
		self.table.setHorizontalHeaderLabels(["Invoice #", "Client", "Issue Date", "Due Date", "Total", "Status"])
		layout.addWidget(self.table)

		buttons = QHBoxLayout()
		self.generate_btn = QPushButton("Generate")
		self.print_btn = QPushButton("Print/PDF")
		self.email_btn = QPushButton("Send Email")
		buttons.addWidget(self.generate_btn)
		buttons.addWidget(self.print_btn)
		buttons.addWidget(self.email_btn)
		buttons.addStretch(1)
		layout.addLayout(buttons)

		self.setLayout(layout)