# Bike Sharing Analysis Dashboard

Repository ini berisi analisis data untuk sistem berbagi sepeda serta dashboard interaktif yang dibuat menggunakan Python.

## 🚀 Instalasi dan Menjalankan Dashboard

Ikuti langkah-langkah berikut untuk menjalankan dashboard secara lokal:

### 1️⃣ **Clone Repository**

```bash
git clone https://github.com/hara29/BikeSharingAnalysisData.git
cd BikeSharingAnalysisData
```

### 2️⃣ **Buat Virtual Environment (Opsional, tetapi Disarankan)**

```bash
python -m venv venv
source venv/bin/activate  # Untuk macOS/Linux
venv\Scripts\activate    # Untuk Windows
```

### 3️⃣ **Instal Dependencies**

```bash
pip install -r requirements.txt
```

### 4️⃣ **Jalankan Dashboard**

```bash
streamlit run dashboard/dashboard.py
```

## 📁 Struktur Direktori

```
BikeSharingAnalysisData/
│── dashboard/
│   ├── dashboard.py   # File utama untuk menjalankan dashboard
│   ├── utils.py       # Fungsi bantu untuk analisis data
│── data/
│   ├── bike_data.csv  # Data utama untuk analisis
│── notebooks/
│   ├── analysis.ipynb # Notebook Jupyter untuk eksplorasi awal
│── requirements.txt   # Daftar dependencies
│── README.md          # Dokumentasi ini
```

## 📝 Fitur Dashboard

- Visualisasi tren peminjaman sepeda berdasarkan waktu 
- Analisis faktor lingkungan (suhu, kelembapan, dan kecepatan angin)  yang memengaruhi penggunaan sepeda
- Grafik interaktif dengan Streamlit

## 📸 Dashboard Preview
![Screen Recording 2025-03-09 at 15 16 48](https://github.com/user-attachments/assets/7a5b2ecb-77d3-4df1-b671-d97aa876ef9b)


## 📌 Referensi Dataset

Dataset yang digunakan dapat ditemukan di: [Dataset Bike Sharing](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)

## 🤝 Kontribusi

Jika ingin berkontribusi, silakan lakukan fork repository ini dan ajukan pull request!

## 📧 Kontak

Jika ada pertanyaan atau saran, silakan hubungi saya melalui [GitHub Issues](https://github.com/hara29/BikeSharingAnalysisData/issues).

