#Business logic such as the actual creating, destroying, and upating will go here


def create_book(data):
    Title = data.get('Title')
    Author = data.get('Author')
    ID = data.get('ID')
    Genre = data.get('Genre')
    YearReleased = data.get('YearReleased')
    CheckedOut = data.get('CheckedOut')