import streamlit as st
import pandas as pd
import numpy as np

st.title('Widgets')

st.write('Sliders')
x = st.slider('x')
st.write(x, 'squared is', x*x)

st.write('Input')
st.text_input("Write your name", key="name")
st.session_state.name

st.write('Checkbox')

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns = ['a', 'b', 'c']
    )
    chart_data

df = pd.DataFrame({
    'first_column': [1, 2, 3, 4],
    'second_column': [10, 20, 30, 40]
})

option = st.selectbox(
    label = 'Which number do you like best?',
    options = df['first_column']
)

st.write('You selected: ', option)

add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

st.write('Column Layout')

left_column, right_column = st.columns(2)

left_column.button('Press me!')

with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin")
    )