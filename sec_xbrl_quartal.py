from sec_api import QueryApi;
import requests;
import json;
import pandas as pd;

import fs;

def xbrl(ticker, start, end):
  Api_Key = "05e62f82cdd820101a1ffe5d0c55a3e9583a11df51b0a296aefbeb4f3fa4352f";

  queryApi = QueryApi(api_key=Api_Key);

  query_quartal = {
    "query": { "query_string": {
        "query": "ticker:" + ticker + " AND filedAt:{" + start + " TO " + end + "} AND formType:\"10-Q\""
              } 
    },
    "from": "0",
    "size": "35",
    "sort": [{ "filedAt": { "order": "desc" } }]
  };

  filings_quartal = queryApi.get_filings(query_quartal);
  # XBRL-to-JSON converter API endpoint
  xbrl_converter_api_endpoint = "https://api.sec-api.io/xbrl-to-json"

  frames = [];

  for i in range(len(filings_quartal['filings'])):

    filing_quartal_url = filings_quartal['filings'][i]['linkToFilingDetails'];

    # get your API key at https://sec-api.io
    api_key = Api_Key;

    final_url = xbrl_converter_api_endpoint + "?htm-url=" + filing_quartal_url + "&token=" + api_key;

    # make request to the API
    response = requests.get(final_url);

    # load JSON into memory
    try:
      xbrl_json = json.loads(response.text);

      income_statement = fs.get_income_statement(xbrl_json);

      frames.append(income_statement);
    except:
      continue;

  result = pd.concat(frames, axis=1);

  return result;