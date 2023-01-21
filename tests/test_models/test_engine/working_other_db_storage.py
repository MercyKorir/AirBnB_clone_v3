#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""
import unittest
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage

class TestDBStorage(unittest.TestCase):

    def setUp(self):
        """initializes new storage object for testing"""
        storage.__init__()

    def test_all_with_class(self):
        """tests all method to retrieve all objects of a specific class"""
        state = State(name="California")
        city = City(state_id=state.id, name="San Francisco")
        storage.new(state)
        storage.new(city)
        storage.save()
        retrieved_objs = storage.all(State)
        self.assertEqual(len(retrieved_objs), 1)
        self.assertIsInstance(list(retrieved_objs.values())[0], State)

    def test_all_without_class(self):
        """tests all method to retrieve all objects without specific class"""
        state = State(name="California")
        city = City(state_id=state.id, name="San Francisco")
        user = User(email="test@example.com", password="password")
        storage.new(state)
        storage.new(city)
        storage.new(user)
        storage.save()
        retrieved_objs = storage.all()
        self.assertEqual(len(retrieved_objs), 3)

    def test_new(self):
        """tests new method to add object to storage"""
        state = State(name="California")
        storage.new(state)
        storage.save()
        retrieved_objs = storage.all(State)
        self.assertEqual(len(retrieved_objs), 1)
        self.assertIsInstance(list(retrieved_objs.values())[0], State)

    def test_save(self):
        """tests save method to commit changes to storage"""
        state = State(name="California")
        storage.new(state)
        storage.save()
        retrieved_objs = storage.all(State)
        self.assertEqual(len(retrieved_objs), 1)

    def test_delete(self):
        """tests delete method to remove object from storage"""
        state = State(name="California")
        storage.new(state)
        storage.save()
        storage.delete(state)
        retrieved_objs = storage.all(State)
        self.assertEqual(len(retrieved_objs), 0)

    def test_get(self):
        """tests get method to retrieve object from storage"""
        state = State(name="California")
        storage.new(state)
        storage.save()
        retrieved_obj = storage.get(State, state.id)
        self.assertIsInstance(retrieved_obj, State)
        self.assertEqual(retrieved_obj.name, "California")

    def test_count(self):
        """tests count method to retrieve number of objects of a class in storage"""
        state1 = State(name="California")
        state

