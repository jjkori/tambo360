import os
import pandas as pd
import database as db

def migrate_csv_to_database():
    """Migrate data from CSV files to the database"""
    print("Starting data migration from CSV files to database...")
    
    data_dir = "data"
    if not os.path.exists(data_dir):
        print("No data directory found. Nothing to migrate.")
        return
    
    # Check for CSV files
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    if not csv_files:
        print("No CSV files found. Nothing to migrate.")
        return
    
    # Map CSV files to database functions
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
    
    # Process each CSV file
    for csv_file in csv_files:
        if csv_file in file_to_func:
            print(f"Migrating {csv_file}...")
            
            # Read CSV file
            csv_path = os.path.join(data_dir, csv_file)
            df = pd.read_csv(csv_path)
            
            # If the dataframe is empty, skip
            if df.empty:
                print(f"No data in {csv_file}. Skipping...")
                continue
            
            # Get the appropriate database function
            db_func = file_to_func[csv_file]
            
            # Special case for datos_generales.csv (farm data)
            if csv_file == 'datos_generales.csv':
                # Process farm data first
                farm_id = None
                for _, row in df.iterrows():
                    farm_id = db_func(row.to_dict())
                
                # Store farm_id for related entities
                if farm_id:
                    print(f"Farm ID: {farm_id} migrated.")
                    
                    # Now process the related entities using the farm_id
                    for related_csv in csv_files:
                        if related_csv != 'datos_generales.csv' and related_csv in file_to_func:
                            print(f"Migrating {related_csv} for farm {farm_id}...")
                            
                            # Read related CSV file
                            related_csv_path = os.path.join(data_dir, related_csv)
                            related_df = pd.read_csv(related_csv_path)
                            
                            # If the dataframe is empty, skip
                            if related_df.empty:
                                print(f"No data in {related_csv}. Skipping...")
                                continue
                            
                            # Get the appropriate database function
                            related_db_func = file_to_func[related_csv]
                            
                            # Process each row
                            for _, row in related_df.iterrows():
                                data_dict = row.to_dict()
                                related_db_func(data_dict, farm_id)
                    
                    # Skip further processing as we've already handled all files
                    break
            # Regular case for non-farm data (only used if farm data is not present)
            else:
                # Process each row
                for _, row in df.iterrows():
                    db_func(row.to_dict())
    
    print("Migration completed successfully!")

if __name__ == "__main__":
    # Ensure database tables exist
    db.create_tables()
    
    # Migrate data from CSV files to database
    migrate_csv_to_database()