from datetime import datetime, timedelta
from app.extensions import db
from sqlalchemy import desc, cast, Integer
from sqlalchemy.types import Numeric
from app.models.precios import precios_site, competencia

def data_for_graph(place_id_value, product_value):
    date_threshold = datetime.now() - timedelta(days=30)
    
    results = (
        precios_site.query.join(competencia, cast(precios_site.place_id, Integer) == competencia.place_id)
        .filter(competencia.compite_a == place_id_value)
        .filter(precios_site.product == product_value)
        .filter(precios_site.date >= date_threshold)
        .order_by(desc(precios_site.date))  # Order by date in descending order
        .with_entities(
            precios_site.date,
            competencia.marca,
            precios_site.prices
        )
        .all()
    )
 
    brand_prices = {}
    
    for date, marca, price in results:
        if marca not in brand_prices:
            brand_prices[marca] = {'precio': [], 'fecha': []}
        
        brand_prices[marca]['precio'].append(price)
        brand_prices[marca]['fecha'].append(str(date))
    
    return brand_prices
