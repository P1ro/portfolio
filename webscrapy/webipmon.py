import requests
import socket
from bs4 import BeautifulSoup
import logging as logger

# Configure logging
logger.basicConfig(level=logger.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_local_ip():
    """
    Retrieves the local IP address of the machine.
    Returns:
        str: The local IP address.
    """
    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        temp_socket.connect(('8.8.8.8', 80))
        local_ip = temp_socket.getsockname()[0]
    except socket.error:
        local_ip = 'Unknown'
    finally:
        temp_socket.close()
        logger.info(f'Local IP: {local_ip}')
    return local_ip

def get_my_ext_ip(website_url):
    """
    Retrieves the external IP address from a given website URL.
    Args:
        website_url (str): The URL of the website to fetch the IP address from.
    Returns:
        str: The external IP address.
    """
    url = website_url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    my_ext_ip = soup.get_text().strip()
    logger_ipinfoio.info(f'IP from ipinfo.io: {my_ext_ip}')
    return my_ext_ip

def get_ext_ip_iproyalcom(website_url):
    """
    Retrieves the external IP address from iproyal.com/ip-lookup website.
    Args:
        website_url (str): The URL of the website to fetch the IP address from.
    Returns:
        str: The external IP address.
    """
    url = website_url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    ip_element = soup.find('div', string='IP:').find_next_sibling('div')
    my_ext_ip = ip_element.get_text().strip()
    logger_iproyalcom.info(f'IP from iproyal.com/ip-lookup: {my_ext_ip}')
    return my_ext_ip

def compare_ip(local_ip, website_url, website_ip):
    """
    Compares the local IP with the IP obtained from a website.
    Args:
        local_ip (str): The local IP address.
        website_url (str): The URL of the website.
        website_ip (str): The IP address obtained from the website.
    """
    if local_ip == website_ip:
        logger.info(f"Local IP ({local_ip}) matches the IP: {website_ip} from: {website_url}")
    else:
        logger.info(f"Local IP ({local_ip}) does not match the IP: {website_ip} from: {website_url}")

def main():
    """
    Retrieves the local IP address and compares it with external IP addresses from different websites.
    """
    # Get the local IP address
    local_ip = get_local_ip()
    
    # IP services with clean return of the IP Address.
    websites_direct_ip = [
        'https://ipinfo.io/ip',
        'https://ipx.ac/ip'        
    ]
    for website_url in websites_direct_ip:
        website_ip = get_my_ext_ip(website_url)
        compare_ip(local_ip, website_url, website_ip)

    # IP services without a clean return of the IP Address need their own method
    website_url = 'https://iproyal.com/ip-lookup'
    website_ip = get_ext_ip_iproyalcom(website_url)
    compare_ip(local_ip, website_url, website_ip)

if __name__ == '__main__':
    # Create separate file handlers for each website
    file_handler_ipinfoio = logger.FileHandler('ipinfoio.log')
    file_handler_ipxac = logger.FileHandler('ipxac.log')
    file_handler_iproyalcom = logger.FileHandler('iproyalcom.log')
    
    # Configure loggers with file handlers
    logger_ipinfoio = logger.getLogger('ipinfoio')
    logger_ipinfoio.setLevel(logger.INFO)
    logger_ipinfoio.addHandler(file_handler_ipinfoio)
    
    logger_ipxac = logger.getLogger('ipxac')
    logger_ipxac.setLevel(logger.INFO)
    logger_ipxac.addHandler(file_handler_ipxac)
    
    logger_iproyalcom = logger.getLogger('iproyalcom')
    logger_iproyalcom.setLevel(logger.INFO)
    logger_iproyalcom.addHandler(file_handler_iproyalcom)
    
    main()