import collections
from datetime import datetime, timedelta
from locale import currency
from pycoingecko import CoinGeckoAPI
from django.utils import timezone
from django.apps import apps
from django.db.models import Max, Min

from cryptosignals.utils import send_email
from cryptosignals.constants import COINS, ALTCOINS, COINS_SYMBOLS, INTERVALS_TO_CHECK_CHANGES_WITH_THRESHOLD

Price = apps.get_model('price', 'Price')
Alarm = apps.get_model('price', 'Alarm')
Job = apps.get_model('price', 'Job')


def new_batch():
    all_coins = COINS + ALTCOINS
    coins = ",".join(all_coins)
    cg = CoinGeckoAPI()
    coins_data = cg.get_price(vs_currencies='usd', ids=coins)
    for coin in all_coins:
        coin_data = coins_data.get(coin)
        if coin_data:
            Price.create_new(COINS_SYMBOLS[coin], coin_data['usd'])
            if COINS_SYMBOLS[coin] in ["BTC", "ETH"]:
                set_alarms(COINS_SYMBOLS[coin], coin_data['usd'])


def set_alarms(coin, current_price):
    body = ""
    for i, t in INTERVALS_TO_CHECK_CHANGES_WITH_THRESHOLD:
        prices_to_check = Price.objects.filter(coin=coin, created_at__gt=timezone.now()-timedelta(minutes=i)).aggregate(Min('price'), Max('price'))
        max, min = prices_to_check.get('price__max'), prices_to_check.get('price__min')
        if min and current_price > min * (1 + (0.01 * t)) and not Alarm.is_active(coin):
            body = write_body(body, i, coin, current_price, min)
        elif max and current_price < max * (1 - (0.01 * t))  and not Alarm.is_active(coin):
            body = write_body(body, i, coin, current_price, max)

    if body:
        send_email(f"{coin} alert", body)
        Alarm.create_new(coin=coin)
        

def write_body(body, interval, coin, current_price, threshold):
    body += f"<h3>Changes in last {interval} minutes: "
    body += f"New {'high' if current_price > threshold else 'low'} price {current_price}</h3>"
    minutes_ago = int((timezone.now() - Price.objects.filter(price=threshold, coin=coin)[0].created_at).seconds / 60)
    body += f"<p>it has {'increased' if current_price > threshold else 'decreased'} {round((current_price - threshold) / threshold * 100, 2)}% from {threshold} since {minutes_ago} minutes ago</p>"

    references = {}
    for alt in COINS_SYMBOLS.values():
        try:
            current_price = Price.objects.filter(coin=alt).last().price
            time_of_threshold = Price.objects.filter(coin=coin, price=threshold).last().created_at
            reference_price = Price.objects.filter(
                coin=alt,
                created_at__gt=(time_of_threshold-timedelta(seconds=20)),
                created_at__lt=(time_of_threshold+timedelta(seconds=20))
                ).last().price
            difference =  (current_price - reference_price) / reference_price * 100
            color = "green" if difference > 0 else "red"
            message = f"<p style='color:{color}'>{alt} price has changed {round(difference, 2)}% since then at {time_of_threshold.strftime('%H:%M:%S')} </p>"
            references[difference] = message
        except AttributeError:
            continue
        except Exception:
            raise

    order_coins = collections.OrderedDict(sorted(references.items()))
    for od in order_coins:
        body += order_coins[od]
    body += "<br>"
    return body



    

