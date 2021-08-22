import sys
import fire
import questionary
import subprocess

from db import update_portfolio_db, update_report_db


def get_report_details():
  '''
    Gets the report details from user via questionary

    Returns:
    report_details (dict): Dict of report attributes
  '''

  report_details = {}
  report_details['risk_tolerance'] = questionary.select(
      "What is your current risk profile?",
      choices=[
          questionary.Choice(
            title = "YOLO! (high risk)",
            value = 'high',
          ),
          questionary.Choice(
            title = "Moderation is best in all the things. (moderate risk)",
            value = 'moderate',
          ),
          questionary.Choice(
            title = "I'm afraid of losing money. (low risk)",
            value = 'low',
          )
      ]
    ).ask()
  report_details['years_until_retirement'] = questionary.text("How many years until you retire?", validate=lambda text: text.isdecimal()).ask()
  return report_details



def get_portfolio():
  '''
    Gets the portfolio positions from user via questionary

    Returns:
    portfolio (list): List of portfolio positions 
  '''

  portfolio = []

  more_assets = True
  while more_assets:
    asset = {}
    asset['symbol'] = questionary.text(
      "What's the symbol of your portfolio asset?",
      validate=lambda text: len(text) > 0
    ).ask()

    asset['quantity'] = questionary.text(
      f"How many units of {asset['symbol']} are in your portfolio?",
      validate=lambda text: text.isdecimal()
    ).ask()

    asset['type'] = questionary.select(
      f"What type of asset is {asset['symbol']}?",
      choices=[
          "Equity",
          "Fixed Income"
      ]
    ).ask()

    portfolio.append(asset)

    print()
    more_assets = questionary.confirm("Add another asset to your portfolio?").ask()
  
  if not more_assets:
    return portfolio


def awesome_app():
  '''
    Runs the main program

    Returns:
    None
  '''
  print("Welcome to the Awesome Retirement Portfolio Projector Tool!")
  
  print()
  portfolio = get_portfolio()

  if len(portfolio) == 0:
    sys.exit("Thanks for nothing... Goodbye!")

  update_portfolio_db(portfolio)

  print()
  report_details = get_report_details()

  update_report_db(report_details)

  print()
  show_dashboard = questionary.confirm('Show the dashboard?').ask()

  if show_dashboard:
    voila_process = subprocess.Popen(['voila', 'awesome_portfolio_final.ipynb', '--theme=light'])
    voila_process.communicate()

  else:
    sys.exit("Goodbye!")


if __name__ == '__main__':
  try: 
    fire.Fire(awesome_app)
  except KeyboardInterrupt:
    sys.exit("Goodbye!")