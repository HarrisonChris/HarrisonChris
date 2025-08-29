from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session

from ..models import Client, Project, TimeEntry, Invoice, InvoiceItem, InvoiceStatus


def generate_invoice_from_unbilled(session: Session, client_id: str, issue_date: date, due_date: date) -> Invoice:
	client = session.get(Client, client_id)
	if client is None:
		raise ValueError("Client not found")

	# Gather unbilled time entries for client's projects
	entries = (
		session.query(TimeEntry)
		.join(Project)
		.filter(Project.client_id == client_id, TimeEntry.is_billed == False)  # noqa: E712
		.all()
	)

	if not entries:
		raise ValueError("No unbilled time entries for this client")

	invoice = Invoice(
		client_id=client_id,
		invoice_number=_next_invoice_number(session),
		issue_date=issue_date,
		due_date=due_date,
		status=InvoiceStatus.DRAFT,
	)
	session.add(invoice)
	total = Decimal("0.00")
	for e in entries:
		amount = Decimal(str(e.hours)) * Decimal(str(e.rate))
		total += amount
		item = InvoiceItem(
			invoice=invoice,
			description=e.notes or f"Time entry {e.entry_date}",
			hours=e.hours,
			rate=e.rate,
			amount=float(amount),
		)
		session.add(item)
		# Mark as billed
		e.is_billed = True

	invoice.total_amount = float(total)
	session.commit()
	return invoice


def _next_invoice_number(session: Session) -> str:
	# Simple sequential counter based on count; in production, use sequences
	count = session.query(Invoice).count()
	return f"INV-{count + 1:05d}"


def export_invoice_pdf(invoice: Invoice, output_path: str) -> None:
	from reportlab.lib.pagesizes import LETTER
	from reportlab.pdfgen import canvas

	c = canvas.Canvas(output_path, pagesize=LETTER)
	width, height = LETTER
	cursor_y = height - 72

	c.setFont("Helvetica-Bold", 16)
	c.drawString(72, cursor_y, "Invoice")
	cursor_y -= 24

	c.setFont("Helvetica", 10)
	c.drawString(72, cursor_y, f"Invoice #: {invoice.invoice_number}")
	cursor_y -= 14
	c.drawString(72, cursor_y, f"Issue Date: {invoice.issue_date}")
	cursor_y -= 14
	c.drawString(72, cursor_y, f"Due Date: {invoice.due_date}")
	cursor_y -= 24

	c.setFont("Helvetica-Bold", 12)
	c.drawString(72, cursor_y, "Items")
	cursor_y -= 18
	c.setFont("Helvetica", 10)

	for item in invoice.items:
		c.drawString(72, cursor_y, item.description)
		c.drawRightString(width - 72, cursor_y, f"{item.hours:.2f} h x {item.rate:.2f} = {item.amount:.2f}")
		cursor_y -= 14
		if cursor_y < 72:
			c.showPage()
			cursor_y = height - 72

	cursor_y -= 10
	c.setFont("Helvetica-Bold", 12)
	c.drawRightString(width - 72, cursor_y, f"Total: {invoice.total_amount:.2f}")

	c.showPage()
	c.save()