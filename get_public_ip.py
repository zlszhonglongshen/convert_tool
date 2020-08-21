from requests import get
# Get external ip for host machine

def get_public_ip():
    return get('https://api.ipify.org').text

if __name__ == '__main__':
    print('Public IP: {}'.format(get_public_ip()))

