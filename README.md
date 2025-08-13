# E-commerce Price Monitoring & Alert Dashboard

A powerful Streamlit-based dashboard for tracking and comparing product prices across competitors, providing visual insights, and sending alerts when competitors drop their prices below yours.

![Dashboard Preview](https://via.placeholder.com/1200x600?text=E-commerce+Price+Monitoring+Dashboard)

## Project Overview

This dashboard helps e-commerce businesses stay competitive by tracking competitor pricing in real-time. The system analyzes price differences, highlights opportunities for price adjustments, and sends alerts when competitors undercut your prices.

## Architecture

### System Architecture

```
┌─────────────────┐     ┌───────────────┐     ┌───────────────────┐
│                 │     │               │     │                   │
│  Streamlit UI   │◄────┤  Application  │◄────┤  SQLite Database  │
│  (app.py)       │     │  Logic        │     │  (data/price_     │
│                 │     │               │     │   monitor.db)     │
└────────┬────────┘     └───────┬───────┘     └───────────────────┘
         │                      │
         │                      │
         ▼                      ▼
┌─────────────────┐     ┌───────────────┐
│                 │     │               │
│  Data Upload    │     │  Email Alert  │
│  & Processing   │     │  System       │
│                 │     │               │
└─────────────────┘     └───────────────┘
```

### Data Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │     │             │
│  CSV Data   │────►│  Database   │────►│  Price      │────►│  Dashboard  │
│  Upload     │     │  Storage    │     │  Analysis   │     │  Display    │
│             │     │             │     │             │     │             │
└─────────────┘     └─────────────┘     └──────┬──────┘     └─────────────┘
                                               │
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │             │
                                        │  Alert      │
                                        │  System     │
                                        │             │
                                        └─────────────┘
```

### Component Breakdown

| Component | File | Description |
|-----------|------|-------------|
| Web Interface | `app.py` | Streamlit application with dashboard, upload, comparison, and alert pages |
| Database Layer | `db.py` | SQLite database operations for storing and retrieving product data |
| Price Comparison | `price_compare.py` | Logic for comparing prices and calculating statistics |
| Alert System | `email_alert.py` | Email notifications for price drops |

## Features

- **Interactive Dashboard**: Visual representation of price comparisons and statistics
- **Data Management**: Upload CSV files or use sample data to populate the system
- **Price Comparison**: Automatically compare your prices with competitors
- **Search & Filter**: Find specific products or focus on price drop alerts
- **Email Alerts**: Get notified when competitors lower their prices
- **Database Management**: Add, view, and clear data as needed

## Usage Guide

### 1. Navigation

The dashboard consists of several pages accessible from the sidebar:

- **Home**: Overview with key statistics and charts
- **Price Comparison Table**: Detailed product-by-product price comparison
- **Upload Data**: Import your product and competitor data
- **Search & Filter**: Find specific products or apply filters
- **Alert Settings**: Configure email notifications for price drops

### 2. Data Upload

You have two options for adding data:

1. **Upload Your CSV**: Prepare a CSV file with these columns:
   - `product_id`: Unique identifier for each product
   - `product_name`: Name of the product
   - `our_price`: Your selling price
   - `competitor_name`: Name of the competitor
   - `competitor_price`: Competitor's price
   - `last_updated`: Date of the price check (YYYY-MM-DD format)

2. **Use Sample Data**: Click the "Load Sample Data" button to populate the dashboard with 100 sample products for testing.

### 3. Dashboard Overview

The Home page displays:
- Total products monitored
- Number of price drop alerts
- Products where your prices are more competitive
- Average price advantages
- Visual breakdowns of price comparisons
- Top alerts requiring attention

### 4. Price Comparison

The Price Comparison Table shows all products with color coding:
- **Red**: Competitor's price is lower (alert)
- **Green**: Your price is lower (good)
- **Gray**: Identical prices (neutral)

### 5. Search & Filter

Use the Search & Filter page to:
- Search by product name or competitor name
- Filter to show only products with specific price comparison statuses
- Sort results by price difference or percentage

### 6. Setting Up Alerts

1. Navigate to the Alert Settings page
2. Configure your email address for notifications
3. Test the email configuration
4. Set up alert frequency preferences

## License

This project is licensed under the MIT License - see the LICENSE file for details.
