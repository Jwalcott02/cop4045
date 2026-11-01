# p6_Walcott_Justice.py
# Justice Walcott
# Estimating storage size of folders holding files and other folders,
# using an Entry base class with File and Folder subclasses.

from __future__ import annotations


class Entry:
    """Base class for anything stored on the storage system.

    An Entry has a name and an optional parent folder. Subclasses must
    override size(). Nested structures are assumed to contain no cycles.
    """

    def __init__(self, name: str, parent: Folder | None = None) -> None:
        """Create an entry called name, optionally placed inside parent.

        Parameters:
            name: the entry's name; must be a non-empty string.
            parent: the Folder that contains this entry, or None for a
                top-level (root) entry.

        Preconditions: name is a non-empty str; parent is a Folder or None.
        Postconditions: self.name == name. If parent is given, this entry
            has been added to parent's children and self.parent() is parent;
            otherwise self.parent() is None.

        Raises:
            TypeError: if name is not a str, or parent is not a Folder/None.
            ValueError: if name is the empty string.
        """
        if not isinstance(name, str):
            raise TypeError("name must be a str, got " + type(name).__name__)
        if name == "":
            raise ValueError("name must not be empty")
        self.name: str = name
        self._parent: Entry | None = None
        if parent is not None:
            if not isinstance(parent, Folder):
                raise TypeError("parent must be a Folder or None, got " +
                                type(parent).__name__)
            parent.add(self)

    def parent(self) -> Entry | None:
        """Return the folder containing this entry.

        Preconditions: none.
        Postconditions: the entry is unchanged.

        Returns:
            The parent Entry, or None if this entry is a root.
        """
        return self._parent

    def size(self) -> int:
        """Return the number of bytes this entry uses.

        This is the base-class interface; each subclass overrides it.

        Preconditions: none.
        Postconditions: the entry is unchanged.

        Returns:
            The size in bytes as a nonnegative int.

        Raises:
            NotImplementedError: always, since a plain Entry has no size.
        """
        raise NotImplementedError("subclasses of Entry must override size()")

    def absolute_path(self) -> list[Entry]:
        """Return the path from this entry up to the root, recursively.

        Base case: a root entry (no parent) returns [self].
        Recursive case: [self] followed by the parent's absolute path.

        Preconditions: the parent chain contains no cycles.
        Postconditions: the entry and its ancestors are unchanged.

        Returns:
            A list of Entry objects starting with self, then its parent, and
            so on, ending with the top-most (root) entry.
        """
        if self._parent is None:
            return [self]
        return [self] + self._parent.absolute_path()

    def __repr__(self) -> str:
        """Return a short debugging representation such as Entry('x').

        Returns:
            A string with the class name and the entry's name.
        """
        return type(self).__name__ + "(" + repr(self.name) + ")"


class File(Entry):
    """A file that occupies a fixed, nonnegative number of bytes."""

    def __init__(self, name: str, bytes_used: int,
                 parent: Folder | None = None) -> None:
        """Create a file called name that uses bytes_used bytes.

        Parameters:
            name: the file's name; must be a non-empty string.
            bytes_used: number of bytes the file occupies; an int >= 0.
            parent: the Folder that contains this file, or None.

        Preconditions: bytes_used is a nonnegative int (bool not allowed).
        Postconditions: self.bytes_used == bytes_used, and the file is in
            parent's children if parent was given.

        Raises:
            TypeError: if bytes_used is not an int, or name/parent are of
                the wrong type (see Entry.__init__).
            ValueError: if bytes_used is negative or name is empty.
        """
        if isinstance(bytes_used, bool) or not isinstance(bytes_used, int):
            raise TypeError("bytes_used must be an int, got " +
                            type(bytes_used).__name__)
        if bytes_used < 0:
            raise ValueError("bytes_used must be nonnegative, got " +
                             str(bytes_used))
        # Validate before calling the base constructor so a bad file is
        # never added to its parent folder.
        self.bytes_used: int = bytes_used
        super().__init__(name, parent)

    def size(self) -> int:
        """Return the number of bytes used by this file.

        Overrides Entry.size().

        Preconditions: none.
        Postconditions: the file is unchanged.

        Returns:
            self.bytes_used.
        """
        return self.bytes_used


