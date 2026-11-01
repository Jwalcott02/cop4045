print("FAU ID: Z23692334")

# a
a = [(a, b, c, d) for a in range(1, 11) for b in range(1, 11)
     for c in range(1, 11) for d in range(1, 11)
     if len({a, b, c, d}) == 4 and a**2 + b**2 == c**2 + d**2]
print("a)", a)

# b
words = ['One', 'SEVEN', 'three', 'two', 'Ten']
b = [(w.lower(), len(w)) for w in words if len(w) < 5]
print("b)", b)

# c
names = ['Christopher Ashton Kutcher', 'Elizabeth Stamatina Fey']
c = [n.split()[0] + " " + n.split()[1][0] + ". " + n.split()[2] for n in names]
print("c)", c)

# d
lst1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
lst2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]
d = [(w1, w2) for w1 in lst1 for w2 in lst2
     if sorted(w1.lower()) == sorted(w2.lower())]
print("d)", d)

# e
s = ['one', 'two', 'three']
e = {word: len(word) for word in s}
print("e)", e)

# f
text = "Hello world"
f = {i: ch for i, ch in enumerate(text) if ch.lower() in "aeiou"}
print("f)", f)
