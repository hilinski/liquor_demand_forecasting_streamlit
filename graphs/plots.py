import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def create_category_sales_chart(df):
    # Group by category_name and sum the bottles_sold
    grouped_data = df.groupby('category_name')['bottles_sold'].sum().reset_index()
    
    # Create the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(grouped_data['category_name'], grouped_data['bottles_sold'])
    
    # Customize the chart
    ax.set_xlabel('Category')
    ax.set_ylabel('Bottles Sold')
    ax.set_title('Total Bottles Sold by Category')
    
    # Add value labels on top of each bar
    for i, v in enumerate(grouped_data['bottles_sold']):
        ax.text(i, v, str(v), ha='center', va='bottom')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    return fig, grouped_data


def moth_category_name(df):
    df['date_week'] = pd.to_datetime(df['date_week'])
    df['month_year'] = df['date_week'].dt.to_period('M').astype(str)

    # Group data by month-year and category_name
    grouped_data = df.groupby(['month_year', 'category_name'])['bottles_sold'].sum().unstack()

    # Create the bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    grouped_data.plot(kind='bar', ax=ax)

    # Customize the chart
    plt.xlabel('Month-Year')
    plt.ylabel('Bottles Sold')
    plt.legend(title='Category')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig, grouped_data


def create_weekly_sales_chart(df):
    # Convert date_week to datetime
    df['date_week'] = pd.to_datetime(df['date_week'])
    
    # Group by date_week and is_pred, sum bottles_sold
    weekly_sales = df.groupby(['date_week', 'is_pred'])['bottles_sold'].sum().reset_index()
    
    # Sort by date
    weekly_sales = weekly_sales.sort_values('date_week')
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(15, 8))
    
    # Plot actual data
    actual_data = weekly_sales[weekly_sales['is_pred'] == False]
    sns.lineplot(data=actual_data, x='date_week', y='bottles_sold', ax=ax, 
                 marker='o', markersize=6, label='Actual', color='blue')
    
    # Plot predicted data
    predicted_data = weekly_sales[weekly_sales['is_pred'] == True]
    sns.lineplot(data=predicted_data, x='date_week', y='bottles_sold', ax=ax, 
                 marker='o', markersize=6, label='Predicted', color='red', linestyle='--')
    
    # Customize the plot
    plt.title('Weekly Bottles Sold (Actual vs Predicted)', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Bottles Sold', fontsize=12)
    
    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right')
    
    # Add gridlines
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Add legend
    plt.legend(fontsize=10)
    
    # Tight layout to prevent clipping of labels
    plt.tight_layout()
    
    return fig, weekly_sales
