start: lines

lines: imports lines
  | /[.\n]/ lines
  | NEWLINE

imports: (FROM id_dot)? (IMPORT id_seq) (AS id_seq)? NEWLINE

id_seq: id_dot (COMMA id_dot)*
id_dot: ID? (DOT ID)*
  | DOT
