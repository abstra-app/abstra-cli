def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text

def digits(n):
    return len(str(n))

def format_digits (n, d): 
    return " " * (d - digits(n)) + str(n)