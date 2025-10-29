def eficiencia_horizontal(throughput_base, throughput_n, n_servidores):
    # throughput_base: req/s com 1 servidor
    # throughput_n: req/s medido com n servidores
    ideal = throughput_base * n_servidores
    eficiencia = (throughput_n / ideal) * 100
    return eficiencia

throughput_1srv = 200   # medido
throughput_4srv = 720   # medido com load balancer em 4 instâncias

ef = eficiencia_horizontal(throughput_1srv, throughput_4srv, 4)

print(f"Eficiência horizontal: {ef:.2f}%")

if ef >= 80:
    print("STATUS: PASSOU (escala bem)")
else:
    print("STATUS: FALHOU (perde eficiência ao escalar)")
