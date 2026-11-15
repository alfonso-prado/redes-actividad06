import sys
import socket
from router import create_packet

if __name__ == "__main__":
    ip_destino = sys.argv[1]
    puerto_destino = int(sys.argv[2])

    mensaje = sys.argv[3]
    mensaje_bytes = mensaje.encode()

    ip_envio = sys.argv[4]
    puerto_envio = int(sys.argv[5])

    ttl = int(sys.argv[6])

    if not 1 <= ttl <= 255:
        sys.exit("El TTL inicial debe estar entre 1 y 255.")

    paquete = create_packet((ip_destino, puerto_destino, ttl, mensaje_bytes))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(paquete, (ip_envio, puerto_envio))
    sock.close()