import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

potongan = {
    "fungsi": b"def sapa(nama):\n    return nama\n",
    "if_else": b"if x > 0:\n    y = 1\nelse:\n    y = 2\n",
    "kelas": b"class Hewan:\n    def bicara(self):\n        return 'halo'\n",
    "rusak": b"def sapa(nama)\n    return nama\n",   # sengaja tanpa ':'
}

for judul, kode in potongan.items():
    tree = parser.parse(kode)
    print(f"=== {judul} ===")
    print(tree.root_node)
    print("has_error:", tree.root_node.has_error)

    # node anonim vs bernama pada child pertama root (def/if/class)
    for c in tree.root_node.children[0].children:
        print("  ", c.type, "bernama" if c.is_named else "anonim")
    print()