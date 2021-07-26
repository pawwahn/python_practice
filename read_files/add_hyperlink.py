def is_text_link(text):
    for i in ['http', '://', 'www.', '.com', '.org', '.cn', '.xyz', '.htm']:
        if i in text:
            return True
        else:
            return False

def add_text_link(document, text):
    paragraph = document.add_paragraph()
    text = re.split(r'<a href="|">|</a>',text)
    keyword = None
    for i in range(len(text)):
        if not is_text_link(text[i]):
            if text[i] != keyword:
                paragraph.add_run(text[i])
        elif i + 1<len(text):
            url=text[i]
            keyword=text[i + 1]
            add_hyperlink(paragraph, url, keyword, None, True)