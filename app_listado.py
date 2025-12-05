# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request
import mysql.connector

app = Flask(__name__)

# === CONFIGURACIÓN BASE DE DATOS ===
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",       # agrega tu contraseña si tienes
    "database": "gymwork"
}

# === PLANTILLA HTML ===
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Listado de Clientes - GymWork</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #2c3e50, #4ca1af);
            color: #fff;
            margin: 0;
            padding: 0;
        }
        h1 {
            text-align: center;
            margin-top: 30px;
        }
        form {
            text-align: center;
            margin: 20px;
        }
        input[type="text"] {
            padding: 10px;
            width: 300px;
            border-radius: 5px;
            border: none;
        }
        button {
            padding: 10px 15px;
            border: none;
            background-color: #27ae60;
            color: white;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #2ecc71;
        }
        table {
            width: 95%;
            margin: 20px auto;
            border-collapse: collapse;
            background-color: rgba(255,255,255,0.1);
        }
        th, td {
            border: 1px solid rgba(255,255,255,0.2);
            padding: 10px;
            text-align: center;
        }
        th {
            background-color: rgba(0,0,0,0.3);
        }
        tr:hover {
            background-color: rgba(255,255,255,0.2);
        }
        .estatus-vigente { color: #2ecc71; font-weight: bold; }
        .estatus-vencido { color: #e74c3c; font-weight: bold; }
        .estatus-porvencer { color: #f1c40f; font-weight: bold; }
    </style>
</head>
<body>
    <h1>🏋️‍♂️ Listado de Clientes - GymWork</h1>
    <form method="GET" action="/">
        <input type="text" name="q" placeholder="Buscar por cédula o nombre..." value="{{ q }}">
        <button type="submit">🔍 Buscar</button>
    </form>

    <table>
        <tr>
            <th>Cédula</th>
            <th>Nombre</th>
            <th>Teléfono</th>
            <th>Fecha Ingreso</th>
            <th>Fecha Retiro</th>
            <th>Días Faltantes</th>
            <th>Estatus</th>
        </tr>
        {% for c in clientes %}
        <tr>
            <td>{{ c['cedula'] }}</td>
            <td>{{ c['nombre'] }}</td>
            <td>{{ c['telefono'] }}</td>
            <td>{{ c['fecha_ingreso'] or '' }}</td>
            <td>{{ c['fecha_retiro'] or '' }}</td>
            <td>{{ c['dias_faltantes'] or '' }}</td>
            <td class="
                {% if c['estatus'] == 'Vencido' %}estatus-vencido{% elif c['estatus'] == 'Por vencer' %}estatus-porvencer{% else %}estatus-vigente{% endif %}
            ">
                {{ c['estatus'] }}
            </td>
        </tr>
        {% endfor %}
    </table>

    {% if not clientes %}
        <p style="text-align:center; color:#ccc;">No se encontraron resultados.</p>
    {% endif %}
</body>
</html>
"""

# === RUTA PRINCIPAL ===
@app.route("/", methods=["GET"])
def listado():
    q = request.args.get("q", "").strip()

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    if q:
        sql = """
        SELECT cedula, nombre, telefono, fecha_ingreso, fecha_retiro, dias_faltantes, estatus
        FROM clientes
        WHERE cedula LIKE %s OR nombre LIKE %s
        ORDER BY nombre
        """
        cursor.execute(sql, (f"%{q}%", f"%{q}%"))
    else:
        cursor.execute("""
        SELECT cedula, nombre, telefono, fecha_ingreso, fecha_retiro, dias_faltantes, estatus
        FROM clientes
        ORDER BY nombre
        """)

    clientes = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template_string(HTML, clientes=clientes, q=q)

if __name__ == "__main__":
    app.run(debug=True)
