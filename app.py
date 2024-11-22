import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Website Performance Analyzer")

# Deskripsi aplikasi
st.markdown("""
Aplikasi ini membantu menganalisis performa website berdasarkan dataset yang disediakan.
Masukkan nama domain untuk melihat data kinerjanya dan melakukan analisis lebih lanjut.
""")

# URL dataset
DATA_URL = "https://raw.githubusercontent.com/khairunnas-github/website-performance-data/main/labeled_dataset.csv"

# Fungsi untuk membaca dataset
@st.cache
def load_data():
    try:
        data = pd.read_csv(DATA_URL)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load dataset
data = load_data()

if data is not None:
    # Menampilkan dataset
    st.subheader("Dataset")
    st.dataframe(data)

    # Input untuk mencari domain
    st.subheader("Search Website Performance by Domain")
    domain = st.text_input("Enter domain (e.g., example.com):", "").strip()

    if domain:
        filtered_data = data[data['domain'].str.contains(domain, case=False, na=False)]
        
        if not filtered_data.empty:
            st.write(f"Results for: **{domain}**")
            st.dataframe(filtered_data)

            # Menampilkan visualisasi
            st.subheader("Performance Metrics")
            metric = st.selectbox(
                "Select a metric to visualize:",
                [col for col in filtered_data.columns if filtered_data[col].dtype in ['int64', 'float64']]
            )
            
            if metric:
                fig, ax = plt.subplots()
                filtered_data.plot(kind='bar', x='domain', y=metric, ax=ax, legend=False, color='skyblue')
                ax.set_title(f"{metric.capitalize()} for {domain}")
                ax.set_ylabel(metric.capitalize())
                ax.set_xlabel("Domain")
                st.pyplot(fig)
        else:
            st.warning(f"No data found for domain: {domain}")

else:
    st.info("Please enter a domain to search.")
