# Instructions

### To execute the program

```bash

git clone <THIS REPO>

cd market_pos

docker build --tag market .

docker run --rm -i market
```

### To inspect the container

```bash
docker run --rm -it market /bin/bash
```

### To build local

```console
python3 -m venv .venv3
source .venv3/bin/activate
pip install -r requirements.lock.txt
```

### To run local

```console
python src/PointOfSale.py
```

### To test local

```console
python -m pytest --cov=src --cov-report=html --cov-report=term
```
-----
## Data

Prices are located in: ./src/prices.json

```json
{
     "CH1": { "name": "Chai", "price": "3.11"},
     "AP1": { "name": "Apples", "price": "6.00"},
     "CF1": { "name": "Coffee", "price": "11.23"},
     "MK1": { "name": "Milk", "price": "4.75"},
     "OM1": { "name": "Oatmeal", "price": "3.69"}
}
```

Deals are located in: ./src/deals.json
```json
{
    "BOGO-Coffee": "MultiBuyOffer('BOGO-Coffee', 'CF1', 1, 1)",
    "APPL3": "ThresholdOffer('APPL3', 'AP1', 3, '0.25')",
    "APOM": "DependentDiscountOffer('APOM', 'AP1', 'OM1', Decimal(0.5))",
    "CHMK": "DependentDiscountOffer('CHMK', 'MK1', 'CH1', 1.0, limit=1)"
}
```
