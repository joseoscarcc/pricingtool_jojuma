from flask import render_template, jsonify,request
from app.maps import bp
from app.extensions import db
from config import Config
from sqlalchemy import func, cast, Integer
from app.models.precios import precios_site,competencia,get_unique_municipios,get_site_data_by_municipio
from app.models.auth import login_required


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index(municipio_value=None, product_value=None):
    title="Mapa Precios"

    if request.method == 'POST':
        municipio_value = request.form.get('municipio')
        product_value = request.form.get('product')

    if municipio_value is None:
         municipio_value = 'Juarez'
    if product_value is None:
        product_value = 'regular'
    
    if municipio_value == 'Juarez':
        citylat = 31.71947
        citylon = -106.4514
    elif municipio_value == "Aguascalientes":
        citylat = 21.91797
        citylon = -102.2973
    elif municipio_value == "Delicias":
        citylat = 28.184184
        citylon = -105.463511
    elif municipio_value == "Parral":
        citylat = 26.933387
        citylon = -105.669176
    elif municipio_value == "Ahumada":
        citylat = 30.574909
        citylon = -106.510286
    else:
        citylat = 31.71947
        citylon = -106.4514

    place_ids = get_site_data_by_municipio(municipio_value)

    latest_date = (
        db.session.query(func.max(precios_site.date))
        .scalar()
    )

    results = (
        precios_site.query.join(competencia, cast(precios_site.place_id, Integer) == competencia.place_id)
        .filter(competencia.compite_a.in_(place_ids))
        .filter(precios_site.product == product_value)
        .filter(precios_site.date == latest_date)
        .with_entities(
            competencia.cre_id,
            competencia.marca,
            precios_site.prices,
            competencia.x,
            competencia.y
        )
        .all()
    )

    rows = []
    
    for result in results:
        row = {
            'marca': result.marca,
            'cre_id': result.cre_id,
            'precio': result.prices,
            'x': result.x,
            'y': result.y,
        }
        row['text'] = '" '+row['marca'] + ' ' + row['cre_id'] + ', Precio: ' + str(row['precio'])+' "'
        rows.append(row)

    x_values = [row['x'] for row in rows]
    y_values = [row['y'] for row in rows]
    text_values = [row['text'] for row in rows]
    map_box = Config.mapbox_access_token
    return render_template('maps/mapa.html',title=title,
                           x = x_values,
                           y = y_values,
                           texto = text_values,
                           citylat=citylat,
                           citylon=citylon,
                           map_box = map_box)

@bp.route('/municipios/', methods=['GET'])
def get_municipios():
    municipios = get_unique_municipios()
    return jsonify({'municipios': municipios})

@bp.route('/data/', methods=['GET'])
@bp.route('/data/<int:municipio_value>/<string:product_value>', methods=['GET'])
@login_required
def data(municipio_value=None, product_value=None):

    if municipio_value is None:
         municipio_value = 'Juarez'
    if product_value is None:
        product_value = 'regular'

    place_ids = get_site_data_by_municipio(municipio_value)

    latest_date = (
        db.session.query(func.max(precios_site.date))
        .scalar()
    )

    results = (
        precios_site.query.join(competencia, cast(precios_site.place_id, Integer) == competencia.place_id)
        .filter(competencia.compite_a.in_(place_ids))
        .filter(precios_site.product == product_value)
        .filter(precios_site.date == latest_date)
        .with_entities(
            competencia.cre_id,
            competencia.marca,
            precios_site.prices,
            competencia.x,
            competencia.y
        )
        .all()
    )

    rows = []
    
    for result in results:
        row = {
            'marca': result.marca,
            'cre_id': result.cre_id,
            'precio': result.prices,
            'x': result.x,
            'y': result.y,
        }
        row['text'] = row['marca'] + ' ' + row['cre_id'] + ', Precio: ' + str(row['precio'])
        rows.append(row)

    return jsonify({'data': rows })


