from abstra_cli.file_utils import remove_filepath_prefix
import unittest

class TestFileUtils(unittest.TestCase):
  def test_remove_filepath_prefix_no_dot(self):
    filepath = "folder/file"
    prefix = "folder"
    self.assertEquals(remove_filepath_prefix(filepath, prefix), "file")

  def test_remove_filepath_prefix_dotted_both(self):
    filepath = "./folder/file"
    prefix = "./folder"
    self.assertEquals(remove_filepath_prefix(filepath, prefix), "file")
  
  def test_remove_filepath_prefix_dotted_filepath(self):
    filepath = "./folder/file"
    prefix = "folder"
    self.assertEquals(remove_filepath_prefix(filepath, prefix), "file")

  def test_remove_filepath_prefix_dotted_prefix(self):
    filepath = "folder/file"
    prefix = "./folder"
    self.assertEquals(remove_filepath_prefix(filepath, prefix), "file")

if __name__ == '__main__':
    unittest.main()
