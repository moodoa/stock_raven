# stock_raven
stock_raven 是一個在 CMD 操作的股票篩選程式，透過此程式可以篩選出:
1. 符合型態過濾 ( 5 日均價 < 10 日均價 and 日收盤價 > 20 日均價 and 日收盤價 > 5 日均價 and 5 日均量 > 1000 and 日成交量 > 1 日前的日成交量)。
2. 主力買超 and 主力成交量 > 30%。
3. 該股籌碼集中度 >= 60%。
4. 在 top 50 主力買超名單內，並連續買超兩天。

![alt text](https://i.pinimg.com/474x/c2/ea/74/c2ea74d12d54e4a783f3ef4151d70418.jpg)

## STOCK_RAVEN
* _collect_stock : 蒐集近 20 開盤日股市資訊。 
* qualified_stock : 型態過濾篩選。

## INS_RAVEN
* _get_major_institutions : 蒐集近 5 開盤日主力(三大法人)資訊。 
* major_ins_output : 查詢近五日買賣超資訊。
* major_rank_output : 查詢近五日買賣超 TOP 10。

## EXCEL_RAVEN
* _get_top50_stock : 蒐集 TOP50 買超股票。
* excel_maker : 製作含有四種篩選的 excel 檔案。

## Requirements
python 3

## Usage
```
python .\stock_raven.py

之後照著 CMD 顯示的指示操作，每天第一次操作會需要約 8 分鐘蒐集資料。
```
## Installation
`pip install -r requriements.txt`。
