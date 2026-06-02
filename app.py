import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Bengaluru Housing Analytics",
    page_icon="🏠",
    layout="wide"
)

DATA_PATH = Path(__file__).resolve().parent / "data" / "bengaluru_cleaned_data.csv"

@st.cache_data(show_spinner=False)
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df['BHK'] = pd.to_numeric(df['BHK'], errors='coerce')
    df = df.dropna(subset=['location', 'BHK', 'price', 'price_per_sqft'])
    return df


df = load_data(DATA_PATH)

st.title("🏠 Bengaluru Housing Analytics")
st.markdown(
    "Explore Bengaluru housing affordability, premium neighbourhoods, and price-per-sqft trends using interactive filters and polished analytics charts."
)

# Sidebar filters
st.sidebar.header("Filter listings")
all_locations = sorted(df['location'].unique())
selected_locations = st.sidebar.multiselect(
    "Location",
    options=all_locations,
    default=all_locations,
    help="Select one or more Bengaluru locations to focus the analysis."
)

bhk_options = sorted(df['BHK'].dropna().astype(int).unique())
selected_bhk = st.sidebar.multiselect(
    "BHK",
    options=bhk_options,
    default=bhk_options,
    help="Select apartment sizes to compare price trends across BHK segments."
)

price_min = float(df['price'].min())
price_max = float(df['price'].max())
selected_price = st.sidebar.slider(
    "Price range (Lakhs)",
    min_value=round(price_min, 2),
    max_value=round(price_max, 2),
    value=(round(price_min, 2), round(price_max, 2)),
    step=1.0,
    help="Filter listings by price range in lakhs."
)

# Apply filters
df_filtered = df.copy()
if selected_locations:
    df_filtered = df_filtered[df_filtered['location'].isin(selected_locations)]
if selected_bhk:
    df_filtered = df_filtered[df_filtered['BHK'].astype(int).isin(selected_bhk)]
df_filtered = df_filtered[df_filtered['price'].between(*selected_price)]

if df_filtered.empty:
    st.warning("No listings match the selected filters. Adjust the location, BHK, or price range.")
else:
    # KPI summary
    avg_price = df_filtered['price'].mean()
    avg_pps = df_filtered['price_per_sqft'].mean()
    avg_sqft = df_filtered['total_sqft'].mean()
    listing_count = len(df_filtered)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Listings", listing_count)
    kpi2.metric("Average Price", f"₹{avg_price:.2f} Lakhs")
    kpi3.metric("Average Price/Sqft", f"₹{avg_pps:.0f}")
    kpi4.metric("Average Total Sqft", f"{avg_sqft:.0f}")

    st.markdown("---")

    # Charts
    premium_locations = df_filtered.groupby('location')['price_per_sqft'].mean().nlargest(10).reset_index()
    affordable_locations = df_filtered.groupby('location')['price_per_sqft'].mean().nsmallest(10).reset_index()
    bhk_price = df_filtered.groupby('BHK')['price'].mean().reset_index()

    col1, col2 = st.columns(2)
    with col1:
        fig_premium = px.bar(
            premium_locations,
            x='price_per_sqft',
            y='location',
            orientation='h',
            title='Top Premium Locations by Price per Sqft',
            labels={'price_per_sqft': 'Price per Sqft', 'location': 'Location'},
            text='price_per_sqft'
        )
        fig_premium.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_premium, use_container_width=True)

    with col2:
        fig_affordable = px.bar(
            affordable_locations,
            x='price_per_sqft',
            y='location',
            orientation='h',
            title='Top Affordable Locations by Price per Sqft',
            labels={'price_per_sqft': 'Price per Sqft', 'location': 'Location'},
            text='price_per_sqft'
        )
        fig_affordable.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_affordable, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        fig_bhk = px.bar(
            bhk_price.sort_values('BHK'),
            x='BHK',
            y='price',
            title='Average Price by BHK',
            labels={'BHK': 'BHK', 'price': 'Average Price (Lakhs)'},
            text='price'
        )
        fig_bhk.update_traces(marker_color='indianred')
        st.plotly_chart(fig_bhk, use_container_width=True)

    with col4:
        fig_pps = px.histogram(
            df_filtered,
            x='price_per_sqft',
            nbins=35,
            title='Price per Sqft Distribution',
            labels={'price_per_sqft': 'Price per Sqft'},
            marginal='box'
        )
        st.plotly_chart(fig_pps, use_container_width=True)

    st.markdown("---")
    st.subheader("Filtered Data Sample")
    st.dataframe(df_filtered[['location', 'BHK', 'price', 'total_sqft', 'price_per_sqft']].sort_values('price_per_sqft', ascending=False).head(15))
