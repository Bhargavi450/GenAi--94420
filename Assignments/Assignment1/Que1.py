sentence=input("Enter a sentence: ")
words=sentence.split()
print("Number of words in the sentence:", len(words))

cnt=0
for word in words:
    cnt=cnt+len(word)

print("number of characters in the sentence :",cnt)

def count_vowels(word):
    vowels='aeiouAEIOU'
    count=0
    for char in word:
        if char in vowels:
            count+=1
    return count
 
tot=0
for word in words:
    
    tot=tot+count_vowels(word)
    
print("Total number of vowels in the sentence:",tot)
    
    
 