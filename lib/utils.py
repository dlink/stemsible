""" Utility functions that don't deserve a separate module"""


def js_arg(string_to_escape):
    """
    js_arg(string) -> string

    Takes a string and modifies it that so it can be used as an argument in
    a function specified in HTML (<elem onevent="myFunction(myArgument)" />)
    """
    escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "\\'",    # Doesn't work with "&apos;" because browser's html
        "\\": "\\\\",  # parser unescapes it
        ">": "&gt;",
        "<": "&lt;",
    }
    return "".join(escape_table.get(c, c) for c in string_to_escape)
