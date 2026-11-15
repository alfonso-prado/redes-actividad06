from router import parse_packet, create_packet

ip = bytes([127, 0, 0, 1])
puerto = (8885).to_bytes(2, "big")
ttl = bytes([10])
identificacion = (347).to_bytes(2, "big")
offset = (0).to_bytes(2, "big")
tamano = (5).to_bytes(4, "big")
flag = bytes([0])
mensaje = b"hola!"

IP_packet_v1 = ip + puerto + ttl + identificacion
IP_packet_v1 += offset + tamano + flag + mensaje

parsed_IP_packet = parse_packet(IP_packet_v1)
IP_packet_v2 = create_packet(parsed_IP_packet)

print("IP_packet_v1 == IP_packet_v2 ?", IP_packet_v1 == IP_packet_v2)