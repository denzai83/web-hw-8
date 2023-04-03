import redis
from redis_lru import RedisLRU
from mongoengine import connect, DoesNotExist
from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

connect(host='mongodb+srv://hw8:567432@cluster0.g08jtiw.mongodb.net/hw8?retryWrites=true&w=majority')

if __name__ == '__main__':
    while True:
        input_str = input('Please enter command:')
        if input_str == 'exit':
            break
        input_data = input_str.split(':')
        command = input_data[0]
        value = input_data[1].strip() if len(input_data) > 1 else None

        try:
            if command == 'name':
                cache_key = f'name:{value}'
                result = cache.get(cache_key)
                if result is None:
                    author = Author.objects.get(fullname=value.title())
                    quotes = Quote.objects(author=author)
                    result = [f"{quote.quote} ({quote.author.fullname}, {', '.join(quote.tags)})" for quote in quotes]
                    cache.set(cache_key, result)
                
                for quote in result:
                    print(quote)
            
            elif command == 'tag':
                cache_key = f'tag:{value}'
                result = cache.get(cache_key)
                if result is None:
                    quotes = Quote.objects(tags=value.lower())
                    result = [f"{quote.quote} ({quote.author.fullname}, {', '.join(quote.tags)})" for quote in quotes]
                    cache.set(cache_key, result)
                
                for quote in result:
                    print(quote)
            
            elif command == 'tags':
                tags = value.split(',')
                quotes = Quote.objects(tags__in=tags)
                for quote in quotes:
                    print(f"{quote.quote} ({quote.author.fullname}, {', '.join(quote.tags)})")
            
            else:
                print('Wrong command format')
        except DoesNotExist as e:
            print(f'Error: {e}')
        except Exception as e:
            print(f'Error: {e}')
