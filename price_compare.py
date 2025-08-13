import pandas as pd
import numpy as np

def compare_prices(df):
    """
    Compare our prices with competitor prices and add status and message columns
    """
    if df.empty:
        return df
    
    # making a copy to avoid warnings
    result_df = df.copy()
    
    # add status column for styling
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    result_df['status'] = ''
    result_df['message'] = ''
    
    # Let's check each product one by one and see how our prices stack up
    # This is like being a price detective! 🕵️‍♂️
    for idx, row in result_df.iterrows():
        my_price = row['our_price']
        comp_price = row['competitor_price']
        
        # Figure out who's cheaper and by how much
        if comp_price < my_price:
            # Oh no! They're beating our price - this is bad news!
            price_diff = my_price - comp_price
            percentage = (price_diff / my_price) * 100
            result_df.at[idx, 'status'] = 'alert'
            result_df.at[idx, 'message'] = f"Price Drop Alert (${price_diff:.2f} / {percentage:.1f}% cheaper)"
        elif my_price < comp_price:
            # Woohoo! We're cheaper than them - customers will love us!
            price_diff = comp_price - my_price
            percentage = (price_diff / comp_price) * 100
            result_df.at[idx, 'status'] = 'good'
            result_df.at[idx, 'message'] = f"We are cheaper (${price_diff:.2f} / {percentage:.1f}% cheaper)"
        else:
            # Exactly the same price - weird coincidence!
            result_df.at[idx, 'status'] = 'neutral'
            result_df.at[idx, 'message'] = "Prices are identical"
    
    return result_df

def get_price_change_stats(df):
    """
    Calculate stats about price differences for dashboard
    """
    if df.empty:
        return {
            'total_products': 0,
            'competitors_cheaper': 0,
            'we_are_cheaper': 0,
            'identical_prices': 0,
            'avg_competitor_advantage': 0,
            'avg_our_advantage': 0
        }
    
    # count products where competitor is cheaper (status = alert)
    competitors_cheaper = len(df[df['status'] == 'alert'])
    
    # count products where we are cheaper (status = good)
    we_are_cheaper = len(df[df['status'] == 'good'])
    
    # count products with identical prices (status = neutral)
    identical_prices = len(df[df['status'] == 'neutral'])
    
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    # might be useful to know average price differences
    comp_cheaper_df = df[df['status'] == 'alert']
    we_cheaper_df = df[df['status'] == 'good']
    
    avg_competitor_advantage = 0
    if not comp_cheaper_df.empty:
        avg_competitor_advantage = (comp_cheaper_df['our_price'] - comp_cheaper_df['competitor_price']).mean()
    
    avg_our_advantage = 0
    if not we_cheaper_df.empty:
        avg_our_advantage = (we_cheaper_df['competitor_price'] - we_cheaper_df['our_price']).mean()
    
    return {
        'total_products': len(df),
        'competitors_cheaper': competitors_cheaper,
        'we_are_cheaper': we_are_cheaper,
        'identical_prices': identical_prices,
        'avg_competitor_advantage': round(avg_competitor_advantage, 2),
        'avg_our_advantage': round(avg_our_advantage, 2)
    }