class Folder(Entry):
    """A folder that holds files and other folders as its children."""

    def __init__(self, name: str, parent: Folder | None = None) -> None:
        """Create an empty folder called name.

        Parameters:
            name: the folder's name; must be a non-empty string.
            parent: the Folder that contains this folder, or None.

        Preconditions: same as Entry.__init__.
        Postconditions: the folder has no children, and it is in parent's
            children if parent was given.

        Raises:
            TypeError, ValueError: as described in Entry.__init__.
        """
        self._children: list[Entry] = []
        super().__init__(name, parent)

    def add(self, entry: Entry) -> None:
        """Add entry to the end of this folder's children.

        Parameters:
            entry: the File or Folder to place inside this folder.

        Preconditions: entry is an Entry with no parent yet, and entry is
            not this folder or one of its ancestors.
        Postconditions: entry is the last element of self.children() and
            entry.parent() is self.

        Raises:
            TypeError: if entry is not an Entry.
            ValueError: if entry already belongs to a folder, or adding it
                would make a folder contain itself.
        """
        if not isinstance(entry, Entry):
            raise TypeError("can only add Entry objects to a Folder, got " +
                            type(entry).__name__)
        if entry._parent is not None:
            raise ValueError(repr(entry) + " already belongs to " +
                             repr(entry._parent))
        if entry in self.absolute_path():
            raise ValueError("adding " + repr(entry) + " to " + repr(self) +
                             " would create a cycle")
        self._children.append(entry)
        entry._parent = self

    def children(self) -> tuple[Entry, ...]:
        """Return this folder's direct children.

        Preconditions: none.
        Postconditions: the folder is unchanged (a tuple is returned so the
            caller cannot modify the internal list).

        Returns:
            A tuple of the child entries in the order they were added.
        """
        return tuple(self._children)

    def size(self) -> int:
        """Return the total size of everything inside this folder.

        Overrides Entry.size(). Each child's own size() is called, so files
        report their bytes and nested folders recurse into their contents.
        An empty folder has size 0.

        Preconditions: the folder structure contains no cycles.
        Postconditions: the folder and its contents are unchanged.

        Returns:
            The sum of size() over all children, as a nonnegative int.
        """
        total = 0
        for child in self._children:
            total = total + child.size()
        return total


def find_large_files(entry: Entry, minimum_size: int | float) -> list[File]:
    """Return every File at or under entry whose size is >= minimum_size.

    Behavior:
        - If entry is a File: returns [entry] if entry.size() >= minimum_size,
          otherwise [] (base case).
        - If entry is a Folder: recursively searches every child, including
          nested folders, and returns the matching files in depth-first
          order (the order children were added). An empty folder gives [].
        - Folders themselves are never included in the result.

    Parameters:
        entry: the File or Folder to start searching from.
        minimum_size: the smallest size (in bytes) a file needs to be
            included; a nonnegative int or float.

    Preconditions: the structure under entry contains no cycles.
    Postconditions: entry and its contents are unchanged.

    Returns:
        A new list of File objects (possibly empty).

    Raises:
        TypeError: if entry is not a File or Folder, or minimum_size is not
            an int or float.
        ValueError: if minimum_size is negative.
    """
    if (isinstance(minimum_size, bool) or
            not isinstance(minimum_size, (int, float))):
        raise TypeError("minimum_size must be a number, got " +
                        type(minimum_size).__name__)
    if minimum_size < 0:
        raise ValueError("minimum_size must be nonnegative, got " +
                         str(minimum_size))
    if isinstance(entry, File):
        if entry.size() >= minimum_size:
            return [entry]
        return []
    if isinstance(entry, Folder):
        found: list[File] = []
        for child in entry.children():
            found = found + find_large_files(child, minimum_size)
        return found
    raise TypeError("entry must be a File or Folder, got " +
                    type(entry).__name__)


