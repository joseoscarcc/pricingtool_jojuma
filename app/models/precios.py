from app.extensions import db

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