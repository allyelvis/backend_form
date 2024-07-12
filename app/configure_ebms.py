from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import EBMSConfiguration
from app.forms import EBMSConfigForm

configure_ebms_bp = Blueprint('configure_ebms', __name__)

@configure_ebms_bp.route('/configure-ebms', methods=['GET', 'POST'])
def configure_ebms():
    form = EBMSConfigForm()
    if form.validate_on_submit():
        ebms_config = EBMSConfiguration(
            api_url=form.api_url.data,
            stock_api_url=form.stock_api_url.data,
            bearer_token=form.bearer_token.data
        )
        db.session.add(ebms_config)
        db.session.commit()
        flash('EBMS configuration saved successfully!', 'success')
        return redirect(url_for('configure_ebms.configure_ebms'))

    return render_template('configure_ebms.html', form=form)
