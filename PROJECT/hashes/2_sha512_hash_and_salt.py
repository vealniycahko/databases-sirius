from itertools import product
import hashlib

alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()+'

hash = '457d2dee67c5cdee1d987706ecdb6dfe1a18861b180acc2b4024b07a46cce0bb5261477d15d4278669764ac4163b5ac630f32f7e52ed8f5ec34ebc3c3d844d0e'
salt = '0275d7e2-121f-4ca8-a230-53d35ca3ba64'

found = False
pass_length = 0

while not found:
    pass_length += 1

    combinations = product(alphabet, repeat=pass_length)
    
    for combination in combinations:
        password = ''.join(combination)

        if hashlib.sha512((password + salt).encode('utf-8')).hexdigest() == hash:
            print(f'password = {password}')
            found = True
            break
