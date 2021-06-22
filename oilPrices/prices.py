import requests, re
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning
# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Dict for sites to check
oilSites = {
    "Liberty": "https://libertydiscountfuel.com/shop/heating-oil/",
    "REIS": "https://www.reisfuel.com/",
    "Hackettstown Oil": "https://hackettstownoil.net/",
    "Frigid": "https://frigidoilnj.com/"
    # "COD": "https://codoil.com/heating-oil-residential-and-commercial.html"
    }
# Define HTML header, one of the sites required it
header = {
    "User-Agent": "Python3"
}


# Get Current Date, for HTML page
NOW = datetime.now().strftime('%m-%d-%Y')
# Leaving for quick testing local
dipityShitsies = open('/var/www/html/index.html', 'w')
# dipityShitsies = open('./index.html', 'w')

# Create CSS style for HTML
cssBullshit = '<style>table.stupidTable { \
  border: 1px solid #1C6EA4; \
  background-color: #EEEEEE; \
  width: 50%; \
  text-align: left; \
  border-collapse: collapse; \
} \
table.stupidTable td, table.stupidTable th { \
  border: 1px solid #AAAAAA; \
  padding: 3px 2px; \
} \
table.stupidTable tbody td { \
  font-size: 16px; \
} \
table.stupidTable tr:nth-child(even) { \
  background: #D0E4F5; \
} \
table.stupidTable thead { \
  background: #1C6EA4; \
  background: -moz-linear-gradient(top, #5592bb 0%, #327cad 66%, #1C6EA4 100%); \
  background: -webkit-linear-gradient(top, #5592bb 0%, #327cad 66%, #1C6EA4 100%); \
  background: linear-gradient(to bottom, #5592bb 0%, #327cad 66%, #1C6EA4 100%); \
  border-bottom: 2px solid #444444; \
} \
table.stupidTable thead th { \
  font-size: 18px; \
  font-weight: bold; \
  color: #FFFFFF; \
  border-left: 2px solid #D0E4F5; \
} \
table.stupidTable thead th:first-child { \
  border-left: none; \
} \
 \
table.stupidTable tfoot td { \
  font-size: 16px; \
} \
table.stupidTable tfoot .links { \
  text-align: right; \
} \
table.stupidTable tfoot .links a{ \
  display: inline-block; \
  background: #1C6EA4; \
  color: #FFFFFF; \
  padding: 2px 8px; \
  border-radius: 5px; \
} \
</style> \
<body>'
# Start HTML
html = "<html> \
    <head> \
      <title>Oil Prices</title> \
    <script> \
        function autoRefresh() { \
            window.location = window.location.href; \
        } \
        setInterval('autoRefresh()', 300000); \
    </script> \
    </head>"
# Create Body for HTML
htmlBody = f'<center><h1>Oil Prices <br>{NOW}</h1> \
<table class="stupidTable"> \
<thead> \
<tr> \
<th>Oil Company</th> \
<th>Current Price</th> \
</tr> \
</thead> \
<tbody>'

# END HTML
htmlCloser = '</tr> \
</tbody> \
</table> \
<b>This page auto-refreshes</b><br> \
If the page reloads blank, manually reload it. \
</body></html>'

# Create index.html file
dipityShitsies.write(html)
dipityShitsies.write(cssBullshit)
dipityShitsies.write(htmlBody)

# Empty Dict to sort later
priceDict = {}

# Look at all sites in oilSites Dict
for company in oilSites:
    price = "" # reset price each time
    print(f'{company}:') # console outputs
    url = oilSites[company] # define URL to querry
    try:
      response = requests.request("GET", url, headers=header) # Send request to the web pages
      # Each site is different, take the response and pull out the online price only
      if company.lower() == 'liberty':
        price = re.sub(".*Online Price: (\$\d\.\d+).*", r"\1", str(response.content))
      if company.lower() == 'reis':
        price = re.sub(".*(Today.*)&.*(\$\d\.\d+).*", r"\2", str(response.content))
      if company.lower() == 'hackettstown oil':
        price = re.sub("Phone Today.*(\$\d.\d+).*", "", str(response.content))
        price = re.sub(".*Order Online.*(\$\d.\d+).*", r"\1", price)
      if company.lower() == 'frigid':
        price = re.sub(".*Current Oil Price.*(\$\d.\d+).*", r"\1", str(response.content))
      # if company.lower() == 'cod':
      #   price = re.sub(".*299.*(\$\d.\d+).*300.*", r"\1", str(response.content))
      print(f'  {price}') # console outputs
      priceDict[company] = [price, oilSites[company]] # compile priceDict, or fail.. whatever
    except:
        priceDict['*FAILED REQUEST*   ' + company] = ['9999', oilSites[company]] # make it known failed and put at the bottom of the list
        
# Sort the price list (Lowest to Highest)
sortedList = sorted(priceDict.items(), key=lambda x:x[1])
sortDict = dict(sortedList)
print(sortDict) # console output

# Generate price table
for company in sortDict:
  try:
    dipityShitsies.write(f'<tr><td><a href="{sortDict[company][1]}">{company}</a></td><td>{sortDict[company][0]}</td></tr>')
  except:
    dipityShitsies.write(f'<tr><td>Something broke {company}</td><td></td></tr>')

# Close files out
dipityShitsies.write(htmlCloser)
dipityShitsies.close()
