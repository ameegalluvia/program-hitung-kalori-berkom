import csv
from datetime import date, datetime, timedelta
import json


# ==========================================
# FUNGSI DASAR & PERHITUNGAN KALORI
# ==========================================


def hitung_bmr(gender, berat, tinggi, umur):
  if gender == "pria":
    return (10 * berat) + (6.25 * tinggi) - (5 * umur) + 5.0
  else:
    return (10 * berat) + (6.25 * tinggi) - (5 * umur) - 161.0


def hitung_target(profil):
  bmr = hitung_bmr(
      profil["gender"], profil["berat"], profil["tinggi"], profil["umur"]
  )

  if profil["aktivitas"] == "sangat_ringan":
    tdee = bmr * 1.2
  elif profil["aktivitas"] == "ringan":
    tdee = bmr * 1.375
  elif profil["aktivitas"] == "sedang":
    tdee = bmr * 1.55
  elif profil["aktivitas"] == "berat":
    tdee = bmr * 1.725
  else:
    tdee = bmr * 1.9

  if profil["tujuan"] == "turun":
    target = tdee - 500
  elif profil["tujuan"] == "naik":
    target = tdee + 500
  else:
    target = tdee

  if target < bmr:
    target = bmr

  return round(target)


# ==========================================
# BACA DAN SIMPAN PROFIL & CATATAN
# ==========================================


def muat_profil():
  try:
    with open("profil.json", "r") as f:
      return json.load(f)
  except FileNotFoundError:
    return None


def simpan_profil(profil):
  with open("profil.json", "w") as f:
    json.dump(profil, f, indent=2)


def minta_profil_baru():
  print("\n--- SILAKAN ISI DATA DIRI ---")

  # Tampilkan profil lama jika ada
  profil_lama = muat_profil()
  if profil_lama is not None:
    print("Data Profil Anda Saat Ini:")
    print(f"- Gender    : {profil_lama['gender']}")
    print(f"- Umur      : {profil_lama['umur']} tahun")
    print(f"- Berat     : {profil_lama['berat']} kg")
    print(f"- Tinggi    : {profil_lama['tinggi']} cm")
    print(f"- Aktivitas : {profil_lama['aktivitas']}")
    print(f"- Tujuan    : {profil_lama['tujuan']}")
    print("---------------------------------")
    print("Masukkan data baru di bawah ini:")

  while True:
    gender = input("Gender (pria / wanita): ").strip().lower()
    if gender in ["pria", "wanita"]:
      break
    print("Ketik 'pria' atau 'wanita' ya!")

  while True:
    try:
      umur = int(input("Umur (tahun): "))
      if 10 <= umur <= 100:
        break
      print("Umur tidak valid! Masukkan antara 10 sampai 100 tahun.")
    except ValueError:
      print("Harus berupa angka bulat!")

  while True:
    try:
      berat = float(input("Berat badan (kg): ").replace(",", "."))
      if 20 <= berat <= 300:
        break
      print("Berat badan harus antara 20 sampai 300 kg.")
    except ValueError:
      print("Harus berupa angka!")

  while True:
    try:
      tinggi = float(input("Tinggi badan (cm): ").replace(",", "."))
      if 100 <= tinggi <= 250:
        break
      print("Tinggi badan harus antara 100 sampai 250 cm.")
    except ValueError:
      print("Harus berupa angka!")

  print("\nPilih tingkat aktivitas:")
  print("1. sangat_ringan")
  print("2. ringan")
  print("3. sedang")
  print("4. berat")
  print("5. sangat_berat")

  while True:
    aktivitas = input("Ketik pilihan aktivitas: ").strip().lower()
    if aktivitas in [
        "sangat_ringan",
        "ringan",
        "sedang",
        "berat",
        "sangat_berat",
    ]:
      break
    print("Pilihan aktivitas tidak sesuai daftar! Ketik sesuai teks di atas.")

  while True:
    tujuan = input("Tujuan (turun / jaga / naik): ").strip().lower()
    if tujuan in ["turun", "jaga", "naik"]:
      break
    print("Pilihan tujuan salah! Ketik: turun, jaga, atau naik.")

  profil = {
      "gender": gender,
      "umur": umur,
      "berat": berat,
      "tinggi": tinggi,
      "aktivitas": aktivitas,
      "tujuan": tujuan,
  }
  simpan_profil(profil)
  print("Profil berhasil disimpan!\n")
  return profil


