from flask import render_template, request
from app.precios import bp
from app.models.auth import login_required
from app.models.precios import get_data_table, get_competencia_by_place_id
import json

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index(target_cre_id=None):
    title="Tabla Precios"
    if request.method == 'POST':
        target_cre_id = request.form.get('target_cre_id')
    
    print(target_cre_id)
    latest = get_data_table(target_cre_id)
    #test = get_competencia_by_place_id('640')
    #print(test)
    return render_template('precios/index.html', title=title,latest=latest)

@bp.route('cambios/')
@login_required
def cambioprecio():
    return "en Construccion"
