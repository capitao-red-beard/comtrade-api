import itertools
import os.path
import os
from time import sleep

import numpy as np
import pandas as pd
import requests

import blob_manager

base_url = "https://comtrade.un.org/api/get?"


def download_trade_data(
    filename,
    human_readable=False,
    verbose=True,
    period="2016",
    frequency="A",
    reporter="USA",
    partner="all",
    product="total",
    tradeflow="exports",
    blob=False,
):

    # (1) replace more convenient input options by ones that can by
    # understood by API e.g. replace country names by country codes or
    # 'YYYYMM-YYYYMM' by a list of months

    reporter = transform_reporter(reporter)

    partner = transform_partner(partner)

    tradeflow = transform_trade_flow(tradeflow)

    period = transform_period(period, frequency)

    # (2) warn/ raise an error if appropriate

    if sum("all" in inpt for inpt in [reporter, partner, period]) > 1:
        raise ValueError(
            "Only one of the parameters 'reporter', 'partner' and 'period' "
            "may use the special ALL value in a given API call."
        )

    if any(len(inpt) > 5 for inpt in [reporter, partner, period]) and human_readable:
        print(
            "Using the option human_readable=True is not recommended "
            "in this case because several API calls are necessary."
        )

        print(
            "When using the human_readable=True option, messages from "
            "the API cannot be received!"
        )

        response = input("Press y if you want to continue anyways. ")

        if response != "y":
            return None  # exit function

    # (3) download data by doing one or several API calls

    dfs = []

    slice_points = [range(0, len(inpt), 5) for inpt in [reporter, partner, period]] + [
        range(0, len(product), 20)
    ]
    # since the parameters reporter, partner and period are limited to
    # 5 inputs each and product is limited to 20 inputs

    for i, j, k, m in itertools.product(*slice_points):
        df = download_trade_database(
            human_readable=human_readable,
            verbose=verbose,
            period=period[k : k + 5],
            reporter=reporter[i : i + 5],
            partner=partner[j : j + 5],
            product=product[m : m + 20],
            tradeflow=tradeflow,
            frequency=frequency,
        )

        if df is not None:
            dfs.append(df)

        # sleep(1)  # wait 1 second because of API rate limit
        # (this is no longer required if using the api key)

    # (4) save dataframe as csv file

    if len(dfs) > 0:
        df_all = pd.concat(dfs)

        filename = filename if len(filename.split(".")) == 2 else filename + ".csv"
        # add '.csv' if necessary

        df_all.to_csv(filename)

        if blob:
            blob_manager.create_blob_from_path(
                blob_manager.generate_blob_name(filename),
                blob_manager.to_parquet(filename),
            )

        if verbose:
            print(f"{len(df_all)} records downloaded and saved as {filename}.")


def download_trade_database(
    human_readable=False,
    verbose=True,
    period="recent",
    frequency="A",
    reporter=842,
    partner="all",
    product="total",
    tradeflow=2,
):

    keypath = os.getcwd() + "\key\comtrade_api_key.txt"
    f = open(keypath, "r")
    api_key = f.read()

    fmt = "csv" if human_readable else "json"
    head = "H" if human_readable else "M"

    parameters = {
        "ps": period,
        "freq": frequency,
        "r": reporter,
        "p": partner,
        "cc": product,
        "rg": tradeflow,
        "px": "HS",  # Harmonized System (as reported) as classification scheme
        "type": "C",  # Commodities ('S' for Services)
        "fmt": fmt,  # format of the output
        "max": 50000,  # maximum number of rows
        # https://comtrade.un.org/data/dev/portal#subscription says it is 100 000
        "head": head,  # human readable headings ('H') or machine readable headings ('M')
        "token": api_key,  # the api key used to access the premium version of the api
    }

    url = base_url + dict_to_string(parameters)

    if verbose:
        print(url)

    if human_readable:
        dataframe = pd.read_csv(url)

    else:
        json_dict = requests.get(url).json()

        """
        r = ProxyRequests(url)
        r.get()
        json_dict = json.loads(r.get_raw().decode())
        """

        n_records = json_dict["validation"]["count"]["value"]
        message = json_dict["validation"]["message"]

        if not json_dict["dataset"]:

            if verbose:
                print(f"Error: empty dataset \n Message: {message}")

            dataframe = None

        else:

            if verbose and message:
                print(f"Message: {message}")

            dataframe = pd.DataFrame.from_dict(json_dict["dataset"])

    return dataframe


