import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


st.write("""
# Analyze product sales dataset
""")   #>streamlit run ASM_ADV.py
df_data=pd.read_csv('Sales_v1.csv')
df_data.info()
df_data['Gross Sales'] = df_data['Gross Sales'].replace('[\$,]', '', regex=True)
df_data['Gross Sales'] = df_data['Gross Sales'].replace('[\.]', '', regex=True).astype(float)
df_data['Units Sold'] = pd.to_numeric(df_data['Units Sold'].str.replace(',', '.'))
st.write(df_data)

def calculate_avg_gross_sales(df_data):
    avg_gross_sales = df_data.groupby('Country')['Gross Sales'].mean().sort_values().reset_index()
    plt.figure(figsize=(10, 6))
    plt.bar(avg_gross_sales['Country'], avg_gross_sales['Gross Sales'], color='skyblue')
    plt.xlabel('Country')
    plt.ylabel('Average Gross Sales')
    plt.title('Average Gross Sales by Country')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('avg_gross_sales3.png')
    return avg_gross_sales
avg_gross_sales = calculate_avg_gross_sales(df_data)
print(avg_gross_sales)
st.bar_chart(avg_gross_sales, x = "Country", y ="Gross Sales")

def count_product_sold_sp(df_data):
    count_table = df_data.groupby(['Product', 'Sale Price']).size().unstack(fill_value=0)
    count_table.columns = [f"{col}$" for col in count_table.columns]
    count_table.reset_index(inplace=True)
    
    return count_table
result = count_product_sold_sp(df_data)

fig = go.Figure()
for col in result.columns[1:]:
    fig.add_trace(go.Bar(
        x=result['Product'],
        y=result[col],
        name=col
    ))
fig.update_layout(
    barmode='group',
    title='Products Sold at Different Sale Prices',
    xaxis_title='Product',
    yaxis_title='Count',
    legend_title='Sale Price'
)

st.plotly_chart(fig)


def calculate_sum_unit_sold(df_data):
    calculate_sum_unit_sold = df_data.groupby('Sale Price')['Units Sold'].sum()
    return calculate_sum_unit_sold

sum_unit_sold = calculate_sum_unit_sold(df_data)
print(sum_unit_sold)
fig = px.pie(values=sum_unit_sold, names=sum_unit_sold.index, title='Sum Unit Sold by Sale Price')
st.plotly_chart(fig)

def calculate_sum_product_sold(df_data):
    sum_product_sold = df_data.groupby('Product')['Units Sold'].sum().sort_values()
    return sum_product_sold

print(calculate_sum_product_sold(df_data))
sum_product_sold = calculate_sum_product_sold(df_data)
fig = px.pie(values=sum_product_sold, names=sum_product_sold.index, title='Sum Unit Sold by Product')
st.plotly_chart(fig)


def gross_sales_q4_2014vs2013(df_data):
    df_data_quarter = df_data[df_data['Month Name'].isin(['September','October', 'November', 'December'])]
    df_data_quarter.sort_values(by='Month Name', ascending=True, inplace=True)
    pivot_table = df_data_quarter.pivot_table(index='Month Name', columns='Year', values='Gross Sales', aggfunc='sum')
    return pivot_table
gross_sales_data = gross_sales_q4_2014vs2013(df_data)

gross_sales_data = gross_sales_data.reset_index()
print(gross_sales_data)
fig = px.line(gross_sales_data, x='Month Name', y=[2013, 2014], title='Gross Sales Q4: 2014 vs 2013')
fig.update_layout(xaxis_title='Month', yaxis_title='Sum Gross Sales')

fig.write_image('gross_sales_q4_2014vs2013.png') 
st.plotly_chart(fig)


