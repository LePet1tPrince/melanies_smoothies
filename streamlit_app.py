# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie
    """
)


cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input('Name on Smoothie')
if name_on_order:
    st.write('The name on the smoothie will be: ', name_on_order)

st.divider()
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string = ''
    for el in ingredients_list:
        ingredients_string += el + ' '
        st.subheader(el + ' Nutrition Information')
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{el}")
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
        values('""" + ingredients_string + """','"""+name_on_order+ """')"""

    # st.write(my_insert_stmt)
    order_button = st.button('Submit Order')

    if order_button:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order, icon="✅")




