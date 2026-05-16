def infinite_counter(start:int=0)->int:
    while True:
        yield start
        start+=1
counter=infinite_counter()
print(next(counter))
print(next(counter))
print(next(counter))
print(next(counter))
print(next(counter))

def read_in_chunks(text:str, chunk_size:int)->str:
    for i in range(0, len(text), chunk_size):
        yield text[i:i+chunk_size]
    
text="Testing the generator function to read text as chunks"
for chunk in read_in_chunks(text,5):
    print(chunk)