import pandas as pd
import streamlit as st

# --- 1. PENGATURAN TAMPILAN HALAMAN ---
st.set_page_config(page_title="Kamus 3 Bahasa", page_icon="📚")
st.title("📚 Kamus Pencari 3 Bahasa")
st.write("Menerjemahkan: **Indonesia ➔ Inggris ➔ Daerah**")

# --- 2. MEMUAT DATA DARI GOOGLE DRIVE ---
# GANTI teks di dalam tanda kutip di bawah ini dengan link CSV dari Google Sheets Anda
URL_GOOGLE_SHEETS = "https://drive.google.com/drive/folders/1BxIau3YElOrGJNhXb1dFKcEaOLs2tUCM"

# Menggunakan cache agar aplikasi tidak mendownload ulang data setiap kali mengetik
@st.cache_data
def load_data(url):
    # Membaca data dari link CSV
    df = pd.read_csv(url)
    # Memastikan semua data teks menjadi tipe string agar tidak error saat dicari
    df = df.astype(str) 
    return df

try:
    # Menjalankan fungsi memuat data
    df = load_data(URL_GOOGLE_SHEETS)
    
    # --- 3. KOTAK PENCARIAN ---
    st.markdown("---")
    kata_cari = st.text_input("🔍 Masukkan kata (Bahasa Indonesia):")

    if kata_cari:
        # Mencari kata di kolom 'Indonesia' (mengabaikan huruf besar/kecil)
        hasil = df[df['Indonesia'].str.contains(kata_cari, case=False, na=False)]
        
        # --- 4. MENAMPILKAN HASIL TERJEMAHAN ---
        if not hasil.empty:
            st.success(f"Ditemukan {len(hasil)} hasil untuk kata '{kata_cari}':")
            
            for index, row in hasil.iterrows():
                st.markdown(f"### 🇮🇩 {row['Indonesia']}")
                
                # Membagi tampilan menjadi 2 kolom (kiri dan kanan)
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**🇬🇧 Bahasa Inggris:**\n\n{row['Inggris']}")
                with col2:
                    st.warning(f"**🏘️ Bahasa Daerah:**\n\n{row['Daerah']}")
                    
                st.markdown("---") # Garis pemisah antar hasil
        else:
            st.error("⚠️ Kata tidak ditemukan dalam kamus.")

except Exception as e:
    st.error("Gagal memuat data. Pastikan link CSV sudah benar dan laptop terhubung internet.")
    st.write(f"Detail error: {e}")
