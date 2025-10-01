# file_path = "example.text"
# file = open(file_path , "r")
#
# content=file.read()
# print(content)

# file.close()
#
file_path="example.text"
# # with open (file_path, "r") as file:
# #     content= file.read()
# # print(content)
#
# with open("example.text","r") as file:
#     line1 = file.readline()
#     print(line1)
#
# with open("example.text","r") as file:
#     lines = file.readlines()
#     print(lines)
#
# with open ("example.text","w") as file:
#     file.write = ("Hello World")
#
# lines = ['Hello,World \n', 'Welcome \n']
# with open('example.text','w') as file:
#     file.writelines(lines)

# import os
# if os.path.exists("example.txt"):
#     print("File exists!")

# with open("example.txt", 'a') as file:
#     file.write("New data appended")

# data = b'this is a binary data'
#
# with open('example.bin', 'wb') as file:
#     file.write(data)


with open('example.text', 'r') as file:
    for line in file:
        cleaned_line = line.strip()
        print(cleaned_line)

