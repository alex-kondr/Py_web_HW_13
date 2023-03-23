import dateutil
from mongoengine import Document
from mongoengine.fields import DateTimeField, ListField, StringField, ReferenceField


class Author(Document):
    
    fullname = StringField()
    born_date = DateTimeField(default=dateutil.parser)
    born_location = StringField()
    description = StringField()
    

class Quote(Document):
    
    tags = ListField()
    author = ReferenceField(Author)
    quote = StringField()