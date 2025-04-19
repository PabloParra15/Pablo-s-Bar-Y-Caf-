import streamlit as st
import pandas as pd
import os
import joblib
import ast
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer


# --------------------- Productos ---------------------
productos = [
    # Licores
    {"nombre": "Ron Esencial (Garrafa)", "tipo": "Licor", "sabor": "fuerte", "alcohol": True, "descripcion": "Para fiestas con amigos. Fuerte y rendidor.", "imagen": "ron_garrafa.jpg"},
    {"nombre": "Ron Esencial (Botella)", "tipo": "Licor", "sabor": "fuerte", "alcohol": True, "descripcion": "Ron en presentación de botella. Sabor clásico.", "imagen": "ron_botella.jpg"},
    {"nombre": "Ron Esencial (Caneca)", "tipo": "Licor", "sabor": "fuerte", "alcohol": True, "descripcion": "Ron económico y fuerte, ideal para compartir.", "imagen": "ron_caneca.jpg"},
    {"nombre": "Aguardiente Nariño (Botella)", "tipo": "Licor", "sabor": "anisado", "alcohol": True, "descripcion": "Aguardiente con sabor anisado tradicional.", "imagen": "aguardiente_botella.jpg"},
    {"nombre": "Aguardiente Nariño (Caneca)", "tipo": "Licor", "sabor": "anisado", "alcohol": True, "descripcion": "Caneca perfecta para compartir el sabor de Nariño.", "imagen": "aguardiente_caneca.jpg"},
    {"nombre": "Tequila Olmeca (Litro)", "tipo": "Licor", "sabor": "cítrico fuerte", "alcohol": True, "descripcion": "Tequila fuerte para los valientes.", "imagen": "tequila_litro.jpg"},
    {"nombre": "Tequila Olmeca (Botella)", "tipo": "Licor", "sabor": "cítrico fuerte", "alcohol": True, "descripcion": "Botella de tequila Olmeca con sabor intenso.", "imagen": "tequila_botella.jpg"},
    {"nombre": "Brandy Domecq (Botella)", "tipo": "Licor", "sabor": "dulce suave", "alcohol": True, "descripcion": "Brandy suave y dulce. Ideal para ocasiones especiales.", "imagen": "brandy_botella.jpg"},
    {"nombre": "Brandy Domecq (Caneca)", "tipo": "Licor", "sabor": "dulce suave", "alcohol": True, "descripcion": "Caneca de Brandy para compartir.", "imagen": "brandy_caneca.jpg"},
    {"nombre": "Old Parr (Litro)", "tipo": "Licor", "sabor": "fuerte", "alcohol": True, "descripcion": "Whisky premium para un gusto refinado.", "imagen": "old_parr.jpg"},
    {"nombre": "Buchanan's Master (Botella)", "tipo": "Licor", "sabor": "fuerte", "alcohol": True, "descripcion": "Licor elegante con sabor robusto.", "imagen": "buchanans.jpg"},

    # Vinos
    {"nombre": "Vino Storil", "tipo": "Vino", "sabor": "dulce", "alcohol": True, "descripcion": "Vino dulce para una noche tranquila.", "imagen": "vino_storil.jpg"},
    {"nombre": "Vino Sansón", "tipo": "Vino", "sabor": "dulce", "alcohol": True, "descripcion": "Dulce y tradicional, ideal para compartir.", "imagen": "vino_sanson.jpg"},

    # Cervezas
    {"nombre": "Poker", "tipo": "Cerveza", "sabor": "amarga", "alcohol": True, "descripcion": "Cerveza tradicional con sabor fuerte.", "imagen": "poker.jpg"},
    {"nombre": "Club Colombia Dorada", "tipo": "Cerveza", "sabor": "suave dorada", "alcohol": True, "descripcion": "Cerveza premium dorada y suave.", "imagen": "club_dorada.jpg"},
    {"nombre": "Águila Light", "tipo": "Cerveza", "sabor": "suave ligera", "alcohol": True, "descripcion": "Cerveza ligera y refrescante.", "imagen": "aguila_light.jpg"},
    {"nombre": "Redd's", "tipo": "Cerveza", "sabor": "dulce afrutada", "alcohol": True, "descripcion": "Sabor dulce y afrutado, ideal para todos.", "imagen": "redds.jpg"},
    {"nombre": "Coronita", "tipo": "Cerveza", "sabor": "suave clara", "alcohol": True, "descripcion": "Cerveza clara para refrescar.", "imagen": "coronita.jpg"},
    {"nombre": "Stella Artois", "tipo": "Cerveza", "sabor": "refinada amarga", "alcohol": True, "descripcion": "Cerveza elegante de sabor refinado.", "imagen": "stella.jpg"},
    {"nombre": "Cola y Pola", "tipo": "Cerveza", "sabor": "dulce malteada", "alcohol": True, "descripcion": "Combinación de cerveza y soda dulce.", "imagen": "cola_pola.jpg"},

    # Micheladas
    {"nombre": "Michelada Soda", "tipo": "Michelada", "sabor": "refrescante sin alcohol", "alcohol": False, "descripcion": "Refrescante y sin licor. Perfecta para todos.", "imagen": "michelada_soda.jpg"},
    {"nombre": "Michelada Personalizada", "tipo": "Michelada", "sabor": "depende de cerveza elegida", "alcohol": True, "descripcion": "Hazla a tu manera con tu cerveza favorita.", "imagen": "michelada_personalizada.jpg"},

    # Café
    {"nombre": "Café Americano", "tipo": "Café", "sabor": "suave amargo", "alcohol": False, "descripcion": "Clásico café negro para energizarte.", "imagen": "cafe_americano.jpg"},
    {"nombre": "Café Irlandés / Carajillo", "tipo": "Café", "sabor": "café con licor", "alcohol": True, "descripcion": "Café especial con un toque de licor. ¡Exquisito!", "imagen": "cafe_irlandes.jpg"},

    # Snacks
    {"nombre": "Rizadas Pollo", "tipo": "Papas", "sabor": "salado pollo", "alcohol": False, "descripcion": "Papas con sabor a pollo, perfectas para picar.", "imagen": "papas_pollo.jpg"},
    {"nombre": "Rizadas Limón", "tipo": "Papas", "sabor": "salado limón", "alcohol": False, "descripcion": "Papas con toque ácido para acompañar tu bebida.", "imagen": "papas_limon.jpg"},
    {"nombre": "Rizadas Mayonesa", "tipo": "Papas", "sabor": "cremoso", "alcohol": False, "descripcion": "Papas con mayonesa. ¡Una delicia cremosa!", "imagen": "papas_mayonesa.jpg"},
    {"nombre": "Golpe con Todo (Pollo y Ranchero)", "tipo": "Papas", "sabor": "intenso", "alcohol": False, "descripcion": "¡Combo explosivo de sabores fuertes!", "imagen": "papas_combo.jpg"},

    # Otras Bebidas
    {"nombre": "Gatorade", "tipo": "Bebida", "sabor": "hidratante", "alcohol": False, "descripcion": "Rehidrátate después de una buena rumba.", "imagen": "gatorade.jpg"},
    {"nombre": "Agua Natural", "tipo": "Bebida", "sabor": "natural", "alcohol": False, "descripcion": "Agua para acompañar o descansar.", "imagen": "agua.jpg"},
    {"nombre": "Agua con Gas", "tipo": "Bebida", "sabor": "efervescente", "alcohol": False, "descripcion": "Agua burbujeante para un toque elegante.", "imagen": "agua_gas.jpg"},
    {"nombre": "Jugo Hit Mango", "tipo": "Bebida", "sabor": "dulce mango", "alcohol": False, "descripcion": "Jugo natural para refrescarte.", "imagen": "jugo_mango.jpg"},
    {"nombre": "Jugo Hit Tropical", "tipo": "Bebida", "sabor": "dulce tropical", "alcohol": False, "descripcion": "Sabor tropical para los días calurosos.", "imagen": "jugo_tropical.jpg"},
    {"nombre": "Jugo Hit Piña Naranja", "tipo": "Bebida", "sabor": "dulce cítrico", "alcohol": False, "descripcion": "Combinación frutal que encanta.", "imagen": "jugo_pina.jpg"},
    {"nombre": "Gaseosa Manzana", "tipo": "Bebida", "sabor": "dulce", "alcohol": False, "descripcion": "Gaseosa clásica y dulce.", "imagen": "manzana.jpg"},
    {"nombre": "Gaseosa Colombiana", "tipo": "Bebida", "sabor": "dulce", "alcohol": False, "descripcion": "Sabor nacional inconfundible.", "imagen": "colombiana.jpg"},
    {"nombre": "Gaseosa Premio", "tipo": "Bebida", "sabor": "dulce", "alcohol": False, "descripcion": "La clásica premio para acompañar tu combo.", "imagen": "premio.jpg"},
    {"nombre": "Gaseosa Cola", "tipo": "Bebida", "sabor": "dulce", "alcohol": False, "descripcion": "La tradicional de todos los tiempos.", "imagen": "cola.jpg"},
    {"nombre": "Speed Max", "tipo": "Bebida Energética", "sabor": "energizante", "alcohol": False, "descripcion": "Energía instantánea para seguir la fiesta.", "imagen": "speedmax.jpg"},
    {"nombre": "Spartan", "tipo": "Bebida Energética", "sabor": "energizante fuerte", "alcohol": False, "descripcion": "Poder total para toda la noche.", "imagen": "spartan.jpg"},
]

