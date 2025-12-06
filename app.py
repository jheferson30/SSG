from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from pymongo import MongoClient
from datetime import datetime, timedelta
from fpdf import FPDF
import os

app = Flask(__name__)
app.secret_key = "mi_clave_super_secreta_123"

# =======================
# CONEXIÓN A MONGODB ATLAS (¡VERSIÓN FINAL PARA VERCEL!)
# =======================

MONGO_URI = os.environ.get('MONGO_URI')

# ❌ ELIMINAMOS EL BLOQUE 'if not MONGO_URI' 
# Esto fuerza al despliegue a fallar si la variable no está, 
# en lugar de intentar usar localhost.

try:
    # Si MONGO_URI es 'None' (variable no encontrada), 
    # esto generará una excepción que será atrapada y registrada.
    mongo_client = MongoClient(MONGO_URI)
    
    # Base de datos que restauraste
    db = mongo_client["trabajo de gimnasio"] 
    clientes_collection = db["clientes"]
    print("✅ Conexión a MongoDB establecida correctamente.")

except Exception as e:
    # Este print se registrará en los logs de Vercel si falla.
    print(f"❌ ERROR FATAL AL CONECTAR A MONGODB (Usando MONGO_URI): {e}")
    

# Carpeta donde se guardan los PDF
RUTA_RECIBOS = "recibos"
os.makedirs(RUTA_RECIBOS, exist_ok=True)

# =======================
# PANTALLA INICIO
# =======================
@app.route("/inicio", methods=["GET", "POST"])
def inicio():
    cliente = None
    dias_restantes = None
    no_encontrado = False
    proximos_vencer = []

    try:
        cedula = request.form.get("cedula") or request.args.get("cedula")
        if cedula:
            cliente = clientes_collection.find_one({"cedula": cedula})

            if cliente:
                fecha_ingreso = cliente.get("fecha_ingreso")
                fecha_retiro = cliente.get("fecha_retiro")

                if isinstance(fecha_ingreso, str):
                    fecha_ingreso = datetime.fromisoformat(fecha_ingreso)
                if isinstance(fecha_retiro, str):
                    fecha_retiro = datetime.fromisoformat(fecha_retiro)

                duracion = int(cliente.get("duracion", 0))
                if not fecha_retiro and fecha_ingreso and duracion > 0:
                    fecha_retiro = fecha_ingreso + timedelta(days=duracion)

                dias_restantes = max((fecha_retiro - datetime.now()).days, 0)
                estatus = "Activo" if dias_restantes > 0 else "Vencido"

                clientes_collection.update_one(
                    {"cedula": cedula},
                    {"$set": {
                        "dias_faltantes": dias_restantes,
                        "estatus": estatus,
                        "fecha_retiro": fecha_retiro
                    }}
                )

                cliente["fecha_ingreso"] = fecha_ingreso
                cliente["fecha_retiro"] = fecha_retiro
            else:
                no_encontrado = "⚠️ El cliente no existe."

        hoy = datetime.now()
        todos_clientes = list(clientes_collection.find())
        for c in todos_clientes:
            fecha_retiro = c.get("fecha_retiro")
            if isinstance(fecha_retiro, str):
                fecha_retiro = datetime.fromisoformat(fecha_retiro)
            if not fecha_retiro:
                continue
            dias_faltan = (fecha_retiro - hoy).days
            if 0 < dias_faltan <= 3:
                proximos_vencer.append({
                    "nombre": c.get("nombre", "Sin nombre"),
                    "cedula": c.get("cedula"),
                    "dias_restantes": dias_faltan
                })

    except Exception as err:
        print("❌ Error:", err)

    return render_template("inicio.html",
                           cliente=cliente,
                           dias_restantes=dias_restantes,
                           no_encontrado=no_encontrado,
                           proximos_vencer=proximos_vencer)

# =======================
# PROXIMOS A VENCER
# =======================
@app.route("/proximos_vencer")
def clientes_proximos():
    clientes = list(clientes_collection.find())
    proximos_vencer = []
    hoy = datetime.now()

    for c in clientes:
        fecha_retiro = c.get("fecha_retiro")
        if isinstance(fecha_retiro, str):
            fecha_retiro = datetime.fromisoformat(fecha_retiro)
        if not fecha_retiro:
            continue
        dias_restantes = (fecha_retiro - hoy).days
        if 0 <= dias_restantes <= 3:
            proximos_vencer.append({
                "nombre": c.get("nombre", "Desconocido"),
                "cedula": c.get("cedula", "N/A"),
                "plan": c.get("plan", "Sin plan"),
                "dias_restantes": dias_restantes
            })

    return render_template("clientes_proximos.html", proximos_vencer=proximos_vencer)

