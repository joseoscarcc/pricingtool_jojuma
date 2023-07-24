from flask import render_template
from app.precios import bp
from app.models.auth import login_required
from app.models.precios import get_data_table

@bp.route('/')
@login_required
def index():
    
    latest = get_data_table()
    return render_template('precios/index.html', latest=latest)

@bp.route('cambios/')
@login_required
def cambioprecio():
    return 
