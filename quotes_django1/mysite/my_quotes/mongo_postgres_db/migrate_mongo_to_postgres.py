from sqlalchemy import select

from .connect_by_mongo import connect
from .models_mongo import Author as mongoAuthor, Quote as mongoQuote
from .models_postgres import Author as postAuthor, Quote as postQuote, session


def get_all_obj_mongo(objects_name: str): #choice Authors or Quotes
    
    match objects_name:
        
        case "Authors":
            print("Get authors to mongo")
            return mongoAuthor.objects()
        
        case "Quotes":
            print("Get quotes to mongo ")
            return mongoQuote.objects()
        

def get_id_mongo_to_id_postgres(mongo_authors_obj):
   
    id_mongo_to_id_postgres = {}

    for mongo_author in mongo_authors_obj:
        
        postgres_author = session.execute(
            select(postAuthor.id)
            .where(postAuthor.fullname==mongo_author.fullname)
        ).fetchone()
        
        id_mongo_to_id_postgres.update({
            str(mongo_author.id): postgres_author.id
        })
        
    return id_mongo_to_id_postgres


def save_authors_to_postgres(mongo_authors_obj):

    for mongo_author_obj in mongo_authors_obj:
        author_dict = mongo_author_obj.to_mongo().to_dict()
        author_dict.pop("_id")
        
        author_postgres = postAuthor(**author_dict)
        session.add(author_postgres)

    session.commit()
    
    print("Saved authors to postgres DB")
    
    
def save_quotes_to_postgres(mongo_quotes_odj, id_mongo_to_id_postgres):
    
    for mongo_quote_odj in mongo_quotes_odj:
        
        quote_dict = mongo_quote_odj.to_mongo().to_dict()
        quote_dict.pop("_id")
        id_mongo = str(quote_dict.pop("author"))
        id_postgres = id_mongo_to_id_postgres.get(id_mongo)
        quote_dict.update({"author_id": id_postgres})
        
        quote_postgres = postQuote(**quote_dict)
        session.add(quote_postgres)
        
    session.commit()
    
    print("Saved quotes to postgres DB")
    
    
def main_migrate():

    mongo_authors_obj = get_all_obj_mongo("Authors")
    save_authors_to_postgres(mongo_authors_obj)
    
    id_mongo_to_id_postgres = get_id_mongo_to_id_postgres(mongo_authors_obj)        
    mongo_quotes_obj = get_all_obj_mongo("Quotes")    
    save_quotes_to_postgres(mongo_quotes_obj, id_mongo_to_id_postgres)
    

if __name__ == "__main__":
    main_migrate()