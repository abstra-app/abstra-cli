from abstra_cli.upload import files_from_directory
import unittest
import random
import os
from pathlib import PosixPath

def generate_random_folder():
    name = 'dir-' + random.randbytes(5).hex()
    path = "/tmp/" + name
    os.mkdir(path)
    return path

def add_file(path, name, content):
    filepath = path + "/" + name
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath

def add_folder(path, name):
    folderpath = path + "/" + name
    os.mkdir(folderpath)
    return folderpath

class TestListing(unittest.TestCase):
    def test_empty_directory(self):
        path = generate_random_folder()
        files = files_from_directory(path)
        self.assertEqual(files, [])


    def test_no_ignore(self):
        path = generate_random_folder()
        filepath = add_file(path, "foo", "bar")
        files = files_from_directory(path)
        self.assertEqual(files, [PosixPath(filepath)])

    def test_ignore_file(self):
        path = generate_random_folder()
        add_file(path, "ignored", "foo")
        tracked = add_file(path, "tracked", "bar")
        filepath = add_file(path, ".abstraignore", "ignored")
        files = files_from_directory(path)
        self.assertEqual(files, [PosixPath(tracked)])

    def test_ignore_empty(self):
        path = generate_random_folder()
        add_folder(path, "ignored")
        add_folder(path, "empty")
        filepath = add_file(path, ".abstraignore", "ignored")
        files = files_from_directory(path)
        self.assertEqual(files, [])

    def test_ignore_folder(self):
        path = generate_random_folder()
        ignored = add_folder(path, "ignored")
        add_file(ignored, 'ignored', 'foo')
        folder = add_folder(path, "tracked")
        tracked = add_file(folder, 'tracked', 'tracked')
        filepath = add_file(path, ".abstraignore", "ignored")
        files = files_from_directory(path)
        self.assertEqual(files, [PosixPath(tracked)])

if __name__ == '__main__':
    unittest.main()