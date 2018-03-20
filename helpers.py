def url_from_form(form_data):
    return "-".join(form_data.split())

def readable_from_url(url):
    return " ".join(url.split('-'))
