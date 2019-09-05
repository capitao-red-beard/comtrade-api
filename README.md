# Comtrade API

This project is a collection of functions which help a user to download data from the Comtrade API.

## Dependencies

Please read the requirements.txt file for all the requirements. To install them once you clone this repo:

- `pip install -r requirements.txt`

## How to

This is a short into on how to use each of the functions, I originally placed this within the code itself to support Jupyter notebook users as docstrings but this was cumborsome and verbose.

### download_trade_data

Downloads records from the UN Comtrade database and saves them in a csv-file with the name `filename`.
If necessary, it calls the API several times.

There are two modes:

- `human_readable = False (default):`
    headings in output are not human-readable but error messages from the API are received and displayed

- `human_readable = True:`
headings in output are human-readable but we do not get messages from the API about potential problems
(not recommended if several API calls are necessary)

Additional option:
`verbose = False:`
in order to suppress both messages from the API and messages like '100 records downloaded and saved in filename.csv'
(True is default)

Parameters:
Using parameter values suggested in the API documentation should always work.
For the parameters period, reporter, partner and tradeflow more intuitive options have been added.

- `period     [ps]   :` depending on freq, either `YYYY` or `YYYYMM` (or `YYYY-YYYY`/ `YYYYMM-YYYYMM` or a list of those)
or `now` or `recent` (= 5 most recent years/ months) or `all`

- `frequency  [freq] :` 'A' (= annual) or 'M' (= monthly)

- `reporter   [r]    :` reporter code/ name (case-sensitive!) or list of reporter codes/ names or `all`
(see `https://comtrade.un.org/data/cache/reporterAreas.json`)

- `partner    [p]    :` partner code/ name  (case-sensitive!) or list of partner codes/ names or `all`
(see `https://comtrade.un.org/data/cache/partnerAreas.json`)

- `product    [cc]   :` commodity code valid in the selected classification (here: Harmonized System HS) or `total`
(= aggregated) or `all` or `HG2`, `HG4` or `HG6` (= all 2-, 4- and 6-digit HS commodities)

- `tradeflow  [rg]   :` 'import[s]' or 'export[s]';
(see `https://comtrade.un.org/data/cache/tradeRegimes.json`) for further, lower-level options

- `blob       [bl]   :` boolean variable to check whether to send the CSV to the `azure blob storage`

Information copied from the API Documentation (`https://comtrade.un.org/data/doc/api/`):
Usage limits
`Rate limit (guest):` 1 request every second (per IP address or authenticated user).

`Usage limit (guest):` 100 requests per hour (per IP address or authenticated user).

Parameter combination limit: `ps`, `r` and `p` are limited to `5 codes each`.
Only one of the above codes may use the special ALL value in a given API call.

Classification codes (cc) are limited to `20 items`. ALL is always a valid classification code.

If you hit a usage limit a `409 (conflict) error` is returned
along with a message specifying why the request was blocked and when requests may resume.

### download_trade_database

Downloads records from the UN Comtrade database and returns pandas dataframe using one API call.

There are two modes:

- `human_readable = False (default):` headings in output are not human-readable
    but error messages from the API are received and displayed
- `human_readable = True:` headings in output are human-readable
    but we do not get messages from the API about potential problems

Additional option:
    `verbose = False:` in order to suppress messages from the API (True is default)

Parameters of the API call:
As documented in the API documentation.

More intuitive options for the parameters:
period, reporter, partner and tradeflow are only available in the function `download_trade_data`

- `period     [ps]   :` depending on freq, either `YYYY` or `YYYYMM` (or a list of those) or `now` or `recent`
(= 5 most recent years/ months) or `all`

- `frequency  [freq] :` `A` (= annual) or `M` (= monthly)

- `reporter   [r]    :` reporter code or list of reporter codes or `all`
(see `https://comtrade.un.org/data/cache/reporterAreas.json`)

- `partner    [p]    :` partner code or list of partner codes or `all`
(see `https://comtrade.un.org/data/cache/partnerAreas.json`)

- `product    [cc]   :` commodity code valid in the selected classification
(here: Harmonized System HS) or `total` (= aggregated) or `all` or `HG2`, `HG4` or `HG6`
(= all 2-, 4- and 6-digit HS commodities)

- `tradeflow  [rg]   :` 1 (for imports) or 2 (for exports);
(see `https://comtrade.un.org/data/cache/tradeRegimes.json`) for further options

### main.py

1. Pick your date range and instantiate the variable `years` with this value, this can be either year-year or monthyear-monthyear.
2. Pick the countries which you are interested to see data pulled from, fill these values into `dict_countries`, if you need help to find country codes simply navigate to the `reporterAreas.csv` in this repo.
3. Pick your product list, these values can be found on the comtrade API web page `https://comtrade.un.org/data`.
4. Run the code in whichever way you see fit my advice is go into the terminal and navigate to the directory and type in `python3 main.py`.
5. ***WARNING*** this project may take an extremely long time to run due to the limitatios of the API... there is currently a hard coded pause built into the code which helps us not reach the API request limit and get an error code back.
6. If you have any questions just shoot by my desk!
