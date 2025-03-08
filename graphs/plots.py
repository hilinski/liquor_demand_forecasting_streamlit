import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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


def create_weekly_sales_chart(sales_data: pd.DataFrame, start_year: int = 2020) -> tuple:
    # Check if required columns exist
    required_columns = ['date', 'is_pred', 'category_name', 'bottles_sold']
    if not all(col in sales_data.columns for col in required_columns):
        raise ValueError("Missing required columns in the DataFrame.")

    # Convert timestamp to datetime
    sales_data['date'] = pd.to_datetime(sales_data['date'], unit='ms')
    
    # Filter data by year
    sales_data = sales_data.query(f'date >= {start_year}')
    
    # Group by date, is_pred, and category_name, sum bottles_sold
    weekly_sales = sales_data.groupby(['date', 'is_pred', 'category_name'])['bottles_sold'].sum().reset_index()
    
    # Sort by date
    weekly_sales = weekly_sales.sort_values('date')
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(15, 8))
    
    # Plot data for each category
    categories = weekly_sales['category_name'].unique()
    for category in categories:
        category_data = weekly_sales[weekly_sales['category_name'] == category]
        
        # Plot actual data
        actual_data = category_data[category_data['is_pred'] == False]
        sns.lineplot(data=actual_data, x='date', y='bottles_sold', ax=ax, 
                     marker='o', markersize=6, label=f'{category} (Actual)')
        
        # Plot predicted data
        predicted_data = category_data[category_data['is_pred'] == True]
        sns.lineplot(data=predicted_data, x='date', y='bottles_sold', ax=ax, 
                     marker='o', markersize=6, label=f'{category} (Predicted)', linestyle='--')
    
    # Customize the plot
    plt.title('Weekly Bottles Sold by Category (Actual vs Predicted)', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Bottles Sold', fontsize=12)
    
    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right')
    
    # Add gridlines
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Add legend at the bottom
    plt.legend(fontsize=10, bbox_to_anchor=(0.5, -0.2), loc='center', ncol=len(categories))
    
    # Tight layout to prevent clipping of labels
    plt.tight_layout(rect=[0, 0.05, 1, 1])  # Adjust layout to fit the legend
    
    return fig, weekly_sales



def multiple_categories_chat(df, category_names):
    # Convert timestamp to datetime
    df['date'] = pd.to_datetime(df['date'], unit='ms')
    df = df.query('date >= 2020')  
    # Calculate the number of rows and columns for subplots
    n_categories = len(category_names)
    n_cols = 2
    n_rows = (n_categories + 1) // 2
    
    # Create the figure and subplots
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 10 * n_rows))
    axes = axes.flatten()  # Flatten the axes array for easier indexing
    
    weekly_sales_data = {}
    
    for idx, category_name in enumerate(category_names):
        # Filter data for the specified category
        df_category = df[df['category_name'] == category_name]
        
        # Group by date and is_pred, sum bottles_sold
        weekly_sales = df_category.groupby(['date', 'is_pred'])['bottles_sold'].sum().reset_index()
        
        # Sort by date
        weekly_sales = weekly_sales.sort_values('date')
        
        # Store the weekly sales data
        weekly_sales_data[category_name] = weekly_sales
        
        # Plot actual data
        actual_data = weekly_sales[weekly_sales['is_pred'] == False]
        sns.lineplot(data=actual_data, x='date', y='bottles_sold', ax=axes[idx], 
                     marker='o', markersize=6, label='Actual', color='blue')
        
        # Plot predicted data
        predicted_data = weekly_sales[weekly_sales['is_pred'] == True]
        sns.lineplot(data=predicted_data, x='date', y='bottles_sold', ax=axes[idx], 
                     marker='o', markersize=6, label='Predicted', color='red', linestyle='--')
        
        # Customize the subplot
        axes[idx].set_title(f'Weekly Bottles Sold for {category_name}', fontsize=14)
        axes[idx].set_xlabel('Date', fontsize=10)
        axes[idx].set_ylabel('Bottles Sold', fontsize=10)
        axes[idx].tick_params(axis='x', rotation=45)
        axes[idx].grid(True, linestyle='--', alpha=0.7)
        axes[idx].legend(fontsize=8, loc='best')
    
    # Remove any unused subplots
    for idx in range(n_categories, len(axes)):
        fig.delaxes(axes[idx])
    
    # Adjust layout and add main title
    plt.tight_layout()
    fig.suptitle('Weekly Bottles Sold by Category (Actual vs Predicted)', fontsize=20, y=1.02)
    
    return fig, weekly_sales_data
    
