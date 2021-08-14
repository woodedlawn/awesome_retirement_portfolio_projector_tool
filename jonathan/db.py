import sqlalchemy as sql

def get_db():
  connection_string = 'sqlite:///awesome_app.db'
  engine = sql.create_engine(connection_string, echo=False)
  
  return engine



def update_portfolio(portfolio):
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