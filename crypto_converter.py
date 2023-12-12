import requests

x = [10, "ETH", "USDT"]
y = [10, "ETH", "BNB", "BTC", "USDT"]
def get_better_price(*args):
    gas = 0.1 / 100
    all_prices = requests.get("https://api.binance.com/api/v3/ticker/price")
    pair = args[0][1] + args[0][-1]
    pair2 = args[0][-1] + args[0][1]

    for pairs in all_prices.json():
        if pairs['symbol'] == pair:
            return f'{args[0][0]} {args[0][1]} - {str((args[0][0] * (float(pairs["price"])) - (args[0][0] * (float(pairs["price"])) * gas)))} {args[0][-1]}'
        elif pairs['symbol'] == pair2:
            return f'{args[0][0]} {args[0][1]} - {str((args[0][0] / (float(pairs["price"])) - (args[0][0] * (float(pairs["price"])) * gas)))} {args[0][-1]}'

def get_price(*args):
    all_prices = requests.get("https://api.binance.com/api/v3/ticker/price")
    gas = 0.1 / 100
    quantity = args[0][0]
    unic_args = []
    result = {}
    result_str = ''
    for z in args[0][1:]:
        if z not in unic_args:
            unic_args.append(z)

    for i in range(0, len(unic_args) - 1):
        for elem in all_prices.json():
            if elem['symbol'] == unic_args[i] + unic_args[i+1]:
                quantity = quantity * (float(elem['price'])) - (quantity * (float(elem['price']) * gas))
            elif elem['symbol'] == unic_args[i+1] + unic_args[i]:
                quantity = quantity / (float(elem['price'])) - (quantity * (float(elem['price']) * gas))
            result[unic_args[i]] = f'{[unic_args[i]]}{str(quantity)} {unic_args[i + 1]}'
    for k, v in result.items():
        result_str += f'{k} - {v.split()[-1]} {v}\n'
    return result_str


print(get_price(y))
print(get_better_price(x))
