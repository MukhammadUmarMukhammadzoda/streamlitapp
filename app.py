import streamlit as st
import pandas as pd
from typing import List
import os



def create_price_dataframe(data: pd.DataFrame, brands: List[str]):
    """
    Creates ....

    :param data:
    :param brands:
    :return:
    """
    prices = []
    for brand in brands:
        total_price = data.loc[data['Make'] == brand].Invoice.sum()
        prices.append(total_price)

    data = {'Brand': brands, 'Money': prices}
    return pd.DataFrame(data)


def transform_prices(data: pd.DataFrame):
    """

    :param data:
    :return:
    """

    converted_prices = []
    for i in list(data.Invoice):
        if type(i) == str:
            i = i[1:-1]
            i = i.replace(',', '')
        i = int(i)
        converted_prices.append(i)
    data.Invoice = converted_prices
    return data


def find_most_expensive(data: pd.DataFrame):
    """

    :param data:
    :return:
    """

    most_expencive_car = data.loc[data['Invoice'] == data['Invoice'].max()]
    most_expencive_car.reset_index(inplace=True)
    return most_expencive_car


data = pd.read_csv(os.environ.get('DATA_PATH', 'data/cars.csv'))
data.dropna(inplace=True)
header = st.container()
dataset = st.container()
features = st.container()

with header:
    st.title('Streamlit Project on Cars dataset')

with dataset:
    st.header('Cars Dataset')
    st.write(data.head(15))
    st.text("Let`s analyze our dataset!")
    st.write(data.columns)
    st.write(data.describe())

with features:
    data = transform_prices(data)
    st.header("features I have created.")
    st.text("What kind of Car Type is popular and most sold in the World")
    st.write(data['Type'].value_counts())
    st.bar_chart(data['Type'].value_counts())
    st.text("The most expencive car in this dataframe is Porsche")
    st.write(find_most_expensive(data=data))
    st.text('The most car sold continent :')
    st.write(data['Origin'].value_counts())
    st.line_chart(data.Origin.value_counts())
    st.text("What kind of engine sizes we have")
    st.write(data['EngineSize'].unique())
    st.text("Which are the most favourable")
    st.write(data['EngineSize'].value_counts())
    st.area_chart(data['EngineSize'].value_counts())
    inp = st.text_input('Which data do you want to know', 'Origin')
    inp = inp.capitalize()
    try:
        st.write(data[inp].value_counts())
    except KeyError:
        st.text(f"Please input valid name between values below :")
        st.write(data.columns)
choose = st.slider('Select cars with it`s horsepower:', min_value=30, max_value=300, step=10)
selected = data.loc[data['Horsepower'] >= choose]
st.write(selected)
brands = list(data['Make'].unique())
brandselect = st.selectbox('Choose brands from DataFrame', brands)
select_brand = data.loc[data['Make'] == brandselect]
st.write(select_brand)
st.text(f'We have {len(select_brand)} of {brandselect} and earned {select_brand["Invoice"].sum()}$')
new_data = create_price_dataframe(data=data, brands=brands)
new_data.set_index('Brand', inplace=True)
st.write("The most profited company for selling cars")
filtered = new_data.nlargest(len(new_data), 'Money')
st.write(filtered)
st.bar_chart(new_data.Money)