# =======================
# FORMULARIO DE RENOVACIÓN
# =======================
@app.route("/renovar/<cedula>", methods=["GET", "POST"])
def renovar_cliente(cedula):
    cliente = clientes_collection.find_one({"cedula": cedula})
    if request.method == "POST":
        nuevo_plan = request.form["plan"]
        forma_pago = request.form["forma_pago"]
        valor_pagar = float(request.form["valor_pagar"])
        fecha_inicio = datetime.fromisoformat(request.form["fecha_inicio"])
        duracion = int(request.form["duracion"])

        fecha_retiro = fecha_inicio + timedelta(days=duracion)

        clientes_collection.update_one(
            {"cedula": cedula},
            {"$set": {
                "plan": nuevo_plan,
                "forma_pago": forma_pago,
                "valor_pagar": valor_pagar,
                "fecha_ingreso": fecha_inicio,
                "duracion": duracion,
                "fecha_retiro": fecha_retiro
            }}
        )
        flash("✅ Cliente renovado correctamente", "success")
        return redirect(url_for("inicio"))

    return render_template("renovar.html", cliente=cliente)

# =======================
# LISTADO DE CLIENTES
# =======================
@app.route("/")
def listado():
    q = request.args.get("q", "").strip()
    page = int(request.args.get("page", 1))
    per_page = 20
    skip = (page - 1) * per_page

    filtro = {}
    if q:
        filtro = {"$or": [
            {"cedula": {"$regex": q, "$options": "i"}},
            {"nombre": {"$regex": q, "$options": "i"}}
        ]}

    total = clientes_collection.count_documents(filtro)
    total_pages = (total + per_page - 1) // per_page
    clientes = list(clientes_collection.find(filtro).skip(skip).limit(per_page))
    hoy = datetime.now()

    for c in clientes:
        fecha_retiro = c.get("fecha_retiro")
        if isinstance(fecha_retiro, str):
            fecha_retiro = datetime.fromisoformat(fecha_retiro)
        dias_restantes = max((fecha_retiro - hoy).days, 0)
        estatus = "Activo" if dias_restantes > 0 else "Vencido"
        clientes_collection.update_one(
            {"cedula": c["cedula"]},
            {"$set": {"dias_faltantes": dias_restantes, "estatus": estatus}}
        )
        c["dias_faltantes"] = dias_restantes
        c["estatus"] = estatus
        c["fecha_retiro"] = fecha_retiro

    return render_template("listado.html", clientes=clientes, q=q, page=page, total_pages=total_pages)

# ======================
# EDITAR CLIENTE
# ======================
@app.route("/editar/<cedula>", methods=["GET", "POST"])
def editar_cliente(cedula):
    cliente = clientes_collection.find_one({"cedula": cedula})
    if request.method == "POST":
        clientes_collection.update_one(
            {"cedula": cedula},
            {"$set": {
                "nombre": request.form["nombre"],
                "correo": request.form["correo"],
                "telefono": request.form["telefono"],
               
            }}
        )
        return redirect("/")
    return render_template("editar.html", cliente=cliente)

# ======================
# ELIMINAR CLIENTE
# ======================
@app.route("/eliminar/<cedula>", methods=["POST"])
def eliminar_cliente(cedula):
    clientes_collection.delete_one({"cedula": cedula})
    return redirect(url_for("listado"))

# ======================
# NUEVO CLIENTE
# ======================
@app.route("/nuevo_cliente", methods=["GET", "POST"])
def nuevo_cliente():
    if request.method == "POST":
        cedula = request.form["cedula"]
        if clientes_collection.find_one({"cedula": cedula}):
            flash(f"⚠️ El cliente con cédula {cedula} ya existe.", "warning")
            return redirect(url_for("nuevo_cliente"))

        fecha_ingreso = datetime.fromisoformat(request.form["fecha_ingreso"])
        fecha_retiro = datetime.fromisoformat(request.form["fecha_retiro"])
        dias_faltantes = (fecha_retiro - datetime.now()).days
        estatus = "Activo" if dias_faltantes >= 0 else "Vencido"

        nuevo = {
            "cedula": cedula,
            "nombre": request.form["nombre"],
            "telefono": request.form["telefono"],
            "correo": request.form["correo"],
            "forma_pago": request.form["forma_pago"],
            "valor_pagar": request.form["valor_pagar"],
            "fecha_ingreso": fecha_ingreso,
            "fecha_retiro": fecha_retiro,
            "dias_faltantes": dias_faltantes,
            "estatus": estatus
        }
        clientes_collection.insert_one(nuevo)
        flash("✅ Cliente registrado correctamente.", "success")
        return redirect(url_for("inicio"))

    return render_template("nuevo_cliente.html")

