import pandas as pd
import yagmail
import access
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def transform_number(number):
    return float(number.replace('R$', '').replace('.','').replace(',', '.'))


df = pd.read_excel('Produtos.xlsx')

amz_iphone = df['Amazon'][0]
amr_iphone = df['Lojas Americanas'][0]
mgz_iphone = df['Magazine Luiza'][0]

amz_tv = df['Amazon'][1]
amr_tv = df['Lojas Americanas'][1]
mgz_tv = df['Magazine Luiza'][1]

iphone_original_price = float(df['Preço Original'][0])
tv_original_price = float(df['Preço Original'][1])

# iPhones routine
cheaper = None

driver = webdriver.Chrome(ChromeDriverManager().install()) # starting the webdriver

# amazon iphone
driver.get(amz_iphone)
price = transform_number(driver.find_element(By.ID, 'priceblock_ourprice').text)

if price < float(iphone_original_price):
    cheaper = price
    df['Preço Atual'][0] = cheaper
    df['Local'][0] = 'Amazon'

# americanas iphone
driver.get(amr_iphone)
price = transform_number(driver.find_element(By.CLASS_NAME, 'priceSales').text)

if price < cheaper:
    cheaper = price
    df['Preço Atual'][0] = cheaper
    df['Local'][0] = 'Americanas'
    
# magalu iphone
driver.get(mgz_iphone)
price = transform_number(driver.find_element(By.CLASS_NAME, 'price-template__text').text)

if price < cheaper:
    df['Preço Atual'][0] = cheaper
    df['Local'][0] = 'Magazine Luiza'


# TVs routine
cheaper = None # clearing the cheaper variable
# amazon tv
driver.get(amz_tv)
price = transform_number(driver.find_element(By.ID, 'price_inside_buybox').text)

if price < float(tv_original_price):
    cheaper = price
    df['Preço Atual'][1] = cheaper
    df['Local'][1] = 'Amazon'

# americanas tv
driver.get(amr_tv)
price = transform_number(driver.find_element(By.CLASS_NAME, 'priceSales').text)

if price < cheaper:
    cheaper = price
    df['Preço Atual'][1] = cheaper
    df['Local'][1] = 'Americanas'
    
# magalu tv
driver.get(mgz_tv)
price = transform_number(driver.find_element(By.CLASS_NAME, 'price-template__text').text)

if price < cheaper:
    df['Preço Atual'][1] = cheaper
    df['Local'][1] = 'Magazine Luiza'

# saving the dataframe with updated prices
df.to_excel('Produtos Atualizado.xlsx')

# sending e-mail with the updated dataframe
user = yagmail.SMTP(user=access.user, password=access.password)

content = '''Segue em anexo planilha com preços atualizados.

Att,

Kaio.'''

user.send(to = access.user, 
          subject = 'Planilha Atualizada', 
          contents = content,
          attachments = 'Produtos Atualizado.xlsx'
         )

