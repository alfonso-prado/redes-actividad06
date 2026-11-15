
import sys
import socket
import ipaddress

def parse_packet(IP_packet: bytes):
    ip_partes = []

    # header: 4 bytes de ip, 2 de puerto y 1 de ttl
    for byte in IP_packet[:4]:
        ip_partes.append(str(byte))

    ip = ".".join(ip_partes)
    puerto = int.from_bytes(IP_packet[4:6], "big")
    ttl = IP_packet[6]
    mensaje = IP_packet[7:]

    return ip, puerto, ttl, mensaje

def create_packet(parsed_IP_packet):
    ip, puerto, ttl, mensaje = parsed_IP_packet
    ip_bytes = b""

    for numero in ip.split("."):
        ip_bytes += int(numero).to_bytes(1, "big")

    puerto_bytes = puerto.to_bytes(2, "big")
    ttl_bytes = ttl.to_bytes(1, "big")

    return ip_bytes + puerto_bytes + ttl_bytes + mensaje

# diccionario de indice de la proxima ruta que toca usar en cada grupo
turnos = {}

def check_routes(routes_file_name: str, destination_address: tuple[str, int]) -> tuple[str, int] | None:
    ip_destino, puerto_destino = destination_address
    ip_destino = ipaddress.ip_address(ip_destino)

    rutas_posibles = []
    grupo = None

    with open(routes_file_name, "r") as archivo:
        for linea in archivo:
            partes = linea.split()

            if not partes or partes[0].startswith("#"):
                continue

            red, puerto_inicial, puerto_final, ip_salto, puerto_salto = partes

            # obtiene la red a partir de la ip de un host y su prefijo
            red = ipaddress.ip_network(red, strict=False)
            puerto_inicial = int(puerto_inicial)
            puerto_final = int(puerto_final)

            if ip_destino in red and puerto_inicial <= puerto_destino <= puerto_final:
                clave = (routes_file_name, str(red), puerto_inicial, puerto_final)

                # determina el grupo que se va a usar.
                if grupo is None:
                    grupo = clave

                # guarda todas las rutas posibles del primer grupo que coincide
                if grupo == clave:
                    rutas_posibles.append((ip_salto, int(puerto_salto)))

    if not rutas_posibles:
        return None

    # utiliza el dicccionario turnos para elegir la que corresponde
    indice = turnos.get(grupo, 0) % len(rutas_posibles)
    siguiente_salto = rutas_posibles[indice]

    #despues de la ultima ruta, el turno vuelve a la primera
    turnos[grupo] = (indice + 1) % len(rutas_posibles)

    return siguiente_salto

if __name__ == "__main__":
    router_ip = sys.argv[1]
    router_puerto = int(sys.argv[2])
    router_rutas = sys.argv[3]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((router_ip, router_puerto))

    print(f"ROUTER: {router_ip}:{router_puerto}\n")

    while True:
        data, addr = sock.recvfrom(65535)

        if len(data) < 7:
            continue

        ip, puerto, ttl, mensaje = parse_packet(data)
        mensaje_texto = mensaje.decode(errors="replace")
        paquete_ip = f"{ip};{puerto};{ttl};{mensaje_texto}"

        if ttl == 0:
            print(f"Se recibió paquete {paquete_ip} con TTL 0")
            continue

        destination_address = (ip, puerto)

        # comprueba si el paquete esta dirigido al router actual
        if destination_address == (router_ip, router_puerto):
            print(mensaje.decode())
        # si el destino es otro router va consultar la tabla
        else:
            next_hop = check_routes(router_rutas, destination_address)

            if next_hop is not None:
                ttl_salida = ttl - 1
                paquete_reenviado = create_packet((ip, puerto, ttl_salida, mensaje))
                paquete_ip = f"{ip};{puerto};{ttl_salida};{mensaje_texto}"
                print(f"redirigiendo paquete {paquete_ip} con destino final {destination_address} desde {(router_ip, router_puerto)} hacia {next_hop}")
                sock.sendto(paquete_reenviado, next_hop)
            else:
                print(f"No hay rutas hacia {destination_address} para paquete {paquete_ip}")
