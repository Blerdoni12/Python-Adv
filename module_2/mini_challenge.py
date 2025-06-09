# 1.  Create two dictionaries, Jane and John, to store contact information for Jane and John, respectively.
# 2.  Each contact dictionary contains keys for 'name,' 'phone,' and 'email' with corresponding values.
# 3.  Create a contacts dictionary and use the names 'Jane' and 'John' as keys, associating them with their respective contact dictionaries.
# 4.  Print Jane's contact information.
# 5.  Update Jane's phone number.
# 6.  Print Jane's updated contact information.

Jane = {
    'name': 'Jane',
    'phone': '123-123-123',
    'email': 'jane@gmail.com'
}

John = {
    'name': 'John ',
    'phone': '999-999-999',
    'email': 'john.smith@gmail.com'
}
contacts = {
    'Jane': Jane,
    'John': John
}
print("Jane's contact information:")
print(contacts['Jane'])
contacts['Jane']['phone'] = '123-123-123'
print("\nJane's updated contact information:")
print(contacts['Jane'])