# --------------------- IA basada en reglas ---------------------
def recomendar_productos(seleccionados):
    recomendaciones = []

    nombres = [p["nombre"] for p in seleccionados]
    tipos = [p["tipo"].lower() for p in seleccionados]

    # Reglas simples
    if "licor" in tipos and "papas" not in tipos:
        recomendaciones.append("🍟 Te recomendamos acompañar tu licor con unas papas 'Golpe con todo'.")
    if "cerveza" in tipos and "papas" not in tipos:
        recomendaciones.append("🥔 Una Poker se disfruta más con papas 'Rizadas de Pollo'.")
    if "michelada" not in tipos:
        recomendaciones.append("🍺 ¿Has probado nuestra michelada de soda? ¡Refrescante y sin alcohol!")

    # Especialidad
    recomendaciones.append("☕ No olvides probar nuestro Café Irlandés (Carajillo), especialidad de la casa.")

    return recomendaciones


# --------------------- IA de aprendizaje ---------------------
class ModeloIA:
    def __init__(self):
        self.archivo_datos = 'registros_clientes.csv'
        self.model = None
        self.mlb = MultiLabelBinarizer()
        self.entrenado = False

    def entrenar(self, df=None):
        if df is None:
            if not os.path.exists(self.archivo_datos):
                self.entrenado = False
                return
            df = pd.read_csv(self.archivo_datos)
        if df.empty:
            self.entrenado = False
            return
        X = self.mlb.fit_transform(
    df['productos'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) and x.strip().startswith('[') else [])
)
        y = df['aceptó_recomendación']
        self.model = RandomForestClassifier()
        self.model.fit(X, y)
        self.entrenado = True

    def predecir(self, productos):
        if not self.entrenado:
            return None
        X = self.mlb.transform([productos])
        return self.model.predict(X)[0]

