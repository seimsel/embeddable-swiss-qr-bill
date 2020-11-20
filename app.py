from flask import Flask, request, send_file
from qrbill.bill import QRBill
from io import BytesIO, StringIO

app = Flask(__name__)

@app.route('/')
def main():
    try:
        payment_parts = QRBill(
            account=request.args.get('account'),
            amount=request.args.get('amount'),
            currency=request.args.get('currency'),
            due_date=request.args.get('due-date'),
            creditor={
                'name': request.args.get('creditor-name'),
                'line1': request.args.get('creditor-line1'),
                'line2': request.args.get('creditor-line2'),
                'street': request.args.get('creditor-street'),
                'house_num': request.args.get('creditor-house-num'),
                'pcode': request.args.get('creditor-pcode'),
                'city': request.args.get('creditor-city'),
                'country': request.args.get('creditor-country')
            },
            debtor={
                'name': request.args.get('debtor-name'),
                'line1': request.args.get('debtor-line1'),
                'line2': request.args.get('debtor-line2'),
                'street': request.args.get('debtor-street'),
                'house_num': request.args.get('debtor-house_num'),
                'pcode': request.args.get('debtor-pcode'),
                'city': request.args.get('debtor-city'),
                'country': request.args.get('debtor-country')
            },
            ref_number=request.args.get('ref-number'),
            extra_infos=request.args.get('extra-infos'),
            alt_procs=request.args.get('alt-procs', '').split(','),
            language=request.args.get('language'),
            top_line=request.args.get('top_line'),
            payment_line=request.args.get('payment_line')
        )

        response = StringIO()
        payment_parts.as_svg(response)

        return send_file(
            BytesIO(response.getvalue().encode('utf-8')),
            mimetype='image/svg+xml'
        )

    except ValueError as e:
        return str(e)
