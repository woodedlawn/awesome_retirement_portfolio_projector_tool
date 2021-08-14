import sys
import fire
import questionary
import subprocess

from db import update_portfolio


def get_portfolio():
  portfolio = []

  more_assets = True
  while more_assets:
    asset = {}
    print("\n")
    asset['symbol'] = questionary.text("What's the symbol of your portfolio asset?").ask()
    asset['type'] = questionary.select(
      f"What type of asset is {asset['symbol']}?",
      choices=[
          "Equity",
          "Fixed Income",
          "Other",
      ]
    ).ask()
    asset['quantity'] = questionary.text(f"How many units of {asset['symbol']} are in the portfolio?", validate=lambda text: text.isdecimal()).ask()
    portfolio.append(asset)
    more_assets = questionary.confirm("Add another asset to your portfolio?").ask()
  
  if not more_assets:
    return portfolio


def awesome_app():
  print("Welcome to the Awesome Retirement Portfolio Projector Tool!")
  portfolio = get_portfolio()

  if len(portfolio) == 0:
    sys.exit("Thanks for nothing... Goodbye!")

  update_portfolio(portfolio)

  show_dashboard = questionary.confirm('Show the dashboard?').ask()

  if show_dashboard:
    voila_process = subprocess.Popen(['voila', 'portfolio.ipynb', '--theme=light'])
    voila_process.communicate()

  else:
    sys.exit("Goodbye!")


if __name__ == '__main__':
  try: 
    fire.Fire(awesome_app)
  except KeyboardInterrupt:
    sys.exit("Goodbye!")