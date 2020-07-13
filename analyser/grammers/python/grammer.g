start: import
import: (FROM id_seq)? (IMPORT (id_seq|"*")) (AS ID)?
id_seq: id_ext (COMMA_OP id_ext)*
id_ext: ID (DOT_OP ID)*
