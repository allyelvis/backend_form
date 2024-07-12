import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    EBMS_API_URL = os.environ.get('EBMS_API_URL') or 'https://ebms.obr.gov.bi:9443/ebms_api/addInvoice'
    EBMS_STOCK_API_URL = os.environ.get('EBMS_STOCK_API_URL') or 'https://ebms.obr.gov.bi:9443/ebms_api/updateStock'
    EBMS_BEARER_TOKEN = os.environ.get('EBMS_BEARER_TOKEN') or 'YOUR_EBMS_BEARER_TOKEN'
