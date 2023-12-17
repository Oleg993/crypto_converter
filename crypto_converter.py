import requests

def get_price(*args):
    all_prices_k = requests.get("https://api.kucoin.com/api/v1/market/allTickers").json()
    all_prices_b = requests.get("https://api.binance.com/api/v3/ticker/price").json()
    gas = 0.1 / 100
    unic_args = [c for c in args[0][1:] if args[0][1:].count(c) == 1]
    result = []
    quantity_k = args[0][0]
    quantity_b = args[0][0]

    if args[0][1] == 'Kucoin' or args[0][1] == 'Binance':
        unic_args = unic_args[1:]

    for i in range(0, len(unic_args) - 1):
        for elem_k in all_prices_k['data']['ticker']:
            if elem_k['symbolName'] == f"{unic_args[i]}-{unic_args[i + 1]}":
                quantity_k = quantity_k * float(elem_k['buy']) * (1 - gas)
                result.append(f'{unic_args[i]} - {unic_args[i + 1]} {str(quantity_k)} {unic_args[i + 1]}(K)')
                break
            elif elem_k['symbolName'] == f"{unic_args[i + 1]}-{unic_args[i]}":
                quantity_k = quantity_k / float(elem_k['buy']) * (1 - gas)
                result.append(f'{unic_args[i]} - {unic_args[i + 1]} {str(quantity_k)} {unic_args[i + 1]}(K)')
                break
        else:
            result.append(f'Пара {unic_args[i]} - {unic_args[i + 1]} не найдена, конвертация невозможна.(K)')

        for elem_b in all_prices_b:
            if elem_b['symbol'] == unic_args[i] + unic_args[i + 1]:
                quantity_b = quantity_b * float(elem_b['price']) * (1 - gas)
                result.append(f'{unic_args[i]} - {unic_args[i + 1]} {str(quantity_b)} {unic_args[i + 1]}(B)')
                break
            elif elem_b['symbol'] == unic_args[i + 1] + unic_args[i]:
                quantity_b = quantity_b / float(elem_b['price']) * (1 - gas)
                result.append(f'{unic_args[i]} - {unic_args[i + 1]} {str(quantity_b)} {unic_args[i + 1]}(B)')
                break
        else:
            result.append(f'Пара {unic_args[i]} - {unic_args[i + 1]} не найдена, конвертация невозможна.(B)')

    result_k = []
    for pair in result:
        if pair[-3:] == "(K)":
            if pair[:4] == "Пара":
                result_k.append(pair)
                break
            result_k.append(pair)
    result_b = []
    for pair in result:
        if pair[-3:] == "(B)":
            if pair[:4] == "Пара":
                result_b.append(pair)
                break
            result_b.append(pair)

    if args[0][1].lower() == 'binance':
        return '\n'.join(result_b)
    elif args[0][1].lower() == 'kucoin':
        return '\n'.join(result_k)

    n_res = []
    for i in range(0, min(len(result_k), len(result_b)), 1):
        if result_k[i][:4] == 'Пара' and result_b[i][:4] == "Пара":
            n_res.append(result_k[i])
            n_res.append(result_b[i])
            break
        elif result_k[i][:4] == 'Пара' and result_b[i][:4] != "Пара":
            n_res.append(result_k[i])
            n_res.extend(result_b[i:])
            break
        elif result_k[i][:4] != 'Пара' and result_b[i][:4] == "Пара":
            n_res.append(result_b[i])
            n_res.extend(result_k[i:])
            break
        else:
            if float(result_k[i].split()[3]) > float(result_b[i].split()[3]):
                n_res.append(result_k[i])
            else:
                n_res.append(result_b[i])
    return '\n'.join(n_res)

v = [10, 'Binance', "ETH", "XRP", "USDT", "BTC"]
z = [10, "ETH", "BTC", "XRP", "USDT"]
print(get_price(z))
# print(get_price(v))