def transform_reporter(reporter):
    """
    replaces country names in reporter by the corresponding country codes
    """
    # if single country code/ name, convert to list
    reporter = [reporter] if not isinstance(reporter, list) else reporter

    # replace country names by country codes
    reporter = [r if is_country_code(r) else find_reporter_code(r) for r in reporter]

    return reporter


def transform_partner(partner):
    """
    replaces country names in partner by the corresponding country codes
    """
    # if single country code/ name, convert to list
    partner = [partner] if not isinstance(partner, list) else partner

    # replace country names by country codes
    partner = [p if is_country_code(p) else find_partner_code(p) for p in partner]

    return partner


def transform_trade_flow(tradeflow):
    """
    replace tradeflow "import(s)" or "export(s)" by the corresponding numbers (1 / 2)
    """
    if isinstance(tradeflow, str):

        if "export" in tradeflow.lower():
            tradeflow = 2

        elif "import" in tradeflow.lower():
            tradeflow = 1

    return tradeflow


def transform_period(period, frequency):
    """
    detects 'YYYY-YYYY' or 'YYYYMM-YYYYMM' inputs and transforms them
    into lists of YYYY or YYYYMM that the API can understand
    the function does not check whether the other inputs for period are valid!

    period: depending on freq, either YYYY or YYYYMM
    (or 'YYYY-YYYY'/ 'YYYYMM-YYYYMM' or a list of those) or 'now' or 'recent' or 'all' frequency: 'A' or 'M'
    """

    period = [period] if not isinstance(period, list) else period

    period_new = []

    for p in period:

        if isinstance(p, str) and "-" in p:
            start, end = p.split("-")

            if frequency.lower() == "a":
                y_start = int(start)
                y_end = int(end)

                for y in range(y_start, y_end + 1):
                    period_new.append(y)

            elif frequency.lower() == "m":
                y_start, m_start = int(start[:4]), int(start[4:])
                y_end, m_end = int(end[:4]), int(end[4:])

                n = (m_end - m_start + 1) + 12 * (y_end - y_start)

                y, m = y_start, m_start

                for _ in range(n):
                    period_new.append("{}{:02d}".format(y, m))

                    if 1 <= m < 12:
                        m += 1

                    elif m == 12:
                        m = 1
                        y += 1

                    else:
                        raise Exception("Shouldn't get here.")

            else:
                raise Exception("Frequency neither 'A'/'a' nor 'M'/'m'.")

        else:
            period_new.append(p)

    return period_new


def is_country_code(inpt):
    """
    checks if inpt is a valid country code, i.e. an integer, an integer converted to a string or 'all'
    output: True or False
    """
    if isinstance(inpt, str):
        return inpt.lower() == "all" or inpt.isdigit()

    else:
        return isinstance(inpt, int) or isinstance(inpt, np.int64)


def find_reporter_code(country):
    """
    see 'find_country_code'
    """
    return find_country_code(country, "reporter")


def find_partner_code(country):
    """
    see 'find_country_code'
    """
    return find_country_code(country, "partner")


def find_country_code(country, reporter_or_partner):
    """
    tries to find the country code corresponding to a country name

    procedure:
    try to find exact match, if not look for partial matches
    input country: country name or part of country name (case-sensitive!)
    input reporter_or_partner: 'reporter' or 'partner'

    output: country code
    """

    # we use a local copy of the file with country codes so that we do
    # not have to use
    # https://comtrade.un.org/data/cache/reporterAreas.json every time
    if not os.path.exists(reporter_or_partner + "Areas.csv"):
        download_country_codes_file(reporter_or_partner)

    df = pd.read_csv(reporter_or_partner + "Areas.csv", encoding="latin_1", index_col=0)

    # look for an exact match
    mask = df.text == country

    if sum(mask) == 1:
        code = df.index[mask].tolist()[0]

        return code

    # look for a partial match
    # this might be useful because some 'official' names of countries
    # are not always that well-known
    # e.g. 'Bolivia (Plurinational State of)' instead of Bolivia'
    mask2 = df.text.str.contains(country)

    if sum(mask2) > 0:
        print(
            f'There is no country in the json-file with the exact name "{country}". '
            + f'The following countries contain the word "{country}". '
            + f'If you think that one of the following countries is the one that you are looking for, press "y".'
        )

        dict_matches = df[mask2].text.to_dict()

        for code, country in dict_matches.items():
            response = input(f"{code} {country} [y?] ")

            if response == "y":
                return code

    # if no code could be found:
    raise LookupError(
        f"It was not possible to find a code that corresponds to the country {country}."
    )


