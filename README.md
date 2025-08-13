# MarketPulse Monitor - E-commerce Price Monitoring Dashboard

MarketPulse Monitor is a powerful web-based dashboard built with Streamlit that helps e-commerce businesses track competitor pricing, compare with their own prices, and make data-driven pricing decisions.

![MarketPulse Monitor Dashboard](https://i.ibb.co/qnwP3jw/market-pulse-dashboard.png)

## 📊 Project Overview

In today's competitive e-commerce landscape, staying on top of competitor pricing is essential for maintaining market share and maximizing profits. MarketPulse Monitor provides a real-time view of how your prices compare to competitors, helping you identify opportunities and threats.

## 🏗️ Architecture

The application follows a modular architecture designed for maintainability and extensibility:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  User Interface │────▶│  Business Logic │────▶│  Data Access    │
│  (Streamlit)    │     │  (Processing)   │     │  Layer (SQLite) │
│                 │◀────│                 │◀────│                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  UI Components  │     │  Price Analysis │     │  Database       │
│  (app.py)       │     │  (price_compare)│     │  Operations     │
│                 │     │                 │     │  (db.py)        │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         app.py (Main Application)               │
├─────────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Dashboard   │ │ Price       │ │ Data        │ │ Search &    │ │
│ │ Home Page   │ │ Comparison  │ │ Upload      │ │ Filter      │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  price_compare  │     │     db.py       │     │  email_alert    │
│  (Analysis)     │     │  (Data Access)  │     │  (Notification) │
│                 │     │                 │     │                 │
└─────────────────┘     └───────┬─────────┘     └─────────────────┘
                                │
                                ▼
                        ┌─────────────────┐
                        │                 │
                        │  SQLite DB      │
                        │  (Storage)      │
                        │                 │
                        └─────────────────┘
```

### Data Flow Diagram

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│             │      │             │      │             │
│  CSV File   │─────▶│  Data       │─────▶│  Database   │
│  Upload     │      │  Validation │      │  Storage    │
│             │      │             │      │             │
└─────────────┘      └─────────────┘      └─────────────┘
                                                 │
                                                 ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│             │      │             │      │             │
│  Dashboard  │◀─────│  Data       │◀─────│  Price      │
│  Display    │      │  Retrieval  │      │  Analysis   │
│             │      │             │      │             │
└─────────────┘      └─────────────┘      └─────────────┘
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Database**: SQLite
- **Data Format**: CSV

## 📱 Features

- **Interactive Dashboard**: Visual overview of price comparisons
- **Data Upload**: Import pricing data via CSV files
- **Sample Data**: Test with pre-configured sample data
- **Price Comparison**: Automatically analyze price differences
- **Search & Filter**: Find specific products or competitors
- **Database Management**: Reset database when needed

## 📖 Usage Guide

### Dashboard Overview

The home page dashboard provides a comprehensive overview of your price comparison data:

1. **Key Metrics**: See at a glance how many products are priced competitively
2. **Price Comparison Charts**: Visual representation of price differences
3. **Last Update**: Timestamp of the most recent data update

### Adding Product Data

There are two ways to add data to the system:

1. **Upload Your Own CSV**:
   - Navigate to the "Upload Data" page
   - Prepare a CSV with columns: product_id, product_name, our_price, competitor_name, competitor_price, last_updated
   - Click "Upload CSV" and select your file

2. **Use Sample Data**:
   - Navigate to the "Upload Data" page
   - Click "Load Sample Data" to populate the database with 100 sample products

### Comparing Prices

The "Price Comparison Table" page displays all products with visual indicators:

- **Red Background**: Competitor is cheaper (potential threat)
- **Green Background**: Your price is lower (competitive advantage)
- **No Highlight**: Identical pricing (parity)

### Searching Products

To find specific products:

1. Navigate to the "Search & Filter" page
2. Enter a product name or competitor in the search box
3. Use the filter buttons to show only products where competitors are cheaper or where you have a price advantage

### Managing the Database

If you need to start fresh:

1. Navigate to the "Upload Data" page
2. In the "Database Management" section, use the "Delete Database" button
3. Confirm your action (this will permanently remove all product data)

## 🚀 Deployment on Streamlit Cloud

To deploy this project on Streamlit Cloud:

1. Fork this repository to your GitHub account
2. Log in to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app" and select your forked repository
4. Set the main file path to `app.py`
5. Deploy your app

The application will be publicly accessible with an automatic HTTPS certificate.

## 🔧 Project Structure

```
├── app.py               # Main Streamlit application
├── db.py                # Database operations
├── price_compare.py     # Price comparison logic
├── email_alert.py       # Alert notification system (coming soon)
├── requirements.txt     # Python dependencies
├── .gitignore           # Git ignore file
├── README.md            # Project documentation
└── data/                # Database storage directory
    └── price_monitor.db # SQLite database
```

## 🤝 Contributing

Contributions are welcome! Feel free to submit pull requests with improvements or new features.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.