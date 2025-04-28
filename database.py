import os
import pandas as pd
from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
import uuid

# Create engine using the DATABASE_URL environment variable
engine = create_engine(os.environ['DATABASE_URL'])

# Create declarative base
Base = declarative_base()

# Create Session class
Session = sessionmaker(bind=engine)

# Model classes
class Farm(Base):
    """Farm model representing 'datos_generales'"""
    __tablename__ = 'farms'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    city = Column(String)
    breed = Column(String)
    year = Column(Integer)
    month = Column(String)
    total_area = Column(Float)
    total_cows_area = Column(Float)
    production_per_cow = Column(Float)
    milking_cows = Column(Integer)
    industry_sales_percentage = Column(Integer)
    cheese_usage_percentage = Column(Integer)
    discard_percentage = Column(Integer)
    protein_percentage = Column(Float)
    fat_percentage = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    surfaces = relationship("Surface", back_populates="farm")
    management = relationship("Management", back_populates="farm")
    fertilizations = relationship("Fertilization", back_populates="farm")
    crop_protections = relationship("CropProtection", back_populates="farm")
    irrigation = relationship("Irrigation", back_populates="farm")
    energy = relationship("Energy", back_populates="farm")
    herd = relationship("Herd", back_populates="farm")
    effluents = relationship("Effluent", back_populates="farm")
    transport = relationship("Transport", back_populates="farm")

class Surface(Base):
    """Surface model representing 'superficies_insumos'"""
    __tablename__ = 'surfaces'
    
    id = Column(String, primary_key=True)
    farm_id = Column(String, ForeignKey('farms.id'))
    crop = Column(String, nullable=False)
    season = Column(String)
    hectares = Column(Float)
    green_matter_productivity = Column(Float)
    waste_generated = Column(Float)
    waste_destination = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship
    farm = relationship("Farm", back_populates="surfaces")

class Management(Base):
    """Management model representing 'manejo'"""
    __tablename__ = 'management'
    
    id = Column(String, primary_key=True)
    farm_id = Column(String, ForeignKey('farms.id'))
    tillage_type = Column(String)
    coverage_proportion = Column(Integer)
    no_coverage_proportion = Column(Integer)
    soil_changes = Column(String)
    soil_change_year = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship
    farm = relationship("Farm", back_populates="management")

class Fertilization(Base):
    """Fertilization model representing 'fertilizacion'"""
    __tablename__ = 'fertilization'
    
    id = Column(String, primary_key=True)
    farm_id = Column(String, ForeignKey('farms.id'))
    area = Column(String)
    hectares = Column(Float)
    type = Column(String)
    area_percentage = Column(Integer)
    applied_quantity_kg_ha = Column(Float)
    applied_quantity_total = Column(Float)
    application_method = Column(String)
    use_inhibitors = Column(String)
    protected_urea = Column(String)
    n_adjustment = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship
    farm = relationship("Farm", back_populates="fertilizations")

class CropProtection(Base):
    """Crop Protection model representing 'proteccion_cultivos'"""
    __tablename__ = 'crop_protection'
    
    id = Column(String, primary_key=True)
    farm_id = Column(String, ForeignKey('farms.id'))
    area = Column(String)
    product = Column(String)
    category = Column(String)
    application_type = Column(String)
    active_ingredient_percentage = Column(Float)
    dose = Column(Float)
    active_ingredient = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship
    farm = relationship("Farm", back_populates="crop_protections")

class Irrigation(Base):
    """Irrigation model representing 'riego'"""
    __tablename__ = 'irrigation'
    
    id = Column(String, primary_key=True)
    farm_id = Column(String, ForeignKey('farms.id'))
    source_type = Column(String)
    total_consumption = Column(Float)
    drinking_use = Column(Integer)
    cleaning_use = Column(Integer)
    irrigation_use = Column(Integer)
    water_permit = Column(String)
    irrigation_monitoring = Column(String)
    irrigation_events = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship
    farm = relationship("Farm", back_populates="irrigation")

