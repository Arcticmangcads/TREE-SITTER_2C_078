import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

BATAS_BARIS = 30
SKIP = {"venv", ".venv", ".git", "node_modules", "__pycache__"}

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNC = Query(PY, "(function_definition name: (identifier) @nama) @fungsi")


def cari_error(node):
    """Cari node ERROR / MISSING pertama (paling awal) di dalam pohon."""
    if node.is_error or node.is_missing:
        return node
    for c in node.children:
        if c.has_error or c.is_missing:
            hasil = cari_error(c)
            if hasil:
                return hasil
    return None


def cek_file(path):
    temuan = 0
    tree = parser.parse(path.read_bytes())

    # Fitur 1: komentar TODO / FIXME
    nodes = QueryCursor(Q_TODO).captures(tree.root_node).get("c", [])
    for node in sorted(nodes, key=lambda n: n.start_byte):
        teks = node.text.decode(errors="replace").strip()
        print(f"{path}:{node.start_point[0] + 1}: {teks}")
        temuan += 1

    # Fitur 2: fungsi lebih dari BATAS_BARIS baris
    for _, cap in QueryCursor(Q_FUNC).matches(tree.root_node):
        fn = cap["fungsi"][0]
        nama = cap["nama"][0].text.decode()
        jumlah = fn.end_point[0] - fn.start_point[0] + 1
        if jumlah > BATAS_BARIS:
            print(f"{path}:{fn.start_point[0] + 1}: fungsi {nama} terlalu panjang ({jumlah} baris)")
            temuan += 1

    # Fitur 3: file dengan error sintaks
    if tree.root_node.has_error:
        err = cari_error(tree.root_node)
        baris = err.start_point[0] + 1 if err else "?"
        print(f"{path}:{baris}: ERROR sintaks")
        temuan += 1

    return temuan


def main():
    if len(sys.argv) < 2:
        print("Pemakaian: python cek.py <folder>")
        sys.exit(1)

    akar = Path(sys.argv[1])
    if not akar.is_dir():
        print(f"Folder tidak ditemukan: {akar}")
        sys.exit(1)

    jumlah_file = 0
    jumlah_temuan = 0
    for path in sorted(akar.rglob("*.py")):
        if SKIP & set(path.parts):
            continue
        jumlah_file += 1
        jumlah_temuan += cek_file(path)

    print(f"\nSelesai: {jumlah_file} file diperiksa, {jumlah_temuan} temuan.")


if __name__ == "__main__":
    main()