import os
import pandas as pd
import streamlit as st
import uuid
import re
import database as db

def save_dataframe(df, filename):
    """Save a dataframe to the database based on filename"""
    # Map filename to the appropriate database function
    if 'uuid' not in df.columns:
        df['uuid'] = generate_uuid()
    
    file_to_func = {
        'datos_generales.csv': db.add_farm,
        'superficies_insumos.csv': db.add_surface,
        'manejo.csv': db.add_management,
        'fertilizacion.csv': db.add_fertilization,
        'proteccion_cultivos.csv': db.add_crop_protection,
        'riego.csv': db.add_irrigation,
        'energia.csv': db.add_energy,
        'rebano.csv': db.add_herd,
        'efluentes.csv': db.add_effluent,
        'transporte.csv': db.add_transport
    }
    
    # Get the appropriate database function
    db_func = file_to_func.get(filename)
    if db_func:
        # Convert dataframe to dictionary
        data = df.iloc[0].to_dict()
        # Call the appropriate database function
        db_func(data)
        return True
    
    # Fallback to file-based storage for backward compatibility
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Create a path to save the file
    file_path = os.path.join("data", filename)
    
    # Check if file exists and load existing data if it does
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        # Check if data already exists (based on UUID if available)
        if 'uuid' in df.columns and 'uuid' in existing_df.columns:
            # Remove existing row with same UUID and append new data
            existing_df = existing_df[existing_df['uuid'] != df['uuid'].iloc[0]]
            updated_df = pd.concat([existing_df, df], ignore_index=True)
        else:
            # Simply append the new data
            updated_df = pd.concat([existing_df, df], ignore_index=True)
    else:
        updated_df = df
    
    # Save the updated dataframe
    updated_df.to_csv(file_path, index=False)
    return True

def load_dataframe(filename):
    """Load a dataframe from the database based on filename and current farm"""
    # For datos_generales.csv, always show all farms
    if filename == "datos_generales.csv":
        return db.get_farm_data()
    
    # For other files, filter by current farm if one is selected
    if "farm_id" in st.session_state:
        farm_id = st.session_state.farm_id
    else:
        farm_id = None
        
    # Map filename to the appropriate database function
    file_to_func = {
        'datos_generales.csv': db.get_farm_data,
        'superficies_insumos.csv': db.get_surfaces_data,
        'manejo.csv': db.get_management_data,
        'fertilizacion.csv': db.get_fertilization_data,
        'proteccion_cultivos.csv': db.get_crop_protection_data,
        'riego.csv': db.get_irrigation_data,
        'energia.csv': db.get_energy_data,
        'rebano.csv': db.get_herd_data,
        'efluentes.csv': db.get_effluent_data,
        'transporte.csv': db.get_transport_data
    }
    
    # Get the appropriate database function
    db_func = file_to_func.get(filename)
    if db_func:
        return db_func()
    
    # Fallback to file-based storage for backward compatibility
    file_path = os.path.join("data", filename)
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame()

def validate_numeric(value, min_val=None, max_val=None, allow_empty=False):
    """Validate if a value is numeric and within range"""
    if allow_empty and (value == "" or value is None):
        return True
    
    try:
        num_value = float(value)
        if min_val is not None and num_value < min_val:
            return False
        if max_val is not None and num_value > max_val:
            return False
        return True
    except (ValueError, TypeError):
        return False

def validate_percentage(value, allow_empty=False):
    """Validate if a value is a percentage (0-100)"""
    return validate_numeric(value, min_val=0, max_val=100, allow_empty=allow_empty)

def validate_text(value, min_length=1, max_length=None, allow_empty=False):
    """Validate if a value is text and within length constraints"""
    if allow_empty and (value == "" or value is None):
        return True
    
    if not isinstance(value, str):
        try:
            value = str(value)
        except:
            return False
    
    if len(value) < min_length:
        return False
    if max_length is not None and len(value) > max_length:
        return False
    return True

def generate_uuid():
    """Generate a unique identifier"""
    return str(uuid.uuid4())

def show_validation_error(message):
    """Display a standardized validation error message"""
    st.error(f"⚠️ {message}")

def show_success_message(message):
    """Display a standardized success message"""
    st.success(f"✅ {message}")

def format_filename(farm_name):
    """Convert a farm name to a safe filename"""
    # Remove special characters, replace spaces with underscores
    return re.sub(r'[^\w\s]', '', farm_name).replace(' ', '_').lower()

def get_all_data():
    """Get all data from database"""
    return db.get_all_data()

def check_data_exists():
    """Check if any data has been collected"""
    return db.check_data_exists()
