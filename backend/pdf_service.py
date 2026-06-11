from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer

from reportlab.lib.styles import getSampleStyleSheet

from backend.database import SessionLocal
from backend.models import User
from backend.transaction_models import  Transaction
from backend.bank_account_models import BankAccount

def generate_pdf_statement(email):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email
    ).first()



    active_account = db.query(
        BankAccount
    ).filter(
        BankAccount.user_email == email,
        BankAccount.is_active == True
    ).first()

    if not active_account:
        return None

    transactions = db.query(
        Transaction
    ).filter(
        (
                Transaction.sender_account_no ==
                active_account.account_no
        ) |
        (
                Transaction.receiver_account_no ==
                active_account.account_no
        )
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

    Paragraph(
        f"Account No: {active_account.account_no}",
        styles['BodyText']
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