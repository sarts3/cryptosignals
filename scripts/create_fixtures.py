import json
from cryptosignals.constants import ALTCOINS, COINS

initial_coins = []

fixtures_coins = COINS
fixtures_coins.extend(ALTCOINS)
for i, coin in enumerate(fixtures_coins):
    coin_dict = {
        "model":"price.job",
        "pk": i+1,
        "fields": {
            "coin": coin,
            "created_at": "2022-01-01T00:00:00.000Z",
            "expired_at": "2099-01-01T00:00:00.000Z" if coin in COINS else "2022-01-01T00:00:00.000Z"
        }

    }
    initial_coins.append(coin_dict)

with open('fixtures/initial_data.json', 'w') as f:
    json.dump(initial_coins, f)




