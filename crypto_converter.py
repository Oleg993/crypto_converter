import requests

def get_better_price(*args):
    gas = 0.1 / 100
    all_prices = requests.get("https://api.binance.com/api/v3/ticker/price").json()
    pair = args[0][1] + args[0][-1]
    pair2 = args[0][-1] + args[0][1]
    for pairs in all_prices:
        if pairs['symbol'] == pair:
            return f'{args[0][0]} {args[0][1]} - {str((args[0][0] * (float(pairs["price"])) - (args[0][0] * (float(pairs["price"])) * gas)))} {args[0][-1]}'
        elif pairs['symbol'] == pair2:
            return f'{args[0][0]} {args[0][1]} - {str((args[0][0] / (float(pairs["price"])) - (args[0][0] * (float(pairs["price"])) * gas)))} {args[0][-1]}'


def get_price(*args):
    all_prices_k = requests.get("https://api.kucoin.com/api/v1/market/allTickers").json()
    all_prices_b = requests.get("https://api.binance.com/api/v3/ticker/price").json()
    gas = 0.1 / 100
    unic_args = []
    result = []
    quantity_k = [args[0][0]]
    quantity_b = [args[0][0]]
    for z in args[0][1:]:
        if z not in unic_args:
            unic_args.append(z)

    for i in range(0, len(unic_args) - 1):
        for elem_k in all_prices_k['data']['ticker']:
            if elem_k['symbolName'] == f"{unic_args[i]}-{unic_args[i + 1]}":
                quantity_k.append((quantity_k[-1] * (float(elem_k['buy']))) - (quantity_k[-1] * (float(elem_k['buy'])) * gas))
                result.append(f'{unic_args[i]} - {unic_args[i + 1]}(K) {str(quantity_k[-1])} {unic_args[i + 1]}')
                break
            elif elem_k['symbolName'] == f"{unic_args[i + 1]}-{unic_args[i]}":
                quantity_k.append((quantity_k[-1] / (float(elem_k['buy']))) - (quantity_k[-1] * (float(elem_k['buy'])) * gas))
                result.append(f'{unic_args[i]} - {unic_args[i + 1]}(K) {str(quantity_k[-1])} {unic_args[i + 1]}')
                break
        else:
            result.append(f'Пара {unic_args[i]} - {unic_args[i + 1]}(K) не найдена, конвертация невозможна.')

        for elem_b in all_prices_b:
            if elem_b['symbol'] == unic_args[i] + unic_args[i + 1]:
                quantity_b.append((quantity_b[-1] * (float(elem_b['price']))) - (quantity_b[-1] * (float(elem_b['price'])) * gas))
                result.append(f'{unic_args[i]} - {unic_args[i + 1]}(B) {str(quantity_b[-1])} {unic_args[i + 1]}')
                break
            elif elem_b['symbol'] == unic_args[i + 1] + unic_args[i]:
                quantity_b.append((quantity_b[-1] / (float(elem_b['price']))) - (quantity_b[-1] * (float(elem_b['price'])) * gas))
                result.append(f'{unic_args[i]} - {unic_args[i + 1]}(B) {str(quantity_b[-1])} {unic_args[i + 1]}')
                break
        else:
            result.append(f'Пара {unic_args[i]} - {unic_args[i + 1]}(B) не найдена, конвертация невозможна.')
            break

    if args[0][1].lower() == 'Kucoin'.lower():
        result_k = [k for k in result if '(K)' in k]
        return '\n'.join(result_k[1:])
    elif args[0][1].lower() == 'Binance'.lower():
        result_b = [b for b in result if '(B)' in b]
        return '\n'.join(result_b[1:])

    return '\n'.join(result)


x = [10, "ETH", "USDT"]
y = [10, 'Binance', "ETH", "XRP", "BTC", "USDT"]
z = [10, "ETH", "BNB", "BTC", "USDT"]
print(get_price(z))
print(get_better_price(x))


