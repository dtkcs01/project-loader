DOT: "."
COMMA: ","
ALPHA: /[a-zA-Z_]/
DIGIT: /[0-9]/

ID: ALPHA (ALPHA|DIGIT)*
COMMENT: /"""([^"]|("{1,2}))*"""/
 | /'''([^']|('{1,2}))*'''/

LF: /\n/
CR: /\r/
NEWLINE: LF | (CR LF)
