from io import BytesIO
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

MONTH_NAMES = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
]


def format_quotation_date(value):
    quotation_date = value.date() if hasattr(value, "date") else value
    return f"{quotation_date.day} {MONTH_NAMES[quotation_date.month - 1]} {quotation_date.year}"


def quotation_pdf(quotation, totals):
    output = BytesIO()
    pdf = canvas.Canvas(output, pagesize=A4)
    width, height = A4
    letterhead_path = Path(__file__).resolve().parent.parent / "static" / "images" / "Alanka-KOP.png"
    if letterhead_path.exists():
        # The supplied PNG is a complete A4 stationery template, including footer artwork.
        pdf.drawImage(ImageReader(str(letterhead_path)), 0, 0, width=width, height=height, preserveAspectRatio=False, mask="auto")
    y = height - 205
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(width / 2, y, "PENAWARAN CCTV / IT")
    y -= 30
    pdf.setFont("Helvetica", 10)
    pdf.drawString(45, y, f"Kepada: {quotation.customer.name}")
    pdf.drawRightString(width - 45, y, f"No: {quotation.number}")
    y -= 16
    pdf.drawString(45, y, f"Alamat: {quotation.customer.address or '-'}")
    pdf.drawRightString(width - 45, y, "Perihal: Penawaran")
    y -= 30
    left, right = 45, width - 45
    table_width = right - left
    columns = [left, left + 30, left + 245, left + 285, left + 335, left + 425, right]
    row_height = 20
    pdf.setFillColorRGB(0.06, 0.24, 0.38)
    pdf.rect(left, y - row_height + 4, table_width, row_height, fill=1, stroke=0)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 10)
    for label, x in zip(["No", "Description", "Qty", "Satuan", "Price", "Total"], columns[:-1]):
        pdf.drawString(x + 5, y - 10, label)
    y -= row_height
    pdf.setFont("Helvetica", 10)
    pdf.setFillColorRGB(0, 0, 0)
    for index, item in enumerate(quotation.items, start=1):
        subtotal = item.quantity * item.selling_price - item.discount
        pdf.rect(left, y - row_height + 4, table_width, row_height, fill=0, stroke=1)
        for x in columns[1:-1]:
            pdf.line(x, y - row_height + 4, x, y + 4)
        pdf.drawCentredString((columns[0] + columns[1]) / 2, y - 10, str(index))
        pdf.drawString(columns[1] + 5, y - 10, item.product.name[:35])
        pdf.drawCentredString((columns[2] + columns[3]) / 2, y - 10, str(item.quantity))
        pdf.drawString(columns[3] + 5, y - 10, item.product.unit[:10])
        pdf.drawRightString(columns[5] - 5, y - 10, f"Rp {item.selling_price:,.0f}")
        pdf.drawRightString(columns[6] - 5, y - 10, f"Rp {subtotal:,.0f}")
        y -= row_height
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawRightString(columns[5] - 5, y - 10, "Total")
    pdf.drawRightString(right - 5, y - 10, f"Rp {totals['total']:,.0f}")
    y -= 48
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(65, y, "Syarat & Ketentuan:")
    y -= 18
    pdf.setFont("Helvetica", 9)
    terms = [
        "- Pembayaran dapat dilakukan 100% di awal sebelum proses pemasangan dilaksanakan,",
        "  atau 50% sebelum pemasangan dan dilunasi setelah pemasangan selesai.",
        "  Setelah melakukan pembayaran, harap mengirimkan bukti pembayaran kepada kami.",
        "",
        "Pembayaran bisa dilakukan melalui transfer ke nomor rekening berikut:",
        "Bank            : Krom Bank",
        "No. Rekening    : 770092935506",
        "Atas Nama       : Ni Putu Ayu Lesparini",
    ]
    for line in terms:
        pdf.drawString(75, y, line)
        y -= 14
    y -= 10
    pdf.drawRightString(right, y, f"Denpasar, {format_quotation_date(quotation.created_at)}")
    y -= 18
    pdf.drawRightString(right, y, "Hormat kami,")
    pdf.drawRightString(right, y - 45, "AlankaTech - Jasa Instalasi")
    pdf.save()
    output.seek(0)
    return output
