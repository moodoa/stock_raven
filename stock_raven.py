import time
import requests
from datetime import datetime, timedelta


class STOCK_RAVEN:
    def _collect_stock(self):
        print("開始收集近 20 日股市資訊")
        day_searched = 0
        today = datetime.now()
        stocks = {}
        url = "http://www.twse.com.tw/exchangeReport/MI_INDEX"
        query_params = {
            "date": "",
            "response": "json",
            "type": "ALL",
        }
        while day_searched < 20:
            date = today.strftime("%Y%m%d")
            today = today + timedelta(days=-1)
            query_params["date"] = date
            try:
                page = requests.get(url, params=query_params)
            except:
                print(f"retry {date}")
            time.sleep(5)
            if page.json()["stat"] == "OK":
                day_searched += 1
                print(f"{date} added")
                if day_searched == 10:
                    time.sleep(10)
                for stock in page.json()["data9"]:
                    if stock[0] not in stocks:
                        try:
                            stocks[stock[0]] = {
                                "name": stock[1],
                                "price": [float(stock[8])],
                                "volume": [int(stock[2].replace(",", ""))],
                            }
                        except:
                            pass
                    else:
                        try:
                            stocks[stock[0]]["price"].append(float(stock[8]))
                            stocks[stock[0]]["volume"].append(
                                int(stock[2].replace(",", ""))
                            )
                        except:
                            del stocks[stock[0]]
        return stocks

    def qualified_stock(self):
        stocks = self._collect_stock()
        qualified = []
        for k, v in stocks.items():
            if len(v["price"]) == 20:
                if (
                    (sum(v["price"][:5]) / 5) < (sum(v["price"][:10]) / 10)
                    and v["price"][0] > (sum(v["price"][:20]) / 20)
                    and (sum(v["volume"][:5]) / 5) > 1000
                    and v["price"][0] > (sum(v["price"][:5]) / 5)
                    and v["volume"][0] > v["volume"][1]
                ):
                    qualified.append((k, v["name"]))
        print(f"符合條件股票 ({len(qualified)} 家):")
        for qualified_stock in qualified:
            print(qualified_stock)
        while True:
            print("輸入想查詢的股票代號或輸入 leave 離開: ")
            code = input()
            if code in stocks:
                print(stocks[code]["name"])
                print(f'收盤價 : {stocks[code]["price"][0]}\n')
                print(f'五日均價 : {round(sum(stocks[code]["price"][:5])/5,2)}\n')
                print(f'十日均價 : {round(sum(stocks[code]["price"][:10])/10,2)}\n')
                print(f'二十日均價 : {round(sum(stocks[code]["price"][:20])/20,2)}\n')
                print(f'五日均量 : {sum(stocks[code]["volume"][:5])/5}\n')
                print("近 20 日收盤價 :")
                for price in stocks[code]["price"]:
                    print(f"{price} 元")
                print("\n近 20 日成交量(股) :")
                for volume in stocks[code]["volume"]:
                    print(f"{volume} 股")
            elif code.lower() == "leave":
                break
            else:
                print(f"{code} 此股不符合條件")
        return "DONE"


class INS_RAVEN:
    def _get_major_institutions(self):
        near_five_days_info = {}
        day = 0
        while len(near_five_days_info) < 5:
            today = (datetime.now() + timedelta(days=-day)).strftime("%Y%m%d")
            day += 1
            institutions = requests.get(
                f"https://www.twse.com.tw/fund/BFI82U?response=json&dayDate={today}"
            ).json()
            time.sleep(3)
            if institutions["stat"] == "OK":
                print(f"{today} checked")
                near_five_days_info[today] = institutions["data"]
        return near_five_days_info

    def _add_market_total(self):
        data = self._get_major_institutions()
        market_info = {}
        for k, v in data.items():
            if k not in market_info:
                market = requests.get(
                    f"https://www.twse.com.tw/exchangeReport/FMTQIK?response=json&date={k}"
                ).json()
                time.sleep(5)
                for info in market["data"]:
                    date = info[0].split("/")
                    date = f"{int(date[0])+1911}{date[1]}{date[2]}"
                    market_info[date] = int(info[2].replace(",", ""))
                data[k].append({"market_total": market_info[k]})
            else:
                data[k].append({"market_total": market_info[k]})
        return data

    def _major_ins_rank(self):
        near_five_days_rank = {}
        day = 0
        while len(near_five_days_rank) < 5:
            today = (datetime.now() + timedelta(days=-day)).strftime("%Y%m%d")
            day += 1
            data = requests.get(
                f"https://www.twse.com.tw/fund/T86?response=json&date={today}&selectType=ALL"
            ).json()
            time.sleep(3)
            if data["stat"] == "OK":
                print(f"{today} checked")
                sort_volume = sorted(
                    data["data"], key=lambda x: float(x[-1].replace(",", ""))
                )
                near_five_days_rank[today] = {
                    "buy10": sort_volume[-10::][::-1],
                    "sell10": sort_volume[:10],
                }
        return near_five_days_rank

    def major_ins_output(self):
        data = self._add_market_total()
        for k, v in data.items():
            print(k)
            status = "賣超" if v[4][3].startswith("-") else "買超"
            print(f"{status} {v[4][3]}")
            buy = float(v[4][1].replace(",", ""))
            sell = float(v[4][2].replace(",", ""))
            total = v[-1]["market_total"]
            print(f"主力交易佔比 {round((buy + sell) / total / 2 * 100, 2)} %")
            print("\n")
        return "DONE"

    def major_rank_output(self):
        rank = self._major_ins_rank()
        for k, v in rank.items():
            print(f"\n\n{k}")
            print("買超 TOP 10:")
            for stock_info in v["buy10"]:
                print(f"{stock_info[0]} {stock_info[1].strip()} : {stock_info[-1]}")
            print("\n賣超 TOP 10:")
            for stock_info in v["sell10"]:
                print(f"{stock_info[0]} {stock_info[1].strip()} : {stock_info[-1]}")
        return "DONE"


if __name__ == "__main__":
    while True:
        print("想查詢 1: 型態過濾, 2: 籌碼過濾")
        system = input()
        if system == "1":
            raven = STOCK_RAVEN()
            print(raven.qualified_stock())
        elif system == "2":
            raven = INS_RAVEN()
            print("1: 查詢近五交易日買賣超資訊, 2:查詢近五交易日買賣超 TOP 10 ")
            choose = input()
            if choose == "1":
                print("開始查詢近五日買賣超資訊")
                raven.major_ins_output()
                print("請按任意鍵結束")
                input()
            elif choose == "2":
                print("開始查詢近五日買賣超 TOP 10")
                raven.major_rank_output()
                print("請按任意鍵結束")
                input()
            else:
                print("尚無此功能")
        else:
            print("尚無此功能")
