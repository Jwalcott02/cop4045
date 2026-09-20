"""Problem 2: Comprehensions."""


def main() -> None:
    """Run and print the results of parts a-f."""
    print("FAU ID: Z23692334")

    # a) all (a, b, c, d) with distinct integers 1-10 where a^2+b^2 = c^2+d^2
    a_result = [
        (a, b, c, d)
        for a in range(1, 11)
        for b in range(1, 11)
        for c in range(1, 11)
        for d in range(1, 11)
        if len({a, b, c, d}) == 4 and a ** 2 + b ** 2 == c ** 2 + d ** 2
    ]
    print("\na)")
    print(a_result)

    # b) (lowercase string, length) for strings shorter than 5 characters
    words = ['One', 'SEVEN', 'three', 'two', 'Ten']
    b_result = [(w.lower(), len(w)) for w in words if len(w) < 5]
    print("\nb)")
    print(b_result)

    # c) "Firstname M. Lastname" from "Firstname Middlename Lastname"
    names = ['Christopher Ashton Kutcher', 'Elizabeth Stamatina Fey']
    c_result = [
        f"{n.split()[0]} {n.split()[1][0]}. {n.split()[2]}" for n in names
    ]
    print("\nc)")
    print(c_result)

    # d) anagram pairs (case insensitive) between lst1 and lst2
    lst1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
    lst2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]
    d_result = [
        (w1, w2)
        for w1 in lst1
        for w2 in lst2
        if sorted(w1.lower()) == sorted(w2.lower())
    ]
    print("\nd)")
    print(d_result)

    # e) string -> length dictionary
    s = ['one', 'two', 'three']
    e_result = {word: len(word) for word in s}
    print("\ne)")
    print(e_result)

    # f) index -> vowel character dictionary
    text = "Hello world"
    f_result = {i: c for i, c in enumerate(text) if c.lower() in "aeiou"}
    print("\nf)")
    print(f_result)


if __name__ == "__main__":
    main()