import pandas as pd

# Baca file Excel
file_path = "/mnt/data/template_generate_jadwal (3).xlsx"
df = pd.read_excel(file_path)

# Pastikan kolom waktu dalam format time
df['Mulai'] = pd.to_datetime(df['Mulai']).dt.time
df['Selesai'] = pd.to_datetime(df['Selesai']).dt.time

# Fungsi untuk mengecek bentrok jadwal
def cek_bentrok(jadwal):
    konflik = []
    for i, row1 in jadwal.iterrows():
        for j, row2 in jadwal.iterrows():
            if i >= j:
                continue
            if row1['Hari'] == row2['Hari']:
                if (row1['Mulai'] < row2['Selesai']) and (row2['Mulai'] < row1['Selesai']):
                    if (
                        row1['Kelas'] == row2['Kelas'] or 
                        row1['Ruang'] == row2['Ruang'] or 
                        row1['Dosen'] == row2['Dosen']
                    ):
                        konflik.append({
                            "Baris_1": i,
                            "Baris_2": j,
                            "Hari": row1['Hari'],
                            "Kelas_1": row1['Kelas'],
                            "Kelas_2": row2['Kelas'],
                            "Ruang_1": row1['Ruang'],
                            "Ruang_2": row2['Ruang'],
                            "Dosen_1": row1['Dosen'],
                            "Dosen_2": row2['Dosen'],
                            "Jam_1": f"{row1['Mulai']} - {row1['Selesai']}",
                            "Jam_2": f"{row2['Mulai']} - {row2['Selesai']}"
                        })
    return konflik

# Jalankan fungsi pengecekan
bentrok = cek_bentrok(df)
bentrok[:5]  # tampilkan 5 konflik pertama (jika ada)

import pandas as pd

# Baca file Excel
df = pd.read_excel("template_generate_jadwal (3).xlsx")

# Rename kolom agar mudah dibaca
df_jadwal = df.rename(columns={
    'DOSEN PENGAJAR': 'Dosen',
    'KELAS': 'Kelas',
    'DOSEN_HARI_KAMPUS': 'Hari',
    'DOSEN_JAM_KAMPUS': 'Jam'
})

# Filter hanya baris dengan format jam valid (misalnya 08:00-10:00)
df_jadwal = df_jadwal[df_jadwal['Jam'].str.contains('-', na=False)].copy()

# Pisahkan jam menjadi 'Mulai' dan 'Selesai'
df_jadwal[['Mulai', 'Selesai']] = df_jadwal['Jam'].str.split('-', expand=True)
df_jadwal['Mulai'] = pd.to_datetime(df_jadwal['Mulai'], format="%H:%M").dt.time
df_jadwal['Selesai'] = pd.to_datetime(df_jadwal['Selesai'], format="%H:%M").dt.time

# Fungsi untuk cek bentrok
def cek_bentrok(jadwal):
    konflik = []
    for i, row1 in jadwal.iterrows():
        for j, row2 in jadwal.iterrows():
            if i >= j:
                continue
            if row1['Hari'] == row2['Hari']:
                if (row1['Mulai'] < row2['Selesai']) and (row2['Mulai'] < row1['Selesai']):
                    if (
                        row1['Kelas'] == row2['Kelas'] or
                        row1['Dosen'] == row2['Dosen']
                    ):
                        konflik.append((i, j, row1['Hari'], row1['Jam'], row2['Jam']))
    return konflik

# Jalankan
bentrok = cek_bentrok(df_jadwal)

# Tampilkan hasil
if not bentrok:
    print("✅ Tidak ada jadwal bentrok.")
else:
    print("❌ Bentrok ditemukan:")
    for konflik in bentrok:
        print(f" - Baris {konflik[0]} dan {konflik[1]} bentrok pada hari {konflik[2]} jam {konflik[3]} & {konflik[4]}")
