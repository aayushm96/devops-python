"""from collections import Counter
print(Counter("engineering"))
"""
word = "funny"
char_count = {}

for ch in word:
    if ch in char_count:
        char_count[ch] += 1
    else:
        char_count[ch] = 1

print(char_count)

#word = "devops"
#print(word[::-1])  

s = "engineering"
seen = set()
duplicates = set()

for ch in s:
    if ch in seen:
        duplicates.add(ch)
    else:
        seen.add(ch)

print(list(duplicates))


s = "devops"
rev = ""

for ch in s:
    rev = ch + rev
print(rev)