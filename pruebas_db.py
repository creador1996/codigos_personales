import sqlite3
import datetime

class fields():
    value = ""
    type_field = ""
    required = False
    readonly = False
    def __init__(self, type_field, required=False, readonly=False):        
        self.type_field = type_field
        self.required = required
        self.readonly = readonly
    def __str__(self):
        return self.value

def get_columns(dict):
    result = ''
    for key, value in dict.items():
        result += "{} {}".format(key, value.type_field)
        if value.required:
            result += " NOT NULL"
        result += ",\n"
    return result[0:-2]

def create_table(name, dict):
    conn = sqlite3.connect("/home/pedro/Documentos/pruebas_db.db")
    cur = conn.cursor()
    sql = "CREATE TABLE IF NOT EXISTS {}({})".format(name, get_columns(dict))
    cur.execute(sql)
    conn.commit()
    conn.close()

def add_columns(table, dict):
    conn = sqlite3.connect("/home/pedro/Documentos/pruebas_db.db")
    cur = conn.cursor()
    for key, value in dict.items():
        sql = ""
        sql_verify = (
            "SELECT * FROM sqlite_master WHERE type = 'table' AND name = "
            + "'{}' AND sql LIKE '%{}%'".format(
                table,
                key
            )
        )
        cur.execute(sql_verify)
        verify = cur.fetchone()
        if not verify:
            sql = "alter table {} add column {} {}".format(
                table,
                key,
                value.type_field
            )
            if value.required:
                sql += " NOT NULL DEFAULT False"
            cur.execute(sql)
            conn.commit()
    conn.close()

pokemon = {
    "nombre": fields("CHAR", required=True),
    "tipo_1": fields("CHAR", required=True),
    "tipo_2": fields("CHAR", required=True),
    "habilidad": fields("CHAR", required=True),
    "fecha": fields("DATE", required=True),
    "vida": fields("INT", required=True),
    "ataque": fields("INT", required=True),
    "ataque_especial": fields("INT", required=True),
    "defensa": fields("INT", required=True),
    "defensa_especial": fields("INT", required=True),
    "velocidad": fields("INT", required=True),
    "tecnica_1": fields("CHAR"),
    "tecnica_2": fields("CHAR"),
    "tecnica_3": fields("CHAR"),
    "tecnica_4": fields("CHAR"),
    "genero": fields("CHAR")
}
add_columns("entrenador", {
    "segundo_nombre": fields("CHAR"),
    "segundo_apellido": fields("CHAR"),
    "bici": fields("BOOLEAN")
})
create_table("pokemon", pokemon)
