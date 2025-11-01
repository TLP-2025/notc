errors = []

def reportError(reporter, msg):
    print(f'ERROR {reporter}: {msg}',)
    errors.append(msg)