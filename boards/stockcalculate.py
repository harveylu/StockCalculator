import urllib2
import ssl
import json
from urllib2 import HTTPError, URLError
from socket import timeout
import random

# Example use:
#    result = investment_with_strategy(5000, False, False, False, True, False)
# Print Result:
#    print(json.dumps(result, indent=2, sort_keys=False))

stock_profiles = {
    "Ethical":  ["INTU",
                 "AAPL",
                 "ADBE",
                 "GOOG",
                 "BEP",
                 "TSLA"],
    "Growth":   ["NHTC",
                 "PAYC",
                 "TREE",
                 "ABMD",
                 "NTES",
                 "AMD"],
    "Index":    ["VOO",
                 "SCHA",
                 "VEU",
                 "SCHE",
                 "SCHZ",
                 "BLV"],
    "Quality":  ["AAL",
                 "AXP",
                 "IBM",
                 "DAL",
                 "BAC",
                 "STOR"],
    "Value":    ["AFL",
                 "SKX",
                 "VZ",
                 "BRFS",
                 "CTRP",
                 "PSA"],
}


def investment_with_strategy(amount, ethical, growth, index, quality, value):
    if amount < 5000:
        return {"error": "Minimum investment is $5000 USD"}

    strategy = []
    if ethical:
        strategy.append("Ethical")
    if growth:
        strategy.append("Growth")
    if index:
        strategy.append("Index")
    if quality:
        strategy.append("Quality")
    if value:
        strategy.append("Value")

    recommended_stocks = get_recommend_stock(strategy)
    if recommended_stocks.get("error") is not None:
        return recommended_stocks

    recommended_stock = recommended_stocks.get("value")

    quote = get_stock_quote(recommended_stock)
    if quote.get("error") is not None:
        return quote

    return calculate_investment(amount, strategy, quote)


def get_recommend_stock(strategy):
    # type: (list) -> dict
    if len(strategy) != 1 and len(strategy) != 2:
        return {"error": "Please select 1 or 2 investment strategy"}

    selections = []
    if len(strategy) == 1:
        selections = select_random_stocks(stock_profiles.get(strategy[0]), 4)
    elif len(strategy) == 2:
        selections = select_random_stocks(stock_profiles.get(strategy[0]), 2)
        selections.extend(select_random_stocks(stock_profiles.get(strategy[1]), 2))

    return {"value": selections}


def select_random_stocks(stocks, count):
    result = []
    for index in random.sample(xrange(0, len(stocks)), count):
        result.append(stocks[index])

    return result


def get_stock_quote(symbols):
    if len(symbols) == 0:
        return {"error": "No symbol selected"}

    symbol_url_string = ""
    for symbol in symbols:
        symbol_url_string += "{},".format(symbol)

    context = ssl._create_unverified_context()
    url = "https://api.iextrading.com/1.0/stock/market/batch?symbols={}&types=quote,chart&range=1m".format(
        symbol_url_string)
    try:
        resource = urllib2.urlopen(url, context=context)
        responseText = resource.read().decode(resource.headers.getparam("charset"))
        result = json.loads(responseText)
    except HTTPError as e:
        return {"error": e.read().decode(e.headers.getparam("charset"))}
    except URLError as e:
        return {"error": "You might be offline, please check your network connection and retry"}
    except timeout:
        return {"error": "Request timeout, please retry or check your network connection"}
    except:
        return {"error": "Unknown error, please retry"}

    if len(result) <= 0:
        return {"error": "No result was returned, please retry"}

    return result


def calculate_investment(amount, strategy, quote):
    result = {"investmentStrategies": strategy,
              "totalInvestment": amount}
    remainingBalance = amount

    quote = map(lambda_format_quote, quote.values())
    quote.sort(key=lambda x: x.get("latestPrice"), reverse=True)
    suggestedStocks = []

    for index, stock in enumerate(quote):
        price = stock.get("latestPrice")
        share = (remainingBalance / (len(quote) - index)) // price
        buyAmount = share * price
        remainingBalance -= buyAmount
        stock["investment"] = {"share": share,
                               "amount": buyAmount}
        suggestedStocks.append(stock)

    result["suggestedStocks"] = suggestedStocks
    result["actualInvestment"] = amount - remainingBalance
    result["remainingBalance"] = remainingBalance

    return result


def lambda_format_quote(value):
    result = value.get("quote")
    history = value.get("chart")
    if history is not None:
        result["history"] = history[-5:]

    return result

