import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Load and preprocess data
df_data = pd.read_csv('Sales_v1.csv')
df_data['Gross Sales'] = df_data['Gross Sales'].replace('[\$,]', '', regex=True)
df_data['Gross Sales'] = df_data['Gross Sales'].replace('[\.]', '', regex=True).astype(float)
df_data['Units Sold'] = pd.to_numeric(df_data['Units Sold'].str.replace(',', '.'))

# Function 1: Calculate average gross sales by country and save the bar chart
def calculate_avg_gross_sales(df_data):
    avg_gross_sales = df_data.groupby('Country')['Gross Sales'].mean().sort_values().reset_index()
    plt.figure(figsize=(10, 6))
    plt.bar(avg_gross_sales['Country'], avg_gross_sales['Gross Sales'], color='skyblue')
    plt.xlabel('Country')
    plt.ylabel('Average Gross Sales')
    plt.title('Average Gross Sales by Country')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('chart\ avg_gross_sales.png')
    return avg_gross_sales

# Function 2: Count products sold at different sale prices and save the bar chart
def count_product_sold_sp(df_data):
    count_table = df_data.groupby(['Product', 'Sale Price']).size().unstack(fill_value=0)
    count_table.columns = [f"{col}$" for col in count_table.columns]
    count_table.reset_index(inplace=True)

    fig = go.Figure()
    for col in count_table.columns[1:]:
        fig.add_trace(go.Bar(x=count_table['Product'], y=count_table[col], name=col))
    fig.update_layout(barmode='group', title='Products Sold at Different Sale Prices', xaxis_title='Product', yaxis_title='Count', legend_title='Sale Price')
    fig.write_image('chart\count_product_sold_sp.png')  # Save the plotly figure as an image

    return count_table

# Function 3: Calculate and save the pie chart of the sum of units sold by sale price
def calculate_sum_unit_sold(df_data):
    sum_unit_sold = df_data.groupby('Sale Price')['Units Sold'].sum()
    fig = px.pie(values=sum_unit_sold, names=sum_unit_sold.index, title='Sum Unit Sold by Sale Price')
    fig.write_image('chart\sum_unit_sold.png')  # Save the plotly figure as an image
    return sum_unit_sold

# Function 4: Calculate and save the pie chart of the sum of units sold by product
def calculate_sum_product_sold(df_data):
    sum_product_sold = df_data.groupby('Product')['Units Sold'].sum().sort_values()
    fig = px.pie(values=sum_product_sold, names=sum_product_sold.index, title='Sum Unit Sold by Product')
    fig.write_image('chart\sum_product_sold.png')  # Save the plotly figure as an image
    return sum_product_sold

# Function 5: Compare gross sales in Q4 2014 vs 2013 and save the line chart
def gross_sales_q4_2014vs2013(df_data):
    df_data_quarter = df_data[df_data['Month Name'].isin(['September','October', 'November', 'December'])]
    df_data_quarter.sort_values(by='Month Name', ascending=True, inplace=True)
    pivot_table = df_data_quarter.pivot_table(index='Month Name', columns='Year', values='Gross Sales', aggfunc='sum').reset_index()

    fig = px.line(pivot_table, x='Month Name', y=[2013, 2014], title='Gross Sales Q4: 2014 vs 2013')
    fig.update_layout(xaxis_title='Month', yaxis_title='Sum Gross Sales')
    fig.write_image('chart\gross_sales_q4_2014vs2013.png')  # Save the plotly figure as an image

    return pivot_table

# Call and generate charts
calculate_avg_gross_sales(df_data)
count_product_sold_sp(df_data)
calculate_sum_unit_sold(df_data)
calculate_sum_product_sold(df_data)
gross_sales_q4_2014vs2013(df_data)
