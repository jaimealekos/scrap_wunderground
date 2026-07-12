# scrap_wunderground

A small Python scraper that extracts precipitation data (**Time**, **Precip. Rate** and **Precip. Accum.**) from the daily observations table of a [Weather Underground](https://www.wunderground.com/) personal weather station (PWS).

## Requirements

- Python 3.8+
- [requests](https://pypi.org/project/requests/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

## Installation

```bash
git clone https://github.com/jaimealekos/scrap_wunderground.git
cd scrap_wunderground
pip install -r requirements.txt
```

## Usage

The URL must be the *daily table* view of a station's dashboard:

```
https://www.wunderground.com/dashboard/pws/<STATION_ID>/table/<DATE>/<DATE>/daily
```

### As a library

```python
from scrap_wunderground import scrap_wunderground

rows = scrap_wunderground(
    "https://www.wunderground.com/dashboard/pws/ICHIVA39/table/2024-10-29/2024-10-29/daily"
)

for time, precip_rate, precip_accum in rows:
    print(time, precip_rate, precip_accum)
```

### From the command line

```bash
python scrap_wunderground.py "https://www.wunderground.com/dashboard/pws/ICHIVA39/table/2024-10-29/2024-10-29/daily"
```

Output (tab-separated):

```
Time    Precip. Rate    Precip. Accum.
12:04 AM        0.00 in 0.00 in
12:09 AM        0.00 in 0.00 in
...
```

## Notes

- The scraper parses the public dashboard HTML. If Weather Underground changes its markup, it may need updating.
- Be considerate with request rates. The data belongs to Weather Underground and the station owners.

## License

[MIT](LICENSE)
