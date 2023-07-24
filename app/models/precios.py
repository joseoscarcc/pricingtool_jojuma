from app.extensions import db
from sqlalchemy import and_, case, func

class precios_site(db.Model):
    place_id = db.Column(db.Text, primary_key=True)
    prices = db.Column(db.Float(8))
    product = db.Column(db.Text)
    date = db.Column(db.Date)

class competencia(db.Model):
    id_micromercado = db.Column(db.Integer, primary_key=True)
    id_estacion = db.Column(db.Integer)
    place_id = db.Column(db.Integer)
    cre_id = db.Column(db.Text)
    marca = db.Column(db.Text)
    distancia = db.Column(db.Float)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    compite_a = db.Column(db.Integer)

class sites(db.Model):
    place_id = db.Column(db.Integer, primary_key=True)
    cre_id = db.Column(db.Text)
    nombre = db.Column(db.Text)
    rfc = db.Column(db.Text)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    municipio = db.Column(db.Text)
    estado = db.Column(db.Text)
    terminal = db.Column(db.Text)
    marca = db.Column(db.Text)
    address = db.Column(db.Text)
    geolocation = db.Column(db.Text)
    codigo_postal = db.Column(db.Text)
    es_norte = db.Column(db.Text)

def round_float(value):
    if isinstance(value, float):
        return round(value, 2)
    else:
        return value

def get_site_data():
    result = sites.query.with_entities(
        sites.place_id,
        sites.cre_id,
        sites.marca,
        sites.municipio
    ).all()

    site_list = []
    for row in result:
        place_id = row.place_id
        cre_id = row.cre_id
        marca = row.marca
        municipio = row.municipio

        site_data = {
            'place_id': place_id,
            'cre_id': cre_id,
            'marca': marca,
            'municipio': municipio
        }

        site_list.append(site_data)

    return site_list

def get_unique_municipios():
    result = sites.query.with_entities(sites.municipio).distinct().all()
    municipios = [row[0] for row in result]
    return municipios

def get_site_data_by_municipio(municipio):
    result = sites.query.with_entities(sites.place_id).filter_by(municipio=municipio).all()
    place_ids = [row[0] for row in result]
    return place_ids
    
def get_place_id_by_cre_id(target_cre_id):
    site = sites.query.filter_by(cre_id=target_cre_id).first()

    return site.place_id

