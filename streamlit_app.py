import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


def normalize_data(fruit_choice):
  fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
  #streamlit.text(fruityvice_response.json())
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

def getdata():
  my_cur = my_cnx.cursor()
  my_cur.execute("SELECT * from FRUIT_LOAD_LIST")
  my_data_row = my_cur.fetchall()
  return my_data_row

def insertdata(new_fruit):
  my_cur = my_cnx.cursor()
  my_cur.execute(f"insert into FRUIT_LOAD_LIST values(\'{new_fruit}\')")
  return "Record Added Successfully"
  
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header('🍌🥭 Fruityvice Fruit Advise 🥝🍇')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please provide a fruit")
  else:
    streamlit.write('The user entered ', fruit_choice)
    fruityvice_normalized = normalize_data(fruit_choice)
    streamlit.dataframe(fruityvice_normalized)
except URLError  as e :
  streamlit.error()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
if (streamlit.button('Click to List Fruit List')):
  my_data_row = getdata()
  streamlit.header("Fruit list contains:")
  streamlit.dataframe(my_data_row)

new_fruit = streamlit.text_input('What fruit would you like to add ?')  
if (streamlit.button('Add a Fruit')):
  result = insertdata(new_fruit)
  streamlit.text(result)

  
#add_fruit = streamlit.text_input('What Fruit would you like to add ?')
#my_cur.execute("SELECT * from FRUIT_LOAD_LIST where fruit_name ")
