import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# 1. PAGE CONFIG
st.set_page_config(page_title="Nifty 50 Ultra Analytics", layout="wide", initial_sidebar_state="expanded")

# CSS Fix for Dark Theme Visibility
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stMetric"] {
        background-color: #1a1c24;
        border: 1px solid #31333f;
        padding: 15px 20px;
        border-radius: 12px;
    }
    [data-testid="stMetricLabel"] { color: #a3a8b4 !important; }
    [data-testid="stMetricValue"] { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

DB_PATH = r"C:\Users\velua\OneDrive\Desktop\Stock_Analysis_Project\nifty50.db"

def get_data(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 2. ANALYSIS FUNCTIONS
def get_market_performance():
    all_data = get_data("SELECT Ticker, Close, Date FROM stock_prices")
    all_data.columns = [c.lower() for c in all_data.columns]
    all_data['date'] = pd.to_datetime(all_data['date'])
    perf = []
    for t in all_data['ticker'].unique():
        t_df = all_data[all_data['ticker'] == t].sort_values('date')
        if len(t_df) > 1:
            r = ((t_df['close'].iloc[-1] - t_df['close'].iloc[0]) / t_df['close'].iloc[0]) * 100
            perf.append({'Ticker': t, 'Yearly Return %': round(r, 2)})
    return pd.DataFrame(perf).sort_values('Yearly Return %', ascending=False)

def get_correlation_matrix():
    df_corr = get_data("SELECT Ticker, Date, Close FROM stock_prices ORDER BY Date DESC LIMIT 500")
    df_corr.columns = [c.lower() for c in df_corr.columns]
    return df_corr.pivot(index='date', columns='ticker', values='close').corr()

# 3. SIDEBAR (The missing piece!)
st.sidebar.title("Project Nifty50")
st.sidebar.markdown("---")

# Load Sector List
sector_df = get_data("SELECT * FROM stock_sectors")
sectors = ["All"] + sorted(sector_df['sector'].unique().tolist())
selected_sector = st.sidebar.selectbox("Industry Sector", sectors)

# Filter Ticker List based on Sector
if selected_sector == "All":
    ticker_list = get_data("SELECT DISTINCT Ticker FROM stock_prices")['Ticker'].tolist()
else:
    ticker_list = sector_df[sector_df['sector'] == selected_sector]['Ticker'].tolist()

selected_stock = st.sidebar.selectbox("Select Stock Ticker", ticker_list)

# 4. DATA PROCESSING
df = get_data(f"SELECT * FROM stock_prices WHERE Ticker='{selected_stock}'")
df.columns = [c.lower() for c in df.columns]
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Metrics
latest_price = df['close'].iloc[-1]
df['cum_return'] = (df['close'] / df['close'].iloc[0]) * 100 
y_return = df['cum_return'].iloc[-1] - 100
volatility = df['close'].pct_change().std() * (252**0.5) * 100

# 5. HEADER & METRICS
st.title(f"Market Analysis: {selected_stock}")
st.caption(f"Sector: {selected_sector}")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Current Price", f"₹{latest_price:,.2f}")
c2.metric("Cumulative Growth", f"{y_return:+.2f}%")
c3.metric("Annual Volatility", f"{volatility:.2f}%")
c4.metric("52W High", f"₹{df['high'].max():,.2f}")

# 6. THE 5 TABS (Completing the Requirements)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Price", "📈 Growth", "🔥 Correlation", "🏆 Leaderboard", "📋 Data"])

with tab1:
    fig = go.Figure(data=[go.Candlestick(x=df['date'], open=df['open'], high=df['high'], low=df['low'], close=df['close'])])
    fig.update_layout(template="plotly_dark", height=500, xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Growth of ₹100 Investment")
    fig_cum = px.line(df, x='date', y='cum_return', template="plotly_dark")
    fig_cum.add_hline(y=100, line_dash="dash", line_color="red")
    st.plotly_chart(fig_cum, use_container_width=True)

with tab3:
    st.subheader("Inter-Stock Correlation")
    st.plotly_chart(px.imshow(get_correlation_matrix(), text_auto=True, color_continuous_scale='RdBu_r'), use_container_width=True)

with tab4:
    st.subheader("Market Performance Leaderboard")
    perf_df = get_market_performance()
    
    # 1. Requirement: Sector Performance Bar Chart
    st.write("### Average Yearly Return by Sector")
    try:
        # Merging stock performance with sector info
        sector_perf = sector_df.merge(perf_df, on='Ticker').groupby('sector')['Yearly Return %'].mean().reset_index()
        fig_sector = px.bar(sector_perf, x='sector', y='Yearly Return %', 
                            color='Yearly Return %', 
                            color_continuous_scale='RdYlGn',
                            template="plotly_dark")
        st.plotly_chart(fig_sector, use_container_width=True)
    except Exception as e:
        st.info("Add Sector Data to see Industry performance.")

    st.markdown("---")

    # 2. Requirement: Top 10 Green vs Top 10 Red
    col_green, col_red = st.columns(2)
    
    with col_green:
        st.success("🟢 Top 10 Green (Best Performers)")
        # Already sorted descending in get_market_performance()
        st.table(perf_df.head(10))
        
    with col_red:
        st.error("🔴 Top 10 Red (Worst Performers)")
        # Sort ascending to get the biggest losers
        worst_perf = perf_df.sort_values('Yearly Return %', ascending=True).head(10)
        st.table(worst_perf)
with tab5:
    st.subheader("Monthly Performance Summary")
    
    # Create a 'Month' column for grouping
    df['month'] = df['date'].dt.strftime('%B %Y')
    
    # Calculate monthly return
    monthly_perf = df.groupby('month').apply(
        lambda x: ((x['close'].iloc[-1] - x['close'].iloc[0]) / x['close'].iloc[0]) * 100
    ).reset_index(name='Monthly Return %')
    
    st.dataframe(monthly_perf.sort_values('Monthly Return %', ascending=False), use_container_width=True)
    
    st.markdown("---")
    st.subheader("Raw Transactional Data")
    st.dataframe(df.sort_values('date', ascending=False), use_container_width=True)