class Energy(Base):
    """Energy model representing 'energia'"""
    __tablename__ = 'energy'
    
    id = Column(String, primary_key=True)
    farm_id = Column(String, ForeignKey('farms.id'))
    diesel_consumption = Column(Float)
    gasoline_consumption = Column(Float)
    gnc_consumption = Column(Float)
    electricity_consumption = Column(Float)
    use_solar_panels = Column(String)
    solar_panels_capacity = Column(Float)
    use_biodigesters = Column(String)
    biodigesters_capacity = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship
    farm = relationship("Farm", back_populates="energy")

class Herd(Base):
    """Herd model representing 'rebano'"""
    __tablename__ = 'herd'
    
    id = Column(String, primary_key=True)
    farm_id = Column(String, ForeignKey('farms.id'))
    category = Column(String)
    animal_count = Column(Integer)
    average_weight = Column(Float)
    grazing_hours = Column(Integer)
    dry_matter_diet = Column(Float)
    pasture_percentage = Column(Integer)
    concentrate_percentage = Column(Integer)
    others_percentage = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship
    farm = relationship("Farm", back_populates="herd")

class Effluent(Base):
    """Effluent model representing 'efluentes'"""
    __tablename__ = 'effluents'
    
    id = Column(String, primary_key=True)
    farm_id = Column(String, ForeignKey('farms.id'))
    sector = Column(String)
    hours_per_day = Column(Integer)
    excreta_management = Column(String)
    separation_efficiency = Column(Integer)
    liquid_destination = Column(String)
    solid_destination = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship
    farm = relationship("Farm", back_populates="effluents")

class Transport(Base):
    """Transport model representing 'transporte'"""
    __tablename__ = 'transport'
    
    id = Column(String, primary_key=True)
    farm_id = Column(String, ForeignKey('farms.id'))
    transported_product = Column(String)
    origin = Column(String)
    destination = Column(String)
    distance_km = Column(Float)
    vehicle_type = Column(String)
    frequency = Column(String)
    fuel_type = Column(String)
    average_load = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship
    farm = relationship("Farm", back_populates="transport")

# Function to create all tables
def create_tables():
    Base.metadata.create_all(engine)

# Data handling functions
def get_session():
    """Get a new database session"""
    return Session()

def add_farm(farm_data):
    """Add a new farm or update existing farm data"""
    session = get_session()
    
    # Check if farm already exists
    farm_id = farm_data.get('uuid', str(uuid.uuid4()))
    existing_farm = session.query(Farm).filter_by(id=farm_id).first()
    
    if existing_farm:
        # Update existing farm
        for key, value in farm_data.items():
            if key != 'uuid':
                # Map CSV column names to model attribute names
                mapped_key = {
                    'nombre_tambo': 'name',
                    'ciudad': 'city',
                    'raza': 'breed',
                    'año': 'year',
                    'mes': 'month',
                    'sup_total': 'total_area',
                    'sup_vt': 'total_cows_area',
                    'produccion_ind': 'production_per_cow',
                    'vacas_ordeñe': 'milking_cows',
                    'venta_industria': 'industry_sales_percentage',
                    'uso_queseria': 'cheese_usage_percentage',
                    'descarte': 'discard_percentage',
                    'porcentaje_proteina': 'protein_percentage',
                    'porcentaje_grasa': 'fat_percentage'
                }.get(key, key)
                
                if hasattr(existing_farm, mapped_key):
                    setattr(existing_farm, mapped_key, value)
    else:
        # Create new farm
        new_farm = Farm(
            id=farm_id,
            name=farm_data.get('nombre_tambo', ''),
            city=farm_data.get('ciudad', ''),
            breed=farm_data.get('raza', ''),
            year=farm_data.get('año', None),
            month=farm_data.get('mes', ''),
            total_area=farm_data.get('sup_total', 0.0),
            total_cows_area=farm_data.get('sup_vt', 0.0),
            production_per_cow=farm_data.get('produccion_ind', 0.0),
            milking_cows=farm_data.get('vacas_ordeñe', 0),
            industry_sales_percentage=farm_data.get('venta_industria', 0),
            cheese_usage_percentage=farm_data.get('uso_queseria', 0),
            discard_percentage=farm_data.get('descarte', 0),
            protein_percentage=farm_data.get('porcentaje_proteina', 0.0),
            fat_percentage=farm_data.get('porcentaje_grasa', 0.0)
        )
        session.add(new_farm)
    
    session.commit()
    farm_id = farm_id  # Return the farm ID for reference in other tables
    session.close()
    return farm_id

