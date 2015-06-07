#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ConfigParser import SafeConfigParser
import Crypto.Random
from Crypto.Cipher import AES
import hashlib

config = {}
execfile("Control.conf", config)  

class encryption():
	def generate_key(self, password, salt, iterations):
		assert iterations > 0
		key = password + salt
		for i in range(iterations):
			key = hashlib.sha256(key).digest()  
		return key
	
	def pad_text(self, text, multiple):
		extra_bytes = len(text) % multiple
		padding_size = multiple - extra_bytes
		padding = chr(padding_size) * padding_size
		padded_text = text + padding
		return padded_text

	def unpad_text(self, padded_text):
		padding_size = ord(padded_text[-1])
		text = padded_text[:-padding_size]
		return text
	
	def encrypt(self, plaintext, password):
		salt = Crypto.Random.get_random_bytes(config["SALT_SIZE"])
		key = encryption().generate_key(password, salt, config["NUMBER_OF_ITERATIONS"])
		cipher = AES.new(key, AES.MODE_ECB)
		padded_plaintext = encryption().pad_text(plaintext, config["AES_MULTIPLE"])
		ciphertext = cipher.encrypt(padded_plaintext)
		ciphertext_with_salt = salt + ciphertext
		return ciphertext_with_salt

	def decrypt(self, ciphertext, password):
		salt = ciphertext[0:config["SALT_SIZE"]]
		ciphertext_sans_salt = ciphertext[config["SALT_SIZE"]:]
		key = encryption().generate_key(password, salt, config["NUMBER_OF_ITERATIONS"])
		cipher = AES.new(key, AES.MODE_ECB)
		padded_plaintext = cipher.decrypt(ciphertext_sans_salt)
		plaintext = encryption().unpad_text(padded_plaintext)
		return plaintext

if __name__ == "__main__":
    encryption=encryption()
