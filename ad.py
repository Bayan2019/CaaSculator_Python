import requests;
import pandas as pd;
import json;

def downloading(ticker, email):
  headers = {'User-Agent': email};

  tickers_cik = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers);
  tickers_cik = pd.json_normalize(pd.json_normalize(tickers_cik.json(), max_level=0).values[0]);
  tickers_cik["cik_str"] = tickers_cik["cik_str"].astype(str).str.zfill(10);
  tickers_cik.set_index("ticker",inplace=True);

  try:
    cik = tickers_cik.loc[ticker, 'cik_str'];
  except:
    return "The Ticker is not found!"

  metrics = pd.read_csv("https://raw.githubusercontent.com/Bayan2019/CaaSculator_Python/main/list_of_companies/metrics.csv")
  metrics.set_index("metrics", inplace=True);
  metrics_list = list(metrics.index)

  url_facts = "https://data.sec.gov/api/xbrl/companyfacts/CIK" + cik + ".json";

  facts = requests.get(url_facts, headers=headers);

  try:
    facts_json = json.loads(facts.text);
  except:
    return "No data for this Ticker"

  if "us-gaap" in facts_json['facts'].keys():
    cik_facts = list(facts_json['facts']['us-gaap'].keys());
    facts = facts_json['facts']['us-gaap']
    method = "/us-gaap/";
  else:
    cik_facts = list(facts_json['facts']['ifrs-full'].keys());
    facts = facts_json['facts']['ifrs-full']
    method = "/ifrs-full/";

  company_data = {};
  for metric in metrics_list:
    if metric in cik_facts:
      # print(metric)
      try: 
        if metric in ["EarningsPerShareBasic", "EarningsPerShareDiluted"]:
          try:
            response_df = pd.json_normalize(facts[metric]["units"]["USD/shares"])
            currency = 'USD'
          except:
            keys = list(facts[metric]['units'].keys())
            response_df = pd.json_normalize(facts[metric]['units'][keys[0]]);
            currency = keys[0];

        else:
          try:
            response_df = pd.json_normalize(facts[metric]["units"]["USD"]);
            currency = 'USD';
          except:
            key = list(facts[metric]['units'].keys());
            response_df = pd.json_normalize(facts[metric]['units'][keys[0]]);
            currency = keys[0];
      except:
        url_metric = "https://data.sec.gov/api/xbrl/companyconcept/CIK" + cik + method + metric + ".json";
        response = requests.get(url_metric, headers=headers);
        response_json = json.loads(response.text);

        if metric in ["EarningsPerShareBasic", "EarningsPerShareDiluted"]:
          try:
            response_df = pd.json_normalize(response_json["units"]["USD/shares"]);
            currency = 'USD'
          except:
            keys = list(response_json["units"].keys());
            currency = keys[0];
            response_df = pd.json_normalize(response_json['units'][currency])
        else:
          try:
            response_df = pd.json_normalize(response_json["units"]["USD"]);
            currency = 'USD'
          except:
            keys = list(response_json['units'].keys());
            currency = keys[0];
            response_df = pd.json_normalize(response_json['units'][currency]);

      response_df["filed"] = pd.to_datetime(response_df["filed"])
      response_df = response_df.sort_values(by = ["end", "filed"])

      ends = set(list(response_df['end']))
      reporting = {};
      for end in ends:
        response_df_end = response_df[response_df['end'] == end];
        response_df_end_max_filed = response_df_end[response_df_end.filed == response_df_end['filed'].max()];
        reporting[end] = response_df_end_max_filed.loc[response_df_end_max_filed.index[0], 'val'];

      company_data[metric] = {"reporting": reporting, "currency": currency};

  return company_data;

# Quartal data

