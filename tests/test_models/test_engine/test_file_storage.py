import unittest
import os
from datetime import datetime
from models.engine.file_storage import FileStorage
from models import *


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE', 'fs') == 'db',
                 "db does not have FileStorage")
class Test_FileStorage(unittest.TestCase):
    """
    Test the file storage class
    """

    def setUp(self):
        """
        Set up test method
        """
        self.store = FileStorage()

        test_args = {'name': 'goof', 'updated_at': datetime(2017, 2, 12, 00, 31, 53, 331997),
                     'id': 'f519fb40-1f5c-458b-945c-2ee8eaaf4900',
                     'created_at': datetime(2017, 2, 12, 00, 31, 53, 331900)}
        self.model = Amenity(test_args)

        self.test_len = len(self.store.all())

#    @classmethod
#    def tearDownClass(cls):
#        import os
#        if os.path.isfile("test_file.json"):
#            os.remove('test_file.json')

    def test_all(self):
        """
        Test all method
        """
        self.assertEqual(len(self.store.all()), self.test_len)

    def test_new(self):
        """
        Test new method
        """
        # note: we cannot assume order of test is order written
        test_len = len(self.store.all())
        # self.assertEqual(len(self.store.all()), self.test_len)
        new_obj = State()
        new_obj.save()
        self.assertEqual(len(self.store.all()), test_len + 1)
        a = BaseModel()
        a.save()
        self.assertEqual(len(self.store.all()), self.test_len + 2)

    def test_save(self):
        """
        Test save method
        """
        self.test_len = len(self.store.all())
        a = BaseModel()
        a.save()
        self.assertEqual(len(self.store.all()), self.test_len + 1)
        b = User()
        self.assertNotEqual(len(self.store.all()), self.test_len + 2)
        b.save()
        self.assertEqual(len(self.store.all()), self.test_len + 2)

    def test_reload(self):
        """
        Test reload method
        """
        self.model.save()
        a = BaseModel()
        a.save()
        self.store.reload()
        for value in self.store.all().values():
            self.assertIsInstance(value.created_at, datetime)

    def test_state(self):
        """
        Test State creation with an argument
        """
        pass

    def test_get(self):
        """
        Test get object retrieval
        """
        self.model.save()
        my_list = ["name", "id", "created_at", "updated_at"]
        a = self.store.get("Amenity", "f519fb40-1f5c-458b-945c-2ee8eaaf4900")
        for item in my_list:
            self.assertIn(items, my_list
        b = self.store.get(None, "invalid-id")
        self.assertIs(None, b)

    def test_count(self):
        """
        Test counting of objects
        """
        length = len(self.store.all())
        a = Amenity(name="amenity_test")
        a.save()
        self.assertEqual(amenity_test + 1, self.store.count("Amenity"))

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(1, os.path.join(os.path.split(__file__)[0], '../../..'))
    from models import *
    from models.engine.file_storage import FileStorage
    unittest.main()
