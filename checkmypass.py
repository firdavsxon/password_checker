import requests
import hashlib
import sys
from pathlib import Path


def request_api_data(query_char):
	url = 'https://api.pwnedpasswords.com/range/' + query_char
	res = requests.get(url)
	if res.status_code !=200:
		raise RuntimeError(f"Error fetching: {res.status_code}, check the API and try again.")
	return res

with open('paswords_for_check.txt', 'r') as file:
	r=file.read()


def get_password_leaks_count(hashes, hash_to_check):
	hashes = (line.split(':') for line in hashes.text.splitlines())
	for h, count in hashes:
		if h==hash_to_check:
			return count
	return 0


def pwned_api_ceck(password):
	sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	first5_char, tail = sha1password[:5], sha1password[5:]
	response = request_api_data(first5_char)
	return get_password_leaks_count(response, tail)


def main():
	args = input("Enter password to check: ")
	for password in args.split('\n'):
		count = pwned_api_ceck(password)
		if count:
			print(f"{password} was found {count} times..you should probably change password!")
		else:
			print(f"{password} was NOT found. Carry on!")
	return 'Done!'


if __name__ == '__main__':
	sys.exit((main()))


