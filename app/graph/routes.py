from flask import render_template, jsonify, request
import json
from app.graph import bp
from app.models.auth import login_required
from app.models.graph import data_for_graph
from app.models.precios import get_site_data, get_place_id_by_cre_id


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index(cre_id=None, product_value=None):
    title="Grafica de precios"

    if request.method == 'POST':
        cre_id = request.form.get('cre_id')
        product_value = request.form.get('product')
        site_data = get_site_data()
        place_id_value = next((site['place_id'] for site in site_data if site['cre_id'] == cre_id), None)
    if cre_id is None:
        place_id_value = 22534
    if product_value is None:
        product_value = "regular"
    
    brand_prices = data_for_graph(place_id_value, product_value)
  
    return render_template('graph/graph.html',title=title,
                            brand_prices = json.dumps(brand_prices))

@bp.route('/data/', methods=['GET'])
def data():
    site_data = get_site_data()

    totalgas_cre_ids = [site['cre_id'] for site in site_data if site['marca'] == 'TOTALGAS']

    return jsonify({'cre_id': totalgas_cre_ids})
