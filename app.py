import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Website Performance Analyzer")

# Deskripsi aplikasi
st.markdown("""
Aplikasi ini membantu menganalisis performa website berdasarkan dataset yang disediakan.
Jika website yang dicari belum ada, aplikasi akan menambahkannya secara otomatis dengan data yang diminta dan melakukan analisis langsung.
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
def add_new_website(data, website_url, category, page_size, load_time, response_time, throughput, performance_label, user_response):
    # Menambah website baru dengan data performa
    new_data = {
        'website_url': [website_url],
        'Category': [category],
        'Page Size (KB)': [page_size],
        'Load Time(s)': [load_time],
        'Response Time(s)': [response_time],
        'Throughput': [throughput],
        'Performance_Label': [performance_label],
        'User Response': [user_response]
    }
    new_df = pd.DataFrame(new_data)
    
    # Menambahkan data baru ke dataset
    updated_data = pd.concat([data, new_df], ignore_index=True)
    updated_data.to_csv(DATA_URL, index=False)  # Simpan perubahan ke file CSV
    return updated_data

# Load dataset
data = load_data()

if data is not None:
    # Menampilkan nama kolom untuk memeriksa struktur data
    st.write("Dataset Columns:", data.columns.tolist())

    # Menampilkan dataset
    st.subheader("Dataset Overview")
    st.dataframe(data)

    # Input website untuk analisis
    st.subheader("Search or Add New Website")
    website_url_input = st.text_input("Enter the website URL to search or add (e.g., https://example.com):", "").strip()

    if website_url_input:
        # Cek apakah website sudah ada
        if 'website_url' in data.columns:
            # Cek apakah website ada dalam dataset
            if website_url_input.lower() in data['website_url'].str.lower().values:
                st.write(f"Website **{website_url_input}** already exists in the dataset.")
            else:
                st.write(f"Website **{website_url_input}** not found in the dataset. Adding it now...")
                
                # Input data performa untuk website yang baru
                category_input = st.text_input("Enter the website category:", "General")
                page_size_input = st.number_input("Enter the page size (KB):", min_value=0)
                load_time_input = st.number_input("Enter the load time (seconds):", min_value=0.0)
                response_time_input = st.number_input("Enter the response time (seconds):", min_value=0.0)
                throughput_input = st.number_input("Enter the throughput:", min_value=0.0)
                performance_label_input = st.selectbox("Select the performance label:", ['Good', 'Average', 'Poor'])
                user_response_input = st.number_input("Enter user response (0 to 100):", min_value=0, max_value=100, value=75)

                # Menambahkan website baru dengan nilai performa yang diberikan
                updated_data = add_new_website(
                    data, website_url_input, category_input, page_size_input,
                    load_time_input, response_time_input, throughput_input,
                    performance_label_input, user_response_input
                )
                st.write("New website added successfully!")

                # Menampilkan hasil dataset yang diperbarui
                st.dataframe(updated_data)
                
                # Visualisasi performa untuk website yang baru ditambahkan
                st.subheader("Performance Metrics Visualization")
                selected_metric = st.selectbox("Select a metric to visualize:", ['Load Time(s)', 'Response Time(s)', 'Throughput', 'User Response'])

                if selected_metric:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    updated_data.sort_values(by=selected_metric, ascending=False).plot(
                        kind='bar', x='website_url', y=selected_metric, ax=ax, color='skyblue', legend=False
                    )
                    ax.set_title(f"{selected_metric} Performance", fontsize=16)
                    ax.set_ylabel(selected_metric, fontsize=12)
                    ax.set_xlabel("Website URL", fontsize=12)
                    plt.xticks(rotation=45, ha='right')
                    st.pyplot(fig)
        else:
            st.error("The dataset does not contain a 'website_url' column.")
else:
    st.error("Failed to load the dataset. Please check the data source.")
