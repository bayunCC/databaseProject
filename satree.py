import ply.lex as lex
import ply.yacc as yacc

# 定义词法单元
tokens = (
    'SELECT',
    'FROM',
    'WHERE',
    'AND',
    'ID',
    'EQUAL',
)

# 定义词法规则
t_SELECT = r'SELECT'
t_FROM = r'FROM'
t_WHERE = r'WHERE'
t_AND = r'AND'
t_ID = r'\w+'
t_EQUAL = r'='

# 忽略空格和制表符
t_ignore = ' \t'

# 定义错误处理函数
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# 构建词法分析器
lexer = lex.lex()

# 定义语法规则
def p_query(p):
    '''query : SELECT ID FROM ID WHERE condition'''
    p[0] = ('SELECT', p[2], 'FROM', p[4], 'WHERE', p[6])

def p_condition(p):
    '''condition : atomic_condition
                 | atomic_condition AND condition'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_atomic_condition(p):
    '''atomic_condition : ID EQUAL ID'''
    p[0] = (p[1], p[2], p[3])

def p_error(p):
    print("Syntax error in input!")

# 构建语法分析器
parser = yacc.yacc()

# 输入一个完整的SQL查询语句
sql_query = input("请输入SQL查询语句：")

# 执行语法分析并输出语法分析树
result = parser.parse(sql_query)
print(result)
