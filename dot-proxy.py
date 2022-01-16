import socket
import ssl
import logging
from multiprocessing import Process

logging.basicConfig(filename='/var/log/dot-proxy.log', level=logging.DEBUG)

class TCPProxy:

  def __init__(self):
    self.LISTENING_IP = '0.0.0.0'
    self.LISTENING_PORT = 53
    self.DNS_PROVIDER_IP = '1.1.1.1'
    self.DNS_PROVIDER_PORT = 853
    self.TCP_BUFFER_SIZE = 1024

  def dns_query(self, query):
    """Encrypt the connection and send the DNS query to the DNS provider
    
    Parameters:
      query (bytes):         DNS query
    
    Return:
      dns_results (bytes):   DNS query results
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('/etc/ssl/certs/ca-certificates.crt')

    encrypt_socket = context.wrap_socket(sock, server_hostname=self.DNS_PROVIDER_IP)
    encrypt_socket.connect((self.DNS_PROVIDER_IP, self.DNS_PROVIDER_PORT))
    encrypt_socket.send(query)

    dns_results = encrypt_socket.recv(self.TCP_BUFFER_SIZE)
    return dns_results

  def tcp_handler(self, conn, data):
    """TO-DO
    
    Parameters:
      conn (socket.socket): TCP connection
      data (bytes):         DNS query
    """
    logging.info('Incoming TCP connection from: ', conn.getpeername())
    response = self.dns_query(data)
    if response:
      conn.sendto(response, conn.getpeername())
      logging.info('DNS results sent back to {}'.format(conn.getpeername()))
    else:
      logging.error('DNS query is not valid: \n', data)

  def main(self):
    """Create the TCP server"""

    try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((self.LISTENING_IP, self.LISTENING_PORT))
        s.listen()
        logging.info('TCP server is listening on port', self.LISTENING_PORT)
        while True:
          conn= s.accept()[0]
          data = conn.recv(self.TCP_BUFFER_SIZE)

          if not data:
            break
          p = Process(target=self.tcp_handler, args=(conn, data))
          p.start()
    except Exception as e:
      logging.error(e)
      conn.close()


if __name__ == '__main__':
  lookup = TCPProxy()
  lookup.main()