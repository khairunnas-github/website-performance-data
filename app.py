import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Website Performance Analyzer")

# Deskripsi aplikasi
st.markdown("""
Aplikasi ini membantu menganalisis performa website berdasarkan dataset yang disediakan.
Jika website yang dicari belum ada, aplikasi akan menambahkannya secara otomatis dan melakukan analisis.
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

# Fungsi untuk menambahkan website baru ke dataset
def add_new_website(data, new_domain, new_latency, new_response_time, new_availability):
    # Membuat dictionary untuk domain baru
    new_data = {
        'domain': [new_domain],
        'latency': [new_latency],
        'response_time': [new_response_time],
        'availability': [new_availability]
    }
    new_df = pd.DataFrame(new_data)
    
    # Menambahkan data baru ke dataset
    updated_data = pd.concat([data, new_df], ignore_index=True)
    return updated_data

# Load dataset
data = load_data()

if data is not None:
    # Menampilkan dataset
    st.subheader("Dataset Overview")
    st.dataframe(data)

    # Input domain untuk analisis
    st.subheader("Search or Add New Website")
    domain_input = st.text_input("Enter the domain to search or add (e.g., example.com):", "").strip()

    if domain_input:
        # Cek apakah domain sudah ada
        if 'domain' in data.columns:
            if domain_input.lower() in data['domain'].str.lower().values:
                st.write(f"Domain **{domain_input}** already exists in the dataset.")
            else:
                st.write(f"Domain **{domain_input}** not found in the dataset. Adding it now...")
                
                # Misalnya kita mendapatkan data performa website baru dari API atau sumber lain
                # Di sini kita hanya memasukkan data statis sebagai contoh
                new_latency = 100  # Contoh nilai
                new_response_time = 150  # Contoh nilai
                new_availability = 99.8  # Contoh nilai
                
                # Menambahkan domain baru ke dataset
                updated_data = add_new_website(data, domain_input, new_latency, new_response_time, new_availability)
                
                # Simulasi menyimpan data ke file atau database (di sini hanya menampilkan)
                st.write("New website added successfully!")
                st.dataframe(updated_data)
                
                # Menampilkan analisis performa untuk domain yang baru ditambahkan
                st.subheader("Performance Metrics Visualization")
                selected_metric = st.selectbox("Select a metric to visualize:", ['latency', 'response_time', 'availability'])
                
                if selected_metric:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    updated_data.sort_values(by=selected_metric, ascending=False).plot(
                        kind='bar', x='domain', y=selected_metric, ax=ax, color='skyblue', legend=False
                    )
                    ax.set_title(f"{selected_metric.capitalize()} Performance", fontsize=16)
                    ax.set_ylabel(selected_metric.capitalize(), fontsize=12)
                    ax.set_xlabel("Domain", fontsize=12)
                    plt.xticks(rotation=45, ha='right')
                    st.pyplot(fig)
        else:
            st.error("The dataset does not contain a 'domain' column.")
else:
    st.error("Failed to load the dataset. Please check the data source.")
