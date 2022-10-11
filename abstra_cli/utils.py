import re


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


def digits(n):
    return len(str(n))


def format_digits(n, d):
    return " " * (d - digits(n)) + str(n)


def parse_env_var(var):
    match = re.search("^(\w+)=(.+)$", var.strip())
    if match:
        return match.group(1), match.group(2)
    return None, None


def parse_package(pkg):
    # https://peps.python.org/pep-0440/#version-specifiers

    match = re.search(
        "^(([\w\.\-]+)\s*)(~=|===|>=|<=|==)(\s*([^\[\]\,\;\>\<\s]+))$", pkg
    )
    if match:
        name = match.group(2)
        version = match.group(5)
        return name, version

    if re.search("\>|\<|\,|\;|\[|\]", pkg):
        return None, None

    return pkg, None

def remove_from_dict(keys, obj):
    for key in keys:
        obj.pop(key, None)