def path_names(entry: Entry) -> list[str]:
    """Return the names along entry's absolute path, from entry to the root.

    Parameters:
        entry: any Entry.

    Preconditions: the parent chain contains no cycles.
    Postconditions: entry is unchanged.

    Returns:
        A list of names, one per Entry in entry.absolute_path().
    """
    names = []
    for item in entry.absolute_path():
        names.append(item.name)
    return names


def build_sample_tree() -> Folder:
    """Build the sample storage hierarchy used by main().

    Layout (sizes in bytes):
        university/
            readme.txt (1200)
            cs/
                syllabus.pdf (250000)
                cop4045/
                    notes.txt (8000)
                    homework4/
                        p6.py (15000)
                        lecture.mp4 (900000000)
                    grades.csv (4000)
            library/
                catalog.db (500000000)

    Preconditions: none.
    Postconditions: a new, independent tree is created each call.

    Returns:
        The root Folder named "university".
    """
    root = Folder("university")
    File("readme.txt", 1200, root)
    cs = Folder("cs", root)
    File("syllabus.pdf", 250000, cs)
    course = Folder("cop4045", cs)
    File("notes.txt", 8000, course)
    homework = Folder("homework4", course)
    File("p6.py", 15000, homework)
    File("lecture.mp4", 900000000, homework)
    File("grades.csv", 4000, course)
    library = Folder("library", root)
    File("catalog.db", 500000000, library)
    return root


def find_entry(folder: Folder, name: str) -> Entry | None:
    """Search folder (recursively) for the first entry called name.

    Parameters:
        folder: the Folder to search inside.
        name: the entry name to look for.

    Preconditions: the structure contains no cycles.
    Postconditions: folder is unchanged.

    Returns:
        The first matching Entry in depth-first order, or None.
    """
    for child in folder.children():
        if child.name == name:
            return child
        if isinstance(child, Folder):
            found = find_entry(child, name)
            if found is not None:
                return found
    return None


def print_tree(entry: Entry, indent: int = 0) -> None:
    """Print entry and everything beneath it, one entry per line.

    Uses only the common Entry interface (name and size()), so files and
    folders are displayed the same way.

    Parameters:
        entry: the Entry to print.
        indent: number of indentation levels for this entry; an int >= 0.

    Preconditions: the structure contains no cycles.
    Postconditions: nothing is modified; output is written to stdout.
    """
    label = entry.name + ("/" if isinstance(entry, Folder) else "")
    print("  " * indent + "  " + label + "  (" + format(entry.size(), ",") +
          " bytes)")
    if isinstance(entry, Folder):
        for child in entry.children():
            print_tree(child, indent + 1)


def main() -> None:
    """Demonstrate parts f) and g) on a sample storage hierarchy.

    Preconditions: none.
    Postconditions: results are printed to stdout.
    """
    print("Justice Walcott, FAU ID: Z23692334")
    print()

    root = build_sample_tree()

    print("=== Part f) Folder hierarchy (4 levels deep) ===")
    print_tree(root)
    print()

    print("--- Part f) Polymorphism: size() through the Entry interface ---")
    # The same size() call works on every Entry; Python picks
    # File.size() or Folder.size() based on the object's actual class.
    for child in root.children():
        print("  " + type(child).__name__.ljust(6) + " " +
              child.name.ljust(12) + " size() = " +
              format(child.size(), ","))
    print("  One call to root.size() on the outer folder: " +
          format(root.size(), ",") + " bytes")
    print()

    print("--- Part f) find_large_files at two thresholds ---")
    for threshold in (10000, 1000000):
        large = find_large_files(root, threshold)
        print("  Files of at least " + format(threshold, ",") + " bytes (" +
              str(len(large)) + " found):")
        for file in large:
            print("    " + file.name + "  (" + format(file.size(), ",") +
                  " bytes)")
    print()

    print("=== Part g) absolute_path() ===")
    for name in ("p6.py", "homework4", "catalog.db", "university"):
        if name == root.name:
            entry: Entry | None = root
        else:
            entry = find_entry(root, name)
        if entry is None:
            continue
        print("  absolute_path() of " + name + ": " +
              " -> ".join(path_names(entry)))
        print("    as a path string: /" +
              "/".join(reversed(path_names(entry))))


if __name__ == "__main__":
    main()
