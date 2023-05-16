from itertools import product
import hashlib

alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()+'

hashes = {'9f269d8e19f76e6675f6f17d87ab4a54605ad4e229dbf32a45d8904775a741701445c3702b9a5f169ef706c1c5166ab195ebe78df8b34fc95181c69870173ba7', 
    '12fc765f6c422f8cc7755746167b8af829c0cd81994863030df24d8cfca019d5f060387a8d46774550c56d34cb90e28d7ccc46a1ef07dd18ceb5ef16f33cbd2a'}

pass_length = 0

while len(hashes) > 0:
    pass_length += 1

    combinations = product(alphabet, repeat=pass_length)
    
    for combination in combinations:
        password = ''.join(combination)
        sha512hash = hashlib.sha512(password.encode('utf-8')).hexdigest()

        if sha512hash in hashes:
            print(f'password = {password}, hash = {sha512hash}')
            hashes.remove(sha512hash)

        if len(hashes) == 0:
            break
