def load_file(filename):
    with open(filename, 'r') as f:
        s = f.readlines()
    return s