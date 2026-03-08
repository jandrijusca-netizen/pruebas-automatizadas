"""
Prueba E2E - Demoblaze
Flujo de compra: agregar productos al carrito, visualizar carrito,
completar formulario de compra y finalizar hasta la confirmación.

Framework: Selenium WebDriver + Python
Sitio: https://www.demoblaze.com/
"""

import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class DemblazeE2ETest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Configuración inicial del WebDriver."""
        chrome_options = Options()
        # Comentar la siguiente línea si deseas ver el navegador
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 15)
        cls.base_url = "https://www.demoblaze.com/"

    @classmethod
    def tearDownClass(cls):
        """Cierre del navegador al finalizar."""
        cls.driver.quit()

    def setUp(self):
        """Navegar a la página principal antes de cada prueba."""
        self.driver.get(self.base_url)
        time.sleep(2)

    # ---------------------------------------------------------------
    # CASO 1: Agregar primer producto al carrito
    # ---------------------------------------------------------------
    def test_01_agregar_primer_producto(self):
        """Agrega el primer producto (Samsung galaxy s6) al carrito."""
        print("\n[TEST 1] Agregar primer producto al carrito")

        # Hacer clic en el primer producto
        primer_producto = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Samsung galaxy s6')]"))
        )
        primer_producto.click()
        time.sleep(2)

        # Capturar nombre del producto
        nombre_producto = self.driver.find_element(By.CLASS_NAME, "name").text
        print(f"  Producto seleccionado: {nombre_producto}")

        # Clic en "Add to cart"
        btn_add = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='Add to cart']"))
        )
        btn_add.click()
        time.sleep(1)

        # Aceptar alerta de confirmación
        alert = self.wait.until(EC.alert_is_present())
        alert_text = alert.text
        print(f"  Alerta recibida: {alert_text}")
        self.assertIn("Product added", alert_text)
        alert.accept()

        print("Primer producto agregado exitosamente")

    # ---------------------------------------------------------------
    # CASO 2: Agregar segundo producto al carrito
    # ---------------------------------------------------------------
    def test_02_agregar_segundo_producto(self):
        """Agrega el segundo producto (Nokia lumia 1520) al carrito."""
        print("\n[TEST 2] Agregar segundo producto al carrito")

        # Volver a la página principal
        self.driver.get(self.base_url)
        time.sleep(2)

        # Navegar a la categoría de teléfonos
        cat_phones = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='Phones']"))
        )
        cat_phones.click()
        time.sleep(2)

        # Seleccionar segundo producto
        segundo_producto = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Nokia lumia 1520')]"))
        )
        segundo_producto.click()
        time.sleep(2)

        nombre_producto = self.driver.find_element(By.CLASS_NAME, "name").text
        print(f"Producto seleccionado: {nombre_producto}")

        # Clic en "Add to cart"
        btn_add = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='Add to cart']"))
        )
        btn_add.click()
        time.sleep(1)

        # Aceptar alerta
        alert = self.wait.until(EC.alert_is_present())
        alert_text = alert.text
        print(f"Alerta recibida: {alert_text}")
        self.assertIn("Product added", alert_text)
        alert.accept()

        print("Segundo producto agregado exitosamente")

    # ---------------------------------------------------------------
    # CASO 3: Visualizar el carrito
    # ---------------------------------------------------------------
    def test_03_visualizar_carrito(self):
        """Navega al carrito y verifica que contiene productos."""
        print("\n[TEST 3] Visualizar el carrito")

        # Ir al carrito
        btn_cart = self.wait.until(
            EC.element_to_be_clickable((By.ID, "cartur"))
        )
        btn_cart.click()
        time.sleep(3)

        # Verificar que hay productos en el carrito
        filas_carrito = self.driver.find_elements(By.XPATH, "//tbody[@id='tbodyid']/tr")
        cantidad = len(filas_carrito)
        print(f"  Productos en carrito: {cantidad}")
        self.assertGreater(cantidad, 0, "El carrito está vacío")

        # Capturar total
        try:
            total = self.driver.find_element(By.ID, "totalp").text
            print(f"  Total del carrito: ${total}")
        except Exception:
            print("  Total aún no calculado")

        print("Carrito visualizado correctamente")

    # ---------------------------------------------------------------
    # CASO 4: Completar el formulario de compra y finalizar
    # ---------------------------------------------------------------
    def test_04_completar_compra(self):
        """Completa el formulario de compra y verifica la confirmación."""
        print("\n[TEST 4] Completar formulario de compra y finalizar")

        # Ir al carrito
        self.driver.get(self.base_url)
        time.sleep(2)
        btn_cart = self.wait.until(
            EC.element_to_be_clickable((By.ID, "cartur"))
        )
        btn_cart.click()
        time.sleep(3)

        # Clic en "Place Order"
        btn_order = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Place Order']"))
        )
        btn_order.click()
        time.sleep(2)

        # Llenar el formulario de compra
        datos_compra = {
            "name":    "Jandri Justo",
            "country": "Peru",
            "city":    "Lima",
            "card":    "4111111111111111",
            "month":   "12",
            "year":    "2026"
        }

        for campo, valor in datos_compra.items():
            elemento = self.wait.until(EC.presence_of_element_located((By.ID, campo)))
            elemento.clear()
            elemento.send_keys(valor)
            print(f"  Campo '{campo}' ingresado: {valor}")

        time.sleep(1)

        # Confirmar la compra
        btn_purchase = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Purchase']"))
        )
        btn_purchase.click()
        time.sleep(3)

        # Verificar mensaje de confirmación
        confirmacion = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "sweet-alert"))
        )
        texto_confirmacion = confirmacion.text
        print(f"Mensaje de confirmación: {texto_confirmacion}")

        self.assertIn("Gracias por su compra!", texto_confirmacion)

        # Capturar detalles del pedido
        try:
            detalles = self.driver.find_element(By.CLASS_NAME, "lead").text
            print(f"Detalles del pedido:\n{detalles}")
        except Exception:
            pass

        # Clic en OK para cerrar
        btn_ok = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']"))
        )
        btn_ok.click()
        time.sleep(1)

        print("Compra finalizada exitosamente")


if __name__ == "__main__":
    unittest.main(verbosity=2)
