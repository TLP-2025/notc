from modules import scanner

def test(source):
    for token in scanner.tokens(source):
        print(f"{token} --")