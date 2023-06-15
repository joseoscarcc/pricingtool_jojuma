from flask import render_template
from app.precios import bp
from app.extensions import db
from sqlalchemy import func
import pandas as pd
import numpy as np
from app.models.precios import precios_site,competencia,round_float,get_site_data
from app.models.auth import login_required
import json

@bp.route('/')
@login_required
def index():
    placeID = get_site_data()
    latest_date = db.session.query(func.max(precios_site.date)).scalar()

    # Subquery to retrieve the data from competencia and precios_site tables
    subquery = db.session.query(
        competencia.id_micromercado,
        competencia.id_estacion,
        competencia.place_id,
        competencia.cre_id,
        competencia.marca,
        competencia.x,
        competencia.y,
        precios_site.prices,
        precios_site.product,
        competencia.compite_a
        ).join(precios_site, competencia.place_id == func.cast(precios_site.place_id, db.Integer)).\
    filter(precios_site.date == latest_date).subquery()

    # Main query to join the subquery with precios_site again and calculate the difference
    query = db.session.query(
        subquery.c.id_micromercado,
        subquery.c.id_estacion,
        subquery.c.place_id,
        subquery.c.cre_id,
        subquery.c.marca,
        subquery.c.x,
        subquery.c.y,
        subquery.c.prices,
        subquery.c.product,
        subquery.c.compite_a,
        (subquery.c.prices - precios_site.prices).label("dif")
    ).join(precios_site, subquery.c.compite_a == func.cast(precios_site.place_id, db.Integer)).\
    filter(precios_site.date == latest_date)

# Execute the query and fetch the results
    results = query.all()
    rows = []
    
    for result in results:
        row = {
            'id_micromercado': result.id_micromercado,
            'id_estacion': result.id_estacion,
            'place_id': result.place_id,
            'cre_id': result.cre_id,
            'marca': result.marca,
            'x': result.x,
            'y': result.y,
            'prices': result.prices,
            'product': result.product,
            'compite_a': result.compite_a,
            'dif': result.dif
        }
        rows.append(row)

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(rows)
    table01 = pd.pivot_table(df, values='prices', index=['id_micromercado', 'id_estacion','compite_a','cre_id','marca'],
                       columns=['product'], aggfunc=np.mean,fill_value='-')
    table02 = pd.pivot_table(df, values='dif', index=['id_micromercado', 'id_estacion','compite_a','cre_id','marca'],
                         columns=['product'], aggfunc=np.mean,fill_value='-')
    table01 = table01.reset_index()
    table01 =table01[['id_micromercado','id_estacion','cre_id','compite_a','marca','regular','premium','diesel']]
    table01['tipo'] = 'precios'
    table02 = table02.reset_index()
    table02 =table02[['id_micromercado','id_estacion','cre_id','compite_a','marca','regular','premium','diesel']]
    table02['tipo'] ='diferencia'
    newTable = pd.concat([table01,table02])
    newTable = newTable.sort_values(['id_micromercado', 'id_estacion'], ascending = [True, True])
    #newTable = newTable.round({'regular': 2, 'premium': 2, 'diesel': 2})
    newTable['regular']= newTable['regular'].apply(lambda x: round_float(x) if x != '-' else x)
    newTable['premium']= newTable['premium'].apply(lambda x: round_float(x) if x != '-' else x)
    newTable['diesel']= newTable['diesel'].apply(lambda x: round_float(x) if x != '-' else x)
    #newTable = newTable[newTable['compite_a'].isin(placeIDTG)]
    #table = newTable.drop(['id_micromercado', 'id_estacion','compite_a',], axis=1)
    newTable.columns = newTable.columns.rename(None)
    #return render_template('precios/index.html', tables=[table.to_html(index = False)],placeids=cre_id_marca_list)
    data_array = newTable.loc[newTable['tipo'] == 'precios'].to_dict('records')
    # Convert the list of dictionaries to JSON format
    data_json = json.dumps(data_array)
    placeID_json = json.dumps(placeID)
    return render_template('precios/index.html', data_json=data_json, placeids=placeID_json)
    
@bp.route('/categories/')
def categories():
    return render_template('precios/categories.html')