def download_country_codes_file(reporter_or_partner):
    """
    downloads either the reporter or the partner file and saves it in the current directory

    input: 'reporter' or 'partner'
    """
    url = f"https://comtrade.un.org/data/cache/{reporter_or_partner}Areas.json"

    json_dict = requests.get(url).json()

    df = pd.DataFrame.from_dict(json_dict["results"])
    df = df.set_index("id")
    df.drop("all", inplace=True)
    df.to_csv(f"{reporter_or_partner}Areas.csv")


def dict_item_to_string(key, value):
    """
    inputs: key-value pairs from a dictionary

    output: string 'key=value' or 'key=value1,value2' (if value is a list)

    examples: 'fmt', 'csv' => 'fmt=csv' or 'r', [124, 484] => 'r=124,484'
    """
    value_string = (
        str(value) if not isinstance(value, list) else ",".join(map(str, value))
    )

    return "=".join([key, value_string])


def dict_to_string(parameters):
    """
    input: dictionary of parameters

    output: string 'key1=value1&key2=value2&...'
    """
    return "&".join(
        dict_item_to_string(key, value) for key, value in parameters.items()
    )


def product_codes_with_parent(parent_code):
    """
    Returns a python dictionary with all entries that belong to parent_code.
    """
    if not os.path.exists("classificationHS.csv"):
        download_product_codes_file()

    df = load_product_codes_file()

    mask = df.parent == parent_code

    return df.text[mask].to_dict()


def search_product_code(pat, case=True, flags=0, regex=True, n_digits=None):
    """
    Returns a python dictionary with all entries that contain the pattern pat and have a code with length n_digits.
    If n_digits = None (default), we do not care about how many digits the classification code has.

    For searching for the pattern pat, we use pd.Series.str.contains which takes the following parameters:

    pat : string
        Character sequence or regular expression

    case : boolean, default True
        If True, case sensitive

    flags : int, default 0 (no flags)
        re module flags, e.g. re.IGNORECASE

    regex : bool, default True
        If True use re.search, otherwise use Python in operator
    """
    if not os.path.exists("classificationHS.csv"):
        download_product_codes_file()

    df = load_product_codes_file()

    if n_digits is not None:
        mask1 = df.text.str.contains(pat, case=case, flags=flags, regex=regex)

        mask2 = df.index.to_series().apply(lambda digit: len(digit) == n_digits)

        mask = mask1 & mask2

    else:
        mask = df.text.str.contains(pat, case=case, flags=flags, regex=regex)

    return df.text[mask].to_dict()


def load_product_codes_file():
    """
    Loads the product codes file as a pandas dataframe.
    """
    df = pd.read_csv("classificationHS.csv", encoding="latin-1", index_col="id")

    return df


def download_product_codes_file():
    """
    Downloads the product codes files and saves it in the current directory.
    The short-cut entries for 'ALL', 'TOTAL', 'AG2', 'AG4' and 'AG6' are deleted.
    """
    url = "https://comtrade.un.org/data/cache/classificationHS.json"

    json_dict = requests.get(url).json()

    df = pd.DataFrame.from_dict(json_dict["results"])
    df = df.set_index("id")
    df.drop(["ALL", "TOTAL", "AG2", "AG4", "AG6"], inplace=True)
    df.text = df.text.apply(
        lambda x: " - ".join(x.split(" - ")[1:])
    )  # remove digits from beginning of text
    df.to_csv("classificationHS.csv")
