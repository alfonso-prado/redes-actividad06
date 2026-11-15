from router import create_packet, fragment_IP_packet, parse_packet

mensaje = b"a" * 100
paquete = create_packet(("127.0.0.1", 8885, 10, 1, 0, len(mensaje), 0, mensaje))

sin_fragmentar = fragment_IP_packet(paquete, 140)
print("MTU 140:", len(sin_fragmentar), "paquete")
print("Se conserva el original:", sin_fragmentar == [paquete])

fragmentos = fragment_IP_packet(paquete, 50)
print("MTU 50:", len(fragmentos), "fragmentos")

for fragmento in fragmentos:
    _, _, _, _, offset, tamano, flag, _ = parse_packet(fragmento)
    print("Total:", len(fragmento), "Offset:", offset, "Datos:", tamano, "Flag:", flag)