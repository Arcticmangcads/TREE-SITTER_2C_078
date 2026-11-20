import tree_sitter_python as tspython
from tree_sitter import Language, Parser
parser = Parser(Language(tspython.language()))
print(parser.parse(b"def halo(nama):\n    return nama\n").root_node)