def muat_catatan():
  try:
    with open("catatan.json", "r") as f:
      return json.load(f)
  except FileNotFoundError:
    return {}


def simpan_catatan_baru(nama, porsi, kalori):
  semua_data = muat_catatan()
  hari_ini = str(date.today())
  jam_sekarang = datetime.now().strftime("%H:%M")

  if hari_ini not in semua_data:
    semua_data[hari_ini] = []

  catatan_baru = {
      "nama": nama,
      "porsi": porsi,
      "kalori": kalori,
      "jam": jam_sekarang,
  }

  semua_data[hari_ini].append(catatan_baru)

  with open("catatan.json", "w") as f:
    json.dump(semua_data, f, indent=2)


def hapus_catatan_hari_ini(indeks):
  semua_data = muat_catatan()
  hari_ini = str(date.today())

  if hari_ini in semua_data and 0 <= indeks < len(semua_data[hari_ini]):
    semua_data[hari_ini].pop(indeks)
    with open("catatan.json", "w") as f:
      json.dump(semua_data, f, indent=2)
    return True
  return False


# ==========================================
# BACA DATASET MAKANAN CSV
# ==========================================


def baca_makanan_csv():
  daftar = []
  try:
    with open("makanan.csv", "r") as f:
      reader = csv.DictReader(f)
      for baris in reader:
        daftar.append({
            "nama": baris["name"].strip(),
            "porsi": baris["serving_label"].strip(),
            "kalori": float(baris["kcal_per_serving"]),
        })
  except FileNotFoundError:
    pass
  return daftar


def cari_makanan(keyword, daftar_makanan):
  keyword = keyword.strip().lower()
  hasil = []
  for item in daftar_makanan:
    if keyword in item["nama"].lower():
      hasil.append(item)
  return hasil


def atur_urutan_rekomendasi(item):
  return item["selisih"]


# ==========================================
# MAIN PROGRAM
# ==========================================


