
import os,sys
from io import StringIO
from tempfile import TemporaryDirectory
from unittest import TestCase

from ..hashstr.hash_str import hash_str, get_csci_salt, get_csci_pepper


# class FakeFileFailure(IOError):
#     pass

class saltTests(TestCase):
    def test_salt(self):
        self.assertEqual(hash_str(get_csci_salt())[:8], b'\xf0\xcfRG\x9b\xa8\xf0I')
        self.assertEqual(hash_str(get_csci_pepper())[:8], b'\x9e\x0f\xf5\x1f\x0e\xf6J\xdc')

class HashTests(TestCase):
    def test_basic(self):
        self.assertEqual(hash_str("world!", salt="hello, ").hex()[:6], "68e656")

class HashTests_CSCIsalt(TestCase):
    def test_basic(self):
        self.assertEqual(hash_str("world!").hex()[:6], "711e96")