def add_surface(surface_data, farm_id=None):
    """Add a new surface record"""
    session = get_session()
    
    # Use the provided farm_id or the one in the data
    if farm_id is None:
        # Get the most recent farm
        latest_farm = session.query(Farm).order_by(Farm.created_at.desc()).first()
        if latest_farm:
            farm_id = latest_farm.id
        else:
            # No farm exists, can't add surface
            session.close()
            return None
    
    # Create new surface record
    new_surface = Surface(
        id=surface_data.get('uuid', str(uuid.uuid4())),
        farm_id=farm_id,
        crop=surface_data.get('cultivo', ''),
        season=surface_data.get('temporada', ''),
        hectares=surface_data.get('hectareas', 0.0),
        green_matter_productivity=surface_data.get('productividad_materia_verde', 0.0),
        waste_generated=surface_data.get('residuos_generados', 0.0),
        waste_destination=surface_data.get('destino_residuos', '')
    )
    
    session.add(new_surface)
    session.commit()
    surface_id = new_surface.id
    session.close()
    return surface_id

def add_management(management_data, farm_id=None):
    """Add a new management record"""
    session = get_session()
    
    # Use the provided farm_id or the one in the data
    if farm_id is None:
        # Get the most recent farm
        latest_farm = session.query(Farm).order_by(Farm.created_at.desc()).first()
        if latest_farm:
            farm_id = latest_farm.id
        else:
            # No farm exists, can't add management
            session.close()
            return None
    
    # Create new management record
    new_management = Management(
        id=management_data.get('uuid', str(uuid.uuid4())),
        farm_id=farm_id,
        tillage_type=management_data.get('tipo_labranza', ''),
        coverage_proportion=management_data.get('proporción_cobertura', 0),
        no_coverage_proportion=management_data.get('proporción_suelo_sin_cobertura', 0),
        soil_changes=management_data.get('manejo_suelos_cambios', 'No'),
        soil_change_year=management_data.get('año_cambio_manejo', None)
    )
    
    session.add(new_management)
    session.commit()
    management_id = new_management.id
    session.close()
    return management_id

def add_fertilization(fertilization_data, farm_id=None):
    """Add a new fertilization record"""
    session = get_session()
    
    # Use the provided farm_id or the one in the data
    if farm_id is None:
        # Get the most recent farm
        latest_farm = session.query(Farm).order_by(Farm.created_at.desc()).first()
        if latest_farm:
            farm_id = latest_farm.id
        else:
            # No farm exists, can't add fertilization
            session.close()
            return None
    
    # Create new fertilization record
    new_fertilization = Fertilization(
        id=fertilization_data.get('uuid', str(uuid.uuid4())),
        farm_id=farm_id,
        area=fertilization_data.get('área', ''),
        hectares=fertilization_data.get('hectareas', 0.0),
        type=fertilization_data.get('tipo', ''),
        area_percentage=fertilization_data.get('%_área_total', 0),
        applied_quantity_kg_ha=fertilization_data.get('cantidad_aplicada_kg_ha', 0.0),
        applied_quantity_total=fertilization_data.get('cantidad_aplicada_total', 0.0),
        application_method=fertilization_data.get('método_aplicación', ''),
        use_inhibitors=fertilization_data.get('uso_inhibidores', 'No'),
        protected_urea=fertilization_data.get('urea_protegida', 'No'),
        n_adjustment=fertilization_data.get('ajuste_por_N', 'No')
    )
    
    session.add(new_fertilization)
    session.commit()
    fertilization_id = new_fertilization.id
    session.close()
    return fertilization_id

