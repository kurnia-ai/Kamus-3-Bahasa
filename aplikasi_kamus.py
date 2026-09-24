import pandas as pd
import streamlit as st
import re

# --- 1. PENGATURAN TAMPILAN HALAMAN ---
st.set_page_config(page_title="Kamus 3 Bahasa", page_icon="📚")
st.title("📚 Automotive Dictionery         (Bengkel Otomotif)")
st.write("Menerjemahkan: **Indonesia ➔ Inggris ➔ Daerah**")
st.write("Credit by awan")

# --- 2. MEMUAT & MEMBERSIHKAN DATA DARI CSV LOKAL ---
@st.cache_data
def load_data():
    # 1. Baca file CSV
    # Pastikan nama file sama persis dengan yang ada di folder Anda
    df = pd.read_csv("draft_AUTOMOTIVE DICTIONARY 2021.xlsx - Table 1.csv")
    
    # 2. Ambil kolom yang tepat (Kolom 1 = Inggris, Kolom 7 = Indonesia, Kolom 8 = Daerah)
    df_clean = df.iloc[:, [0, 6, 7]].copy()
    df_clean.columns = ['Inggris', 'Indonesia', 'Daerah']
    
    # 3. Hapus baris pertama (karena itu header bawaan) dan baris gambar (Figure)
    df_clean = df_clean.drop(0)
    df_clean = df_clean.dropna(subset=['Inggris'])
    df_clean = df_clean[~df_clean['Inggris'].str.contains('Figure', na=False, case=False)]
    
    # 4. Fungsi untuk membersihkan teks bahasa Inggris dari simbol pelafalan
    def bersihkan_inggris(text):
        if not isinstance(text, str): return text
        # Membuang pelafalan yang dipisah oleh Enter (\n) atau spasi panjang
        parts = re.split(r'\n|\s{4,}', str(text))
        return parts[0].strip()

    df_clean['Inggris'] = df_clean['Inggris'].apply(bersihkan_inggris)
    
    # 5. Hapus baris jika Indonesia dan Daerah-nya sama-sama kosong
    df_clean = df_clean.dropna(subset=['Indonesia', 'Daerah'], how='all')
    df_clean = df_clean.astype(str) 
    
    return df_clean

try:
    df = load_data()
    
    # --- 3. KOTAK PENCARIAN ---
    st.markdown("---")
    kata_cari = st.text_input("🔍 Masukkan kata (Indonesia / Inggris / Daerah):")

    if kata_cari:
        # Mencari kata di kolom 'Indonesia', 'Inggris', ATAU 'Daerah'
        hasil_id = df['Indonesia'].str.contains(kata_cari, case=False, na=False)
        hasil_en = df['Inggris'].str.contains(kata_cari, case=False, na=False)
        hasil_daerah = df['Daerah'].str.contains(kata_cari, case=False, na=False)
        
        # Gabungkan hasil pencarian dari ketiga kolom
        hasil = df[hasil_id | hasil_en | hasil_daerah]
        
        # --- 4. MENAMPILKAN HASIL TERJEMAHAN ---
        if not hasil.empty:
            st.success(f"Ditemukan {len(hasil)} hasil untuk kata '{kata_cari}':")
            
            for index, row in hasil.iterrows():
                # Membersihkan tulisan "nan" jika ada data yang kosong
                teks_indo = row['Indonesia'] if row['Indonesia'] != 'nan' else 'Tidak ada'
                teks_inggris = row['Inggris'] if row['Inggris'] != 'nan' else 'Tidak ada'
                teks_daerah = row['Daerah'] if row['Daerah'] != 'nan' else 'Tidak ada'

                st.markdown(f"### 🇮🇩 {teks_indo}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**🇬🇧 Bahasa Inggris:**\n\n{teks_inggris}")
                with col2:
                    st.warning(f"**🏘️ Bahasa Daerah:**\n\n{teks_daerah}")
                    
                st.markdown("---")
        else:
            st.error("⚠️ Kata tidak ditemukan dalam kamus.")

except Exception as e:
    st.error("Gagal memuat data. Pastikan file CSV sudah berada di folder yang sama.")
    st.write(f"Detail error: {e}")
