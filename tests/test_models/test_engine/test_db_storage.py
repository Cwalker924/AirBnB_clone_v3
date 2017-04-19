import unittest
import os.path
from os import getenv
from datetime import datetime
from models.base_model import Base
from models.amenity import Amenity
from models.engine.db_storage import DBStorage
from models.state import State
from models import *


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE', 'fs') != 'db', "db")
class Test_DBStorage(unittest.TestCase):
    """
    Test the file storage class
    """
    @classmethod
    def setUpClass(cls):
        """
        Create a session
        """
        # close previous connexion to same database
        storage._DBStorage__session.close()
        cls.store = DBStorage()
        test_args = {'updated_at': datetime(2017, 2, 12, 00, 31, 53, 331997),
                     'id': "0234",
                     'created_at': datetime(2017, 2, 12, 00, 31, 53, 331900),
                     'name': 'goof'}
        cls.model = Amenity(**test_args)
        cls.store.reload()
        cls.test_len = 0

    @classmethod
    def tearDownClass(cls):
        """
        Test teardown method
        """
        cls.store._DBStorage__session.close()
        storage.reload()

    def test_all(self):
        """
        Test all method
        """
        l1 = len(storage.all('State'))
        state = State(name = "State test all")
        state.save()
        output = storage.all('State')
        self.assertEqual(len(output), l1 + 1)
        self.assertIn(state.id, output.keys())
        storage.delete(state)

    def test_new(self):
        """
        Test new method
        """
        # note: we cannot assume order of test is order written
        self.test_len = len(self.store.all())
        # self.assertEqual(len(self.store.all()), self.test_len)
        self.model.save()
        self.store.reload()
        self.assertEqual(len(self.store.all()), self.test_len + 1)
        a = Amenity(name="thing")
        a.save()
        self.store.reload()
        self.assertEqual(len(self.store.all()), self.test_len + 2)

        storage.delete(model)
        storage.delete(a)

    def test_save(self):
        """
        Test save method
        """
        test_len = len(self.store.all())
        a = Amenity(name="another")
        a.save()
        self.store.reload()
        self.assertEqual(len(self.store.all()), test_len + 1)
        b = State(name="california")
        self.assertNotEqual(len(self.store.all()), test_len + 2)
        b.save()
        self.store.reload()
        self.assertEqual(len(self.store.all()), test_len + 2)

        storage.delete(a)
        storage.delete(b)

    def test_reload(self):
        """
        Test reload method
        """
        self.model.save()
        a = Amenity(name="different")
        a.save()
        self.store.reload()
        for value in self.store.all().values():
            self.assertIsInstance(value.created_at, datetime)
        storage.delete(a)

    def test_get(self):
        """
        Test get object retrieval
        """
        a = self.get(self.model, cls="Amenity", id="1234")
        self.assertIs(type(a), dict)
        b = self.get(self.model, cls=None, id="1234")
        self.assertIs(type(a), None)

        storage.delete(a)
        storage.delete(b)

    def test_count(self):
        """
        Test count method
        """
        a = self.count(cls="Amenity")
        self.assertEqual(len(self.store.all("Amenity")), a)
        b = self.count(cls=None)
        self.assertEqual(len(self.store.all()), b)

        storage.delete(a)
        storage.delete(b)

if __name__ == "__main__":
    unittest.main()