def add_crop_protection(protection_data, farm_id=None):
    """Add a new crop protection record"""
    session = get_session()
    
    # Use the provided farm_id or the one in the data
    if farm_id is None:
        # Get the most recent farm
        latest_farm = session.query(Farm).order_by(Farm.created_at.desc()).first()
        if latest_farm:
            farm_id = latest_farm.id
        else:
            # No farm exists, can't add protection
            session.close()
            return None
    
    # Create new crop protection record
    new_protection = CropProtection(
        id=protection_data.get('uuid', str(uuid.uuid4())),
        farm_id=farm_id,
        area=protection_data.get('área', ''),
        product=protection_data.get('producto', ''),
        category=protection_data.get('categoría', ''),
        application_type=protection_data.get('tipo_aplicacion', ''),
        active_ingredient_percentage=protection_data.get('%_ingrediente_activo', 0.0),
        dose=protection_data.get('dosis', 0.0),
        active_ingredient=protection_data.get('ingrediente_activo', '')
    )
    
    session.add(new_protection)
    session.commit()
    protection_id = new_protection.id
    session.close()
    return protection_id

def add_irrigation(irrigation_data, farm_id=None):
    """Add a new irrigation record"""
    session = get_session()
    
    # Use the provided farm_id or the one in the data
    if farm_id is None:
        # Get the most recent farm
        latest_farm = session.query(Farm).order_by(Farm.created_at.desc()).first()
        if latest_farm:
            farm_id = latest_farm.id
        else:
            # No farm exists, can't add irrigation
            session.close()
            return None
    
    # Create new irrigation record
    new_irrigation = Irrigation(
        id=irrigation_data.get('uuid', str(uuid.uuid4())),
        farm_id=farm_id,
        source_type=irrigation_data.get('tipo_fuente', ''),
        total_consumption=irrigation_data.get('consumo_total', 0.0),
        drinking_use=irrigation_data.get('uso_para_bebida', 0),
        cleaning_use=irrigation_data.get('uso_para_limpieza', 0),
        irrigation_use=irrigation_data.get('uso_para_riego', 0),
        water_permit=irrigation_data.get('permiso_agua', 'No'),
        irrigation_monitoring=irrigation_data.get('monitoreo_riego', 'No'),
        irrigation_events=irrigation_data.get('eventos_riego', '')
    )
    
    session.add(new_irrigation)
    session.commit()
    irrigation_id = new_irrigation.id
    session.close()
    return irrigation_id

def add_energy(energy_data, farm_id=None):
    """Add a new energy record"""
    session = get_session()
    
    # Use the provided farm_id or the one in the data
    if farm_id is None:
        # Get the most recent farm
        latest_farm = session.query(Farm).order_by(Farm.created_at.desc()).first()
        if latest_farm:
            farm_id = latest_farm.id
        else:
            # No farm exists, can't add energy
            session.close()
            return None
    
    # Create new energy record
    new_energy = Energy(
        id=energy_data.get('uuid', str(uuid.uuid4())),
        farm_id=farm_id,
        diesel_consumption=energy_data.get('consumo_diesel', 0.0),
        gasoline_consumption=energy_data.get('consumo_gasolina', 0.0),
        gnc_consumption=energy_data.get('consumo_GNC', 0.0),
        electricity_consumption=energy_data.get('consumo_electricidad', 0.0),
        use_solar_panels=energy_data.get('uso_paneles_solares', 'No'),
        solar_panels_capacity=energy_data.get('capacidad_paneles', 0.0),
        use_biodigesters=energy_data.get('uso_biodigestores', 'No'),
        biodigesters_capacity=energy_data.get('capacidad_biodigestores', 0.0)
    )
    
    session.add(new_energy)
    session.commit()
    energy_id = new_energy.id
    session.close()
    return energy_id