# =======================
# GENERAR RECIBO PDF
# =======================
def generar_recibo(datos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "GYM WORK - RECIBO DE PAGO", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    for k, v in datos.items():
        pdf.cell(0, 10, f"{k.capitalize()}: {v}", ln=True)
    pdf.ln(10)
    pdf.cell(0, 10, "¡Gracias por entrenar con nosotros!", ln=True, align="C")

    nombre_archivo = f"recibo_{datos['Cédula']}_{datetime.now().strftime('%Y%m%d')}.pdf"
    ruta = os.path.join(RUTA_RECIBOS, nombre_archivo)
    pdf.output(ruta, "F")
    return ruta

# =======================
# DESCARGAR RECIBO PDF
# =======================
@app.route("/recibo/<cedula>")
def descargar_recibo(cedula):
    c = clientes_collection.find_one({"cedula": cedula})
    if not c:
        return f"No existe cliente con cédula {cedula}"

    datos = {
        "Cédula": c["cedula"],
        "Nombre": c["nombre"],
        "Teléfono": c["telefono"],
        "Correo": c["correo"],
        "Forma de pago": c["forma_pago"],
        "Valor a pagar": f"${c['valor_pagar']}",
        "Fecha ingreso": c["fecha_ingreso"].strftime("%Y-%m-%d %H:%M:%S"),
        "Fecha retiro": c["fecha_retiro"].strftime("%Y-%m-%d %H:%M:%S"),
        "Estatus": c["estatus"]
    }
    ruta = generar_recibo(datos)
    return send_file(ruta, as_attachment=True)

# =======================
# ESTADISTICAS
# =======================
from datetime import datetime, timedelta
from flask import render_template, request

@app.route("/estadisticas", methods=["GET", "POST"])
def estadisticas():
    # Obtener todos los clientes desde la base
    clientes = list(clientes_collection.find())
    hoy = datetime.now()

    # Valores por defecto para los filtros
    fecha_seleccionada = request.form.get("fecha", hoy.strftime("%Y-%m-%d"))
    semana_seleccionada = request.form.get("semana", hoy.strftime("%Y-W%U"))
    mes_seleccionado = request.form.get("mes", hoy.strftime("%Y-%m"))

    try:
        fecha_dt = datetime.fromisoformat(fecha_seleccionada)
    except ValueError:
        fecha_dt = hoy  # Evita error si la fecha no tiene formato válido

    # Inicializar variables y estructuras
    diarios = semanales = mensuales = 0
    registros_por_hora = {str(h): 0 for h in range(24)}
    registros_semanales = {d: 0 for d in ['L', 'M', 'MI', 'J', 'V', 'S', 'D']}
    registros_mensuales = {"actual": {}, "anterior": {}}
    metodos_pago = {}

    # Definir rangos de tiempo
    semana_inicio = fecha_dt - timedelta(days=fecha_dt.weekday())
    semana_fin = semana_inicio + timedelta(days=6)

    mes_inicio = fecha_dt.replace(day=1)
    mes_fin = (mes_inicio.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

    mes_anterior_fin = mes_inicio - timedelta(days=1)
    mes_anterior_inicio = mes_anterior_fin.replace(day=1)

    # Procesar cada cliente
    for c in clientes:
        fecha = c.get("fecha_ingreso")
        if not fecha:
            continue

        # Convertir a datetime si es cadena
        if isinstance(fecha, str):
            try:
                fecha = datetime.fromisoformat(fecha)
            except ValueError:
                continue

        fecha_date = fecha.date()

        # Métodos de pago
        metodo = c.get("forma_pago", "Desconocido")
        if isinstance(metodo, list):
            for m in metodo:
                metodos_pago[m] = metodos_pago.get(m, 0) + 1
        else:
            metodos_pago[metodo] = metodos_pago.get(metodo, 0) + 1

        # Conteo diario
        if fecha_date == fecha_dt.date():
            diarios += 1
            registros_por_hora[str(fecha.hour)] += 1

        # Conteo semanal
        if semana_inicio.date() <= fecha_date <= semana_fin.date():
            semanales += 1
            dias_letras = ['L', 'M', 'MI', 'J', 'V', 'S', 'D']
            registros_semanales[dias_letras[fecha.weekday()]] += 1

        # Conteo mensual actual
        if mes_inicio.date() <= fecha_date <= mes_fin.date():
            mensuales += 1
            dia = str(fecha.day)
            registros_mensuales["actual"][dia] = registros_mensuales["actual"].get(dia, 0) + 1

        # Conteo mes anterior
        if mes_anterior_inicio.date() <= fecha_date <= mes_anterior_fin.date():
            dia = str(fecha.day)
            registros_mensuales["anterior"][dia] = registros_mensuales["anterior"].get(dia, 0) + 1

    # Renderizar plantilla con los datos
    return render_template(
        "estadisticas.html",
        diarios=diarios,
        semanales=semanales,
        mensuales=mensuales,
        metodos_pago=metodos_pago,
        registros_por_hora=registros_por_hora,
        registros_semanales=registros_semanales,
        registros_mensuales=registros_mensuales,
        fecha_seleccionada=fecha_seleccionada,
        semana_seleccionada=semana_seleccionada,
        mes_seleccionado=mes_seleccionado
    )

# =======================
# MAIN
# =======================
if __name__ == "__main__":
    app.run(debug=True)
