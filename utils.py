import os
import pandas as pd
import streamlit as st
import uuid
import re

def save_dataframe(df, filename):
    """Save a dataframe to a CSV file in the data directory"""
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
    """Load a dataframe from a CSV file in the data directory"""
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
    """Get all CSV data files as a dictionary of dataframes"""
    data_files = {
        'datos_generales': load_dataframe('datos_generales.csv'),
        'superficies_insumos': load_dataframe('superficies_insumos.csv'),
        'manejo': load_dataframe('manejo.csv'),
        'fertilizacion': load_dataframe('fertilizacion.csv'),
        'proteccion_cultivos': load_dataframe('proteccion_cultivos.csv'),
        'riego': load_dataframe('riego.csv'),
        'energia': load_dataframe('energia.csv'),
        'rebano': load_dataframe('rebano.csv'),
        'efluentes': load_dataframe('efluentes.csv'),
        'transporte': load_dataframe('transporte.csv')
    }
    return data_files

def check_data_exists():
    """Check if any data has been collected"""
    data_folder = "data"
    if not os.path.exists(data_folder):
        return False
    
    # Check if any CSV files exist and have content
    csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
    for csv_file in csv_files:
        df = pd.read_csv(os.path.join(data_folder, csv_file))
        if not df.empty:
            return True
    
    return False