def add_herd(herd_data, farm_id=None):
    """Add a new herd record"""
    session = get_session()
    
    # Use the provided farm_id or the one in the data
    if farm_id is None:
        # Get the most recent farm
        latest_farm = session.query(Farm).order_by(Farm.created_at.desc()).first()
        if latest_farm:
            farm_id = latest_farm.id
        else:
            # No farm exists, can't add herd
            session.close()
            return None
    
    # Create new herd record
    new_herd = Herd(
        id=herd_data.get('uuid', str(uuid.uuid4())),
        farm_id=farm_id,
        category=herd_data.get('categoría', ''),
        animal_count=herd_data.get('número_animales', 0),
        average_weight=herd_data.get('peso_promedio', 0.0),
        grazing_hours=herd_data.get('horas_pastoreo', 0),
        dry_matter_diet=herd_data.get('dieta_materia_seca', 0.0),
        pasture_percentage=herd_data.get('porcentaje_pastura', 0),
        concentrate_percentage=herd_data.get('porcentaje_concentrado', 0),
        others_percentage=herd_data.get('porcentaje_otros', 0)
    )
    
    session.add(new_herd)
    session.commit()
    herd_id = new_herd.id
    session.close()
    return herd_id

def add_effluent(effluent_data, farm_id=None):
    """Add a new effluent record"""
    session = get_session()
    
    # Use the provided farm_id or the one in the data
    if farm_id is None:
        # Get the most recent farm
        latest_farm = session.query(Farm).order_by(Farm.created_at.desc()).first()
        if latest_farm:
            farm_id = latest_farm.id
        else:
            # No farm exists, can't add effluent
            session.close()
            return None
    
    # Create new effluent record
    new_effluent = Effluent(
        id=effluent_data.get('uuid', str(uuid.uuid4())),
        farm_id=farm_id,
        sector=effluent_data.get('sector', ''),
        hours_per_day=effluent_data.get('horas_dia', 0),
        excreta_management=effluent_data.get('manejo_excretas', ''),
        separation_efficiency=effluent_data.get('eficiencia_separación', 0),
        liquid_destination=effluent_data.get('destino_liquidos', ''),
        solid_destination=effluent_data.get('destino_solidos', '')
    )
    
    session.add(new_effluent)
    session.commit()
    effluent_id = new_effluent.id
    session.close()
    return effluent_id

def add_transport(transport_data, farm_id=None):
    """Add a new transport record"""
    session = get_session()
    
    # Use the provided farm_id or the one in the data
    if farm_id is None:
        # Get the most recent farm
        latest_farm = session.query(Farm).order_by(Farm.created_at.desc()).first()
        if latest_farm:
            farm_id = latest_farm.id
        else:
            # No farm exists, can't add transport
            session.close()
            return None
    
    # Create new transport record
    new_transport = Transport(
        id=transport_data.get('uuid', str(uuid.uuid4())),
        farm_id=farm_id,
        transported_product=transport_data.get('producto_transportado', ''),
        origin=transport_data.get('inicio', ''),
        destination=transport_data.get('destino', ''),
        distance_km=transport_data.get('distancia_km', 0.0),
        vehicle_type=transport_data.get('tipo_vehiculo', ''),
        frequency=transport_data.get('frecuencia', ''),
        fuel_type=transport_data.get('tipo_combustible', ''),
        average_load=transport_data.get('carga_promedio', 0.0)
    )
    
    session.add(new_transport)
    session.commit()
    transport_id = new_transport.id
    session.close()
    return transport_id

# Data retrieval functions
def get_farm_data(farm_id=None):
    """Get farm data as a dataframe"""
    session = get_session()
    
    if farm_id:
        # Get specific farm
        farm = session.query(Farm).filter_by(id=farm_id).first()
        farms = [farm] if farm else []
    else:
        # Get all farms
        farms = session.query(Farm).all()
    
    # Convert to dataframe
    data = []
    for farm in farms:
        data.append({
            'uuid': farm.id,
            'nombre_tambo': farm.name,
            'ciudad': farm.city,
            'raza': farm.breed,
            'año': farm.year,
            'mes': farm.month,
            'sup_total': farm.total_area,
            'sup_vt': farm.total_cows_area,
            'produccion_ind': farm.production_per_cow,
            'vacas_ordeñe': farm.milking_cows,
            'venta_industria': farm.industry_sales_percentage,
            'uso_queseria': farm.cheese_usage_percentage,
            'descarte': farm.discard_percentage,
            'porcentaje_proteina': farm.protein_percentage,
            'porcentaje_grasa': farm.fat_percentage
        })
    
    session.close()
    return pd.DataFrame(data) if data else pd.DataFrame()

