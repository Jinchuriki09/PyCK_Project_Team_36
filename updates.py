from bs4 import BeautifulSoup
import functions
import requests
import smtplib
import pandas
import os        

# mail function that takes name, url and a dictionary of all the CHANGED attributes
# here i've used a dummy gmail account to log into to send myself updates 
# replace reciever_email variable value to your email id as a string.
def mail_funct(name, changeDict, url):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
                
        passwrd = ':Rq7L!kwTah?99h'
        email_id = 'producttraxker@gmail.com'

        reciever_email = os.environ.get('mail_id')
        
        mailingList = [reciever_email]
        smtp.login(email_id, passwrd)
        
        attributeChange = 'ATTRIBUTE             OLD             NEW'
        for key, value in changeDict.items():
            attributeChange = attributeChange + f'\n{key}                  {value[0]}             {value[1]}'
        
        subject = f'Hi! There is an update regarding your product: {name[:35]}'
        body = f'your product: {name}\nhas the following changes:\n{attributeChange}\nCheck it out here:\n{url}'
        msg = f'Subject: {subject}\n\n{body}'
        
        for mail in mailingList:
            smtp.sendmail(email_id, mail, msg.encode("utf-8"))
            print('mail sent to '+mail)
    
    
#function that checks the csv database for updating and alerting!    

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

def doCheck():
    df = pandas.read_csv('database.csv', index_col=0, converters={'price_in_rupees' : str,
                                                                  'availability' : str})
    
    for i, line in df.iterrows():
        url = line['link']
        r = requests.get(url, headers)
        htmlContent = r.content
        soup = BeautifulSoup(htmlContent, 'html.parser')
        
        newPrice = functions.getPrice(soup)
        newAvailability = functions.getAvailability(soup)  
        
        changes = {}
        
        if line['price_in_rupees'] != newPrice:
            changes['price'] = [line['price_in_rupees'], newPrice]
            
        if line['availability'] != newAvailability:
            changes['availability'] = [line['availability'], newAvailability]
            
        if changes:
            print(f"Change detected! Product:{line['product_name'][:20]}      {i}")
            mail_funct(line['product_name'], changes, url)
            
            df.at[i, 'price_in_rupees'] = newPrice
            df.at[i, 'availability'] = newAvailability
            
            df.to_csv("database.csv")
            print('database updated!')
            print('############################################')
        else:
            print(f"No change for Product:{line['product_name'][:20]}      {i}")
            print('############################################')
            
#:Rq7L!kwTah?99h 14 july 2000