from mongoengine import Document, ListField, StringField, ReferenceField


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    author = ReferenceField(Author)
    quote = StringField(required=True)
    tags = ListField(StringField())
