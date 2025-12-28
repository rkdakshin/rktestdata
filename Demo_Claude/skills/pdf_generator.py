"""
PDF Generator Skill

Reusable utility for generating invoice PDFs.
Can be used independently or integrated into other services.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO


def generate_simple_pdf(invoice_data: dict) -> bytes:
    """
    Generate a simple PDF invoice

    Args:
        invoice_data: Dictionary containing invoice information

    Returns:
        PDF data as bytes
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []

    # Create table with invoice data
    data = [
        ['Invoice Number', invoice_data.get('invoice_number', 'N/A')],
        ['Client', invoice_data.get('client_name', 'N/A')],
        ['Total', f"${invoice_data.get('total', 0):.2f}"]
    ]

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    doc.build(elements)

    return buffer.getvalue()
