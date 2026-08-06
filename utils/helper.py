import markdown


def format_markdown(text):
    """
    Converts markdown text
    into HTML for display.
    """

    return markdown.markdown(
        text,
        extensions=[
            "fenced_code",
            "tables"
        ]
    )