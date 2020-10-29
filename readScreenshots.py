try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
textMessageDict = pd.DataFrame(columns=['File Name','Phone Number','Date','Message'])
screenshotCount = 0

# working loop for all files
for file in os.listdir(r'.\screenshots'):
  try:
    screenshotCount += 1
    screenshotString = pytesseract.image_to_string(Image.open(os.path.join(r'.\screenshots', file)))
    screenshotString = screenshotString.split('\n')
    if '+1' not in screenshotString[2]:
      screenshotString.remove('x')
    screenshotString = list(filter(None,screenshotString))
    textMessageText = ''.join(screenshotString[4:])
    textMessageDict = textMessageDict.append({'File Name':file,
                                              'Phone Number':screenshotString[1],
                                              'Date':screenshotString[3],
                                              'Message':textMessageText},ignore_index=True)
    print('Processed image {} of {}'.format(screenshotCount, len(os.listdir(r'.\screenshots'))))
  except:
    print('Something wrong with file: {}'.format(file))

# clean up dictionary
toDrop = textMessageDict[textMessageDict['Phone Number'].str.startswith('+1') == False].index # remove any phone numbers that weren't read correctly
textMessageDict.drop(toDrop,inplace=True)
textMessageDict.Date.str.split(',',expand=True)[1:]
textMessageDict['Date'] = textMessageDict.Date.str.slice(start=4) # removes the day of the week

newCols = textMessageDict.Date.str.split(',',expand=True) # create a temp dataframe to hold broken out date and time 
newCols.columns = ['Date','Time']
textMessageDict = textMessageDict.merge(newCols,left_index=True,right_index=True) # combine dataframes
textMessageDict['Date'] = textMessageDict.Date_y # set Date column
textMessageDict = textMessageDict.drop(columns=['Date_x','Date_y'])
textMessageDict['Phone Number'] = textMessageDict['Phone Number'].str.replace(' >','') # remove ' >' from phone numbers
textMessageDict.to_csv('output.csv',index=False)