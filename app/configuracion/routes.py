from flask import render_template, jsonify, flash, request, redirect,url_for,get_flashed_messages
from app.configuracion import bp
from app.extensions import db
from app.models.auth import login_required, users
from app.models.precios import competencia, precios_site, sites, get_site_data
from app.models.configuracion import marcas_places

from sqlalchemy import cast, Integer, func
from sqlalchemy.exc import IntegrityError

import pandas as pd
import plotly
import plotly.express as px
import json
import numpy as np
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash

@bp.route('/')
@login_required
def index():
    title="Configurar APP"
  
    return render_template('configuracion/index.html',title=title)

@bp.route('/usuarios')
def usuarios():
    entries = users.query.filter_by(project='totalgas').all()
    return render_template('configuracion/showusers.html', entries=entries)

@bp.route('/register', methods=('GET', 'POST'))
@login_required
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        error = None

        if not username:
            error = 'Es necesario un usuario.'
        elif not password:
            error = 'Es necesario un password.'
        
        if error is None:
            try:
                new_user = users(username=username, password=generate_password_hash(password), email=email,type='user',project='totalgas')

                # Add the new user to the database
                db.session.add(new_user)
                db.session.commit()
            except IntegrityError:
                error = f"Usuario {username} ya esta registrado."
            else:
                flash('Nuevo usuario agregado con exito', "success")
                return redirect(url_for("configuracion.usuarios"))

        flash(error)
        return()

    return render_template('configuracion/nuevousuario.html')

@bp.route('/delete-user/<int:entry_id>')
@login_required
def delete(entry_id):
    entry = users.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Usuario eliminado", "success")
    return redirect(url_for("configuracion.usuarios"))

@bp.route('/sitios')
@login_required
def sitios():
    entries = sites.query.with_entities(sites.place_id,sites.cre_id, sites.nombre, sites.municipio, sites.estado, sites.marca).all()
    return render_template('configuracion/showsites.html', entries=entries)

@bp.route('/nuevositio', methods=('GET', 'POST'))
@login_required
def nuevositio():
    if request.method == 'POST':
        cre_id = request.form['cre_id']
        max_id = db.session.query(func.max(competencia.id_micromercado)).scalar()

        error = None

        if not cre_id:
            error = 'Es necesario un Permiso CRE ID valido.'
        
        if error is None:
            entries = marcas_places.query.with_entities(marcas_places.place_id,marcas_places.cre_id, marcas_places.municipio, marcas_places.estado, marcas_places.brand,marcas_places.x,marcas_places.y).filter_by(cre_id=cre_id).all()
            bandera = 2
            entry = {
                'id_micromercado':max_id,
                'place_id': entries[0][0],
                'cre_id': entries[0][1],
                'municipio': entries[0][2],
                'estado': entries[0][3],
                'brand': entries[0][4],
                'x':entries[0][5],
                'y':entries[0][6]
            }
            return render_template('configuracion/nuevosite.html', bandera=bandera,entry=entry)

        flash(error)
    bandera = 1
    return render_template('configuracion/nuevosite.html',bandera=bandera)

@bp.route('/guardarsitio', methods=('GET', 'POST'))
@login_required
def guardarsitio():
    id_micromercado = request.form['id_micromercado']
    place_id = request.form['place_id']
    cre_id = request.form['cre_id']
    nombre = request.form['nombre']
    marca = request.form['marca']
    municipio = request.form['municipio']
    estado = request.form['estado']
    x = request.form['x']
    y = request.form['y']
    error = None

    if not cre_id:
        error = 'Es necesario un Permiso CRE ID valido.'
    if error is None:
        try:
            new_sitio = sites(place_id=place_id, cre_id=cre_id, nombre=nombre, marca=marca,municipio=municipio,estado=estado,x=x,y=y)
            new_competencia = competencia(id_micromercado=id_micromercado,id_estacion=1,place_id=place_id, cre_id=cre_id,marca=marca,compite_a=place_id,x=x,y=y)
            # Add the new user to the database
            db.session.add(new_sitio)
            db.session.commit()
            db.session.add(new_competencia)
            db.session.commit()
        except IntegrityError:
            error = f"Estacion {cre_id} ya esta registrado."
        else:
            flash('Nueva estacion agregada con exito', "success")
            return redirect(url_for("configuracion.sitios"))
    flash(error)
    bandera = 1
    return render_template('configuracion/nuevosite.html',bandera=bandera)