def get_surfaces_data(farm_id=None):
    """Get surfaces data as a dataframe"""
    session = get_session()
    
    if farm_id:
        # Get surfaces for specific farm
        surfaces = session.query(Surface).filter_by(farm_id=farm_id).all()
    else:
        # Get all surfaces or for the most recent farm
        latest_farm = session.query(Farm).order_by(Farm.created_at.desc()).first()
        if latest_farm:
            surfaces = session.query(Surface).filter_by(farm_id=latest_farm.id).all()
        else:
            surfaces = []
    
    # Convert to dataframe
    data = []
    for surface in surfaces:
        data.append({
            'uuid': surface.id,
            'cultivo': surface.crop,
            'temporada': surface.season,
            'hectareas': surface.hectares,
            'productividad_materia_verde': surface.green_matter_productivity,
            'residuos_generados': surface.waste_generated,
            'destino_residuos': surface.waste_destination
        })
    
    session.close()
    return pd.DataFrame(data) if data else pd.DataFrame()

def get_management_data(farm_id=None):
    """Get management data as a dataframe"""
    session = get_session()
    
    if farm_id:
        # Get management for specific farm
        managements = session.query(Management).filter_by(farm_id=farm_id).all()
    else:
        # Get all managements or for the most recent farm
        latest_farm = session.query(Farm).order_by(Farm.created_at.desc()).first()
        if latest_farm:
            managements = session.query(Management).filter_by(farm_id=latest_farm.id).all()
        else:
            managements = []
    
    # Convert to dataframe
    data = []
    for management in managements:
        data.append({
            'uuid': management.id,
            'tipo_labranza': management.tillage_type,
            'proporción_cobertura': management.coverage_proportion,
            'proporción_suelo_sin_cobertura': management.no_coverage_proportion,
            'manejo_suelos_cambios': management.soil_changes,
            'año_cambio_manejo': management.soil_change_year
        })
    
    session.close()
    return pd.DataFrame(data) if data else pd.DataFrame()

def get_fertilization_data(farm_id=None):
    """Get fertilization data as a dataframe"""
    session = get_session()
    
    if farm_id:
        # Get fertilization for specific farm
        fertilizations = session.query(Fertilization).filter_by(farm_id=farm_id).all()
    else:
        # Get all fertilizations or for the most recent farm
        latest_farm = session.query(Farm).order_by(Farm.created_at.desc()).first()
        if latest_farm:
            fertilizations = session.query(Fertilization).filter_by(farm_id=latest_farm.id).all()
        else:
            fertilizations = []
    
    # Convert to dataframe
    data = []
    for fertilization in fertilizations:
        data.append({
            'uuid': fertilization.id,
            'área': fertilization.area,
            'hectareas': fertilization.hectares,
            'tipo': fertilization.type,
            '%_área_total': fertilization.area_percentage,
            'cantidad_aplicada_kg_ha': fertilization.applied_quantity_kg_ha,
            'cantidad_aplicada_total': fertilization.applied_quantity_total,
            'método_aplicación': fertilization.application_method,
            'uso_inhibidores': fertilization.use_inhibitors,
            'urea_protegida': fertilization.protected_urea,
            'ajuste_por_N': fertilization.n_adjustment
        })
    
    session.close()
    return pd.DataFrame(data) if data else pd.DataFrame()

