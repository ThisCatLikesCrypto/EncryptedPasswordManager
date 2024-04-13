import random
import hashlib


def generate(sha256output=0, length=7):
  password = ""
  list = ['0' ,'1' ,'2' ,'3' ,'4' ,'5' ,'6' ,'7' ,'8' ,'9' ,'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
  for i in range(length):
    password = password + list[random.randint(1, 36)-1]
  if sha256output == 1:
    sha256 = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return sha256
  elif sha256output == 2:
    sha256 = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return [password, sha256]
  else:
    return password


def check(input_, correcthash):
  sha256 = hashlib.sha256(input_.encode('utf-8')).hexdigest()
  if correcthash == sha256:
    return True
  else:
     return False


def newpass(input_):
  return hashlib.sha256(input_.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    e = input("SHA256 (True) or password (False) returned?:\n")
    b = int(input("Length?:\n"))
    pword = generate(e, b)
    print(pword)
