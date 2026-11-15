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

    identificacion = int(sys.argv[7])

    if not 1 <= ttl <= 255:
        sys.exit("El TTL inicial debe estar entre 1 y 255.")

    if not 0 <= identificacion <= 65535:
        sys.exit("El ID debe estar entre 0 y 65535.")

    # paquete sale completo sin fragmentar
    if len(sys.argv) == 8:
        offset = 0
        flag = 0
    elif len(sys.argv) == 10:
        offset = int(sys.argv[8])
        flag = int(sys.argv[9])
    else:
        sys.exit("Indica el offset y el flag juntos, o deja ambos fuera.")

    tamano = len(mensaje_bytes)

    paquete = create_packet((ip_destino, puerto_destino, ttl, identificacion, offset, tamano, flag, mensaje_bytes))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(paquete, (ip_envio, puerto_envio))
    sock.close()