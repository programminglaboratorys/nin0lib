from dataclasses import dataclass

@dataclass
class Message:
    role: int
    content: str
    username: str


def main():
    m1 = Message(role="user", content="hi", username="John")
    m2 = Message(role="admin", content="hello", username="Jane")

    print(m1)
    print(m2)

if __name__ == "__main__":
    main()

