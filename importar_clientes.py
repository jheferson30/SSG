import pandas as pd
import mysql.connector

# === CONFIGURACIÓN DE CONEXIÓN A MySQL ===
conn = mysql.connector.connect(
    host="localhost",
    user="root",          # cambia si tu usuario no es root
    password="",          # pon tu contraseña si tiene
    database="gymwork"
)
cursor = conn.cursor()

# === CREAR TABLA SI NO EXISTE ===
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cedula VARCHAR(50),
    nombre VARCHAR(255),
    telefono VARCHAR(50),
    direccion VARCHAR(255),
    fecha_inicio DATE,
    fecha_fin DATE,
    dias_faltantes INT,
    estatus VARCHAR(50),
    saldo DECIMAL(10,2) NULL
);
""")
print("✅ Tabla 'clientes' verificada o creada correctamente.\n")

# === LEER ARCHIVO EXCEL ===
ruta_excel = "Copia de Formato_Base_de_Datos_Gym_Work.xlsb(1).xlsm"
print("📂 Leyendo datos desde el archivo Excel...")

# Saltar las primeras 5 filas (encabezados decorativos)
df = pd.read_excel(ruta_excel, sheet_name="BASE DE DATOS", header=4)

# Limpiar columnas vacías o sin nombre
df = df.loc[:, ~df.columns.astype(str).str.contains('^Unnamed', case=False, na=False)]

print("✅ Columnas detectadas:", df.columns.tolist())

# === RENOMBRAR COLUMNAS (según lo que muestra tu archivo) ===
df = df.rename(columns={
    "TI/CC/NIT": "cedula",
    "NOMBRES Y APELLIDOS": "nombre",
    "TELEFONO/CELULAR": "telefono",
    "DIRECCION": "direccion",
    "FECHA INICIO": "fecha_inicio",
    "FECHA FIN": "fecha_fin",
    "DIAS FALTANTES": "dias_faltantes",
    "ESTATUS": "estatus",
    "SALDOS": "saldo"
})

# === QUEDARSE SOLO CON LAS COLUMNAS NECESARIAS ===
columnas_finales = [
    "cedula", "nombre", "telefono", "direccion",
    "fecha_inicio", "fecha_fin", "dias_faltantes", "estatus", "saldo"
]

df = df[columnas_finales]
print(f"✅ {len(df)} registros encontrados.\n")

# === LIMPIAR DATOS ===
df = df.dropna(subset=["cedula", "nombre"])
df["saldo"] = df["saldo"].fillna(0)

# === INSERTAR EN MYSQL ===
insert_query = """
INSERT INTO clientes (cedula, nombre, telefono, direccion, fecha_inicio, fecha_fin, dias_faltantes, estatus, saldo)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

for _, fila in df.iterrows():
    try:
        cursor.execute(insert_query, tuple(fila))
    except Exception as e:
        print(f"⚠️ Error con {fila['nombre']}: {e}")

conn.commit()
print(f"✅ Se importaron correctamente {cursor.rowcount} registros a MySQL.")

cursor.close()
conn.close()
print("🚀 Importación finalizada.")
