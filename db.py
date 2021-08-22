import sqlalchemy as sql

def get_db():
  '''
    Returns the sqlite db engine
  '''
  connection_string = 'sqlite:///awesome_app.db'
  engine = sql.create_engine(connection_string, echo=False)
  
  return engine



def update_portfolio_db(portfolio):
  '''
    Updates the sqlite db with portfolio

    Args:
    portfolio (list): List of portfolio positions 

    Returns:
    None
  '''
  engine = get_db()

  engine.execute("DROP TABLE IF EXISTS portfolio")
  engine.execute("""
    CREATE TABLE portfolio (
      symbol VARCHAR,
      quantity REAL,
      type VARCHAR
    )
  """)

  insert_portfolio_sql = """
    INSERT INTO portfolio ("symbol", "quantity", "type")
    VALUES 
  """

  count = 0
  for asset in portfolio:
    if count > 0:
      insert_portfolio_sql += ", "  
    insert_portfolio_sql += f"(\"{asset['symbol']}\", \"{asset['quantity']}\", \"{asset['type']}\")"
    count += 1
  
  engine.execute(insert_portfolio_sql)



def update_report_db(report_details):
  '''
    Updates the sqlite db with report

    Args:
    report_details (dict): Dict of report attributes

    Returns:
    None
  '''
  engine = get_db()

  engine.execute("DROP TABLE IF EXISTS report")
  engine.execute("""
    CREATE TABLE report (
      risk_tolerance VARCHAR,
      years_until_retirement REAL
    )
  """)
  engine.execute(f"""
    INSERT INTO report ("risk_tolerance", "years_until_retirement")
    VALUES ("{report_details['risk_tolerance']}", "{report_details['years_until_retirement']}")
  """)

