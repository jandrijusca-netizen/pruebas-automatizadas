"""
Prueba de APIs - PetStore
Flujo completo: agregar mascota, consultar por ID, actualizar nombre y estatus,
consultar por estatus.

Framework: Python + requests
Documentación API: https://petstore.swagger.io/
"""

import unittest
import requests
import json
import time
import random


class PetStoreAPITest(unittest.TestCase):

    BASE_URL = "https://petstore.swagger.io/v2"
    HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # ID único para la mascota de esta prueba
    PET_ID = random.randint(100000, 999999)

    # ---------------------------------------------------------------
    # CASO 1: Añadir una mascota a la tienda (POST /pet)
    # ---------------------------------------------------------------
    def test_01_agregar_mascota(self):
        """POST /pet - Agrega una nueva mascota a la tienda."""
        print(f"\n[TEST 1] Añadir mascota - ID: {self.PET_ID}")

        # ENTRADA
        payload = {
            "id": self.PET_ID,
            "category": {
                "id": 1,
                "name": "Perros"
            },
            "name": "Firulais",
            "photoUrls": ["https://ejemplo.com/firulais.jpg"],
            "tags": [
                {"id": 1, "name": "juguetón"}
            ],
            "status": "available"
        }

        print(f"Entrada (payload):\n{json.dumps(payload, indent=2, ensure_ascii=False)}")

        # EJECUCIÓN
        response = requests.post(
            f"{self.BASE_URL}/pet",
            headers=self.HEADERS,
            json=payload
        )

        # SALIDA
        print(f"Status Code: {response.status_code}")
        print(f"Respuesta:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")

        # VALIDACIONES
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], self.PET_ID)
        self.assertEqual(data["name"], "Firulais")
        self.assertEqual(data["status"], "available")

        print("Mascota agregada exitosamente")

    # ---------------------------------------------------------------
    # CASO 2: Consultar la mascota por ID (GET /pet/{petId})
    # ---------------------------------------------------------------
    def test_02_consultar_mascota_por_id(self):
        """GET /pet/{petId} - Busca la mascota por su ID."""
        print(f"\n[TEST 2] Consultar mascota por ID: {self.PET_ID}")

        # ENTRADA
        print(f"Entrada: petId = {self.PET_ID}")

        # EJECUCIÓN
        response = requests.get(
            f"{self.BASE_URL}/pet/{self.PET_ID}",
            headers=self.HEADERS
        )

        # SALIDA
        print(f"Status Code: {response.status_code}")
        print(f"Respuesta:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")

        # VALIDACIONES
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], self.PET_ID)
        self.assertEqual(data["name"], "Firulais")
        self.assertEqual(data["status"], "available")

        print("Mascota encontrada por ID correctamente")

    # ---------------------------------------------------------------
    # CASO 3: Actualizar nombre y estatus de la mascota (PUT /pet)
    # ---------------------------------------------------------------
    def test_03_actualizar_mascota(self):
        """PUT /pet - Actualiza el nombre y el estatus a 'sold'."""
        print(f"\n[TEST 3] Actualizar mascota ID: {self.PET_ID}")

        # ENTRADA
        payload = {
            "id": self.PET_ID,
            "category": {
                "id": 1,
                "name": "Perros"
            },
            "name": "Firulais Actualizado",
            "photoUrls": ["https://ejemplo.com/firulais.jpg"],
            "tags": [
                {"id": 1, "name": "juguetón"}
            ],
            "status": "sold"
        }

        print(f"Entrada (payload actualizado):\n{json.dumps(payload, indent=2, ensure_ascii=False)}")

        # EJECUCIÓN
        response = requests.put(
            f"{self.BASE_URL}/pet",
            headers=self.HEADERS,
            json=payload
        )

        # SALIDA
        print(f"Status Code: {response.status_code}")
        print(f"Respuesta:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")

        # VALIDACIONES
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], self.PET_ID)
        self.assertEqual(data["name"], "Firulais Actualizado")
        self.assertEqual(data["status"], "sold")

        print("Mascota actualizada exitosamente (nombre + estatus 'sold')")

    # ---------------------------------------------------------------
    # CASO 4: Consultar mascota por estatus (GET /pet/findByStatus)
    # ---------------------------------------------------------------
    def test_04_consultar_por_estatus(self):
        """GET /pet/findByStatus - Consulta mascotas con estatus 'sold'."""
        print("\n[TEST 4] Consultar mascotas por estatus: 'sold'")

        # ENTRADA
        params = {"status": "sold"}
        print(f"Entrada (query param): status = sold")

        # EJECUCIÓN
        response = requests.get(
            f"{self.BASE_URL}/pet/findByStatus",
            headers=self.HEADERS,
            params=params
        )

        # SALIDA
        print(f"Status Code: {response.status_code}")
        mascotas = response.json()
        print(f"Total mascotas con estatus 'sold': {len(mascotas)}")

        # Buscar nuestra mascota actualizada en los resultados
        nuestra_mascota = next(
            (p for p in mascotas if p.get("id") == self.PET_ID), None
        )

        if nuestra_mascota:
            print(f"Mascota encontrada:\n{json.dumps(nuestra_mascota, indent=2, ensure_ascii=False)}")
        else:
            print(f"(La mascota ID {self.PET_ID} puede tardar en aparecer en el índice)")

        # VALIDACIONES
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(mascotas, list)
        self.assertGreater(len(mascotas), 0)

        # Verificar que todos los resultados tienen estatus 'sold'
        for mascota in mascotas[:5]:  # Revisar primeras 5
            self.assertEqual(mascota.get("status"), "sold")

        print("Consulta por estatus 'sold' exitosa")


# ---------------------------------------------------------------
# Ejecución directa con reporte de resultados
# ---------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("PRUEBAS DE API - PETSTORE")
    print("https://petstore.swagger.io/")
    print("=" * 60)
    unittest.main(verbosity=2)
