import sys
import tkinter as tk
from tkinter import messagebox, ttk

import main as core


def atur_dpi_windows():
  if sys.platform != "win32":
    return

  import ctypes

  try:
    set_awareness = ctypes.windll.user32.SetProcessDpiAwarenessContext
  except AttributeError:
    try:
      set_awareness = ctypes.windll.shcore.SetProcessDpiAwareness
    except AttributeError:
      ctypes.windll.user32.SetProcessDPIAware()
    else:
      set_awareness(2)
  else:
    set_awareness.argtypes = [ctypes.c_void_p]
    set_awareness.restype = ctypes.c_bool
    set_awareness(ctypes.c_void_p(-4))


class AplikasiKalori:
  WARNA = {
      "latar": "#f4f7f2",
      "putih": "#ffffff",
      "hijau": "#176b52",
      "hijau_gelap": "#124b3b",
      "hijau_muda": "#e5f2eb",
      "teks": "#20332b",
      "redup": "#718078",
      "garis": "#e2e9e3",
      "jingga": "#f3a45b",
      "merah": "#c95555",
  }

  KATEGORI = (
      "Semua kategori",
      "Makanan sehat",
      "Junk food",
      "Minuman",
      "Lainnya",
  )
  HARI = (
      "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"
  )
  BULAN = (
      "Januari", "Februari", "Maret", "April", "Mei", "Juni",
      "Juli", "Agustus", "September", "Oktober", "November", "Desember",
  )

  def __init__(self, root):
    self.root = root
    self.root.title("KaloriKu - Pelacak Kalori Harian")
    self.root.geometry("1120x740")
    self.root.minsize(900, 620)
    self.root.configure(bg=self.WARNA["latar"])

    self.profil = core.muat_profil()
    self.daftar_makanan = core.baca_makanan_csv()
    self.halaman = "Beranda"
    self.nav_buttons = {}
    self._atur_style()
    self._buat_layout()
    self.tampilkan_halaman("Profil" if self.profil is None else "Beranda")

  def _atur_style(self):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background=self.WARNA["putih"],
        foreground=self.WARNA["teks"],
        fieldbackground=self.WARNA["putih"],
        rowheight=34,
        borderwidth=0,
        font=("Segoe UI", 10),
    )
    style.configure(
        "Treeview.Heading",
        background=self.WARNA["latar"],
        foreground=self.WARNA["redup"],
        font=("Segoe UI", 9, "bold"),
        relief="flat",
      )
    style.map(
        "Treeview",
        background=[("selected", self.WARNA["hijau_muda"])],
        foreground=[("selected", self.WARNA["teks"])],
    )
    style.configure(
        "TCombobox",
        padding=8,
        fieldbackground=self.WARNA["putih"],
        background=self.WARNA["putih"],
    )

  def _buat_layout(self):
    self.sidebar = tk.Frame(
        self.root, bg=self.WARNA["hijau_gelap"], width=225
    )
    self.sidebar.pack(side="left", fill="y")
    self.sidebar.pack_propagate(False)

    tk.Label(
        self.sidebar,
        text="🍃  KaloriKu",
        bg=self.WARNA["hijau_gelap"],
        fg="white",
        font=("Segoe UI", 19, "bold"),
    ).pack(anchor="w", padx=24, pady=(30, 4))
    tk.Label(
        self.sidebar,
        text="Teman hidup lebih seimbang",
        bg=self.WARNA["hijau_gelap"],
        fg="#b7d3c6",
        font=("Segoe UI", 9),
    ).pack(anchor="w", padx=26, pady=(0, 32))

    for nama, ikon in (
        ("Beranda", "⌂"),
        ("Catat makanan", "+"),
        ("Rekomendasi", "✦"),
        ("Riwayat", "▤"),
        ("Profil", "○"),
    ):
      button = tk.Button(
          self.sidebar,
          text=f"  {ikon}   {nama}",
          anchor="w",
          relief="flat",
          bd=0,
          padx=18,
          pady=12,
          bg=self.WARNA["hijau_gelap"],
          fg="#dce9e2",
          activebackground=self.WARNA["hijau"],
          activeforeground="white",
          font=("Segoe UI", 10, "bold"),
          command=lambda page=nama: self.tampilkan_halaman(page),
      )
      button.pack(fill="x", padx=12, pady=3)
      self.nav_buttons[nama] = button

    tk.Label(
        self.sidebar,
        text="MAKAN LEBIH SADAR\nSatu langkah setiap hari.",
        justify="left",
        bg=self.WARNA["hijau_gelap"],
        fg="#b7d3c6",
        font=("Segoe UI", 9),
    ).pack(side="bottom", anchor="w", padx=25, pady=26)

    self.area = tk.Frame(self.root, bg=self.WARNA["latar"])
    self.area.pack(side="left", fill="both", expand=True)

  def _kartu(self, parent, title, value, subtitle, color):
    card = tk.Frame(
        parent,
        bg=self.WARNA["putih"],
        highlightthickness=1,
        highlightbackground=self.WARNA["garis"],
    )
    tk.Frame(card, bg=color, width=4).pack(side="left", fill="y")
    content = tk.Frame(card, bg=self.WARNA["putih"])
    content.pack(side="left", fill="both", expand=True, padx=18, pady=16)
    tk.Label(
        content,
        text=title.upper(),
        bg=self.WARNA["putih"],
        fg=self.WARNA["redup"],
        font=("Segoe UI", 9, "bold"),
    ).pack(anchor="w")
    tk.Label(
        content,
        text=value,
        bg=self.WARNA["putih"],
        fg=self.WARNA["teks"],
        font=("Segoe UI", 22, "bold"),
    ).pack(anchor="w", pady=(5, 2))
    tk.Label(
        content,
        text=subtitle,
        bg=self.WARNA["putih"],
        fg=self.WARNA["redup"],
        font=("Segoe UI", 9),
    ).pack(anchor="w")
    return card

  def _judul_halaman(self, title, subtitle):
    header = tk.Frame(self.area, bg=self.WARNA["latar"])
    header.pack(fill="x", padx=32, pady=(27, 20))
    tk.Label(
        header,
        text=title,
        bg=self.WARNA["latar"],
        fg=self.WARNA["teks"],
        font=("Segoe UI", 23, "bold"),
    ).pack(anchor="w")
    tk.Label(
        header,
        text=subtitle,
        bg=self.WARNA["latar"],
        fg=self.WARNA["redup"],
        font=("Segoe UI", 10),
    ).pack(anchor="w", pady=(4, 0))

  def _tombol(self, parent, text, command, secondary=False):
    return tk.Button(
        parent,
        text=text,
        command=command,
        relief="flat",
        bd=0,
        padx=18,
        pady=10,
        bg=self.WARNA["hijau_muda"] if secondary else self.WARNA["hijau"],
        fg=self.WARNA["hijau_gelap"] if secondary else "white",
        activebackground="#cfe7d8" if secondary else self.WARNA["hijau_gelap"],
        activeforeground=self.WARNA["hijau_gelap"] if secondary else "white",
        font=("Segoe UI", 9, "bold"),
        cursor="hand2",
    )

  def _isi_halaman(self):
    for widget in self.area.winfo_children():
      widget.destroy()

  def tampilkan_halaman(self, nama):
    self.halaman = nama
    for page, button in self.nav_buttons.items():
      active = page == nama
      button.configure(
          bg=self.WARNA["hijau"] if active else self.WARNA["hijau_gelap"],
          fg="white" if active else "#dce9e2",
      )
    self._isi_halaman()
    if nama == "Beranda":
      self._halaman_beranda()
    elif nama == "Catat makanan":
      self._halaman_catat()
    elif nama == "Rekomendasi":
      self._halaman_rekomendasi()
    elif nama == "Riwayat":
      self._halaman_riwayat()
    else:
      self._halaman_profil()

  def _data_hari_ini(self):
    catatan = core.muat_catatan().get(str(core.date.today()), [])
    total = sum(item["kalori"] for item in catatan)
    target = core.hitung_target(self.profil) if self.profil else 0
    return catatan, total, target

  def _halaman_beranda(self):
    self._judul_halaman(
        "Ringkasan harian",
        f"Pantau asupanmu hari ini · {self._format_tanggal(core.date.today())}",
    )
    if not self.profil:
      self._tombol(
          self.area, "Lengkapi profil", lambda: self.tampilkan_halaman("Profil")
      ).pack(anchor="w", padx=32)
      return

    catatan, total, target = self._data_hari_ini()
    sisa = max(target - total, 0)
    cards = tk.Frame(self.area, bg=self.WARNA["latar"])
    cards.pack(fill="x", padx=32)
    for index, card in enumerate((
        self._kartu(cards, "Target kalori", f"{target:,}", "kkal per hari", self.WARNA["hijau"]),
        self._kartu(cards, "Sudah dikonsumsi", f"{total:,.0f}", "kkal hari ini", self.WARNA["jingga"]),
        self._kartu(cards, "Sisa kalori", f"{sisa:,.0f}", "kkal tersedia", "#5c9cc5"),
    )):
      card.grid(row=0, column=index, sticky="nsew", padx=(0, 12 if index < 2 else 0))
      cards.grid_columnconfigure(index, weight=1)

    progress_card = tk.Frame(
        self.area,
        bg=self.WARNA["putih"],
        highlightthickness=1,
        highlightbackground=self.WARNA["garis"],
    )
    progress_card.pack(fill="x", padx=32, pady=18)
    tk.Label(
        progress_card,
        text="Perjalanan hari ini",
        bg=self.WARNA["putih"],
        fg=self.WARNA["teks"],
        font=("Segoe UI", 12, "bold"),
    ).pack(anchor="w", padx=20, pady=(17, 5))
    persen = min(total / target * 100, 100) if target else 0
    tk.Label(
        progress_card,
        text=f"{persen:.0f}% dari target harian",
        bg=self.WARNA["putih"],
        fg=self.WARNA["redup"],
        font=("Segoe UI", 9),
    ).pack(anchor="w", padx=20)
    bar = tk.Canvas(progress_card, height=12, bg=self.WARNA["putih"], highlightthickness=0)
    bar.pack(fill="x", padx=20, pady=(9, 18))
    bar.update_idletasks()
    width = max(bar.winfo_width(), 1)
    bar.create_rectangle(0, 2, width, 11, fill="#e9f0eb", outline="")
    bar.create_rectangle(0, 2, width * persen / 100, 11, fill=self.WARNA["hijau"], outline="")

    title_row = tk.Frame(self.area, bg=self.WARNA["latar"])
    title_row.pack(fill="x", padx=32, pady=(2, 10))
    tk.Label(
        title_row,
        text="Asupan terbaru",
        bg=self.WARNA["latar"],
        fg=self.WARNA["teks"],
        font=("Segoe UI", 13, "bold"),
    ).pack(side="left")
    self._tombol(
        title_row, "+ Catat makanan", lambda: self.tampilkan_halaman("Catat makanan")
    ).pack(side="right")
    tree = self._buat_tabel(
        self.area,
        ("jam", "nama", "porsi", "kalori"),
        ("Jam", "Makanan / minuman", "Porsi", "Kalori"),
        height=7,
    )
    start_index = max(0, len(catatan) - 7)
    for index in range(len(catatan) - 1, start_index - 1, -1):
      entry = catatan[index]
      tree.insert(
          "", "end", iid=str(index),
          values=(
              entry.get("jam", ""),
              entry["nama"],
              entry.get("porsi", 1),
              f'{entry["kalori"]:,.0f} kkal',
          ),
      )
    actions = tk.Frame(self.area, bg=self.WARNA["latar"])
    actions.pack(fill="x", padx=32, pady=(0, 16))

    def delete_selected():
      selection = tree.selection()
      if not selection:
        messagebox.showwarning(
            "Pilih catatan", "Pilih catatan yang ingin dihapus."
        )
        return
      if not messagebox.askyesno(
          "Hapus catatan", "Yakin ingin menghapus catatan yang dipilih?"
      ):
        return
      try:
        deleted = core.hapus_catatan_hari_ini(int(selection[0]))
      except OSError as error:
        messagebox.showerror(
            "Gagal menghapus", f"Catatan tidak dapat dihapus:\n{error}"
        )
        return
      if deleted:
        self.tampilkan_halaman("Beranda")
      else:
        messagebox.showerror(
            "Gagal menghapus", "Catatan sudah tidak ditemukan."
        )

    self._tombol(
        actions, "Hapus catatan terpilih", delete_selected, secondary=True
    ).pack(side="right")
    if not catatan:
      tk.Label(
          self.area,
          text="Belum ada makanan tercatat hari ini. Yuk mulai catat!",
          bg=self.WARNA["latar"],
          fg=self.WARNA["redup"],
          font=("Segoe UI", 10),
      ).pack(anchor="w", padx=34, pady=10)

  def _buat_tabel(self, parent, columns, headings, height=10):
    container = tk.Frame(parent, bg=self.WARNA["putih"])
    container.pack(fill="both", expand=True, padx=32, pady=(0, 16))
    tree = ttk.Treeview(
        container, columns=columns, show="headings", height=height
    )
    widths = (95, 300, 160, 120)
    for index, (column, heading) in enumerate(zip(columns, headings)):
      tree.heading(column, text=heading)
      tree.column(
          column,
          width=widths[index] if index < len(widths) else 130,
          anchor="w" if index in (0, 1) else "center",
      )
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return tree

  def _halaman_catat(self):
    self._judul_halaman(
        "Catat makanan",
        "Pilih dari daftar makanan untuk menghitung kalori secara otomatis.",
    )
    controls = tk.Frame(self.area, bg=self.WARNA["latar"])
    controls.pack(fill="x", padx=32, pady=(0, 12))
    tk.Label(
        controls, text="Cari", bg=self.WARNA["latar"], fg=self.WARNA["teks"],
        font=("Segoe UI", 9, "bold")
    ).pack(side="left")
    search = tk.StringVar()
    entry = ttk.Entry(controls, textvariable=search, width=30)
    entry.pack(side="left", padx=(8, 18), ipady=5)
    category = tk.StringVar(value="Semua kategori")
    ttk.Combobox(
        controls, textvariable=category, values=self.KATEGORI, state="readonly",
        width=20
    ).pack(side="left", ipady=3)

    tree = self._buat_tabel(
        self.area,
        ("nama", "kategori", "porsi", "kalori"),
        ("Nama", "Kategori", "Takaran saji", "Kalori"),
        height=12,
    )
    selected = {"item": None}

    def refresh(*_):
      tree.delete(*tree.get_children())
      query = search.get().strip().lower()
      chosen_category = category.get()
      for item in self.daftar_makanan:
        mapped_category = core.kategori_rekomendasi(item)
        if query not in item["nama"].lower():
          continue
        if chosen_category != "Semua kategori" and mapped_category != chosen_category:
          continue
        tree.insert(
            "", "end", values=(
                item["nama"], mapped_category, item["porsi"],
                f'{item["kalori"]:,.0f} kkal',
            ),
        )

    def select_item(_event=None):
      selected_rows = tree.selection()
      if selected_rows:
        values = tree.item(selected_rows[0], "values")
        selected["item"] = next(
            (item for item in self.daftar_makanan if item["nama"] == values[0]),
            None,
        )

    search.trace_add("write", refresh)
    category.trace_add("write", refresh)
    tree.bind("<<TreeviewSelect>>", select_item)
    refresh()

    footer = tk.Frame(self.area, bg=self.WARNA["latar"])
    footer.pack(fill="x", padx=32, pady=(0, 20))
    tk.Label(
        footer, text="Jumlah porsi", bg=self.WARNA["latar"],
        fg=self.WARNA["teks"], font=("Segoe UI", 9, "bold")
    ).pack(side="left")
    portion = tk.StringVar(value="1")
    ttk.Entry(footer, textvariable=portion, width=8).pack(
        side="left", padx=(8, 18), ipady=5
    )

    def save_food():
      item = selected["item"]
      if item is None or not tree.selection():
        messagebox.showwarning("Pilih makanan", "Pilih makanan dari daftar terlebih dahulu.")
        return
      try:
        count = float(portion.get().replace(",", "."))
        if count <= 0:
          raise ValueError
      except ValueError:
        messagebox.showerror("Porsi tidak valid", "Masukkan jumlah porsi lebih dari 0.")
        return
      try:
        core.simpan_catatan_baru(
            item["nama"], count, item["kalori"] * count
        )
      except OSError as error:
        messagebox.showerror("Gagal menyimpan", f"Catatan tidak dapat disimpan:\n{error}")
        return
      messagebox.showinfo("Berhasil", f"{item['nama']} berhasil dicatat.")
      self.tampilkan_halaman("Beranda")

    self._tombol(footer, "Simpan catatan", save_food).pack(side="left")
    self._tombol(
        footer, "Input manual", self._dialog_catatan_manual, secondary=True
    ).pack(side="left", padx=(10, 0))

  def _dialog_catatan_manual(self):
    dialog = tk.Toplevel(self.root)
    dialog.title("Catat secara manual")
    dialog.configure(bg=self.WARNA["latar"])
    dialog.resizable(False, False)
    dialog.transient(self.root)
    dialog.grab_set()
    tk.Label(
        dialog,
        text="Catat makanan manual",
        bg=self.WARNA["latar"],
        fg=self.WARNA["teks"],
        font=("Segoe UI", 15, "bold"),
    ).pack(anchor="w", padx=22, pady=(20, 12))

    fields = {}
    for label, key, default in (
        ("Nama makanan / minuman", "nama", ""),
        ("Jumlah porsi", "porsi", "1"),
        ("Total kalori (kkal)", "kalori", ""),
    ):
      tk.Label(
          dialog, text=label, bg=self.WARNA["latar"],
          fg=self.WARNA["redup"], font=("Segoe UI", 9, "bold")
      ).pack(anchor="w", padx=22)
      variable = tk.StringVar(value=default)
      ttk.Entry(dialog, textvariable=variable, width=36).pack(
          padx=22, pady=(4, 12), ipady=5
      )
      fields[key] = variable

    def save_manual():
      name = fields["nama"].get().strip()
      try:
        portion = float(fields["porsi"].get().replace(",", "."))
        calories = float(fields["kalori"].get().replace(",", "."))
        if not name or portion <= 0 or calories <= 0:
          raise ValueError
      except ValueError:
        messagebox.showerror(
            "Data tidak valid",
            "Isi nama, jumlah porsi, dan kalori dengan nilai lebih dari 0.",
            parent=dialog,
        )
        return
      try:
        core.simpan_catatan_baru(name, portion, calories)
      except OSError as error:
        messagebox.showerror(
            "Gagal menyimpan",
            f"Catatan tidak dapat disimpan:\n{error}",
            parent=dialog,
        )
        return
      dialog.destroy()
      messagebox.showinfo("Berhasil", f"{name} berhasil dicatat.")
      self.tampilkan_halaman("Beranda")

    self._tombol(dialog, "Simpan catatan", save_manual).pack(
        anchor="w", padx=22, pady=(0, 20)
    )

  def _halaman_rekomendasi(self):
    self._judul_halaman(
        "Rekomendasi makanan",
        "Temukan pilihan sesuai kategori dan sisa target kalori harianmu.",
    )
    if not self.profil:
      self._tombol(
          self.area, "Lengkapi profil untuk menghitung target",
          lambda: self.tampilkan_halaman("Profil")
      ).pack(anchor="w", padx=32)
      return
    _, total, target = self._data_hari_ini()
    remaining = target - total
    info = tk.Frame(self.area, bg=self.WARNA["hijau_muda"])
    info.pack(fill="x", padx=32, pady=(0, 16))
    tk.Label(
        info,
        text=f"Sisa target hari ini: {remaining:,.0f} kkal",
        bg=self.WARNA["hijau_muda"],
        fg=self.WARNA["hijau_gelap"],
        font=("Segoe UI", 12, "bold"),
    ).pack(anchor="w", padx=16, pady=13)

    controls = tk.Frame(self.area, bg=self.WARNA["latar"])
    controls.pack(fill="x", padx=32, pady=(0, 12))
    tk.Label(
        controls, text="Kategori", bg=self.WARNA["latar"],
        fg=self.WARNA["teks"], font=("Segoe UI", 9, "bold")
    ).pack(side="left")
    category = tk.StringVar(value="Makanan sehat")
    ttk.Combobox(
        controls, textvariable=category, values=self.KATEGORI, state="readonly",
        width=22
    ).pack(side="left", padx=(10, 14), ipady=3)
    tree = self._buat_tabel(
        self.area,
        ("nama", "kategori", "porsi", "kalori"),
        ("Nama", "Kategori", "Takaran saji", "Kalori"),
        height=14,
    )

    def refresh(*_):
      tree.delete(*tree.get_children())
      choices = []
      for item in self.daftar_makanan:
        item_category = core.kategori_rekomendasi(item)
        if category.get() != "Semua kategori" and item_category != category.get():
          continue
        if item["kalori"] <= remaining + 50:
          choices.append({
              **item,
              "kategori_tampilan": item_category,
              "selisih": abs(remaining - item["kalori"]),
          })
      choices.sort(key=core.atur_urutan_rekomendasi)
      for item in choices[:30]:
        tree.insert(
            "", "end", values=(
                item["nama"], item["kategori_tampilan"], item["porsi"],
                f'{item["kalori"]:,.0f} kkal',
            ),
        )
      if not choices:
        tree.insert(
            "", "end",
            values=("Belum ada pilihan yang sesuai sisa kalori", "", "", ""),
        )

    category.trace_add("write", refresh)
    refresh()

  def _halaman_riwayat(self):
    self._judul_halaman(
        "Riwayat kalori",
        "Catatan asupan harian selama 14 hari terakhir.",
    )
    records = core.muat_catatan()
    today = core.date.today()
    tree = self._buat_tabel(
        self.area,
        ("tanggal", "total", "catatan", "status"),
        ("Tanggal", "Total kalori", "Jumlah catatan", "Status"),
        height=16,
    )
    target = core.hitung_target(self.profil) if self.profil else 0
    for offset in range(14):
      day = today - core.timedelta(days=offset)
      entries = records.get(str(day), [])
      total = sum(item["kalori"] for item in entries)
      tree.insert(
          "", "end",
          values=(
              self._format_tanggal(day),
              f"{total:,.0f} kkal",
              len(entries),
              "Target tercapai" if total >= target and total else "Di bawah target",
          ),
      )

  def _halaman_profil(self):
    self._judul_halaman(
        "Profil & target",
        "Data profil digunakan untuk menghitung kebutuhan kalori harian.",
    )
    form = tk.Frame(
        self.area, bg=self.WARNA["putih"],
        highlightthickness=1, highlightbackground=self.WARNA["garis"]
    )
    form.pack(fill="x", padx=32, pady=(0, 20))
    content = tk.Frame(form, bg=self.WARNA["putih"])
    content.pack(fill="x", padx=24, pady=22)
    profile = self.profil or {
        "gender": "wanita", "umur": "", "berat": "", "tinggi": "",
        "aktivitas": "ringan", "tujuan": "jaga",
    }
    fields = {}

    def add_field(row, column, label, key, values=None):
      cell = tk.Frame(content, bg=self.WARNA["putih"])
      cell.grid(row=row, column=column, sticky="ew", padx=(0, 18), pady=9)
      tk.Label(
          cell, text=label, bg=self.WARNA["putih"],
          fg=self.WARNA["redup"], font=("Segoe UI", 9, "bold")
      ).pack(anchor="w", pady=(0, 5))
      value = tk.StringVar(value=str(profile[key]))
      if values:
        widget = ttk.Combobox(
            cell, textvariable=value, values=values, state="readonly"
        )
      else:
        widget = ttk.Entry(cell, textvariable=value)
      widget.pack(fill="x", ipady=6)
      fields[key] = value

    for col in range(2):
      content.grid_columnconfigure(col, weight=1)
    add_field(0, 0, "Jenis kelamin", "gender", ("wanita", "pria"))
    add_field(0, 1, "Umur (tahun)", "umur")
    add_field(1, 0, "Berat badan (kg)", "berat")
    add_field(1, 1, "Tinggi badan (cm)", "tinggi")
    add_field(
        2, 0, "Tingkat aktivitas", "aktivitas",
        ("sangat_ringan", "ringan", "sedang", "berat", "sangat_berat"),
    )
    add_field(2, 1, "Tujuan", "tujuan", ("turun", "jaga", "naik"))

    def save_profile():
      try:
        umur = int(fields["umur"].get())
        berat = float(fields["berat"].get().replace(",", "."))
        tinggi = float(fields["tinggi"].get().replace(",", "."))
        if not 10 <= umur <= 100:
          raise ValueError("Umur harus antara 10 sampai 100 tahun.")
        if not 20 <= berat <= 300:
          raise ValueError("Berat badan harus antara 20 sampai 300 kg.")
        if not 100 <= tinggi <= 250:
          raise ValueError("Tinggi badan harus antara 100 sampai 250 cm.")
      except ValueError as error:
        messagebox.showerror("Data tidak valid", str(error) or "Periksa kembali data angka.")
        return
      new_profile = {
          "gender": fields["gender"].get(),
          "umur": umur,
          "berat": berat,
          "tinggi": tinggi,
          "aktivitas": fields["aktivitas"].get(),
          "tujuan": fields["tujuan"].get(),
      }
      try:
        core.simpan_profil(new_profile)
      except OSError as error:
        messagebox.showerror("Gagal menyimpan", f"Profil tidak dapat disimpan:\n{error}")
        return
      self.profil = new_profile
      messagebox.showinfo(
          "Profil tersimpan",
          f"Target kalori harianmu sekitar {core.hitung_target(self.profil):,} kkal.",
      )
      self.tampilkan_halaman("Beranda")

    self._tombol(content, "Simpan profil", save_profile).grid(
        row=3, column=0, sticky="w", pady=(14, 0)
    )
    if self.profil:
      target = core.hitung_target(self.profil)
      tk.Label(
          self.area,
          text=f"Target harian saat ini: {target:,} kkal",
          bg=self.WARNA["latar"],
          fg=self.WARNA["hijau"],
          font=("Segoe UI", 11, "bold"),
      ).pack(anchor="w", padx=34)

  def _format_tanggal(self, day):
    return (
        f"{self.HARI[day.weekday()]}, {day.day} "
        f"{self.BULAN[day.month - 1]} {day.year}"
    )


def launch():
  atur_dpi_windows()
  root = tk.Tk()
  AplikasiKalori(root)
  root.mainloop()
