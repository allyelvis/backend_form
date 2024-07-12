from flask import Blueprint, render_template, request, make_response, redirect, url_for
from datetime import datetime
from pydantic import BaseModel
from typing import List
import requests

main = Blueprint('main', __name__)

# Dummy databases (for demonstration purposes)
companies_database = [
    {"name": "Company A", "address": "123 Main St", "nif": "123456789", "vat_subject": True},
    {"name": "Company B", "address": "456 Elm St", "nif": "987654321", "vat_subject": False}
]

products_database = [
    {"code": "P001", "description": "Product 1", "unit_price": 10.0},
    {"code": "P002", "description": "Product 2", "unit_price": 20.0}
]

stock_database = [
    {"company_name": "Company A", "product_code": "P001", "quantity": 100},
    {"company_name": "Company A", "product_code": "P002", "quantity": 50},
    {"company_name": "Company B", "product_code": "P001", "quantity": 75},
]

# Define Pydantic models
class Item(BaseModel):
    product_code: str
    description: str
    quantity: int
    unit_price: float
    total_price: float

class Facture(BaseModel):
    invoice_number: str
    date: datetime
    customer_name: str
    customer_address: str
    customer_nif: str
    items: List[Item]
    total_ht: float
    tax_rate: float
    total_ttc: float
    payment_method: str
    company_name: str
    company_address: str
    company_nif: str
    company_vat_subject: bool

class Product(BaseModel):
    product_code: str
    description: str
    unit_price: float

class Stock(BaseModel):
    company_name: str
    product_code: str
    quantity: int

# EBMS API configuration
EBMS_API_URL = "https://ebms.obr.gov.bi:9443/ebms_api/addInvoice"
EBMS_STOCK_API_URL = "https://ebms.obr.gov.bi:9443/ebms_api/updateStock"
EBMS_BEARER_TOKEN = "YOUR_EBMS_BEARER_TOKEN"

# Function to post facture data to EBMS
def post_to_ebms(facture: Facture):
    headers = {
        "Authorization": f"Bearer {EBMS_BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(EBMS_API_URL, headers=headers, json=facture.dict())
    return response.status_code, response.text

# Function to post stock data to EBMS
def post_stock_to_ebms(stock: Stock):
    headers = {
        "Authorization": f"Bearer {EBMS_BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(EBMS_STOCK_API_URL, headers=headers, json=stock.dict())
    return response.status_code, response.text

# Route for selecting or adding company information to facture
@main.route('/', methods=['GET', 'POST'])
def facture_form():
    if request.method == 'POST':
        # Extract data from form submission
        invoice_number = request.form['invoice_number']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        customer_name = request.form['customer_name']
        customer_address = request.form['customer_address']
        customer_nif = request.form['customer_nif']
        company_name = request.form['company_name']
        
        # Check if existing company selected or new company details provided
        existing_company = next((c for c in companies_database if c['name'] == company_name), None)
        if existing_company:
            company_address = existing_company['address']
            company_nif = existing_company['nif']
            company_vat_subject = existing_company['vat_subject']
        else:
            company_address = request.form['company_address']
            company_nif = request.form['company_nif']
            company_vat_subject = 'company_vat_subject' in request.form

        # Process items dynamically
        items = []
        num_items = int(request.form['num_items'])
        for i in range(1, num_items + 1):
            product_code = request.form[f'product_code_{i}']
            description = request.form[f'description_{i}']
            quantity = int(request.form[f'quantity_{i}'])
            unit_price = float(request.form[f'unit_price_{i}'])
            total_price = float(request.form[f'total_price_{i}'])
            items.append(Item(
                product_code=product_code,
                description=description,
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price
            ))

            # Update stock for the selected company and product
            stock_entry = next((s for s in stock_database if s['company_name'] == company_name and s['product_code'] == product_code), None)
            if stock_entry:
                stock_entry['quantity'] -= quantity
            else:
                # Handle if the stock entry does not exist (for demo purposes, assume it exists)
                pass

        total_ht = float(request.form['total_ht'])
        tax_rate = float(request.form['tax_rate'])
        total_ttc = total_ht * (1 + tax_rate / 100)  # Calculate total_ttc

        payment_method = request.form['payment_method']
        
        # Create Facture object
        facture = Facture(
            invoice_number=invoice_number,
            date=date,
            customer_name=customer_name,
            customer_address=customer_address,
            customer_nif=customer_nif,
            items=items,
            total_ht=total_ht,
            tax_rate=tax_rate,
            total_ttc=total_ttc,
            payment_method=payment_method,
            company_name=company_name,
            company_address=company_address,
            company_nif=company_nif,
            company_vat_subject=company_vat_subject
        )

        # Post facture to EBMS
        status_code, response_text = post_to_ebms(facture)

        # Post stock updates to EBMS
        for stock_entry in stock_database:
            stock = Stock(
                company_name=stock_entry['company_name'],
                product_code=stock_entry['product_code'],
                quantity=stock_entry['quantity']
            )
            post_stock_to_ebms(stock)

        # Handle response from EBMS
        if status_code == 200:
            # Prepare printable invoice
            invoice_html = render_template('invoice_template.html', facture=facture)
            response = make_response(invoice_html)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = f'attachment; filename=invoice_{invoice_number}.pdf'
            return response
        else:
            return f"Failed to Post Facture: {response_text}", status_code

    # Render the facture creation form with company selection/addition
    return render_template('facture_form.html', companies=companies_database)

# Route for adding/selecting products
@main.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_code = request.form['product_code']
        description = request.form['description']
        unit_price = float(request.form['unit_price'])

        product = {"code": product_code, "description": description, "unit_price": unit_price}
        products_database.append(product)

        return redirect(url_for('main.facture_form'))

    return render_template('add_product.html')

# Route for updating stock
@main.route('/update_stock', methods=['GET', 'POST'])
def update_stock():
    if request.method == 'POST':
        company_name = request.form['company_name']
        product_code = request.form['product_code']
        quantity = int(request.form['quantity'])

        # Update the stock in the dummy database (for demo purposes)
        stock_entry = next((s for s in stock_database if s['company_name'] == company_name and s['product_code'] == product_code), None)
        if stock_entry:
            stock_entry['quantity'] += quantity
