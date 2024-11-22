import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Website Performance Analyzer")

# Deskripsi aplikasi
st.markdown("""
Aplikasi ini membantu menganalisis performa website berdasarkan dataset yang disediakan.
Anda dapat melihat semua domain dan grafik metrik performa berdasarkan data.
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
    st.subheader("Dataset Overview")
    st.dataframe(data)

    # Menampilkan daftar domain
    st.subheader("Available Domains")
    if 'domain' in data.columns:
        all_domains = data['domain'].unique()
        st.write(f"Total domains: {len(all_domains)}")
        st.write(all_domains)

        # Memilih domain untuk dianalisis
        st.subheader("Domain Analysis")
        selected_domains = st.multiselect(
            "Select domains to analyze:",
            all_domains,
            default=all_domains[:5]  # Default hanya beberapa domain
        )

        if selected_domains:
            # Filter data berdasarkan domain yang dipilih
            filtered_data = data[data['domain'].isin(selected_domains)]

            # Memilih metrik untuk visualisasi
            st.subheader("Performance Metrics Visualization")
            metrics = [col for col in data.columns if data[col].dtype in ['int64', 'float64']]
            selected_metric = st.selectbox("Select a metric to visualize:", metrics)

            if selected_metric:
                # Grafik performa
                fig, ax = plt.subplots(figsize=(10, 6))
                filtered_data.sort_values(by=selected_metric, ascending=False).plot(
                    kind='bar', x='domain', y=selected_metric, ax=ax, color='skyblue', legend=False
                )
                ax.set_title(f"{selected_metric.capitalize()} Performance", fontsize=16)
                ax.set_ylabel(selected_metric.capitalize(), fontsize=12)
                ax.set_xlabel("Domain", fontsize=12)
                plt.xticks(rotation=45, ha='right')
                st.pyplot(fig)
        else:
            st.warning("Please select at least one domain to analyze.")
    else:
        st.error("The dataset does not contain a 'domain' column.")
else:
    st.error("Failed to load the dataset. Please check the data source.")
