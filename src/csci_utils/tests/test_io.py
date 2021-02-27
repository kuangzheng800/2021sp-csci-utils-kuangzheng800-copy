import os
from tempfile import TemporaryDirectory
from ..io.io import atomic_write
from unittest import TestCase, main

class FakeFileFailure(IOError):
    pass

class TestAtomicWriter(TestCase):
    def test_success(self):
        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with atomic_write(fp, "w") as f:
                assert not os.path.exists(fp)
                tmpfile = f.name
                f.write("asdf")
                print(fp)
            assert(os.path.exists(tmpfile) == False)
            assert(os.path.exists(fp))

            with open(fp) as f:
                assert(f.read() == "asdf")

    def test_fail(self):
        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")
            try:
                with atomic_write(fp, "w") as f:
                    tmpfile = f.name
                    assert(os.path.exists(tmpfile))
                    raise FakeFileFailure()
            except FakeFileFailure:
                pass
            assert not os.path.exists(tmpfile)
            assert not os.path.exists(fp)
