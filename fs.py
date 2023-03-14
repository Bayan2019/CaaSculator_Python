import pandas as pd;


def get_balance_sheet(xbrl_json):
    balance_sheet_store = {}

    for usGaapItem in xbrl_json['BalanceSheets']:
        values = []
        indicies = []

        for fact in xbrl_json['BalanceSheets'][usGaapItem]:
            # only consider items without segment.
            if 'segment' not in fact:
                index = fact['period']['instant']

                # avoid duplicate indicies with same values
                if index in indicies:
                    continue
                    
                # add 0 if value is nil
                if "value" not in fact:
                    values.append(0)
                else:
                    values.append(fact['value'])

                indicies.append(index)                    

            balance_sheet_store[usGaapItem] = pd.Series(values, index=indicies) 

    balance_sheet = pd.DataFrame(balance_sheet_store)
    # switch columns and rows so that US GAAP items are rows and each column header represents a date instant
    return balance_sheet.T


def get_income_statement(xbrl_json):
  income_statement_store = {}

  # iterate over each US GAAP item in the income statement
  for usGaapItem in xbrl_json['StatementsOfIncome']:
    values = []
    indicies = []

    for fact in xbrl_json['StatementsOfIncome'][usGaapItem]:
      # only consider items without segment. not required for our analysis.
      if 'segment' not in fact:
        index = fact['period']['startDate'] + '-' + fact['period']['endDate']
          # ensure no index duplicates are created
        if index not in indicies:
          values.append(fact['value'])
          indicies.append(index)                    

    income_statement_store[usGaapItem] = pd.Series(values, index=indicies) 

  income_statement = pd.DataFrame(income_statement_store)
  # switch columns and rows so that US GAAP items are rows and each column header represents a date range
  return income_statement.T;


def get_cash_flow_statement(xbrl_json):
  cash_flows_store = {}

  for usGaapItem in xbrl_json['StatementsOfCashFlows']:
    values = []
    indicies = []

    for fact in xbrl_json['StatementsOfCashFlows'][usGaapItem]:        
      # only consider items without segment.
      if 'segment' not in fact:
        # check if date instant or date range is present
        if "instant" in fact['period']:
          index = fact['period']['instant']
        else:
          index = fact['period']['startDate'] + '-' + fact['period']['endDate']

        # avoid duplicate indicies with same values
        if index in indicies:
          continue

        if "value" not in fact:
          values.append(0)
        else:
          values.append(fact['value'])

        indicies.append(index)                    

    cash_flows_store[usGaapItem] = pd.Series(values, index=indicies) 


  cash_flows = pd.DataFrame(cash_flows_store)
  return cash_flows.T


