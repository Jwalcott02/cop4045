"""Problem 3: Social Network."""

import csv


def add_user(sn: dict, username: str, fullname: str) -> bool:
    """Add a new user to sn. Return False if the user already exists."""
    try:
        if username in sn:
            return False
        sn[username] = (fullname, [])
        return True
    except Exception as e:
        print(f"Error in add_user: {e}")
        raise


def add_friend(sn: dict, user1: str, user2: str) -> bool:
    """Add a mutual friend link between user1 and user2."""
    try:
        if user1 not in sn or user2 not in sn:
            return False
        if user2 not in sn[user1][1]:
            sn[user1][1].append(user2)
        if user1 not in sn[user2][1]:
            sn[user2][1].append(user1)
        return True
    except Exception as e:
        print(f"Error in add_friend: {e}")
        raise


def get_friends(sn: dict, user1: str, distance: int) -> list:
    """Return all friends of user1 up to the given distance."""
    try:
        if user1 not in sn:
            return []
        visited = [user1]
        level = [user1]
        for _ in range(distance):
            new_level = []
            for u in level:
                for f in sn[u][1]:
                    if f not in visited:
                        visited.append(f)
                        new_level.append(f)
            level = new_level
        visited.remove(user1)
        return visited
    except Exception as e:
        print(f"Error in get_friends: {e}")
        raise


def save_network(filename: str, sn: dict) -> None:
    """Save sn to a .csv file."""
    try:
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            for username, (fullname, friends) in sn.items():
                writer.writerow([username, fullname, ";".join(friends)])
    except Exception as e:
        print(f"Error in save_network: {e}")
        raise


def load_network(filename: str) -> dict:
    """Load a social network saved by save_network() and return it."""
    try:
        sn = {}
        with open(filename, "r", newline="") as f:
            for username, fullname, friends_str in csv.reader(f):
                friends = friends_str.split(";") if friends_str else []
                sn[username] = (fullname, friends)
        return sn
    except Exception as e:
        print(f"Error in load_network: {e}")
        raise


def testif(condition: bool, testname: str) -> None:
    """Print PASS or FAIL for a test."""
    print(("PASS: " if condition else "FAIL: ") + testname)


def test() -> None:
    """Extra credit: test parts a)-e) using testif."""
    sn = {
        'alice': ('Alice Smith', ['maria']),
        'maria': ('Maria Cortez', ['alice', 'joe', 'david']),
        'joe': ('Joseph Adams', ['maria', 'eve']),
        'eve': ('Evelyn Cooper', ['joe']),
        'david': ('David Benson', ['maria']),
    }

    testif(add_user(sn, 'frank', 'Frank Ocean') == True, "add_user new user")
    testif(add_user(sn, 'alice', 'Alice Smith') == False, "add_user existing user")
    testif(add_friend(sn, 'frank', 'eve') == True, "add_friend valid users")
    testif(add_friend(sn, 'frank', 'nobody') == False, "add_friend bad user")
    testif(get_friends(sn, 'alice', 1) == ['maria'], "get_friends distance 1")
    testif(sorted(get_friends(sn, 'alice', 2)) == ['david', 'joe', 'maria'], "get_friends distance 2")
    testif(get_friends(sn, 'nobody', 1) == [], "get_friends bad user")

    save_network("test_network.csv", sn)
    testif(load_network("test_network.csv") == sn, "save/load round trip")


def main() -> None:
    """Test all the functions above."""
    print("FAU ID: Z23692334")

    sn = {
        'alice': ('Alice Smith', ['maria']),
        'maria': ('Maria Cortez', ['alice', 'joe', 'david']),
        'joe': ('Joseph Adams', ['maria', 'eve']),
        'eve': ('Evelyn Cooper', ['joe']),
        'david': ('David Benson', ['maria']),
    }

    print("\na)")
    print(add_user(sn, 'frank', 'Frank Ocean'))
    print(add_user(sn, 'alice', 'Alice Smith'))

    print("\nb)")
    print(add_friend(sn, 'frank', 'eve'))
    print(add_friend(sn, 'frank', 'nobody'))

    print("\nc)")
    print(get_friends(sn, 'alice', 1))
    print(get_friends(sn, 'alice', 2))

    print("\nd)")
    save_network("network.csv", sn)
    print("saved network.csv")

    print("\ne)")
    print(load_network("network.csv"))

    print("\ng)")
    test()


if __name__ == "__main__":
    main()