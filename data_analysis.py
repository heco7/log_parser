# This program will analyse a log file from a webserver and generate a HTML table with statistics.

import re
import dateutil.parser as parser
from collections import Counter

filePath = 'almhuette-raith-at-access.log'

# Regex
IPregex = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
Dateregex = r'\d{2}/\w{3}/\d{4}'
ISOregex = r'\d{4}\-\d{2}\-\d{2}'

# Dictionaries for dates/IP hit count
earliestDate = {}
latestDate = {}
hits = {}

with open(filePath) as infile:
    print('Processing data, please wait..')

    for line in infile:
        # Takes an IP address from the line and converts it into a string
        IP = ''.join(re.findall(IPregex, line))

        # Only proceed with date commands if the line contains a valid date
        if bool(re.search(Dateregex, line)):
            # Grabs the date and turns it into ISO-format
            date = ''.join(re.findall(Dateregex, line))
            date = parser.parse(date)
            date = date.isoformat()
            date = ''.join(re.findall(ISOregex, date))

            # Find the earliest and latest date
            if IP not in earliestDate:
                earliestDate[IP] = date
            if IP not in latestDate:
                latestDate[IP] = date
            else:
                if date < earliestDate[IP]:
                    earliestDate[IP] = date
                if date > latestDate[IP]:
                    latestDate[IP] = date

        # Increment IP hit count
        if IP not in hits:
            hits[IP] = 1
        else:
            hits[IP] += 1

# Grab the 20 most common IPs
count = Counter(hits)
MostCommon = count.most_common(20)

# Generates the total amount of unique IPs, total amount of accesses and how unique each IP is in percentage
totalIPs = len(hits)
totalAccess = sum(hits.values())
IPpercentage = 1/(len(hits))*100

# Data that will be used for the HTML table
IPs = [x[0] for x in MostCommon]
hitCount = [x[1] for x in MostCommon]
PercentageAccess = []
for x in MostCommon:
    percentage = round(hits[x[0]] / totalAccess * 100, 3)
    PercentageAccess.append(percentage)

html_table = """
<html>
<head>
<title>Resultat av loggfil</title>
</head>
<body>
<table border="1">
    <tr>
    <th>IP address</th>
        <th>Amount of hits</th>
        <th>Earliest date</th>
        <th>Latest date</th>
        <th>Percentage of total accesses</th>
        <th>Percentage of total IP addresses</th>
    </tr>
"""

# Add rows to the HTML table for the 20 most common IPs
for x in range(20):
    html_table += '    <tr>\n'
    html_table += '        <td>{}</td>\n'.format(IPs[x])
    html_table += '        <td>{}</td>\n'.format(hitCount[x])
    html_table += '        <td>{}</td>\n'.format(earliestDate[IPs[x]])
    html_table += '        <td>{}</td>\n'.format(latestDate[IPs[x]])
    html_table += '        <td>{}</td>\n'.format(
        str(PercentageAccess[x]) + '%')
    html_table += '        <td>{}</td>\n'.format(
        str(round(IPpercentage, 5)) + '%')
    html_table += '    </tr>\n'

# Closing HTML tags
html_table += """</table>
</body>
</html>
"""

# Write "table.html" HTML document
with open("table.html", "w") as file:
    file.write(html_table)

print('Done! Results saved in table.html')
