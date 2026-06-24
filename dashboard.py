import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ClickHouse Performance Dashboard", layout="wide")

st.title("ClickHouse Query Performance Comparison")
st.markdown("Compare query execution time and read data volume")

# Load results
try:
    df = pd.read_csv('benchmark_results.csv')
except FileNotFoundError:
    st.error("benchmark_results.csv not found. Please run the benchmark first.")
    st.stop()

# Aggregate by query (median time, read_rows, read_bytes)
agg = df.groupby('query').agg({
    'time_sec': 'median',
    'read_rows': 'first',
    'read_bytes': 'first'
}).reset_index()
agg.columns = ['query', 'median_time', 'read_rows', 'read_bytes']

# Execution time chart
col1, col2 = st.columns(2)

with col1:
    st.subheader("⏱ Execution Time (median)")
    fig_time = px.bar(agg, x='query', y='median_time', color='query',
                      text_auto='.4f', title="Median time (sec)")
    fig_time.update_layout(showlegend=False, xaxis_title="", yaxis_title="Time (sec)")
    st.plotly_chart(fig_time, use_container_width=True)

with col2:
    # Read rows chart (if data available)
    if not agg['read_rows'].isna().all():
        st.subheader("📊 Read Rows Count")
        fig_rows = px.bar(agg, x='query', y='read_rows', color='query',
                          title="Number of rows read", log_y=True)
        fig_rows.update_layout(showlegend=False, xaxis_title="", yaxis_title="Rows")
        st.plotly_chart(fig_rows, use_container_width=True)
    else:
        st.info("Read rows data is missing. Check EXPLAIN parsing.")

# Detailed table
st.subheader("📋 Detailed Results")
st.dataframe(agg, use_container_width=True)

# Execution plans (if files exist)
st.subheader("📄 Execution Plans (EXPLAIN)")
for query in agg['query'].unique():
    fname = f"{query}_explain.txt"
    try:
        with open(fname, 'r') as f:
            plan = f.read()
        with st.expander(f"Plan for {query}"):
            st.code(plan, language='sql')
    except FileNotFoundError:
        pass