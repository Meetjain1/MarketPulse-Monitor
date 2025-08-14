import sqlite3
import pandas as pd
import os
import datetime

def get_db_path():
    # create db directory if it doesn't exist
    db_dir = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    # return the full path to the database file
    return os.path.join(db_dir, 'price_monitor.db')

def init_db():
    # get the database file path
    db_path = get_db_path()
    
    # gonna connect to the database now
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # make a table if we don't have one already
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id TEXT NOT NULL,
        product_name TEXT NOT NULL,
        our_price REAL NOT NULL,
        competitor_name TEXT NOT NULL,
        competitor_price REAL NOT NULL,
        last_updated DATE NOT NULL
    )
    ''')
    
    # save our work and close up shop
    conn.commit()
    conn.close()
    
    return True
    
    # create metadata object
    metadata = MetaData()
    
    # define our products table - nothing fancy here
    products = Table(
        'products',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('product_id', String, nullable=False),
        Column('product_name', String, nullable=False),
        Column('our_price', Float, nullable=False),
        Column('competitor_name', String, nullable=False),
        Column('competitor_price', Float, nullable=False),
        Column('last_updated', Date, nullable=False),
    )
    
    # create the tables if they don't exist yet
    metadata.create_all(engine)
    return engine

def save_data_to_db(df):
    # gotta fix the dates so they look nice
    df['last_updated'] = pd.to_datetime(df['last_updated']).dt.date
    
    # better check if we got all the stuff we need
    required_fields = ['product_id', 'product_name', 'our_price', 'competitor_name', 
                      'competitor_price', 'last_updated']
    
    for field in required_fields:
        if field not in df.columns:
            return False, f"Missing required field: {field}"
    
    # nobody's gonna give us money to take their money lol
    if (df['our_price'] < 0).any() or (df['competitor_price'] < 0).any():
        return False, "Negative prices are not allowed"
    
    try:
        # where we storing this stuff?
        db_path = get_db_path()
        
        # open the door to the database
        conn = sqlite3.connect(db_path)
        
        # put all the data in one by one
        for _, row in df.iterrows():
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO products (product_id, product_name, our_price, competitor_name, competitor_price, last_updated)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                row['product_id'], 
                row['product_name'], 
                row['our_price'], 
                row['competitor_name'], 
                row['competitor_price'],
                row['last_updated']
            ))
        
        # save our work and close up shop
        conn.commit()
        conn.close()
        
        return True, "Data saved successfully"
    except Exception as e:
        # uh oh something went wrong
        print(f"Error saving data: {str(e)}")
        return False, f"Error saving data: {str(e)}"

def get_all_products():
    try:
        # where's that database again?
        db_path = get_db_path()
        
        # let pandas do the heavy lifting
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM products", conn)
        conn.close()
        
        return df
    except Exception as e:
        # don't crash if we can't find the data
        print(f"Database error: {str(e)}")
        return pd.DataFrame()

def search_products(search_term):
    try:
        # find the database
        db_path = get_db_path()
        
        # open up the database
        conn = sqlite3.connect(db_path)
        
        # let's find what they're looking for
        query = f"""
        SELECT * FROM products 
        WHERE product_name LIKE '%{search_term}%' 
        OR competitor_name LIKE '%{search_term}%'
        """
        
        # run the search and give back what we found
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    except Exception as e:
        print(f"Search error: {str(e)}")
        return pd.DataFrame()

def filter_cheaper_competitors():
    try:
        # get database path
        db_path = get_db_path()
        
        # connect to database
        conn = sqlite3.connect(db_path)
        
        # query
        query = """
        SELECT * FROM products 
        WHERE competitor_price < our_price
        """
        
        # execute query and return results
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    except Exception as e:
        print(f"Filter error: {str(e)}")
        return pd.DataFrame()

def filter_we_are_cheaper():
    try:
        # get database path
        db_path = get_db_path()
        
        # connect to database
        conn = sqlite3.connect(db_path)
        
        # query
        query = """
        SELECT * FROM products 
        WHERE our_price < competitor_price
        """
        
        # execute query and return results
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    except Exception as e:
        print(f"Filter error: {str(e)}")
        return pd.DataFrame()

def get_last_update_date():
    try:
        # get database path
        db_path = get_db_path()
        
        # connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # query for the most recent date
        cursor.execute("SELECT MAX(last_updated) as last_date FROM products")
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0]:
            return result[0]
        return "No data available"
    except Exception as e:
        print(f"Date query error: {str(e)}")
        return "Database error"

def delete_database():
    """
    Deletes the entire database file.
    """
    try:
        db_path = get_db_path()
        if os.path.exists(db_path):
            os.remove(db_path)
            return True, "Database deleted successfully."
        return False, "Database file not found."
    except Exception as e:
        return False, f"Error deleting database: {str(e)}"