def downloading_quartal(ticker, email):
  headers = {'User-Agent': email};

  tickers_cik = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers);
  tickers_cik = pd.json_normalize(pd.json_normalize(tickers_cik.json(), max_level=0).values[0]);
  tickers_cik["cik_str"] = tickers_cik["cik_str"].astype(str).str.zfill(10);
  tickers_cik.set_index("ticker",inplace=True);

  try:
    cik = tickers_cik.loc[ticker, 'cik_str'];
  except:
    return "The Ticker is not found!"

  metrics = pd.read_csv("https://raw.githubusercontent.com/Bayan2019/CaaSculator_Python/main/list_of_companies/metrics.csv")
  metrics.set_index("metrics", inplace=True);
  metrics_list = list(metrics.index)

  url_facts = "https://data.sec.gov/api/xbrl/companyfacts/CIK" + cik + ".json";

  facts = requests.get(url_facts, headers=headers);

  try:
    facts_json = json.loads(facts.text);
  except:
    return "No data for this Ticker"

  if "us-gaap" in facts_json['facts'].keys():
    cik_facts = list(facts_json['facts']['us-gaap'].keys());
    facts = facts_json['facts']['us-gaap']
    method = "/us-gaap/";
  else:
    cik_facts = list(facts_json['facts']['ifrs-full'].keys());
    facts = facts_json['facts']['ifrs-full']
    method = "/ifrs-full/";

  company_data = {};
  for metric in metrics_list:
    if metric in cik_facts:
      # print(metric)
      try: 
        if metric in ["EarningsPerShareBasic", "EarningsPerShareDiluted"]:
          try:
            list_metric = [];
            for item in facts[metric]["units"]["USD/shares"]:
              if item['form'] == '10-Q':
                list_metric.append(item);
            if list_metric == []:
              continue;
            else:
              response_df = pd.json_normalize(list_metric)
              currency = 'USD'
          except:
            keys = list(facts[metric]['units'].keys())
            list_metric = [];
            for item in facts[metric]['units'][keys[0]]:
              if item['form'] == '10-Q':
                list_metric.append(item);
            if list_metric == []:
              continue;
            else:
              response_df = pd.json_normalize(list_metric);
              currency = keys[0];

        else:
          try:
            list_metric = [];
            for item in facts[metric]["units"]["USD"]:
              if item['form'] == '10-Q':
                list_metric.append(item);
            if list_metric == []:
              continue;
            else:
              response_df = pd.json_normalize(list_metric);
              currency = 'USD';
          except:
            key = list(facts[metric]['units'].keys());
            list_metric = [];
            for item in facts[metric]['units'][keys[0]]:
              if item['form'] == '10-Q':
                list_metric.append(item);
            if list_metric == []:
              continue;
            else: 
              response_df = pd.json_normalize(list_metric);
              currency = keys[0];
      except:
        url_metric = "https://data.sec.gov/api/xbrl/companyconcept/CIK" + cik + method + metric + ".json";
        response = requests.get(url_metric, headers=headers);
        response_json = json.loads(response.text);

        if metric in ["EarningsPerShareBasic", "EarningsPerShareDiluted"]:
          try:
            list_metric = [];
            for item in response_json["units"]["USD/shares"]:
              if item['form'] == '10-Q':
                list_metric.append(item);
            if list_metric == []:
              continue;
            else:
              response_df = pd.json_normalize(list_metric);
              currency = 'USD'
          except:
            keys = list(response_json["units"].keys());
            currency = keys[0];
            list_metric = [];
            for item in response_json['units'][currency]:
              if item['form'] == '10-Q':
                list_metric.append(item);
            if list_metric == []:
              continue;
            else:
              response_df = pd.json_normalize(list_metric)
        else:
          try:
            list_metric = [];
            for item in response_json["units"]["USD"]:
              if item['form'] == '10-Q':
                list_metric.append(item);
            if list_metric == []:
              continue;
            else:
              response_df = pd.json_normalize(list_metric);
              currency = 'USD'
          except:
            keys = list(response_json['units'].keys());
            currency = keys[0];
            list_metric = [];
            for item in response_json['units'][currency]:
              if item['form'] == '10-Q':
                list_metric.append(item);
            if list_metric == []:
              continue;
            else:
              response_df = pd.json_normalize(list_metric);

      response_df["filed"] = pd.to_datetime(response_df["filed"])
      response_df = response_df.sort_values(by = ["end", "filed"])

      ends = set(list(response_df['end']))
      reporting = {};
      for end in ends:
        response_df_end = response_df[response_df['end'] == end];
        response_df_end_max_filed = response_df_end[response_df_end.filed == response_df_end['filed'].max()];
        reporting[end] = response_df_end_max_filed.loc[response_df_end_max_filed.index[0], 'val'];

      company_data[metric] = {"reporting": reporting, "currency": currency};

  return company_data;

# Annual data

