#!/usr/bin/env python3
"""Scrape precipitation data from a Weather Underground weather station.

Extracts the 'Time', 'Precip. Rate' and 'Precip. Accum.' columns from the
daily observations table of a wunderground.com personal weather station
(PWS) dashboard URL.

Usage as a library:

    from scrap_wunderground import scrap_wunderground

    rows = scrap_wunderground(
        "https://www.wunderground.com/dashboard/pws/ICHIVA39/table/2024-10-29/2024-10-29/daily"
    )

Usage from the command line:

    python scrap_wunderground.py <station_table_url>
"""

import sys

import requests
from bs4 import BeautifulSoup

__version__ = "1.0.1"

# Columns extracted from the daily observations table.
TARGET_COLUMNS = ("Time", "Precip. Rate", "Precip. Accum.")

# Timeout for the HTTP request, in seconds.
REQUEST_TIMEOUT = 30

# Browser-like User-Agent, in case Weather Underground rejects the default one.
REQUEST_HEADERS = {
    "User-Agent": f"Mozilla/5.0 (compatible; scrap_wunderground/{__version__})"
}


def _normalize(header):
    """Normalize a column header for comparison ('Precip. Rate.' == 'Precip. Rate')."""
    return header.strip().rstrip(".").lower()


def scrap_wunderground(url, timeout=REQUEST_TIMEOUT):
    """Return the precipitation rows from a station's daily observations table.

    Args:
        url: URL of a wunderground.com PWS daily table, e.g.
            "https://www.wunderground.com/dashboard/pws/<STATION>/table/<DATE>/<DATE>/daily".
        timeout: Timeout for the HTTP request, in seconds.

    Returns:
        A list of ``[time, precip_rate, precip_accum]`` rows (lists of
        strings), one per observation.

    Raises:
        requests.RequestException: If the request fails or the server
            responds with an error status.
        ValueError: If the daily observations table cannot be found or is
            missing any of the expected columns.
    """
    response = requests.get(url, headers=REQUEST_HEADERS, timeout=timeout)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table", class_="history-table")

    if len(tables) < 2:
        raise ValueError(f"Daily observations table not found at {url}")

    table = tables[1]
    headers = [_normalize(th.get_text(strip=True)) for th in table.find_all("th")]

    try:
        indexes = [headers.index(_normalize(column)) for column in TARGET_COLUMNS]
    except ValueError:
        raise ValueError(
            f"Expected columns {TARGET_COLUMNS} not found in table headers"
        ) from None

    rows = []

    for tr in table.find_all("tr")[1:]:
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]

        if len(cells) > max(indexes):
            rows.append([cells[index] for index in indexes])

    return rows


def main(argv=None):
    """Command line entry point: print the extracted rows, tab-separated."""
    argv = sys.argv[1:] if argv is None else argv

    if len(argv) != 1:
        print("Usage: python scrap_wunderground.py <station_table_url>", file=sys.stderr)
        return 2

    print("\t".join(TARGET_COLUMNS))

    for row in scrap_wunderground(argv[0]):
        print("\t".join(row))

    return 0


if __name__ == "__main__":
    sys.exit(main())
