import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image



def process_main_page():
    show_main_page()
    process_side_bar_inputs()


def show_main_page():
    image = Image.open('data/house.jpg')
    image = image.resize((round(image.size[0] * 0.8), round(image.size[1] * 0.8)))

    st.set_page_config(
        layout="wide",
        initial_sidebar_state="auto",
        page_title="Недвижимость - StreamlitApp",
        page_icon=image,
    )
    st.write(
        """
        # Цена недвижимости 
        """
    )
    st.image(image)

def read_df(path="data/train.csv"):
    df = pd.read_csv(path)
    return df[['OverallCond', "Utilities", "Foundation", "YearBuilt", "MSZoning", "SalePrice"]]


def write_user_data(df):
    st.write("## Входные данные")
    st.write(df)


def write_result_data(df):
    st.write("## Результат")
    st.write(df)


def write_avg_price(value):
    st.write(f"## Средняя цена - {value:.2f}$")


def plot_hist(df):
    st.write("## Гистограмма распределения цены")
    fig = px.histogram(df, x="SalePrice", nbins=20)
    st.plotly_chart(fig, theme="streamlit")


def get_result(df, user_input_df):
    query = (df['OverallCond'] == user_input_df['OverallCond'].values[0]) & \
        (df['YearBuilt'] == user_input_df['YearBuilt'].values[0])

    if user_input_df['Utilities'].values[0] != "*":
        query = query & (df['Utilities'] == user_input_df['Utilities'].values[0])
    if user_input_df['Foundation'].values[0] != "*":
        query = query & (df['Foundation'] == user_input_df['Foundation'].values[0])
    if user_input_df['MSZoning'].values[0] != "*":
        query = query & (df['MSZoning'] == user_input_df['MSZoning'].values[0])
    return df.loc[query]
                       

def process_side_bar_inputs():
    st.sidebar.header('Заданные пользователем параметры')
    user_input_df = sidebar_input_features()
    write_user_data(user_input_df)

    df = read_df()
    df_result = get_result(df, user_input_df)
    
    meanPrice = df_result["SalePrice"].mean() if df_result.size > 0 else 0.0
    write_result_data(df_result)
    if meanPrice:
        write_avg_price(meanPrice)
        plot_hist(df_result["SalePrice"])


def sidebar_input_features():
    # 1) property_condition
    property_condition = st.sidebar.slider("Общее состояние", min_value=1, max_value=10, value=5,
                            step=1)
    # 2) utilities
    utilities = st.sidebar.selectbox("Коммуникации", 
                                     ("Неважно",
                                      "Все",
                                      "Электричество, газ, вода",
                                      "Электричество, газ",
                                      "Только электричество")
                                    )
    utilities_mapping = {
        "Неважно": "*",
        "Все" : "AllPub",
        "Электричество, газ, вода": "NoSewr",
        "Электричество, газ": "NoSeWa",
        "Только электричество": "ELO"
    }
    # 3) Type of foundation
    foundation =  st.sidebar.selectbox("Материал конструкции", 
                                       ("Неважно",
                                        "Кирпич и Плитка",
                                        "Шлакоблок",
                                        "Заливной бетон",
                                        "Плита",
                                        "Камень",
                                        "Дерево")
                                       )
    foundation_mapping = {
        "Неважно": "*",
        "Кирпич и Плитка": "BrkTil",
        "Шлакоблок": "CBlock",
        "Заливной бетон": "PConc",
        "Плита": "Slab",
        "Камень": "Stone",
        "Дерево": "Wood"
    }
    # 4) Year Build
    year_built = st.sidebar.slider("Год постройки", min_value=1900, max_value=2010, value=2006,
                            step=1)

    # 5) 
    zone = st.sidebar.selectbox("Тип недвижимости",
                                ("Неважно",
                                 "Жилье сельско хозяйственной зоны",
                                 "Тороговая недвижимость",
                                 "Жилье на воде (хаусбот)",
                                 "Жилье промышленной зоны",
                                 "Жилье высокой плотности", 
                                 "Жилье низкой плотности",
                                 "Жилье низкой плотности рядом с парком",
                                 "Жилье средней плотности"))
    zone_mapping = {
        "Неважно": "*",
        "Жилье сельско хозяйственной зоны": "A",
        "Тороговая недвижимость": "C",
        "Жилье на воде (хаусбот)": "FV",
        "Жилье промышленной зоны": "I",
        "Жилье высокой плотности": "RH",
        "Жилье низкой плотности": "RL",
        "Жилье низкой плотности рядом с парком": "RP",
        "Жилье средней плотности": "RM"
    }

    data = {
        "OverallCond": property_condition,
        "Utilities": utilities_mapping[utilities],
        "Foundation": foundation_mapping[foundation],
        "YearBuilt": year_built,
        "MSZoning": zone_mapping[zone]
    }

    df = pd.DataFrame(data, index=[0])

    return df


if __name__ == "__main__":
    process_main_page()
