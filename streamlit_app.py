import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Set Streamlit page config
st.set_page_config(page_title="Singapore Resale Prices Dashboard", layout="wide")

st.title("🏠 Singapore Resale Prices Dashboard")
st.markdown("Explore insights from resale prices dataset.")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("singapore_cleaned.csv")  
    return df

df = load_data()

# Display dataset preview
st.subheader("📊 Dataset Preview")
st.dataframe(df.head())

# Sidebar filters
st.sidebar.header("Filter Data")
year_range = st.sidebar.slider("Select Year Range", int(df["year"].min()), int(df["year"].max()), (2015, 2023))
flat_type = st.sidebar.multiselect("Select Flat Type", df["flat_type"].unique(), df["flat_type"].unique())

# Apply filters
filtered_df = df[(df["year"].between(year_range[0], year_range[1])) & (df["flat_type"].isin(flat_type))]

# Resale Price Trends Over Time
st.subheader("📈 Resale Price Trends Over Time")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=filtered_df, x="year", y="resale_price", hue="flat_type", marker="o", ax=ax)
plt.xlabel("Year")
plt.ylabel("Average Resale Price (SGD)")
plt.title("Resale Price Trends Over Time")
st.pyplot(fig)

# Average Resale Price by Town
st.subheader("🏙️ Average Resale Price by Town")
st.markdown("""
This bar chart compares the **average resale prices** across different towns in Singapore.  
- **Central Area and Bukit Timah** have the highest resale prices.  
- **Yishun, Woodlands, and Jurong West** have the lowest prices.  
- This allows buyers to compare affordability across different locations.
""")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=filtered_df.groupby("town")["resale_price"].mean().reset_index(), 
            x="town", y="resale_price", color="steelblue", ax=ax)
plt.xlabel("Town")
plt.ylabel("Average Resale Price (SGD)")
plt.xticks(rotation=45)
plt.title("Average Resale Price by Town")
st.pyplot(fig)

# Price vs Floor Area (Regression Plot)
st.subheader("📈 Price vs Floor Area (Regression Plot)")
st.markdown("""
This scatter plot visualizes the relationship between **floor area (sqm)** and **resale price (SGD)** for properties in Singapore.  
- Each dot represents a property listing.  
- The red **regression line** shows the general trend: **larger flats tend to have higher resale prices**.
""")
fig, ax = plt.subplots(figsize=(10, 6))
sns.regplot(data=filtered_df, x="floor_area_sqm", y="resale_price", scatter_kws={"alpha": 0.5}, line_kws={"color": "red"}, ax=ax)
plt.xlabel("Floor Area (sqm)")
plt.ylabel("Resale Price (SGD)")
plt.title("Resale Price vs Floor Area (with Regression Line)")
st.pyplot(fig)

