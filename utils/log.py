def log(message: str, color: str = "cyan", bold: bool = True) -> None:
    """
    Print a message to the console with optional color and bold formatting.

    Args:
        message (str): The message to print.
        color (str): The color of the text. Options are 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'.
        bold (bool): Whether to print the message in bold.
    """
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
    }
    reset = "\033[0m"
    bold_start = "\033[1m" if bold else ""
    print(f"{bold_start}{colors.get(color, colors['cyan'])}{message}{reset}")
