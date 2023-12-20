import requests
import itertools

def get_price(*args):
    all_prices_k = requests.get("https://api.kucoin.com/api/v1/market/allTickers").json()
    all_prices_b = requests.get("https://api.binance.com/api/v3/ticker/price").json()
    gas = 1 - (0.1 / 100)
    unic_args = [c for c in args[0] if args[0].count(c) == 1]
    all_combinations = []
    result = []
    quantity_b = 1
    quantity_k = 1

    if args[0][0].lower() == 'kucoin' or args[0][0].lower() == 'binance':
        unic_args = unic_args[1:]

    for j in range(1, len(unic_args) + 1):
        for u in itertools.permutations(unic_args, j):
            if list(u)[0] == unic_args[0] and list(u)[-1] == unic_args[-1]:
                all_combinations.append(list(u))

    for comb in all_combinations:
        m_res = []
        for i in range(0, len(comb) - 1):
            m_res_b = []
            m_res_k = []
            for elem_b in all_prices_b:
                if elem_b['symbol'] == f"{comb[i]}{comb[i + 1]}":
                    quantity_b = quantity_b * float(elem_b['price']) * gas
                    m_res_b.append(f'{comb[i]} - {comb[i + 1]} {str(quantity_b)} {comb[i + 1]}(B)')
                    break
            else:
                m_res.append(f'Пара {comb[i]} - {comb[i + 1]} не найдена, конвертация невозможна.(B)')

            for elem_k in all_prices_k['data']['ticker']:
                if elem_k['symbolName'] == f"{comb[i]}-{comb[i + 1]}":
                    quantity_k = quantity_k * float(elem_k['buy']) * gas
                    m_res_k.append(f'{comb[i]} - {comb[i + 1]} {str(quantity_k)} {comb[i + 1]}(K)')
                    break
            else:
                m_res.append(f'Пара {comb[i]} - {comb[i + 1]} не найдена, конвертация невозможна.(K)')
                break
            if args[0][0].lower() == 'kucoin':
                m_res.append(m_res_k[-1])
            elif args[0][0].lower() == 'binance':
                m_res.append(m_res_b[-1])
            else:
                if float(m_res_b[-1].split()[3]) > float(m_res_k[-1].split()[3]):
                    m_res.append(m_res_b[-1])
                else:
                    m_res.append(m_res_k[-1])
        quantity_b = 1
        quantity_k = 1

        found_pair = False
        for r in m_res:
            if r[:4] == 'Пара':
                found_pair = True
                break
        if not found_pair:
            result.append(m_res)

    max_price = 0
    max_price_list = None
    for lst in result:
        price = float(lst[-1].split()[3])
        if price > max_price:
            max_price = price
            max_price_list = lst

    for p in max_price_list:
        print(p)

v = ["Kucoin", "ETH", "BTC", "BNB", "USDT"]
z = ["LTC", "ETH", "BTC", "BNB", "USDT"]

get_price(z)

