# p6_Walcott_Justice_test.py
# Justice Walcott
# Unit tests for find_large_files() and Entry.absolute_path().

import unittest

from p6_Walcott_Justice import Entry, File, Folder, find_large_files


def make_tree() -> dict[str, Entry]:
    """Build a small three-level tree and return its entries by name.

    root/
        a.txt (100)
        docs/
            b.txt (500)
            deep/
                c.bin (2000)
                d.txt (0)
        empty/
    """
    root = Folder("root")
    entries: dict[str, Entry] = {"root": root}
    entries["a.txt"] = File("a.txt", 100, root)
    docs = Folder("docs", root)
    entries["docs"] = docs
    entries["b.txt"] = File("b.txt", 500, docs)
    deep = Folder("deep", docs)
    entries["deep"] = deep
    entries["c.bin"] = File("c.bin", 2000, deep)
    entries["d.txt"] = File("d.txt", 0, deep)
    entries["empty"] = Folder("empty", root)
    return entries


class TestFindLargeFiles(unittest.TestCase):
    """Tests for the recursive find_large_files() function."""

    def setUp(self) -> None:
        self.e = make_tree()

    def test_file_at_least_threshold_returns_itself(self) -> None:
        self.assertEqual(find_large_files(self.e["b.txt"], 500),
                         [self.e["b.txt"]])

    def test_file_below_threshold_returns_empty(self) -> None:
        self.assertEqual(find_large_files(self.e["b.txt"], 501), [])

    def test_folder_searches_nested_folders_in_order(self) -> None:
        result = find_large_files(self.e["root"], 100)
        self.assertEqual(result,
                         [self.e["a.txt"], self.e["b.txt"], self.e["c.bin"]])

    def test_high_threshold_only_deepest_large_file(self) -> None:
        self.assertEqual(find_large_files(self.e["root"], 1000),
                         [self.e["c.bin"]])

    def test_threshold_zero_returns_every_file(self) -> None:
        result = find_large_files(self.e["root"], 0)
        self.assertEqual(len(result), 4)
        self.assertIn(self.e["d.txt"], result)

    def test_threshold_above_everything_returns_empty(self) -> None:
        self.assertEqual(find_large_files(self.e["root"], 10 ** 9), [])

    def test_subfolder_only_searches_its_own_contents(self) -> None:
        self.assertEqual(find_large_files(self.e["docs"], 0),
                         [self.e["b.txt"], self.e["c.bin"], self.e["d.txt"]])

    def test_empty_folder_returns_empty(self) -> None:
        self.assertEqual(find_large_files(self.e["empty"], 0), [])

    def test_result_never_contains_folders(self) -> None:
        for item in find_large_files(self.e["root"], 0):
            self.assertIsInstance(item, File)

    def test_float_threshold(self) -> None:
        self.assertEqual(find_large_files(self.e["root"], 499.5),
                         [self.e["b.txt"], self.e["c.bin"]])

    def test_non_entry_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            find_large_files("root", 0)

    def test_non_numeric_threshold_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            find_large_files(self.e["root"], "100")

    def test_negative_threshold_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            find_large_files(self.e["root"], -1)


class TestAbsolutePath(unittest.TestCase):
    """Tests for the recursive Entry.absolute_path() method."""

    def setUp(self) -> None:
        self.e = make_tree()

    def test_root_path_is_just_root(self) -> None:
        self.assertEqual(self.e["root"].absolute_path(), [self.e["root"]])

    def test_top_level_file(self) -> None:
        self.assertEqual(self.e["a.txt"].absolute_path(),
                         [self.e["a.txt"], self.e["root"]])

    def test_deeply_nested_file(self) -> None:
        self.assertEqual(self.e["c.bin"].absolute_path(),
                         [self.e["c.bin"], self.e["deep"], self.e["docs"],
                          self.e["root"]])

    def test_nested_folder(self) -> None:
        self.assertEqual(self.e["deep"].absolute_path(),
                         [self.e["deep"], self.e["docs"], self.e["root"]])

    def test_path_starts_with_self_and_ends_with_root(self) -> None:
        path = self.e["d.txt"].absolute_path()
        self.assertIs(path[0], self.e["d.txt"])
        self.assertIs(path[-1], self.e["root"])
        self.assertIsNone(path[-1].parent())

    def test_each_step_is_the_parent_of_the_previous(self) -> None:
        path = self.e["c.bin"].absolute_path()
        for i in range(len(path) - 1):
            self.assertIs(path[i].parent(), path[i + 1])

    def test_unattached_file_is_its_own_root(self) -> None:
        loose = File("loose.txt", 10)
        self.assertEqual(loose.absolute_path(), [loose])

    def test_path_updates_after_add(self) -> None:
        loose = File("moved.txt", 10)
        self.e["deep"].add(loose)
        self.assertEqual([item.name for item in loose.absolute_path()],
                         ["moved.txt", "deep", "docs", "root"])


class TestInvalidInput(unittest.TestCase):
    """Checks that invalid input raises standard Python exceptions."""

    def test_negative_bytes_used(self) -> None:
        with self.assertRaises(ValueError):
            File("bad.txt", -5)

    def test_non_int_bytes_used(self) -> None:
        with self.assertRaises(TypeError):
            File("bad.txt", "10")

    def test_add_non_entry_to_folder(self) -> None:
        with self.assertRaises(TypeError):
            Folder("f").add("not an entry")

    def test_add_entry_that_already_has_parent(self) -> None:
        first = Folder("first")
        second = Folder("second")
        item = File("x.txt", 1, first)
        with self.assertRaises(ValueError):
            second.add(item)

    def test_add_folder_to_itself(self) -> None:
        folder = Folder("f")
        with self.assertRaises(ValueError):
            folder.add(folder)

    def test_base_entry_size_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            Entry("plain").size()


if __name__ == "__main__":
    unittest.main()
