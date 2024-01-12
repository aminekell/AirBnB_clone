#!/usr/bin/python3
import unittest
import os
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage

class TestFileStorage(unittest.TestCase):
    def setUp(self):
        # Create a temporary file path for testing
        self.test_file_path = "test_file.json"

        # Override the __file_path attribute for testing
        FileStorage._FileStorage__file_path = self.test_file_path

        # Create a unique instance of FileStorage for testing
        self.storage = FileStorage()
        self.storage.reload()  # Reload initially to ensure an empty state

    def tearDown(self):
        # Remove the temporary file after testing
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_save_and_reload(self):
        # Create a BaseModel instance and add it to storage
        base_model = BaseModel()
        self.storage.new(base_model)
        self.storage.save()

        # Create a new instance of FileStorage for reloading
        reloaded_storage = FileStorage()
        reloaded_storage.reload()
        reloaded_objects = reloaded_storage.all()

        # Check if the reloaded objects contain the BaseModel instance
        self.assertIn(f"BaseModel.{base_model.id}", reloaded_objects)

    def test_new_and_save(self):  
        # Create a BaseModel instance
        base_model = BaseModel()

        # Add the BaseModel instance to storage
        self.storage.new(base_model)

        # Save the storage and check if the file is created
        self.storage.save()
        self.assertTrue(os.path.exists(self.test_file_path))

        # Check that the object is in storage
        reloaded_objects = self.storage.all()
        key = f"{base_model.__class__.__name__}.{base_model.id}"
        self.assertIn(key, reloaded_objects)

    def test_reload_empty_file(self):
        # Close the file before trying to reload it
        with open(self.test_file_path, 'w'):
            pass

        reloaded_storage = FileStorage()
        reloaded_storage.reload()
        reloaded_objects = reloaded_storage.all()

        # Check that the reloaded objects are empty
        self.assertEqual(len(reloaded_objects), 0)

if __name__ == '__main__':
    unittest.main()
