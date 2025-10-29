import requests
import time

# CONFIGURA AQUI:
URL = "https://httpbin.org/anything"  # endpoint que aceita POST tranquilo
HEADERS = {"X-Test-IP": "1.2.3.4"}    # se quiser simular IP
TOTAL_REQS = 20                       # quantidade de requisições (pode subir depois)
SLEEP_SECONDS = 0.1                   # pausa entre as tentativas
TIMEOUT_SECONDS = 2                   # máximo que eu espero resposta de cada POST


status_codes = []
inicio = time.time()

for i in range(TOTAL_REQS):
    print(f"[DEBUG] Enviando req {i+1}/{TOTAL_REQS}...", flush=True)

    try:
        resp = requests.post(
            URL,
            json={"user": "teste", "pass": "senha"},
            headers=HEADERS,
            timeout=TIMEOUT_SECONDS
        )
        status_codes.append(resp.status_code)
        print(f"[DEBUG] Resposta {i+1}: HTTP {resp.status_code}", flush=True)
    except requests.exceptions.RequestException as e:
        # qualquer erro de timeout/conexão/etc cai aqui
        status_codes.append("ERR")
        print(f"[DEBUG] ERRO na req {i+1}: {e}", flush=True)

    time.sleep(SLEEP_SECONDS)

fim = time.time()
duracao_seg = fim - inicio
req_por_min = len(status_codes) / (duracao_seg / 60)

# métricas finais
bloqueios = sum(1 for c in status_codes if c == 429)
erros = sum(1 for c in status_codes if c == "ERR")
ok = sum(1 for c in status_codes if isinstance(c, int) and 200 <= c < 300)

print("\n===== RESULTADO DO TESTE DE SEGURANÇA (RATE LIMIT) =====")
print(f"Total de requisições enviadas: {len(status_codes)}")
print(f"Sucesso (2xx): {ok}")
print(f"Erros de rede/timeout: {erros}")
print(f"HTTP 429 recebidos: {bloqueios}")
print(f"Taxa disparada: {req_por_min:.1f} req/min")

if bloqueios > 0 and req_por_min >= 100:
    print("STATUS: PASSOU (rate limiting ativo)")
else:
    print("STATUS: FALHOU (sem proteção adequada)")
