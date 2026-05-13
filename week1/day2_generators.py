def infinite_counter(start=0):
    while True:
        yield start
        start+=1
counter=infinite_counter()
print(next(counter))
print(next(counter))
print(next(counter))
print(next(counter))
print(next(counter))

def read_in_chunks(text, chunk_size):
    for i in range(0, len(text), chunk_size):
        yield text[i:i+chunk_size]
    
text="Lorem ipsum dolor "
for chunk in read_in_chunks(text,5):
    print(chunk)