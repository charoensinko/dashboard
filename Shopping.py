import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.figure_factory as ff
import numpy as np

st.set_page_config(page_title="Shopping EDA", page_icon=":rainbow", layout="wide")

st.title(" :rainbow: Shopping EDA")
st.markdown('<style>div.block-container{padding-top:1rem}</style>', unsafe_allow_html=True)

# File upload
# fl = st.file_uploader(" :file_folder: Upload File", type=(["csv", "xlsx"," xls"]))
# if fl is not None:
#     filename = fl.name
#     # st.write(filename)
#     ext = filename.split('.')[-1]
#     if ext == "csv":
#         df = pd.read_csv(filename)
#     elif (ext == "xlsx") or (ext == "xls"):
#         df = pd.read_excel(filename)
#     else:
#         st.write("Please select CSV or Excel file.")
# else:
#     df = pd.read_csv("shopping_trends.csv")

df = pd.read_csv("shopping_trends.csv")

# Sidebar selector
st.sidebar.header("Select your filter: ")
# Category selector
category = st.sidebar.multiselect("Select your Category", df["Category"].unique())
if not category:
    df2 = df.copy()
else:
    df2 = df[df["Category"].isin(category)]

# Season selector
season = st.sidebar.multiselect("Select your Season", df2["Season"].unique())
if not season:
    df3 = df2.copy()
else:
    df3 = df2[df2["Season"].isin(season)]

# Location selector
location = st.sidebar.multiselect("Select your Location", df3["Location"].unique())
if not location:
    df4 = df3.copy()
else:
    df4 = df3[df3["Location"].isin(location)]

# Filter data based on selected Category, Season, Location
# if not category and not season and not location:
#     filtered_df = df
# elif not season and not location:
#     filtered_df = df[df["Category"].isin(category)]
# elif not category and not location:
#     filtered_df = df[df["Season"].isin(season)]
# elif not category and not season:
#     filtered_df = df[df["Location"].isin(location)]
# elif category and season:
#     filtered_df = df3[df["Category"].isin(category) & df["Season"].isin(season)]
# elif season and location:
#     filtered_df = df3[df["Season"].isin(season) & df["Location"].isin(location)]
# elif category and location:
#     filtered_df = df3[df["Category"].isin(category) & df["Location"].isin(location)]
# else:
#     filtered_df = df3[df["Category"].isin(category) & df["Season"].isin(season) & df["Location"].isin(location)]

filtered_df = df4

category_df = filtered_df.groupby(by=["Category"], as_index=False)["Purchase Amount (USD)"].sum()

