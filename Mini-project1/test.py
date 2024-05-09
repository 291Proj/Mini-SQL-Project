


'''

List = ['Hello how are you', 'Akib Zaman Choudhury']


keywords = input('Enter: ')



b = False

for sentence in List:
    if keywords.lower() in sentence.lower():
        b = True
        break

print(b)
'''
'''
sentence = 'Hello Akib'

print(sentence[1:])

'''


'''
# Two lists of tuples
list1 = [(1, 2), (3, 4), (5, 6)]
list2 = [(3, 4), (7, 8), (1, 2)]

lost = list1 + list2
a_set = set()

for i in lost:
    a_set.add(i)

print(a_set)

'''
#seen = set()
#print([seen.add(tpl) or tpl for tpl in lost if tpl not in seen])

# Display the resulting list
#print("Combined list with no duplicate tuples:", combined_list)





'''
# Get user input
user_input = input("Enter a sentence with hashtag terms: ")

# Split the input sentence into words
words = user_input.split()

# stores hashtag terms in a list
hashtag_terms = [word[1:] for word in words if word.startswith("#")]



if hashtag_terms:
    print("Hashtag terms in the sentence:")
    for term in hashtag_terms:
        print(term)
else:
    print("No hashtag terms found in the sentence.")

'''

timezone = input("Enter your timezone: ")


if int(timezone):
    if (-12 <= int(timezone) <= 14):
        print('yes')