def get_crop_protection_data(farm_id=None):
    """Get crop protection data as a dataframe"""
    session = get_session()
    
    if farm_id:
        # Get crop protection for specific farm
        protections = session.query(CropProtection).filter_by(farm_id=farm_id).all()
    else:
        # Get all protections or for the most recent farm
        latest_farm = session.query(Farm).order_by(Farm.created_at.desc()).first()
        if latest_farm:
            protections = session.query(CropProtection).filter_by(farm_id=latest_farm.id).all()
        else:
            protections = []
    
    # Convert to dataframe
    data = []
    for protection in protections:
        data.append({
            'uuid': protection.id,
            'área': protection.area,
            'producto': protection.product,
            'categoría': protection.category,
            'tipo_aplicacion': protection.application_type,
            '%_ingrediente_activo': protection.active_ingredient_percentage,
            'dosis': protection.dose,
            'ingrediente_activo': protection.active_ingredient
        })
    
    session.close()
    return pd.DataFrame(data) if data else pd.DataFrame()

def get_irrigation_data(farm_id=None):
    """Get irrigation data as a dataframe"""
    session = get_session()
    
    if farm_id:
        # Get irrigation for specific farm
        irrigations = session.query(Irrigation).filter_by(farm_id=farm_id).all()
    else:
        # Get all irrigations or for the most recent farm
        latest_farm = session.query(Farm).order_by(Farm.created_at.desc()).first()
        if latest_farm:
            irrigations = session.query(Irrigation).filter_by(farm_id=latest_farm.id).all()
        else:
            irrigations = []
    
    # Convert to dataframe
    data = []
    for irrigation in irrigations:
        data.append({
            'uuid': irrigation.id,
            'tipo_fuente': irrigation.source_type,
            'consumo_total': irrigation.total_consumption,
            'uso_para_bebida': irrigation.drinking_use,
            'uso_para_limpieza': irrigation.cleaning_use,
            'uso_para_riego': irrigation.irrigation_use,
            'permiso_agua': irrigation.water_permit,
            'monitoreo_riego': irrigation.irrigation_monitoring,
            'eventos_riego': irrigation.irrigation_events
        })
    
    session.close()
    return pd.DataFrame(data) if data else pd.DataFrame()

def get_energy_data(farm_id=None):
    """Get energy data as a dataframe"""
    session = get_session()
    
    if farm_id:
        # Get energy for specific farm
        energies = session.query(Energy).filter_by(farm_id=farm_id).all()
    else:
        # Get all energies or for the most recent farm
        latest_farm = session.query(Farm).order_by(Farm.created_at.desc()).first()
        if latest_farm:
            energies = session.query(Energy).filter_by(farm_id=latest_farm.id).all()
        else:
            energies = []
    
    # Convert to dataframe
    data = []
    for energy in energies:
        data.append({
            'uuid': energy.id,
            'consumo_diesel': energy.diesel_consumption,
            'consumo_gasolina': energy.gasoline_consumption,
            'consumo_GNC': energy.gnc_consumption,
            'consumo_electricidad': energy.electricity_consumption,
            'uso_paneles_solares': energy.use_solar_panels,
            'capacidad_paneles': energy.solar_panels_capacity,
            'uso_biodigestores': energy.use_biodigesters,
            'capacidad_biodigestores': energy.biodigesters_capacity
        })
    
    session.close()
    return pd.DataFrame(data) if data else pd.DataFrame()

def get_herd_data(farm_id=None):
    """Get herd data as a dataframe"""
    session = get_session()
    
    if farm_id:
        # Get herd for specific farm
        herds = session.query(Herd).filter_by(farm_id=farm_id).all()
    else:
        # Get all herds or for the most recent farm
        latest_farm = session.query(Farm).order_by(Farm.created_at.desc()).first()
        if latest_farm:
            herds = session.query(Herd).filter_by(farm_id=latest_farm.id).all()
        else:
            herds = []
    
    # Convert to dataframe
    data = []
    for herd in herds:
        data.append({
            'uuid': herd.id,
            'categoría': herd.category,
            'número_animales': herd.animal_count,
            'peso_promedio': herd.average_weight,
            'horas_pastoreo': herd.grazing_hours,
            'dieta_materia_seca': herd.dry_matter_diet,
            'porcentaje_pastura': herd.pasture_percentage,
            'porcentaje_concentrado': herd.concentrate_percentage,
            'porcentaje_otros': herd.others_percentage
        })
    
    session.close()
    return pd.DataFrame(data) if data else pd.DataFrame()