def get_data_table(target_cre_id):
    latest_date = db.session.query(func.max(precios_site.date)).scalar()
    hoy = get_competencia_by_place_id(target_cre_id, latest_date)
    dia_anterior = db.session.query(func.max(precios_site.date) - 1).scalar()
    ayer = get_competencia_by_place_id(target_cre_id, dia_anterior)
    regular_prices = 1
    premium_prices = 1
    diesel_prices = 1
    row_i = 0
    row_k = 0
    row_j = 0

    table = "<table id=\"table\" class=\"table table-striped table-sm table-responsive\" >"
    table += "<thead class=\"thead-dark\">"
    table += "<tr><th>Permiso CRE</th><th>Marca</th><th>Regular</th><th>-d</th><th>Premium</th><th>-d</th><th>Diesel</th><th>-d</th><th>Cambio</th></tr></thead>"
    table += "<tbody>"
    for data in hoy:
            if data.id_estacion == 1:
                
                cre_id = data.cre_id
                marca = data.marca
                regular_prices = data.regular_prices
                premium_prices = data.premium_prices
                diesel_prices = data.diesel_prices

                desired_row = next((row for row in ayer if row.id_micromercado == data.id_micromercado and row.id_estacion == data.id_estacion and row.cre_id == data.cre_id and row.place_id == data.place_id), None)

                regular_prices_d_1 = desired_row.regular_prices
                premium_prices_d_1 = desired_row.premium_prices
                diesel_prices_d_1 = desired_row.diesel_prices

                try:
                    dif_d_r = round(float(regular_prices) - float(regular_prices_d_1),2)
                    if dif_d_r >0:
                        c = 'text-green'
                        b = '+'
                    elif dif_d_r <0:
                        c = 'text-red'
                        b = ''
                    else:
                        dif_d_r=''
                        c=''
                        b=''
                except:
                    dif_d_r = "-"
                try:
                    dif_d_p = round(float(premium_prices) - float(premium_prices_d_1),2)
                    if dif_d_p >0:
                        c = 'text-green'
                        b = '+'
                    elif dif_d_p <0:
                        c = 'text-red'
                        b = ''
                    else:
                        dif_d_p=""
                        c=''
                        b=''
                except:
                    dif_d_p = "-"
                try:
                    dif_d_d = round(float(diesel_prices) - float(diesel_prices_d_1),2)
                    if dif_d_d >0:
                        c = 'text-green'
                        b = '+'
                    elif dif_d_d <0:
                        c = 'text-red'
                        b = ''
                    else:
                        dif_d_d=""
                        c=''
                        b=''
                except:
                    dif_d_d = "-"

                table += f"<tr class=\"table-primary\"><td>{cre_id}</td><td>{marca}</td><td>{regular_prices}</td><td class=\"{c}\">{b}{dif_d_r}</td><td>{premium_prices}</td><td class=\"{c}\">{b}{dif_d_p}</td><td>{diesel_prices}</td><td class=\"{c}\">{b}{dif_d_d}</td>"
                table += f"<td><a href=\"{{ url_for('precios.cambioprecio', entry_id={data.place_id}) }}\" class=\"btn btn-outline-danger btn-sm\">Cambio</a></td></tr>"
            else:
                cre_id = data.cre_id
                marca = data.marca
                regular_prices_01 = data.regular_prices
                premium_prices_01 = data.premium_prices
                diesel_prices_01 = data.diesel_prices

                desired_row = next((row for row in ayer if row.id_micromercado == data.id_micromercado and row.id_estacion == data.id_estacion and row.cre_id == data.cre_id and row.place_id == data.place_id), None)

                regular_prices_d_1 = desired_row.regular_prices
                premium_prices_d_1 = desired_row.premium_prices
                diesel_prices_d_1 = desired_row.diesel_prices

                try:
                    dif_d_r = round(float(regular_prices_01) - float(regular_prices_d_1),2)
                    if dif_d_r >0:
                        c = 'text-green'
                        b = '+'
                    elif dif_d_r <0:
                        c = 'text-red'
                        b = ''
                    else:
                        dif_d_r=""
                        c=''
                        b=''
                except:
                    dif_d_r = "-"
                try:
                    dif_d_p = round(float(premium_prices_01) - float(premium_prices_d_1),2)
                    if dif_d_p >0:
                        c = 'text-green'
                        b = '+'
                    elif dif_d_p <0:
                        c = 'text-red'
                        b = ''
                    else:
                        dif_d_p=""
                        c=''
                        b=''
                except:
                    dif_d_p = "-"
                try:
                    dif_d_d = round(float(diesel_prices_01) - float(diesel_prices_d_1),2)
                    if dif_d_d >0:
                        c = 'text-green'
                        b = '+'
                    elif dif_d_d <0:
                        c = 'text-red'
                        b = ''
                    else:
                        dif_d_d=""
                        c=''
                        b=''
                except:
                    dif_d_d = "-"
            
                try:
                    dif_reg = round(float(regular_prices) - float(regular_prices_01),2)
                    if dif_reg > 0.30:
                        row_i = 1
                    elif dif_reg < -0.30:
                        row_i = 1
                    else:
                        row_i = 0
                except:
                    dif_reg = "-"
                    row_i = 0
                try:
                    dif_premium = round(float(premium_prices) - float(premium_prices_01),2)
                    if dif_premium > 0.30:
                        row_j = 1
                    elif dif_premium < -0.30:
                        row_j = 1
                    else:
                        row_j = 0
                except:
                    dif_premium = "-"
                    row_j = 0
                try:
                    dif_diesel = round(float(diesel_prices) - float(diesel_prices_01),0)
                    if dif_diesel > 0.30:
                        row_k = 1
                    elif dif_diesel < -0.30:
                        row_k = 1
                    else:
                        row_k = 0
                except:
                    dif_diesel = "-"
                    row_k = 0

                # Determine the color and emoticon based on the difference value
                row_n = row_i + row_k + row_j
                if row_n >= 2:
                    row_color = ""
                    emoticon = "❌"  # Negative emoticon
                elif 0 < row_n > 2:
                    row_color = ""
                    emoticon = "🧐"
                else:
                    row_color = ""
                    emoticon = "✅"  # Positive emoticon

                table += f"<tr class=\"table-secondary\"><td>{cre_id}</td><td>{marca}</td><td>{regular_prices_01}</td><td class=\"{c}\">{b}{dif_d_r}</td><td>{premium_prices_01}</td><td class=\"{c}\">{b}{dif_d_p}</td><td>{diesel_prices_01}</td><td class=\"{c}\">{b}{dif_d_d}</td><td></td></tr>"
                table += f"<tr class=\"{row_color}\"><td></td><td>Diferencia</td><td>{dif_reg}</td><td></td><td>{dif_premium}</td><td></td><td>{dif_diesel}</td><td></td><td>{emoticon}</td></tr>"
    table += "</tbody>"
    table += "</table>"

    return table

def get_place_id_by_cre_id_01(target_cre_id):
    site = competencia.query.filter(competencia.cre_id.like(f'PL/{target_cre_id}/%')).first()

    if site is None:
        return None

    return site.place_id

def get_competencia_by_place_id(target_cre_id, fecha):
    place_id = get_place_id_by_cre_id_01(target_cre_id)
    given_date = fecha

    
    result = db.session.query(
        competencia.id_micromercado,
        competencia.id_estacion,
        competencia.cre_id,
        competencia.place_id,
        competencia.marca,
        func.coalesce(
            func.max(case((precios_site.product == 'regular', func.cast(precios_site.prices, db.Text))), else_="-"),
            "-"
        ).label('regular_prices'),
        func.coalesce(
            func.max(case((precios_site.product == 'premium', func.cast(precios_site.prices, db.Text))), else_="-"),
            "-"
        ).label('premium_prices'),
        func.coalesce(
            func.max(case((precios_site.product == 'diesel', func.cast(precios_site.prices, db.Text))), else_="-"),
            "-"
        ).label('diesel_prices')
    ).outerjoin(
        precios_site,
        and_(
            func.cast(competencia.place_id, db.Text) == precios_site.place_id,
            precios_site.date == given_date
        )
    )

    # Check if place_id is not None and add the filter condition
    if place_id is not None:
        result = result.filter(competencia.compite_a == place_id)

    result = result.group_by(
        competencia.id_micromercado,
        competencia.id_estacion,
        competencia.cre_id,
        competencia.place_id,
        competencia.marca
    ).order_by(
        competencia.id_micromercado,
        competencia.id_estacion
    ).all()

    return result