# Display graphs in 2 columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Purchase Amount (USD) by Gender")
    fig = px.pie(filtered_df, values="Purchase Amount (USD)", names="Gender", hole=0.5)
    fig.update_traces(text=filtered_df["Gender"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Purchase Amount (USD) by Age")
    # fig = px.bar(filtered_df, x="Age", y="Purchase Amount (USD)", text=['${:,}'.format(x) for x in df["Age"]], template="gridon")
    fig = px.bar(filtered_df, x="Age", y="Purchase Amount (USD)", template='gridon', color="Age")
    st.plotly_chart(fig, use_container_width=True, height=200)

with col1:
    st.subheader("Purchase Amount (USD) by Category")
    fig = px.bar(category_df, x="Category", y="Purchase Amount (USD)", text=['${:,.2f}'.format(x) for x in category_df["Purchase Amount (USD)"]], template="simple_white", color="Category")
    st.plotly_chart(fig, use_container_width=True, height=200)

with col2:
    st.subheader("Purchase Amount (USD) by Season")
    fig = px.pie(filtered_df, values="Purchase Amount (USD)", names="Season", hole=0.5, template='ggplot2')
    fig.update_traces(text=filtered_df["Season"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

cl1, cl2 = st.columns(2)
with cl1:
    with st.expander("Category Data View"):
        st.write(category_df)
        csv = category_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Category Data", data=csv, file_name="Category Data.csv", mime="text/csv", help='Click here to download the data as a CSV file')

with cl2:
    with st.expander("Season Data View"):
        season = filtered_df.groupby(by="Season", as_index=False)["Purchase Amount (USD)"].sum()
        st.write(season)
        csv = season.to_csv(index=False).encode("utf-8")
        st.download_button("Download Season Data", data=csv, file_name="Season Data.csv", mime="text/csv", help='Click here to download the data as a CSV file')

# Treemap for Category, Season, Item Purchased, Size, Color
st.subheader("Hierarchical view of Purchase Amount (USD) using TreeMap")
fig2 = px.treemap(filtered_df, path=["Category", "Item Purchased", "Size"], values="Purchase Amount (USD)", hover_data=["Purchase Amount (USD)"], color="Size")
fig2.update_layout(width=800, height=650)
st.plotly_chart(fig2, use_container_width=True)

# Display graphs in 3 columns
chart1, chart2, chart3 = st.columns(3)
with chart1:
    st.subheader("Purchase Amount (USD) by Shipping Type")
    fig = px.pie(filtered_df, values="Purchase Amount (USD)", names="Shipping Type", template="plotly_dark")
    fig.update_traces(text=filtered_df["Shipping Type"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.subheader("Purchase Amount (USD) by Payment Method")
    fig = px.pie(filtered_df, values="Purchase Amount (USD)", names="Payment Method", template="seaborn")
    fig.update_traces(text=filtered_df["Payment Method"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

with chart3:
    st.subheader("Purchase Amount (USD) by Frequency of Purchases")
    fig = px.pie(filtered_df, values="Purchase Amount (USD)", names="Frequency of Purchases", template="simple_white")
    fig.update_traces(text=filtered_df["Frequency of Purchases"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

# Pivot Table Display
st.subheader(" :heavy_check_mark: Pivot table display")
st.write("Average Purchase Amount (USD) - pivoted by Subscription Status & Review Rating")
pivot_df = np.round(pd.pivot_table(df, values="Purchase Amount (USD)", index="Subscription Status", columns="Review Rating", aggfunc="mean").sort_index(ascending=False), 2)
st.write(pivot_df)

# Build scatter plot for Review Rating and Purchase Amount (USD)
data1 = px.scatter(filtered_df, x="Review Rating", y="Purchase Amount (USD)")
data1['layout'].update(title="Relationship between Review Rating and Purchase Amount (USD) using Scatter Plot.",
                       titlefont=dict(size=20), xaxis=dict(title="Review Rating", titlefont=dict(size=19)), yaxis=dict(title="Purchase Amount (USD)", titlefont=dict(size=19)))
st.plotly_chart(data1, use_container_width=True)

st.write("Average Purchase Amount (USD) - pivoted by Discount Applied & Promo Code Used")
pivot_df2 = np.round(pd.pivot_table(df, values="Purchase Amount (USD)", index="Discount Applied", columns="Promo Code Used", aggfunc="mean", margins_name="Promo Code Used").sort_index(ascending=False), 2)
df_col = pivot_df2.columns.sort_values(ascending=False)
# pivot_df2 = pivot_df2[["Yes", "No"]]
pivot_df2 = pivot_df2[df_col] # sorted to Yes and No
st.write(pivot_df2)

# Show filtered data for 100 rows and button to download filtered data
st.subheader(":point_right: Filtered data 100-rows display and filtered data download")
with st.expander("Filtered Data:"):
    st.write(filtered_df.head(100))

# Show sample data and button to download original data
st.subheader(":point_right: Sample data display and original data download")
with st.expander("Sample Data Table:"):
    df_sample = df[0:5][["Customer ID","Age", "Gender", "Category", "Purchase Amount (USD)", "Location", "Season", "Shipping Type", "Payment Method"]]
    fig = ff.create_table(df_sample, colorscale="Cividis")
    st.plotly_chart(fig, use_container_width=True)

with st.expander("View Data"):
    st.write(filtered_df.iloc[:500,1:20:2])

# Download original Dataset
# csv = df.to_csv(index=False).encode('utf-8')
# st.download_button('Download Original Data', data=csv, file_name="Shopping Data.csv", mime='text/csv', help='Click here to download a CSV file')
