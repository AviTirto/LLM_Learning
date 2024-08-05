import streamlit as st
import pandas as pd
import numpy as np

st.title('Test Stream Lit Project')

st.write("This is text")

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

st.write(df)

st.write("This is a static dataframe without using st.write() magic")

st.table(df)

st.write("This is streamlit's dataframe with styling using Styler")

df2 =  pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(df2.style.highlight_max(axis = 0))

st.write("Plotting a Line Chart!")

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns = ['a', 'b', 'c']
)

st.line_chart(chart_data)

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns = ['lat', 'lon']
)

st.map(map_data)