modelo_ia = ModeloIA()
modelo_ia.entrenar()

# --------------------- Streamlit App ---------------------
st.set_page_config(page_title="Recomendador Inteligente - Pablo's Bar", layout="wide")

st.title("🍻 Recomendador Inteligente - Pablo's Bar y Café")
st.markdown("¡Selecciona los productos que te interesan y recibe recomendaciones inteligentes!")

st.subheader("🧾 Elige tus productos:")
seleccionados = []
cols = st.columns(3)

for idx, producto in enumerate(productos):
    with cols[idx % 3]:
        imagen_path = producto["imagen"]
        if os.path.exists(imagen_path):
            st.image(imagen_path, width=150)
        else:
            st.write("📷 Imagen no disponible")

        st.markdown(f"**{producto['nombre']}**")
        st.caption(producto["descripcion"])
        if st.checkbox(f"Seleccionar {producto['nombre']}", key=producto["nombre"]):
            seleccionados.append(producto)

if seleccionados:
    nombres_seleccionados = [p['nombre'] for p in seleccionados]
    st.subheader("🤖 Recomendaciones Inteligentes:")

    # Generar recomendaciones con reglas
    recomendaciones = recomendar_productos(seleccionados)

    # Mostrar recomendaciones
    for r in recomendaciones:
        st.success(r)

    # Predicción IA
    if modelo_ia.entrenado:
        prediccion = modelo_ia.predecir(nombres_seleccionados)
        if prediccion == 1:
            st.info("✅ La IA predice que esta recomendación será **aceptada** por el cliente.")
        else:
            st.warning("❌ La IA predice que esta recomendación **no será aceptada**.")
    else:
        st.info("ℹ️ Aún no hay suficientes datos para que la IA haga predicciones.")

    # Registro de respuesta
    acepto = st.radio("¿Te gustaron nuestras recomendaciones?", ["Sí", "No"], horizontal=True)
    if st.button("Registrar respuesta"):
        nuevo_registro = pd.DataFrame([{
            "productos": nombres_seleccionados,
            "aceptó_recomendación": 1 if acepto == "Sí" else 0
        }])

        # Guardar en CSV
        if os.path.exists(modelo_ia.archivo_datos):
            df_existente = pd.read_csv(modelo_ia.archivo_datos)
            df_existente = pd.concat([df_existente, nuevo_registro], ignore_index=True)
        else:
            df_existente = nuevo_registro

        df_existente.to_csv(modelo_ia.archivo_datos, index=False)
        st.success("¡Gracias! Tu respuesta fue registrada para mejorar la IA.")

        # 🔁 Reentrenar el modelo automáticamente con todos los datos actualizados
        modelo_ia.entrenar(df_existente)
        st.info("🤖 El modelo ha sido reentrenado con los nuevos datos.")

