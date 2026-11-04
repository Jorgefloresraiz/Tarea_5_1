import unittest
import pca_utils

class Permisos(unittest.TestCase):
    def test_rutas_no_autorizadas(self):
        for nombre in ('../iris', '/tmp/iris', '../../etc/passwd', 'desconocido'):
            with self.subTest(nombre=nombre), self.assertRaises(ValueError):
                pca_utils.describir_dataset(nombre)

    def test_datasets_y_pca(self):
        self.assertEqual(pca_utils.listar_datasets(), ['iris', 'wine', 'qa_simulado'])
        self.assertEqual(pca_utils.describir_dataset('wine')['filas'], 178)
        self.assertEqual(pca_utils.ejecutar_pca('iris', 2)['varianza_acumulada'], 0.9581)

if __name__ == '__main__':
    unittest.main()
