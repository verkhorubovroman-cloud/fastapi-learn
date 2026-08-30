#код для проверки id если начинается не с  isbn- или imdb-
def check_valid_id(id : str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id
