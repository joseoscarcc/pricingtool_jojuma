from flask import render_template, jsonify, flash
from app.graph import bp
from app.extensions import db
from app.models.auth import login_required
from app.models.precios import competencia, precios_site, sites, get_site_data
from sqlalchemy import cast, Integer
import pandas as pd
import plotly
import plotly.express as px
import json
import numpy as np
from datetime import datetime, timedelta


@bp.route('/')
@login_required
def index():
    title="Dasboard Precios"
    placeID = get_site_data()
    placeID_json = json.dumps(placeID)
    return render_template('graph/graph.html',title=title,placeids=placeID_json)

@bp.route('/data/', methods=['GET'])
@bp.route('/data/<int:place_id_value>/<string:product_value>', methods=['GET'])
@login_required
def data(place_id_value=None, product_value=None):
    # if cre_id_value is None:
    #     cre_id_value = 'PL/20038/EXP/ES/2017'
    if place_id_value is None:
         place_id_value = 22534
    if product_value is None:
        product_value = 'regular'
    
    site = sites.query.filter_by(place_id=place_id_value).first()
    if site:
        place_id_value = site.place_id
        # Use the place_id as needed
    else:
        # Handle the case when cre_id is not found
        flash('El "CRE ID" no fue encontrado')

    date_threshold = datetime.now() - timedelta(days=30)

    results = (
        precios_site.query.join(competencia, cast(precios_site.place_id, Integer) == competencia.place_id)
        .filter(competencia.compite_a == place_id_value)
        .filter(precios_site.product == product_value)
        .filter(precios_site.date >= date_threshold)
        .with_entities(
            precios_site.date,
            competencia.marca,
            precios_site.prices
        )
        .all()
    )

    data = {}
    for row in results:
        date = row.date.strftime('%Y-%m-%d')
        marca = row.marca
        price = row.prices

        # Create the nested dictionaries if they don't exist
        if date not in data:
            data[date] = {}

        if marca not in data[date]:
            data[date][marca] = price
        
    return jsonify({'data': data})