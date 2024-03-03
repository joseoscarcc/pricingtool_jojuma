from datetime import datetime, timedelta
from app.extensions import db
from sqlalchemy import desc, cast, Integer
from sqlalchemy.types import Numeric
from app.models.precios import precios_site, competencia, totalgas_prices

def data_for_graph(place_id_value, product_value):
    date_threshold = datetime.now() - timedelta(days=30)
    
    results = (
        totalgas_prices.query.join(competencia, totalgas_prices.place_id == competencia.place_id)
        .filter(competencia.compite_a == place_id_value)
        .filter(totalgas_prices.product == product_value)
        .filter(totalgas_prices.date >= date_threshold)
        .order_by(desc(totalgas_prices.date))  # Order by date in descending order
        .with_entities(
            totalgas_prices.date,
            competencia.marca,
            totalgas_prices.prices
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
