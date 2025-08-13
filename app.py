import streamlit as st
import pandas as pd
import io
import os
from datetime import datetime
import plotly.express as px
import numpy as np

# Import our own special code files - they do all the hard work!
import db
import price_compare
import email_alert

# Set up our database when the app first starts
# This is like setting the table before dinner!
db.init_db()

# Make our app look good with a nice title and wide layout
st.set_page_config(
    page_title="Price Monitoring Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add some custom CSS for better styling
# © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
st.markdown("""
<style>
    .dataframe {
        width: 100%;
    }
    .alert {
        background-color: rgba(255, 0, 0, 0.1) !important;
    }
    .good {
        background-color: rgba(0, 255, 0, 0.1) !important;
    }
    .dataframe td:hover {
        background-color: rgba(100, 100, 100, 0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e6f0ff;
        border-bottom: 2px solid #4c78e0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # sidebar navigation
    st.sidebar.title("Price Monitoring Dashboard")
    
    nav_options = [
        "Home", 
        "Price Comparison Table", 
        "Upload Data", 
        "Search & Filter", 
        "Alert Settings"
    ]
    
    page = st.sidebar.radio("Navigation", nav_options)
    
    # run the selected page
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    if page == "Home":
        home_page()
    elif page == "Price Comparison Table":
        price_table_page()
    elif page == "Upload Data":
        upload_page()
    elif page == "Search & Filter":
        search_filter_page()
    elif page == "Alert Settings":
        alert_settings_page()

def home_page():
    st.title("E-commerce Price Monitoring Dashboard")
    
    # get current data
    df = db.get_all_products()
    
    if df.empty:
        st.warning("No data available. Please upload data first.")
        return
    
    # add price comparison status to data
    df = price_compare.compare_prices(df)
    
    # get stats for dashboard
    stats = price_compare.get_price_change_stats(df)
    last_update = db.get_last_update_date()
    
    # main stats in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Products Monitored", stats['total_products'])
    
    with col2:
        st.metric("Price Drop Alerts", stats['competitors_cheaper'])
    
    with col3:
        st.metric("Last Data Update", last_update)
    
    # second row of stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Products Where We're Cheaper", stats['we_are_cheaper'])
    
    with col2:
        if stats['avg_competitor_advantage'] > 0:
            st.metric("Avg. Competitor Price Advantage", f"${stats['avg_competitor_advantage']}")
    
    with col3:
        if stats['avg_our_advantage'] > 0:
            st.metric("Avg. Our Price Advantage", f"${stats['avg_our_advantage']}")
    
    # add some visualizations
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    st.subheader("Price Comparison Overview")
    
    # price status distribution
    fig = px.pie(
        names=["Competitors Cheaper", "We Are Cheaper", "Identical Prices"],
        values=[stats['competitors_cheaper'], stats['we_are_cheaper'], stats['identical_prices']],
        color_discrete_sequence=["#ff9999", "#99ff99", "#cccccc"]
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # show top 5 price drop alerts
    st.subheader("Top Price Drop Alerts")
    alerts_df = df[df['status'] == 'alert'].copy()
    
    if not alerts_df.empty:
        # sort by largest price difference
        alerts_df['price_diff'] = alerts_df['our_price'] - alerts_df['competitor_price']
        alerts_df = alerts_df.sort_values('price_diff', ascending=False).head(5)
        
        # drop status and message columns
        # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
        display_df = alerts_df[['product_name', 'our_price', 'competitor_name', 'competitor_price', 'price_diff']]
        display_df = display_df.rename(columns={
            'product_name': 'Product', 
            'our_price': 'Our Price', 
            'competitor_name': 'Competitor', 
            'competitor_price': 'Their Price', 
            'price_diff': 'Price Difference'
        })
        
        # format currency values
        for col in ['Our Price', 'Their Price', 'Price Difference']:
            display_df[col] = display_df[col].apply(lambda x: f"${x:.2f}")
        
        st.table(display_df)
    else:
        st.info("No price drop alerts currently!")

def price_table_page():
    st.title("Price Comparison Table")
    
    # get data and add comparison status
    df = db.get_all_products()
    
    if df.empty:
        st.warning("No data available. Please upload data first.")
        return
    
    df = price_compare.compare_prices(df)
    
    # make a display dataframe with formatted columns
    display_df = df.copy()
    
    # rename columns for better display
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    display_df = display_df.rename(columns={
        'product_id': 'Product ID',
        'product_name': 'Product Name',
        'our_price': 'Our Price',
        'competitor_name': 'Competitor',
        'competitor_price': 'Their Price',
        'last_updated': 'Last Updated',
        'message': 'Status'
    })
    
    # format currency values
    display_df['Our Price'] = display_df['Our Price'].apply(lambda x: f"${x:.2f}")
    display_df['Their Price'] = display_df['Their Price'].apply(lambda x: f"${x:.2f}")
    
    # drop the status column as we'll use it for styling
    display_df = display_df.drop(columns=['status'])
    
    # apply styling based on status
    def apply_row_styling(row):
        if row.name in df[df['status'] == 'alert'].index:
            return ['background-color: rgba(255, 0, 0, 0.1)'] * len(row)
        elif row.name in df[df['status'] == 'good'].index:
            return ['background-color: rgba(0, 255, 0, 0.1)'] * len(row)
        return [''] * len(row)
    
    # display with styling
    st.dataframe(display_df.style.apply(apply_row_styling, axis=1), use_container_width=True)

def upload_page():
    st.title("Upload Product Data")
    
    st.write("Upload a CSV file with product price data.")
    st.write("Required columns: product_id, product_name, our_price, competitor_name, competitor_price, last_updated")
    
    # Add two columns for the upload and sample data buttons
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload Your Own Data")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            # try to read the file
            try:
                df = pd.read_csv(uploaded_file)
                
                # check for required columns
                required_columns = ['product_id', 'product_name', 'our_price', 'competitor_name', 'competitor_price', 'last_updated']
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    st.error(f"Missing required columns: {', '.join(missing_columns)}")
                    return
                
                # basic validation
                if (df['our_price'] < 0).any() or (df['competitor_price'] < 0).any():
                    st.error("Negative prices are not allowed.")
                    return
                
                # preview the data
                st.write("Data Preview:")
                st.dataframe(df.head())
                
                # save button
                if st.button("Save Uploaded Data"):
                    success, message = db.save_data_to_db(df)
                    
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    
    # Add a section for sample data
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    with col2:
        st.subheader("Try Sample Data")
        st.write("No CSV file? Use our sample dataset with 100 products:")
        
        # Create a container for the sample data
        sample_container = st.container()
        
        # Load sample button
        load_sample = st.button("Preview Sample Data")
        
        # Variable to track if sample data is loaded
        sample_data_loaded = False
        
        if load_sample:
            try:
                sample_path = os.path.join(os.getcwd(), 'sample_data', 'sample_products.csv')
                
                if os.path.exists(sample_path):
                    sample_df = pd.read_csv(sample_path)
                    
                    with sample_container:
                        st.write(f"Sample Data Preview ({len(sample_df)} products):")
                        st.dataframe(sample_df.head(10))
                        sample_data_loaded = True
                        
                        # We'll use a session state to keep track of the sample data
                        # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
                        if 'sample_data' not in st.session_state:
                            st.session_state.sample_data = sample_df
                else:
                    st.error("Sample data file not found. Please check the 'sample_data' directory.")
            except Exception as e:
                st.error(f"Error loading sample data: {str(e)}")
        
        # Separate button to save sample data
        if 'sample_data' in st.session_state:
            if st.button("Save Sample Data to Database"):
                success, message = db.save_data_to_db(st.session_state.sample_data)
                
                if success:
                    st.success(message)
                else:
                    st.error(message)

    # Add a section to delete the database
    st.subheader("Database Management")
    st.warning("Warning: Deleting the database will remove all stored product data.")
    if st.button("Delete Existing Database"):
        success, message = db.delete_database()
        if success:
            st.success(message)
            # also clear the sample data from session state
            if 'sample_data' in st.session_state:
                del st.session_state.sample_data
        else:
            st.error(message)

def search_filter_page():
    st.title("Search & Filter Products")
    
    # get all data first
    all_data = db.get_all_products()
    
    if all_data.empty:
        st.warning("No data available. Please upload data first.")
        return
    
    # add price comparison info
    all_data = price_compare.compare_prices(all_data)
    
    # create tabs for search and filters
    tab1, tab2 = st.tabs(["Search", "Quick Filters"])
    
    with tab1:
        # search by product or competitor name
        search_term = st.text_input("Search by product or competitor name")
        
        if search_term:
            # could use the db search function, but since we already have all data
            # with the status info, we can just filter it here
            # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
            filtered_data = all_data[
                all_data['product_name'].str.contains(search_term, case=False) | 
                all_data['competitor_name'].str.contains(search_term, case=False)
            ]
            
            if filtered_data.empty:
                st.info(f"No results found for '{search_term}'")
            else:
                st.write(f"Found {len(filtered_data)} results:")
                display_filtered_data(filtered_data)
    
    with tab2:
        # quick filter buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Show Only Cheaper Competitors"):
                cheaper_competitors = all_data[all_data['status'] == 'alert']
                if cheaper_competitors.empty:
                    st.info("No products where competitors are cheaper")
                else:
                    st.write(f"Found {len(cheaper_competitors)} products where competitors are cheaper:")
                    display_filtered_data(cheaper_competitors)
        
        with col2:
            if st.button("Show Only Where We Are Cheaper"):
                we_are_cheaper = all_data[all_data['status'] == 'good']
                if we_are_cheaper.empty:
                    st.info("No products where we are cheaper")
                else:
                    st.write(f"Found {len(we_are_cheaper)} products where we are cheaper:")
                    display_filtered_data(we_are_cheaper)

def display_filtered_data(df):
    # prepare for display
    display_df = df.copy()
    
    # rename columns for better display
    display_df = display_df.rename(columns={
        'product_id': 'Product ID',
        'product_name': 'Product Name',
        'our_price': 'Our Price',
        'competitor_name': 'Competitor',
        'competitor_price': 'Their Price',
        'last_updated': 'Last Updated',
        'message': 'Status'
    })
    
    # format currency values
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    display_df['Our Price'] = display_df['Our Price'].apply(lambda x: f"${x:.2f}")
    display_df['Their Price'] = display_df['Their Price'].apply(lambda x: f"${x:.2f}")
    
    # drop the status column as we'll use it for styling
    display_df = display_df.drop(columns=['status'])
    
    # apply styling based on status
    def apply_row_styling(row):
        if row.name in df[df['status'] == 'alert'].index:
            return ['background-color: rgba(255, 0, 0, 0.1)'] * len(row)
        elif row.name in df[df['status'] == 'good'].index:
            return ['background-color: rgba(0, 255, 0, 0.1)'] * len(row)
        return [''] * len(row)
    
    # display with styling
    st.dataframe(display_df.style.apply(apply_row_styling, axis=1), use_container_width=True)

def alert_settings_page():
    st.title("Email Alert Settings")
    
    # get cheaper competitor data for alert preview
    all_data = db.get_all_products()
    
    if all_data.empty:
        st.warning("No data available. Please upload data first.")
        return
    
    all_data = price_compare.compare_prices(all_data)
    alert_data = all_data[all_data['status'] == 'alert']
    
    # email settings form
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    st.subheader("Configure Email Alerts")
    
    # Check if email credentials are configured
    if not email_alert.SMTP_USERNAME or not email_alert.SMTP_PASSWORD:
        st.warning(
            "Email alerts are not configured. To enable email alerts, create a `.env` file in the project root "
            "and add your SMTP credentials. See the `.env.example` file for the required format."
        )
    
    email = st.text_input("Your Email Address", email_alert.DEFAULT_RECIPIENT)
    
    # SMTP settings would be in a proper form here
    # but for demo purposes keeping it simple
    if st.button("Test Alert Email"):
        if alert_data.empty:
            st.warning("No price alerts to send. Add data with competitor prices lower than ours first.")
        else:
            success, message = email_alert.send_price_alert(alert_data, email)
            
            if success:
                st.success(message)
            else:
                st.warning(message)
    
    # alert preview
    st.subheader("Current Price Alerts")
    
    if alert_data.empty:
        st.info("No current price alerts!")
    else:
        st.write(f"{len(alert_data)} products have competitor prices lower than ours:")
        
        # prepare for display
        display_df = alert_data.copy()
        
        # calculate price difference and percentage
        display_df['price_diff'] = display_df['our_price'] - display_df['competitor_price']
        display_df['percentage'] = (display_df['price_diff'] / display_df['our_price']) * 100
        
        # select and rename columns
        display_df = display_df[[
            'product_name', 'our_price', 'competitor_name', 
            'competitor_price', 'price_diff', 'percentage'
        ]]
        
        display_df = display_df.rename(columns={
            'product_name': 'Product',
            'our_price': 'Our Price',
            'competitor_name': 'Competitor',
            'competitor_price': 'Their Price',
            'price_diff': 'Difference',
            'percentage': 'Difference %'
        })
        
        # format values
        # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
        display_df['Our Price'] = display_df['Our Price'].apply(lambda x: f"${x:.2f}")
        display_df['Their Price'] = display_df['Their Price'].apply(lambda x: f"${x:.2f}")
        display_df['Difference'] = display_df['Difference'].apply(lambda x: f"${x:.2f}")
        display_df['Difference %'] = display_df['Difference %'].apply(lambda x: f"{x:.1f}%")
        
        # sort by largest difference
        display_df = display_df.sort_values('Difference', ascending=False)
        
        # display table
        st.dataframe(display_df, use_container_width=True)

if __name__ == "__main__":
    main()