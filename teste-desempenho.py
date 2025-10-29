import requests
import time
import statistics

# CONFIGURA AQUI:
URL = "https://httpbin.org/get"  
TOTAL_REQS = 10                  # número de requisições para amostrar
TIMEOUT_SECONDS = 3              # máximo que espero cada resposta


latencias_ms = []
codigos_http = []

print(f"[INFO] Iniciando teste de desempenho em {URL} com {TOTAL_REQS} requisições...\n")

for i in range(TOTAL_REQS):
    print(f"[DEBUG] Requisição {i+1}/{TOTAL_REQS}...", flush=True)
    inicio = time.time()

    try:
        resp = requests.get(URL, timeout=TIMEOUT_SECONDS)
        fim = time.time()

        tempo_ms = (fim - inicio) * 1000
        latencias_ms.append(tempo_ms)
        codigos_http.append(resp.status_code)

        print(f"[DEBUG] -> HTTP {resp.status_code} em {tempo_ms:.2f} ms", flush=True)

    except requests.exceptions.RequestException as e:
        fim = time.time()
        tempo_ms = (fim - inicio) * 1000

        # marca como erro
        latencias_ms.append(None)
        codigos_http.append("ERR")

        print(f"[DEBUG] -> ERRO ({type(e).__name__}) após {tempo_ms:.2f} ms", flush=True)

print("\n[INFO] Coleta encerrada. Calculando métricas...\n")

# filtrar só as latências válidas (onde realmente teve resposta HTTP)
latencias_validas = [t for t in latencias_ms if t is not None]

if len(latencias_validas) == 0:
    print("Nenhuma resposta válida recebida. Não foi possível calcular média/P95.")
    print("STATUS: FALHOU (serviço não respondeu)")
else:
    # média
    media = statistics.mean(latencias_validas)

    # P95:
    # ordenar e pegar o índice 95%
    ordenadas = sorted(latencias_validas)
    idx_p95 = max(int(len(ordenadas) * 0.95) - 1, 0)
    p95 = ordenadas[idx_p95]

    # contagem de sucesso e erro
    sucesso_2xx = sum(1 for c in codigos_http if isinstance(c, int) and 200 <= c < 300)
    erros_rede = sum(1 for c in codigos_http if c == "ERR")
    outros_http = [
        c for c in codigos_http
        if isinstance(c, int) and not (200 <= c < 300)
    ]

    print("===== RESULTADO DO TESTE DE DESEMPENHO =====")
    print(f"Total de requisições tentadas: {TOTAL_REQS}")
    print(f"Com resposta 2xx: {sucesso_2xx}")
    print(f"Erros de rede/timeout: {erros_rede}")
    print(f"Outros códigos HTTP (não 2xx): {outros_http}")
    print(f"Latências válidas usadas no cálculo: {len(latencias_validas)}")
    print(f"Média de resposta: {media:.2f} ms")
    print(f"P95 de resposta: {p95:.2f} ms")

    if p95 < 500:
        print("STATUS: PASSOU (desempenho ok)")
    else:
        print("STATUS: FALHOU (desempenho abaixo do exigido)")
