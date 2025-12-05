# -*- coding: utf-8 -*-
import pandas as pd

# === CONFIGURACIÓN ===
archivo_excel = "BASE_GYM.xlsx"
nombre_hoja = "BASE DE DATOS"
fila_encabezado = 4
archivo_salida = "clientes_insert.sql"

# === CARGAR ARCHIVO EXCEL ===
print("📂 Leyendo hoja:", nombre_hoja)
df = pd.read_excel(archivo_excel, sheet_name=nombre_hoja, header=fila_encabezado)

# === LIMPIEZA BÁSICA ===
df = df.dropna(how="all")
df = df.dropna(axis=1, how="all")
df = df.loc[:, ~df.columns.astype(str).str.contains("Unnamed", case=False)]

print("✅ Columnas detectadas:", list(df.columns))

# === RENOMBRAR COLUMNAS ===
df.columns = [
    "cedula",
    "nombre",
    "telefono",
    "forma_pago",
    "valor_pagar",
    "numero_recibo",
    "fecha_ingreso",
    "fecha_retiro",
    "correo",
    "valoracion_fisica",
    "dias_faltantes",
    "estatus",
    "saldo"
]

# === LIMPIAR DATOS ===
# Quitar espacios extra
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Eliminar filas con cedula vacía o inválida
df = df[df["cedula"].notna()]                      # elimina nulos
df = df[df["cedula"].astype(str).str.strip() != ""] # elimina vacíos o espacios
df = df[df["nombre"].astype(str).str.strip() != ""] # elimina filas sin nombre

df["saldo"] = df["saldo"].fillna(0)

for col in ["fecha_ingreso", "fecha_retiro"]:
    df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%d")

print(f"🧮 Generando SQL para {len(df)} registros válidos...")

# === GENERAR INSERTS ===
with open(archivo_salida, "w", encoding="utf-8") as f:
    f.write("-- Inserción de clientes para gymwork\n")
    f.write("USE gymwork;\n")
    f.write("DELETE FROM clientes;\n\n")

    for _, row in df.iterrows():
        valores = []
        for val in [
            row["cedula"], row["nombre"], row["telefono"], row["forma_pago"], row["valor_pagar"],
            row["numero_recibo"], row["fecha_ingreso"], row["fecha_retiro"], row["correo"],
            row["valoracion_fisica"], row["dias_faltantes"], row["estatus"], row["saldo"]
        ]:
            if pd.isna(val) or str(val).strip() == "":
                valores.append("NULL")
            elif isinstance(val, str):
                valores.append("'" + val.replace("'", "''") + "'")
            else:
                valores.append("'" + str(val) + "'")

        insert = (
            "INSERT INTO clientes "
            "(cedula, nombre, telefono, forma_pago, valor_pagar, numero_recibo, fecha_ingreso, fecha_retiro, correo, valoracion_fisica, dias_faltantes, estatus, saldo) "
            f"VALUES ({', '.join(valores)});\n"
        )
        f.write(insert)

print(f"✅ Archivo '{archivo_salida}' generado con éxito con {len(df)} registros válidos.")
