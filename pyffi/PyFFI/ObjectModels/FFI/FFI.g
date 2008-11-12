grammar FFI;

options {
    //language = Python;
    output=AST;
    ASTLabelType=CommonTree;
}

tokens {
    // emitted when indentation increases
    // see NEWLINE for details
    INDENT;
    // emitted when indentation decreases
    // see NEWLINE for details
    DEDENT;
    // keywords
    CLASS='class';
    FILEFORMAT='fileformat';
    PARAMETER='parameter';
    TYPE='type';
}

// target specific code
// ====================

// current_indent: lexer variable which measures the current indentation level
// NEWLINE: special lexer token which works as follows
//    indentation increased by one level: emit INDENT
//    indentation remained the same: emit NEWLINE
//    indentation decreased (by any level): emit DEDENT as many as decreased

// JAVA

/* */

@lexer::members {
    // keep track of indentation
    int current_indent = 0;
    
    // allow multiple tokens to be emitted
    // (see http://www.antlr.org/wiki/pages/viewpage.action?pageId=3604497)
    List tokens = new ArrayList();
    public void emit(Token token) {
        state.token = token;
        tokens.add(token);
    }
    public Token nextToken() {
        super.nextToken();
        if ( tokens.size()==0 ) {
            return Token.EOF_TOKEN;
        }
        return (Token)tokens.remove(0);
    }
}

NEWLINE
@init {
    int indent = 0;
}
    :
        (
            (('\f')? ('\r')? '\n'
                {
                    emit(new ClassicToken(NEWLINE, "\n"));
                }
            )
            |
            ' ')*
        (('\f')? ('\r')? '\n'
            {
                emit(new ClassicToken(NEWLINE, "\n"));
            }
        )
        ('    '
        {
            indent++;
        }
        )*
        {
            if (indent == current_indent + 1) {
                current_indent++;
                emit(new ClassicToken(INDENT, ">"));
            }
            else if (indent == current_indent) {
                // nothing happens, newline already emitted
            }
            else if (indent < current_indent) {
                while (indent < current_indent) {
                    current_indent--;
                    emit(new ClassicToken(DEDENT, "<"));
                }
            }
            else {
                throw new RuntimeException("bad indentation");
            }
        }
    ;

/* */

// PYTHON
// note: ANTLR defines Python members on class level, but we want to define an
//       instance variable, not a class variable, hence it must go in __init__
//       so we declare the member in __init__

/*

@lexer::init {
    self.current_indent = 0
}

// TODO multiple tokens per lexical symbol

@lexer::members {
}

NEWLINE
@init {
    indent = 0
}
    :
        ((('\f')? ('\r')? '\n') | ' ')*
        (('\f')? ('\r')? '\n')
        ('    '
            {
                indent += 1
            }
        )*
        {   
            if (indent == self.current_indent + 1):
                self.current_indent += 1
                self.emit(ClassicToken(INDENT, ">"))
            elif indent == self.current_indent:
                self.emit(ClassicToken(NEWLINE, "\n"))
            elif indent < self.current_indent:
                while indent < self.current_indent:
                    self.current_indent -= 1
                    self.emit(ClassicToken(DEDENT, "<"))
            else:
                raise RuntimeError("bad indentation")
        }
    ;

*/

/*------------------------------------------------------------------
 * PARSER RULES
 *------------------------------------------------------------------*/

ffi
    :   formatdef declarations EOF
    ;

formatdef
    :   longdoc FILEFORMAT FORMATNAME shortdoc
    ;

declarations
    :   typeblock? parameterblock? classblock*
    ;

// short documentation following a definition, followed by one or more newlines
// because short style documentation always should come at the end of a definition,
// it includes the newline(s) that follow the definition (this makes the other parser
// rules a bit simpler)
shortdoc
    :   SHORTDOC? NEWLINE+
    ;

// documentation preceeding a definition, with single newline following each line of text
// the number of lines in the documentation is arbitrary, also zero lines is possible (i.e.
// no documentation at all)
longdoc
    :   (SHORTDOC NEWLINE)*
    ;

typeblock
    :   TYPE blockbegin typedef+ blockend
    ;

parameterblock
    :   PARAMETER blockbegin fielddef+ blockend
    ;

classblock
    :   longdoc CLASS TYPENAME blockbegin declarations fielddef+ blockend
    ;

blockbegin
    :   COLON NEWLINE INDENT
    ;

blockend
    :   DEDENT
    ;

typedef
    :   longdoc TYPENAME shortdoc // basic type
    |   longdoc TYPENAME '=' TYPENAME shortdoc // alias
    ;

fielddef
    :    longdoc TYPENAME VARIABLENAME shortdoc
    ;

/*------------------------------------------------------------------
 * LEXER RULES
 *------------------------------------------------------------------*/

// whitespace and comments

// documentation following a definition, no newline
// (on the same line of the definition)
SHORTDOC
    :   '#' ~('\n')*
    ;

fragment
DIGIT
    :   '0'..'9'
    ;

fragment
DIGITS  :   DIGIT+
    ;

INT
    // hex
    :   '0x' ( '0' .. '9' | 'a' .. 'f' | 'A' .. 'F' )+
    // octal
    |   '0o' ( '0' .. '7')+
    // binary
    |   '0b' ( '0' .. '1')+
    // decimal
    |   DIGITS+
    ;

fragment
EXPONENT
    :    'e' ( '+' | '-' )? DIGITS
    ;

FLOAT
    :   DIGITS '.' DIGITS EXPONENT?
    ;

COLON
    :   ':'
    ;

fragment
LCLETTER:   'a'..'z'
    ;

fragment
UCLETTER:   'A'..'Z'
    ;

// UPPERCASE for format name

FORMATNAME
    :   UCLETTER (UCLETTER | DIGITS)*
    ;

// lower_case_with_underscores for variable names (e.g. fields)
VARIABLENAME
    :   LCLETTER (LCLETTER | DIGITS | '_')*
    ;

// CamelCase for type names
TYPENAME
    :   UCLETTER (LCLETTER | UCLETTER | DIGITS)*
    ;

STRING
    :   '"' (ESC|~('\\'|'\n'|'"'))* '"'
    ;

fragment
ESC
    :   '\\' .
    ;

// ignore whitespace
WS
    :   (' ')+ { $channel=HIDDEN; }
    ;
