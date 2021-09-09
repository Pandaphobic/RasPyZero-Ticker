import requests as rq
import json
from RPLCD.i2c import CharLCD

adaLogo = (
        0b00100,
        0b01010,
        0b11111,
        0b01010,
        0b11111,
        0b01010,
        0b10001,
        0b10001
)

btcLogo = ( 
        0b01010,
        0b11110,
        0b10001,
        0b11110,
        0b10001,
        0b10001,
        0b11110,
        0b01010
)

ltcLogo = ( 
  0b01000,
        0b01000,
        0b01010,
        0b01100,
        0b11000,
        0b01000,
        0b01000,
        0b01111
)

ethLogo = ( 
        0b00000,
        0b11111,
        0b00000,
        0b00000,
        0b11111,
        0b00000,
        0b00000,
        0b11111
)
# # open the config file
# with open('config.json') as json_file:
#   data = json.load(json_file)

#   coins = data['coins']

# Gross LCD Part
lcd = CharLCD('PCF8574', 0x27)
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=20, rows=4, dotsize=8,
              charmap='A02',
              backlight_enabled=True)

# Create Character
lcd.create_char(0, adaLogo)
lcd.create_char(1, btcLogo)
lcd.create_char(2, ltcLogo)
lcd.create_char(3, ethLogo)

output = []

def getData(symbol):
  
  # create an api request for each coin
  req = rq.get('https://api.coingecko.com/api/v3/coins/' + x)
  req = req.json() # convert to json
  title = x.title()
  # can only concatenate strings together
  coinOutput = str(req['market_data']['current_price']['cad'])

  # Calculate spacing
  sizeA = "  " + title
  sizeB = "$" + coinOutput
  print(20 - (len(sizeA) + len(sizeB)))
  spaces = " " * (20 - (len(sizeA) + len(sizeB)))

  # Console Message
  #print('The price of ' + title + ' is ' + '$' + coinOutput)
  output.append(symbol + " " + title + spaces + "$" + coinOutput + '\r\n')
  
# crontab has a hard time with the config file
coins = ('cardano', 'bitcoin', 'litecoin', 'ethereum')

for idx, x in enumerate(coins):
  # idx is the index of the current item
  if idx == 0:
    getData("\x00")
  elif idx == 1:
    getData("\x01")
  elif idx == 2:
    getData("\x02")
  elif idx == 3:
    getData("\x03")

lcd.clear()
#lcd.write_string('-- Current Prices --')

for x in output:
  lcd.write_string(x)
  print(x)