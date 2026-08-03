# 🌤️ Aplicación Web del Clima Responsiva

Una aplicación web ligera diseñada para consultar datos meteorológicos en tiempo real de forma rápida y eficiente. 

Este proyecto utiliza **Python (Flask)** en el servidor y una interfaz moderna construida con **HTML5 y CSS3**, conectándose directamente a la API pública y gratuita de **Open-Meteo**.

---

## 🚀 Requisitos de Ejecución

Sigue estos pasos para poner en marcha la aplicación en tu entorno local:

### 1. Instalar dependencias
Asegúrate de tener Python instalado y ejecuta el siguiente comando en tu terminal para instalar los módulos necesarios:
```bash
pip install flask requests
```

### 2. Ejecutar la aplicación
Inicia el servidor local con el siguiente comando:
```bash
python app.py
```

### 3. Acceder en el navegador
Una vez encendido el servidor, abre tu navegador web e ingresa a la siguiente dirección:
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧪 Ejecución de Pruebas

El proyecto incluye pruebas unitarias para garantizar la estabilidad del código. Puedes verificarlas ejecutando:

```bash
python -m unittest test_app.py
```

---

## 🛡️ Consideraciones Éticas, de Seguridad y Uso de IA

* **Uso Responsable de APIs**: Se implementó una arquitectura de *Caché* local en el servidor. Esto evita saturar los servidores de Open-Meteo con llamadas idénticas recurrentes, respetando sus políticas de uso justo y optimizando el tiempo de respuesta.
* **Seguridad en Entrada de Datos**: Se utiliza `encodeURIComponent` en el Frontend y saneamiento de cadenas (`.strip()`) en el Backend para mitigar vulnerabilidades de inyección de parámetros en las URLs.
* **Atribución de IA**: Este código fue co-creado y refinado mediante un modelo de Inteligencia Artificial para fines educativos y de desarrollo rápido. Se realizó una validación manual de la lógica de las llamadas HTTP y de la adaptabilidad móvil (responsive design) del CSS.

---

## 📄 Licencia

Este proyecto está liberado bajo la **Licencia MIT**. Siéntete libre de usarlo, modificarlo y distribuirlo de manera libre.
