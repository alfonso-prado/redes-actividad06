from router import create_packet, fragment_IP_packet, reassemble_IP_packet

mensaje = b"A" * 84 + b"B" * 50
IP_packet_v1 = create_packet(("127.0.0.1", 8882, 10, 2, 0, len(mensaje), 0, mensaje))
fragment_list = fragment_IP_packet(IP_packet_v1, 50)
IP_packet_v2 = reassemble_IP_packet(fragment_list)

print("IP_packet_v1 == IP_packet_v2 ?", IP_packet_v1 == IP_packet_v2)