def get_effluent_data(farm_id=None):
    """Get effluent data as a dataframe"""
    session = get_session()
    
    if farm_id:
        # Get effluent for specific farm
        effluents = session.query(Effluent).filter_by(farm_id=farm_id).all()
    else:
        # Get all effluents or for the most recent farm
        latest_farm = session.query(Farm).order_by(Farm.created_at.desc()).first()
        if latest_farm:
            effluents = session.query(Effluent).filter_by(farm_id=latest_farm.id).all()
        else:
            effluents = []
    
    # Convert to dataframe
    data = []
    for effluent in effluents:
        data.append({
            'uuid': effluent.id,
            'sector': effluent.sector,
            'horas_dia': effluent.hours_per_day,
            'manejo_excretas': effluent.excreta_management,
            'eficiencia_separación': effluent.separation_efficiency,
            'destino_liquidos': effluent.liquid_destination,
            'destino_solidos': effluent.solid_destination
        })
    
    session.close()
    return pd.DataFrame(data) if data else pd.DataFrame()

def get_transport_data(farm_id=None):
    """Get transport data as a dataframe"""
    session = get_session()
    
    if farm_id:
        # Get transport for specific farm
        transports = session.query(Transport).filter_by(farm_id=farm_id).all()
    else:
        # Get all transports or for the most recent farm
        latest_farm = session.query(Farm).order_by(Farm.created_at.desc()).first()
        if latest_farm:
            transports = session.query(Transport).filter_by(farm_id=latest_farm.id).all()
        else:
            transports = []
    
    # Convert to dataframe
    data = []
    for transport in transports:
        data.append({
            'uuid': transport.id,
            'producto_transportado': transport.transported_product,
            'inicio': transport.origin,
            'destino': transport.destination,
            'distancia_km': transport.distance_km,
            'tipo_vehiculo': transport.vehicle_type,
            'frecuencia': transport.frequency,
            'tipo_combustible': transport.fuel_type,
            'carga_promedio': transport.average_load
        })
    
    session.close()
    return pd.DataFrame(data) if data else pd.DataFrame()

def get_all_data():
    """Get all data as a dictionary of dataframes"""
    return {
        'datos_generales': get_farm_data(),
        'superficies_insumos': get_surfaces_data(),
        'manejo': get_management_data(),
        'fertilizacion': get_fertilization_data(),
        'proteccion_cultivos': get_crop_protection_data(),
        'riego': get_irrigation_data(),
        'energia': get_energy_data(),
        'rebano': get_herd_data(),
        'efluentes': get_effluent_data(),
        'transporte': get_transport_data()
    }

def remove_last_entry(table_name):
    """Remove the last entry from a specific table"""
    session = get_session()
    
    # Map table name to model class
    table_map = {
        'datos_generales': Farm,
        'superficies_insumos': Surface,
        'manejo': Management,
        'fertilizacion': Fertilization,
        'proteccion_cultivos': CropProtection,
        'riego': Irrigation,
        'energia': Energy,
        'rebano': Herd,
        'efluentes': Effluent,
        'transporte': Transport
    }
    
    # Get model class
    model_class = table_map.get(table_name)
    if not model_class:
        session.close()
        return False
    
    # Get last entry
    last_entry = session.query(model_class).order_by(model_class.created_at.desc()).first()
    if last_entry:
        session.delete(last_entry)
        session.commit()
        session.close()
        return True
    
    session.close()
    return False

def check_data_exists():
    """Check if any data exists in the database"""
    session = get_session()
    
    # Check if there are any farms
    farm_exists = session.query(Farm).first() is not None
    session.close()
    
    return farm_exists

# Initialize the database
create_tables()