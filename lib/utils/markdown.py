import markdown


def to_html(markdown_str) -> str:
    md = markdown.Markdown(extensions=['tables', 'fenced_code'])
    return md.convert(markdown_str)