@bp.route('/delete-sitios/<int:place_id>')
@login_required
def deletesitios(place_id):
    entry = sites.query.get_or_404(int(place_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Estacion eliminadas", "success")
    return redirect(url_for("configuracion.sitios"))

@bp.route('/competencia/<int:entry_id>')
@login_required
def vercompetencia(entry_id):
    entries = competencia.query.with_entities(competencia.place_id,competencia.cre_id, competencia.marca).filter_by(compite_a=entry_id).all()
    return render_template('configuracion/showtrade.html', entries=entries,place_id=entry_id)

@bp.route('/nuevacompetencia/<int:entry_id>', methods=('GET', 'POST'))
@login_required
def nuevacompetencia(entry_id):
    if request.method == 'POST':
        cre_id = request.form['cre_id']
        result = competencia.query.with_entities(competencia.id_micromercado, func.max(competencia.id_estacion)).filter_by(place_id=entry_id).group_by(competencia.id_micromercado).first()
        id_micromercado, id_estacion = result

        error = None

        if not cre_id:
            error = 'Es necesario un Permiso CRE ID valido.'
        
        if error is None:
            entries = marcas_places.query.with_entities(marcas_places.place_id,marcas_places.cre_id, marcas_places.brand,marcas_places.x,marcas_places.y).filter_by(cre_id=cre_id).all()
            bandera = 2
            entry = {
                'id_micromercado':id_micromercado,
                'id_estacion': id_estacion,
                'place_id': entries[0][0],
                'cre_id': entries[0][1],
                'marca': entries[0][2],
                'x':entries[0][3],
                'y':entries[0][4]
            }
            estacion_propia = sites.query.with_entities(sites.cre_id,sites.nombre).filter_by(place_id=entry_id).all()
            estacion= estacion_propia[0][0] + " " + estacion_propia[0][1]
            return render_template('configuracion/nuevacompetencia.html', bandera=bandera,entry=entry, place_id=entry_id,estacion=estacion)

        flash(error)
    
    estacion_propia = sites.query.with_entities(sites.cre_id,sites.nombre).filter_by(place_id=entry_id).all()
    estacion= estacion_propia[0][0] + " " + estacion_propia[0][1]
    print(estacion)
    bandera = 1
    return render_template('configuracion/nuevacompetencia.html',bandera=bandera,place_id=entry_id,estacion=estacion)

@bp.route('/guardarcompetencia/<int:entry_id>', methods=('GET', 'POST'))
@login_required
def guardarcompetencia(entry_id):
    id_micromercado = request.form['id_micromercado']
    place_id = request.form['place_id']
    cre_id = request.form['cre_id']
    marca = request.form['marca']
    compite_a = entry_id
    x = request.form['x']
    y = request.form['y']
    error = None

    if not cre_id:
        error = 'Es necesario un Permiso CRE ID valido.'
    if error is None:
        try:
            new_competencia = competencia(id_micromercado=id_micromercado,id_estacion=1,place_id=place_id, cre_id=cre_id,marca=marca,compite_a=entry_id,x=x,y=y)
            # Add the new user to the database
            db.session.add(new_competencia)
            db.session.commit()
        except IntegrityError:
            error = f"Estacion {cre_id} ya esta registrado."
        else:
            flash('Nueva competencia agregada con exito', "success")
            return redirect(url_for("configuracion.sitios"))
    flash(error)
    bandera = 1
    return render_template('configuracion/nuevacompetencia.html',place_id=entry_id)

@bp.route('/delete-competencia/<int:place_id>/<int:compite_a>')
@login_required
def deletecompetencia(place_id, compite_a):
    entries = competencia.query.filter(competencia.place_id == place_id, competencia.compite_a == compite_a).all()
    for entry in entries:
        db.session.delete(entry)
    db.session.commit()
    flash("Competencia eliminadas", "success")
    return redirect(url_for("configuracion.vercompetencia", entry_id = compite_a))