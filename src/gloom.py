class GLOOM:
    def __init__(self) -> None:
        pass

    def run(self):
        command = None
        while command != "q":
            command = input("Pick a scenario: ")


if __name__ == "__main__":
    gloom = GLOOM()
    gloom.run()
