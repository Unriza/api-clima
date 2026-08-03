import unittest
import app as app_ # type: ignore


class TestClimaApp(unittest.TestCase):

    def setUp(self):
        """Configura el entorno de prueba antes de cada test."""
        self.app_.app = app_.app.test_client()
        self.app_.app.testing = True

    def test_error_ciudad_vacia(self):
        """Prueba 1: Verificar que el sistema maneja correctamente una solicitud vacía (Error 400)."""
        response = self.app_.app.get("/clima?ciudad=")
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Por favor, ingresa una ciudad valida.", response.data)

    def test_error_ciudad_inexistente(self):
        """Prueba 2: Verificar el manejo de error cuando una ciudad no existe (Error 404)."""
        response = self.app_.app.get("/clima?ciudad=ciudad_ficticia_que_no_existe")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Ciudad no encontrada", response.data)


if __name__ == "__main__":
    unittest.main()
