# ⚠️ PROTECTED CODE - DO NOT COPY ⚠️

This is a personal project by Meet Jain. This repository is publicly visible for demonstration purposes only.

Author: Meet Jain
- This project is protected. Do not copy, fork, or reuse without permission.
- Unauthorized use is strictly prohibited. Only the official deployment is allowed to run.

## Legal Protection
This project is protected by copyright law and includes proprietary security measures. Unauthorized use or attempts to circumvent security measures may result in legal consequences.

## Contact
For any inquiries about this project please contact: meetofficialhere@gmail.com

# MarketPulse Monitor - E-commerce Price Monitoring Dashboard

MarketPulse Monitor is a powerful web-based dashboard built with Streamlit that helps e-commerce businesses track competitor pricing, compare with their own prices, and make data-driven pricing decisions.

## Project Overview

In today's competitive e-commerce landscape, staying on top of competitor pricing is essential for maintaining market share and maximizing profits. MarketPulse Monitor provides a real-time view of how your prices compare to competitors, helping you identify opportunities and threats.

## Architecture

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

## Technology Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Database**: SQLite
- **Data Format**: CSV

## Features

- **Interactive Dashboard**: Visual overview of price comparisons
- **Data Upload**: Import pricing data via CSV files
- **Sample Data**: Test with pre-configured sample data
- **Price Comparison**: Automatically analyze price differences
- **Search & Filter**: Find specific products or competitors
- **Database Management**: Reset database when needed

## Usage Guide

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


## Project Structure

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

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Connect with me through the following platforms:

<!-- <p align="left">
<a href="https://www.linkedin.com/in/meet-jain-413015265/" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="https://www.linkedin.com/in/meet-jain-413015265/" height="35" width="45" /></a>
<a href="https://discordapp.com/users/meetofficial" target="blank"><img align="center" src="https://github.com/Meetjain1/Meetjain1/assets/133582566/098a209a-a1d2-4350-9331-8f90203cc34d" alt="https://discordapp.com/users/meetofficial" height="45" width="45" /></a>
<hr> -->
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/meet-jain-413015265/)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=flat&logo=twitter&logoColor=white)](https://twitter.com/Meetjain_100)

### Social Media and Platforms
[![Discord](https://img.shields.io/badge/Discord-7289DA?style=flat&logo=discord&logoColor=white)](https://discordapp.com/users/meetofficial)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=flat&logo=instagram&logoColor=white)](https://www.instagram.com/m.jain_17/)
[![Stack Overflow](https://img.shields.io/badge/Stack%20Overflow-FE7A16?style=flat&logo=stackoverflow&logoColor=white)](https://stackoverflow.com/users/21919635/meet-jain)
[![Medium](https://img.shields.io/badge/Medium-12100E?style=flat&logo=medium&logoColor=white)](https://medium.com/@meetofficialhere)
[![Hashnode](https://img.shields.io/badge/Hashnode-2962FF?style=flat&logo=hashnode&logoColor=white)](https://hashnode.com/@meetofficial)


## Support Me

<h3>If you like my work, you can support me by buying me a coffee Thanks! </h3>

[![Buy Me A Coffee](https://img.shields.io/badge/-Buy%20Me%20A%20Coffee-orange?style=flat-square&logo=buymeacoffee)](https://buymeacoffee.com/meetjain)
