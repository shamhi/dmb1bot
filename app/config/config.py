from dotenv import dotenv_values

values = dotenv_values()

TOKEN = values.get('TOKEN')
