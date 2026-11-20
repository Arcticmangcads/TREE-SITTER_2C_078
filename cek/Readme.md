# cek.py

Pemeriksa kode Python sederhana berbasis [Tree-sitter](https://tree-sitter.github.io/).
Dibuat untuk Tugas 6 Programming Language Pragmatics.

## Fitur

1. **Komentar `TODO` / `FIXME`.** Diambil dari node `comment`, jadi teks "TODO" di dalam string tidak ikut terhitung.
2. **Fungsi terlalu panjang.** Fungsi dengan lebih dari 30 baris dilaporkan beserta jumlah barisnya.
3. **Error sintaks.** File yang tidak bisa di-parse dengan benar dilaporkan beserta baris error pertamanya.

## Pasang

```bash
pip install tree-sitter tree-sitter-python
```

Membutuhkan Python 3.10 atau lebih baru.

## Jalankan

```bash
python cek.py <folder>
```

Semua file `*.py` di dalam folder (termasuk subfolder) diperiksa. Folder `venv`, `.venv`, `.git`, `node_modules`, dan `__pycache__` dilewati. Jalankan dari terminal, bukan tombol Run editor, karena skrip membutuhkan argumen folder.

## Contoh output

Pada folder uji `uji/`:

```
uji/a_todo.py:1: # TODO: validasi input pengguna
uji/a_todo.py:3: # FIXME: hasil salah untuk x negatif
uji/b_panjang.py:1: fungsi proses terlalu panjang (41 baris)
uji/c_rusak.py:1: ERROR sintaks
uji/sub/e_bersarang.py:3: # TODO: pindahkan ke modul lain

Selesai: 5 file diperiksa, 5 temuan.
```

Pada repo open source [karpathy/minGPT](https://github.com/karpathy/minGPT) (commit `<hash>`, 9 file, 12 temuan). Cuplikan:

```
mingpt/trainer.py:61: fungsi run terlalu panjang (49 baris)
mingpt/utils.py:33: # TODO: convert to subclass from a dict like in yacs?
mingpt/utils.py:34: # TODO: implement freezing to prevent shooting of own foot
mingpt/utils.py:35: # TODO: additional existence/override checks when reading/writing params?
mingpt/utils.py:62: fungsi merge_from_args terlalu panjang (42 baris)
...
Selesai: 9 file diperiksa, 12 temuan.
```

Hasil ini dicocokkan manual: ketiga TODO di `utils.py` sama dengan hasil pencarian teks, dan `run` di `trainer.py` memang membentang baris 61-109 (49 baris).

## Cara kerja

Setiap file diproses dengan pola **parse, query, laporkan**:

1. File di-parse menjadi pohon sintaks oleh `tree-sitter-python`.
2. Query Tree-sitter mengambil node yang dicari: `comment` yang cocok dengan `TODO|FIXME`, dan semua `function_definition`.
3. Panjang fungsi dihitung dari `end_point[0] - start_point[0] + 1`.
4. File bermasalah ditandai `has_error`, lalu pohon ditelusuri untuk menemukan node `ERROR` atau `MISSING` pertama.

Hasil `captures` tidak dijamin terurut menurut posisi, sehingga komentar diurutkan berdasarkan `start_byte` sebelum dicetak.

## Struktur

```
cek/
├── cek.py
├── README.md
└── uji/
    ├── a_todo.py
    ├── b_panjang.py
    ├── c_rusak.py
    ├── d_bersih.py
    ├── sub/e_bersarang.py
    └── venv/lib.py      # sengaja dilewati
```

## Keterbatasan

- Fungsi bersarang dan method kelas ikut dihitung sebagai fungsi.
- Hanya error sintaks pertama per file yang dilaporkan.
- Batas 30 baris bersifat tetap (konstanta `BATAS_BARIS`), belum bisa diubah lewat argumen.
- Hanya memeriksa file Python.