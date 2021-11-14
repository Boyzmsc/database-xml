thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]

print(thislist)
print(thislist[1])
print(thislist[2:5])
print(len(thislist))
print()

for x in thislist:
    print(x)
print()

if "apple" in thislist:
    print("Yes, 'apple' is in the fruits list")
print()

print(thislist.count('kiwi'))
print(thislist.index('kiwi'))

thislist.sort()
print(thislist)
print(thislist.index('kiwi'))

thislist.append("water melon")
print(thislist)
print(thislist.index('water melon'))
