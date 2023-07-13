from django.test import TestCase

from .models import Company

class CompanyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Crea un objeto de la compañía para las pruebas
        Company.objects.create(
            name="Company A",
            ruc="123456789",
            economic_activity="Activity A",
            address="Address A",
            state=True
        )

    def test_company_name(self):
        # Obtiene el objeto de la compañía creado en el método setUpTestData
        company = Company.objects.get(id=1)

        # Verifica que el nombre de la compañía sea correcto
        self.assertEqual(company.name, "Company A")

    def test_company_ruc(self):
        company = Company.objects.get(id=1)
        self.assertEqual(company.ruc, "123456789")

    def test_company_economic_activity(self):
        company = Company.objects.get(id=1)
        self.assertEqual(company.economic_activity, "Activity A")

    def test_company_address(self):
        company = Company.objects.get(id=1)
        self.assertEqual(company.address, "Address A")

    def test_company_state(self):
        company = Company.objects.get(id=1)
        self.assertTrue(company.state)
