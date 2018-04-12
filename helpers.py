def url_from_form(form_data):
    return "-".join(form_data.split())

def readable_from_url(url):
    return " #"+" #".join(url.split('-'))

def get_credentials():
    with open('credentials.txt', 'r') as cred_file:
        contents = cred_file.read().split('\n')
        return (contents[0], contents[1])