def main():
  print("==================================")
  print("     KALKULATOR KALORI SEDERHANA  ")
  print("==================================")

  profil = muat_profil()
  if profil is None:
    print("Belum ada profil. Mari buat dulu.")
    profil = minta_profil_baru()

  daftar_makanan = baca_makanan_csv()

  while True:
    target = hitung_target(profil)

    semua_data = muat_catatan()
    hari_ini = str(date.today())
    catatan_hari_ini = semua_data.get(hari_ini, [])

    total_kalori = 0
    for item in catatan_hari_ini:
      total_kalori = total_kalori + item["kalori"]

    print("\n----------------------------------")
    print(f"Tanggal  : {date.today().strftime('%d-%m-%Y')}")
    print(f"Target   : {target} kkal")
    print(f"Tercatat : {total_kalori} kkal")
    print("----------------------------------")
    print("1. Catat Makanan")
    print("2. Lihat Catatan Hari Ini")
    print("3. Cek Kecukupan Kalori")
    print("4. Hapus Catatan Hari Ini")
    print("5. Ubah Data Profil")
    print("6. Riwayat 14 Hari Terakhir")
    print("0. Keluar")

    pilihan = input("Pilih menu (0-6): ").strip()

    if pilihan == "1":
      print("\n--- CATAT MAKANAN ---")
      query = input("Cari nama makanan: ").strip()
      hasil = cari_makanan(query, daftar_makanan)

      item_terpilih = None
      kalori_final = 0
      porsi_final = 1.0

      if hasil:
        print("\nHasil Pencarian:")
        i = 1
        for m in hasil:
          print(f"{i}. {m['nama']} ({m['porsi']}) — {m['kalori']} kkal")
          i = i + 1

        pilih_no = input("Pilih nomor (0 untuk manual): ").strip()
        if pilih_no.isdigit() and int(pilih_no) > 0:
          idx = int(pilih_no) - 1
          if idx < len(hasil):
            pilih_makanan = hasil[idx]
            try:
              porsi_final = float(
                  input("Jumlah porsi (misal 1 atau 0.5): ").replace(",", ".")
              )
            except ValueError:
              porsi_final = 1.0
            kalori_final = pilih_makanan["kalori"] * porsi_final
            item_terpilih = pilih_makanan["nama"]

      if item_terpilih is None:
        print("\nInput Manual Kalori:")
        item_terpilih = input("Nama makanan/minuman: ").strip()
        try:
          kalori_final = float(
              input("Total kalori (kkal): ").replace(",", ".")
          )
        except ValueError:
          print("Kalori tidak valid! Batal dicatat.")
          continue

      if item_terpilih and kalori_final > 0:
        simpan_catatan_baru(item_terpilih, porsi_final, kalori_final)
        print(f"Berhasil mencatat: {item_terpilih} ({kalori_final} kkal)")

    elif pilihan == "2":
      print("\n--- CATATAN HARI INI ---")
      if not catatan_hari_ini:
        print("Belum ada catatan hari ini.")
      else:
        print("Jam   Nama Makanan            Porsi    Kalori")
        for c in catatan_hari_ini:
          print(
              f"{c['jam']}   {c['nama']} ({c['porsi']} porsi) = {c['kalori']}"
              " kkal"
          )
        print(f"\nTotal: {total_kalori} kkal")

    elif pilihan == "3":
      print("\n--- CEK KECUKUPAN ---")
      sisa = target - total_kalori
      print(f"Target : {target} kkal")
      print(f"Masuk  : {total_kalori} kkal")
      if sisa <= 0:
        print(f"Status : CUKUP (Kelebihan {-sisa} kkal)")
      else:
        print(f"Status : BELUM CUKUP (Sisa kurang {sisa} kkal)")

        if daftar_makanan:
          print("\nRekomendasi makanan yang muat di sisa kalorimu:")
          cocok = []
          for m in daftar_makanan:
            if m["kalori"] <= sisa + 50:
              item_baru = {
                  "nama": m["nama"],
                  "porsi": m["porsi"],
                  "kalori": m["kalori"],
                  "selisih": abs(sisa - m["kalori"]),
              }
              cocok.append(item_baru)

          cocok.sort(key=atur_urutan_rekomendasi)

          i = 0
          for r in cocok:
            if i < 3:
              print(f"- {r['nama']} ({r['porsi']}) = {r['kalori']} kkal")
              i = i + 1
            else:
              break

    elif pilihan == "4":
      print("\n--- HAPUS CATATAN ---")
      if not catatan_hari_ini:
        print("Tidak ada catatan hari ini untuk dihapus.")
      else:
        i = 1
        for c in catatan_hari_ini:
          print(f"{i}. {c['jam']} - {c['nama']} ({c['kalori']} kkal)")
          i = i + 1

        try:
          n = int(input("Nomor yang mau dihapus (0 batal): "))
          if n > 0 and hapus_catatan_hari_ini(n - 1):
            print("Catatan berhasil dihapus!")
          else:
            print("Dibatalkan atau nomor salah.")
        except ValueError:
          print("Masukkan angka yang benar!")

    elif pilihan == "5":
      profil = minta_profil_baru()

    elif pilihan == "6":
      print("\n--- RIWAYAT 14 HARI TERAKHIR ---")
      semua_data = muat_catatan()
      hari_ini = date.today()
      ada = False
      for i in range(1, 15):
        tgl = hari_ini - timedelta(days=i)
        tgl_str = str(tgl)
        if tgl_str in semua_data:
          ada = True
          tot = 0
          for x in semua_data[tgl_str]:
            tot = tot + x["kalori"]

          status = "CUKUP" if tot >= target else "KURANG"
          print(f"{tgl.strftime('%d-%m-%Y')} : {tot} kkal [{status}]")
      if not ada:
        print("Belum ada riwayat.")

    elif pilihan == "0":
      print("Sampai jumpa!")
      break


if __name__ == "__main__":
  main()