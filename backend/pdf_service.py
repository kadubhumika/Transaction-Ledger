from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer

from reportlab.lib.styles import getSampleStyleSheet

from backend.database import SessionLocal
from backend.models import User
from backend.transaction_models import  Transaction

def generate_pdf_statement(email):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email
    ).first()

    transactions = db.query(Transaction).filter(
        (Transaction.sender_email == email) |
        (Transaction.receiver_email == email)
    ).all()

    filename = f"{email}_statement.pdf"

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph("Transaction Ledger Transactions  Statement", styles['Title'])
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(f"Name: {user.name}", styles['BodyText'])
    )

    elements.append(
        Paragraph(f"Email: {user.email}", styles['BodyText'])
    )

    elements.append(
        Paragraph(
            f"Account No: {user.account_no}",
            styles['BodyText']
        )
    )

    elements.append(Spacer(1, 20))

    for txn in transactions:

        text = f"""
        Amount: ₹{txn.amount}<br/>
        From: {txn.sender_email}<br/>
        To: {txn.receiver_email}<br/>
        Category: {txn.category}<br/>
        Note: {txn.note}<br/>
        Status: {txn.status}<br/>
        Date: {txn.created_at}
        """

        elements.append(
            Paragraph(text, styles['BodyText'])
        )

        elements.append(Spacer(1, 15))

    pdf.build(elements)

    return filename