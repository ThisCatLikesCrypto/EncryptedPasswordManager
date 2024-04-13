import base64
from Cryptodome.Cipher import AES
import hashlib

def encrypt(data, key):
  key = bytes(key, 'utf-8')
  data = bytes(data, 'utf-8')
  md5_password = hashlib.md5(key).hexdigest()
  md5_password = bytes(md5_password, 'utf-8')
  cipher = cipherf(md5_password)
  block_size = AES.block_size
  padding_length = block_size - len(data) % block_size
  padded_data = data + bytes([padding_length]) * padding_length
  raw_ciphertext = cipher.encrypt(padded_data)
  return base64.b64encode(raw_ciphertext).decode('utf-8')
  

def decrypt(data, key):
  key = bytes(key, 'utf-8')
  md5_password = hashlib.md5(key).hexdigest()
  md5_password = bytes(md5_password, 'utf-8')
  common_cipher = cipherf(md5_password)
  raw_ciphertext = base64.b64decode(data)
  decrypted_message_with_padding = common_cipher.decrypt(raw_ciphertext)
  return decrypted_message_with_padding.decode('utf-8').strip()

def cipherf(md5_password):
  #This function is only intended to be used within the library
  IV = b'IVIVIVIVIVIVIVIV'
  cipher = AES.new(md5_password, AES.MODE_CBC, IV)
  return cipher