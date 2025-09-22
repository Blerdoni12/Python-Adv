def get_average_age(people):
    """Return the average age from the dictionary of people."""
    if not people:
        return 0
    return sum(people.values()) / len(people)


def get_people(num_people=5):
    """Ask user for names and ages, return dictionary of people."""
    people = {}
    while len(people) < num_people:
        name = input(f"Enter name {len(people)+1}: ").strip()
        try:
            age = int(input(f"Enter age for {name}: "))
            if age < 0:
                raise ValueError("Age cannot be negative.")
            people[name] = age
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
    return people


def main():
    people = get_people(5)
    ages = set(people.values())

    print("\nPeople older than 18:")
    for name, age in people.items():
        if age > 18:
            print(name)

    print("\nUnique ages:", ages)
    print(f"\nAverage age: {get_average_age(people):.2f}")


if __name__ == "__main__":
    main()
