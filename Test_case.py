import pandas as pd
import pytest
from ASM_ADV import (
    calculate_avg_gross_sales,
    count_product_sold_sp,
    calculate_sum_unit_sold,
    calculate_sum_product_sold,
    gross_sales_q4_2014vs2013
)
@pytest.fixture
def sample_data():
    df_data = pd.read_csv('Sales_v1.csv')
    df_data['Gross Sales'] = df_data['Gross Sales'].replace('[\$,]', '', regex=True)
    df_data['Gross Sales'] = df_data['Gross Sales'].replace('[\.]', '', regex=True).astype(float)
    df_data['Units Sold'] = pd.to_numeric(df_data['Units Sold'].str.replace(',', '.'))
    df_data['Sale Price'] = pd.to_numeric(df_data['Sale Price'].str.replace('$', '').str.replace(',', ''))
    return df_data

def test_calculate_avg_gross_sales(sample_data):
    result = calculate_avg_gross_sales(sample_data)
    expected = pd.DataFrame({
        'Country': ['Mexico', 'Germany', 'Canada', 'USA', 'France'],
        'Gross Sales': [162335.250000, 211917.178571, 221330.578571, 228222.364286, 245498.742857]
    })
    pd.testing.assert_frame_equal(result, expected)

def test_count_product_sold_sp(sample_data):
    result = count_product_sold_sp(sample_data)
    expected = pd.DataFrame({
        'Product': ['Amarilla', 'Carretera', 'Montana', 'Paseo', 'VTT', 'Velo'],
        '7$': [12, 12, 18, 30, 14, 14], 
        '12$': [16, 18, 12, 26, 14, 14],  
        '15$': [12, 12, 12, 36, 14, 14],
        '20$': [12, 12, 12, 32, 14, 18],  
        '125$': [12, 15, 12, 26, 14, 21],   
        '300$': [12, 12, 15, 26, 21, 14], 
        '350$': [18, 12, 12, 26, 18, 14]  
    })
    pd.testing.assert_frame_equal(result, expected)

def test_calculate_sum_unit_sold(sample_data):
    result = calculate_sum_unit_sold(sample_data)
    result.index.name = None
    result = result.astype(float)
    expected = pd.Series({
        7: 167304.5,
        12: 161263.5,
        15: 172178.0,
        20: 154385.5,
        125: 168552.0,
        300: 153139.0,
        350: 148983.5
    })

def test_calculate_sum_product_sold(sample_data):
    result = calculate_sum_product_sold(sample_data)
    result.index.name = None
    result = result.astype(float)
    result.name = None
    expected = pd.Series({
        'Carretera': 146846.0,
        'Montana': 154198.0,
        'Amarilla': 155315.0, 
        'Velo': 162424.5,
        'VTT': 168783.0,
        'Paseo': 338239.5
    })
    pd.testing.assert_series_equal(result, expected)

def test_gross_sales_q4_2014vs2013(sample_data):
    result = gross_sales_q4_2014vs2013(sample_data)
    result.columns = result.columns.astype(str)
    result.columns.name = None 
    expected = pd.DataFrame({
        'Month Name': ['December', 'November', 'October', 'September'],
        '2013': [5835025.0, 8167338.0, 9828688.0, 4729736.0], 
        '2014': [12508268.0, 5947910.0, 13313424.0, 6845317.0] 
    }).set_index('Month Name')
    pd.testing.assert_frame_equal(result, expected)

