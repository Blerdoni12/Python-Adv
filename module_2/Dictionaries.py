contact_info = {
    "Blerdon": "5555-444",
    "Ibriqi": "1234-3333"
}

print(contact_info)

alice_phone = contact_info["Blerdon"]
print(alice_phone)

#update Blerdon's phone number
contact_info["Blerdon"]= "123456"
print(contact_info)

#add a new contact
contact_info["Eve"]="555-99999"
print(contact_info)

#delete a contact
del contact_info["Ibriqi"]
print(contact_info)

#.keys()
keys=contact_info.keys()
print(keys)

#get the values
values=contact_info.values()
print(values)

#get the items
items=contact_info.items()
print(items)









