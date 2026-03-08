================================================================
  README - PROYECTO DE PRUEBAS AUTOMATIZADAS
  E2E: Demoblaze | API: PetStore
================================================================

REQUISITOS PREVIOS
------------------
- Python 3.8 o superior instalado
- Google Chrome instalado (versión actualizada)
- ChromeDriver compatible con tu versión de Chrome
  Descarga: https://chromedriver.chromium.org/downloads
- Conexión a internet activa

================================================================
ESTRUCTURA DEL PROYECTO
================================================================

proyecto_pruebas/
├── e2e/
│   └── test_demoblaze_e2e.py     # Pruebas E2E Selenium - Demoblaze
├── api/
│   └── test_petstore_api.py      # Pruebas de API - PetStore
├── requirements.txt               # Dependencias del proyecto
├── readme.txt                     # Este archivo
└── conclusiones.txt               # Hallazgos y conclusiones

================================================================
PASO 1 - CLONAR O DESCOMPRIMIR EL PROYECTO
================================================================

Opción A (desde ZIP):
  1. Descomprimir el archivo .zip en una carpeta de tu elección
  2. Abrir una terminal y navegar a la carpeta del proyecto:
     cd ruta/proyecto_pruebas

Opción B (desde GitHub):
  git clone <URL_DEL_REPOSITORIO>
  cd proyecto_pruebas

================================================================
PASO 2 - CREAR ENTORNO VIRTUAL (RECOMENDADO)
================================================================

Windows:
  python -m venv venv
  venv\Scripts\activate

================================================================
PASO 3 - INSTALAR DEPENDENCIAS
================================================================

  pip install -r requirements.txt

Esto instalará:
  - selenium       → automatización del navegador (E2E)
  - requests       → cliente HTTP para pruebas de API
  - webdriver-manager → gestión automática de ChromeDriver

================================================================
PASO 4 - CONFIGURAR CHROMEDRIVER
================================================================

Opción A (automática con webdriver-manager):
  El proyecto usa webdriver-manager para descargar ChromeDriver
  automáticamente. No se requiere configuración adicional.

Opción B (manual):
  1. Verificar versión de Chrome: chrome://version/
  2. Descargar ChromeDriver correspondiente:
     https://chromedriver.chromium.org/downloads
  3. Colocar el ejecutable en el PATH del sistema o en la
     carpeta raíz del proyecto.

================================================================
PASO 5 - EJECUTAR PRUEBAS DE API (PetStore)
================================================================

Navegar a la carpeta del proyecto y ejecutar:

  python -m pytest api/test_petstore_api.py -v

O directamente:
  python api/test_petstore_api.py

ENTRADAS del flujo API:
  - POST /pet      → id, nombre, categoría, fotos, tags, estatus
  - GET  /pet/{id} → petId (número entero)
  - PUT  /pet      → payload completo con nombre y estatus "sold"
  - GET  /pet/findByStatus → query param: status=sold

SALIDAS esperadas:
  - Status 200 en todos los endpoints
  - Objeto JSON con datos de la mascota creada/actualizada
  - Lista de mascotas con estatus "sold"

================================================================
PASO 6 - EJECUTAR PRUEBAS E2E (Demoblaze)
================================================================

IMPORTANTE: Asegúrate de que Chrome esté instalado y accesible.

Navegar a la carpeta del proyecto y ejecutar:

  python -m pytest e2e/test_demoblaze_e2e.py -v

O directamente:
  python e2e/test_demoblaze_e2e.py

NOTA: Las pruebas deben ejecutarse EN ORDEN (test_01 al test_04).
Para ejecutar en orden con pytest:
  python -m pytest e2e/test_demoblaze_e2e.py -v -p no:randomly

FLUJO E2E que se automatiza:
  1. Abrir https://www.demoblaze.com/
  2. Agregar "Samsung galaxy s6" al carrito
  3. Agregar "Nokia lumia 1520" al carrito
  4. Visualizar el carrito con los productos
  5. Completar formulario (nombre, país, ciudad, tarjeta)
  6. Confirmar compra → verificar "Thank you for your purchase!"

================================================================
PASO 7 - EJECUTAR TODAS LAS PRUEBAS JUNTAS
================================================================

  python -m pytest e2e/ api/ -v

Con reporte HTML (requiere pytest-html):
  pip install pytest-html
  python -m pytest e2e/ api/ -v --html=reportes/reporte.html

================================================================
SOLUCIÓN DE PROBLEMAS COMUNES
================================================================

Error: "chromedriver not found"
  → Instalar con: pip install webdriver-manager
  → Agregar al inicio del test:
    from webdriver_manager.chrome import ChromeDriverManager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

Error: "ConnectionError" en API tests
  → Verificar conexión a internet
  → La API de PetStore puede estar saturada, reintentar

Error: Alerta no encontrada en E2E
  → Aumentar tiempo de espera en WebDriverWait(driver, 20)
  → La respuesta de Demoblaze puede tardar

================================================================
VERSIONES USADAS EN DESARROLLO
================================================================

Python       : 3.11
selenium     : 4.18.1
requests     : 2.31.0
webdriver-manager : 4.0.1
Google Chrome: 122+
ChromeDriver : 122+

================================================================
AUTOR : Jandri Jessi Justo Carazas
================================================================
Proyecto de pruebas automatizadas
Herramientas: Selenium WebDriver + Python + requests
================================================================
