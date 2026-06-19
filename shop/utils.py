from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from django.conf import settings


def generate_order_pdf(order):
    """Generate PDF document for an order"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    title = Paragraph("Order Confirmation", title_style)
    story.append(title)
    story.append(Spacer(1, 0.2*inch))
    
    # Order Information
    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=TA_LEFT
    )
    
    story.append(Paragraph(f"<b>Order Number:</b> {order.order_number}", info_style))
    story.append(Paragraph(f"<b>Order Date:</b> {order.created_at.strftime('%B %d, %Y at %I:%M %p')}", info_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Order Items Table
    data = [['Product Number', 'Product Name', 'Quantity', 'Price', 'Subtotal']]
    
    for item in order.items.values():
        product_number = item.get('product_number', 'N/A')
        name = item.get('name', 'N/A')
        quantity = item.get('quantity', 0)
        price = float(item.get('price', 0))
        subtotal = quantity * price
        
        data.append([
            product_number,
            name,
            str(quantity),
            f"${price:.2f}",
            f"${subtotal:.2f}"
        ])
    
    # Total row
    data.append(['', '', '', 'Total:', f"${order.total_amount:.2f}"])
    
    # Create table
    table = Table(data, colWidths=[1.2*inch, 2.5*inch, 0.8*inch, 1*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -2), colors.black),
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -2), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.lightgrey]),
        ('ALIGN', (0, -1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ecf0f1')),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 0.5*inch))
    
    # Thank you message
    thank_you_style = ParagraphStyle(
        'ThankYouStyle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#27ae60'),
        spaceAfter=12,
        alignment=TA_CENTER
    )
    story.append(Paragraph("Thank you for your order!", thank_you_style))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