def downloading_annual(ticker, email):
  headers = {'User-Agent': email};

  tickers_cik = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers);
  tickers_cik = pd.json_normalize(pd.json_normalize(tickers_cik.json(), max_level=0).values[0]);
  tickers_cik["cik_str"] = tickers_cik["cik_str"].astype(str).str.zfill(10);
  tickers_cik.set_index("ticker",inplace=True);

  try:
    cik = tickers_cik.loc[ticker, 'cik_str'];
  except:
    return "The Ticker is not found!"

  metrics = pd.read_csv("https://raw.githubusercontent.com/Bayan2019/CaaSculator_Python/main/list_of_companies/metrics.csv")
  metrics.set_index("metrics", inplace=True);
  metrics_list = list(metrics.index)

  url_facts = "https://data.sec.gov/api/xbrl/companyfacts/CIK" + cik + ".json";

  facts = requests.get(url_facts, headers=headers);

  try:
    facts_json = json.loads(facts.text);
  except:
    return "No data for this Ticker"

  if "us-gaap" in facts_json['facts'].keys():
    cik_facts = list(facts_json['facts']['us-gaap'].keys());
    facts = facts_json['facts']['us-gaap']
    method = "/us-gaap/";
  else:
    cik_facts = list(facts_json['facts']['ifrs-full'].keys());
    facts = facts_json['facts']['ifrs-full']
    method = "/ifrs-full/";

  company_data = {};
  for metric in metrics_list:
    if metric in cik_facts:
      # print(metric)
      try: 
        if metric in ["EarningsPerShareBasic", "EarningsPerShareDiluted"]:
          try:
            list_metric = [];
            for item in facts[metric]["units"]["USD/shares"]:
              if item['form'] in ['10-K', '10-K/A']:
                list_metric.append(item);
            if list_metric == []:
              continue;
            else:
              response_df = pd.json_normalize(list_metric)
              currency = 'USD'
          except:
            keys = list(facts[metric]['units'].keys())
            list_metric = [];
            for item in facts[metric]['units'][keys[0]]:
              if item['form'] in ['10-K', '10-K/A']:
                list_metric.append(item);
            if list_metric == []:
              continue;
            else:
              response_df = pd.json_normalize(list_metric);
              currency = keys[0];

        else:
          try:
            list_metric = [];
            for item in facts[metric]["units"]["USD"]:
              if item['form'] in ['10-K', '10-K/A']:
                list_metric.append(item);
            if list_metric == []:
              continue;
            else:
              response_df = pd.json_normalize(list_metric);
              currency = 'USD';
          except:
            key = list(facts[metric]['units'].keys());
            list_metric = [];
            for item in facts[metric]['units'][keys[0]]:
              if item['form'] in ['10-K', '10-K/A']:
                list_metric.append(item);
            if list_metric == []:
              continue;
            else: 
              response_df = pd.json_normalize(list_metric);
              currency = keys[0];
      except:
        url_metric = "https://data.sec.gov/api/xbrl/companyconcept/CIK" + cik + method + metric + ".json";
        response = requests.get(url_metric, headers=headers);
        response_json = json.loads(response.text);

        if metric in ["EarningsPerShareBasic", "EarningsPerShareDiluted"]:
          try:
            list_metric = [];
            for item in response_json["units"]["USD/shares"]:
              if item['form'] in ['10-K', '10-K/A']:
                list_metric.append(item);
            if list_metric == []:
              continue;
            else:
              response_df = pd.json_normalize(list_metric);
              currency = 'USD'
          except:
            keys = list(response_json["units"].keys());
            currency = keys[0];
            list_metric = [];
            for item in response_json['units'][currency]:
              if item['form'] in ['10-K', '10-K/A']:
                list_metric.append(item);
            if list_metric == []:
              continue;
            else:
              response_df = pd.json_normalize(list_metric)
        else:
          try:
            list_metric = [];
            for item in response_json["units"]["USD"]:
              if item['form'] in ['10-K', '10-K/A']:
                list_metric.append(item);
            if list_metric == []:
              continue;
            else:
              response_df = pd.json_normalize(list_metric);
              currency = 'USD'
          except:
            keys = list(response_json['units'].keys());
            currency = keys[0];
            list_metric = [];
            for item in response_json['units'][currency]:
              if item['form'] in ['10-K', '10-K/A']:
                list_metric.append(item);
            if list_metric == []:
              continue;
            else:
              response_df = pd.json_normalize(list_metric);

      response_df["filed"] = pd.to_datetime(response_df["filed"])
      response_df = response_df.sort_values(by = ["end", "filed"])

      ends = set(list(response_df['end']))
      reporting = {};
      for end in ends:
        response_df_end = response_df[response_df['end'] == end];
        response_df_end_max_filed = response_df_end[response_df_end.filed == response_df_end['filed'].max()];
        reporting[end] = response_df_end_max_filed.loc[response_df_end_max_filed.index[0], 'val'];

      company_data[metric] = {"reporting": reporting, "currency": currency};

  return company_data;