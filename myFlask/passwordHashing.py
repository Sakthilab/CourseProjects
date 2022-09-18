from passlib.hash import pbkdf2_sha256
password= "hello"
hashed = pbkdf2_sha256.hash(password)
print(hashed)
if pbkdf2_sha256.verify("hello", hashed):
    print("password match succesfully")
else:
    print("password didn't match")