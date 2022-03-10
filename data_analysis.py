# This program will analyse a log file from a webserver and generate a HTML table with statistics.

import re
import dateutil.parser as parser
from collections import Counter

# Creates an absolute filepath variable for the logfile
filePath = 'F:\\almhuette-raith-at-access.log'

# Regex used for finding string patterns
IPregex = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
Dateregex = r'\d{2}/\w{3}/\d{4}'
ISOregex = r'\d{4}\-\d{2}\-\d{2}'

# Dictionary for the earliest date
earliestDate = {}
# Dictionary for the latest date
latestDate = {}
# Count the amount of hits for each IP
hits = {}

# Opens the file specified in the filePath variable
with open(filePath) as infile:
    print('Processing data, please wait..')

    # For every line in the log file, execute this code
    for line in infile:
        # Takes an IP address from the line and converts it into a string
        IP = ''.join(re.findall(IPregex, line))

        # Only proceed with date commands if the line contains a date
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

        # Find amount of occurances for each unique IP address
        if IP not in hits:
            # First occurance of the IP address
            hits[IP] = 1
        else:
            # Count reoccuring hits
            hits[IP] += 1

# Grab the 20 most common IPs
count = Counter(hits)
MostCommon = count.most_common(20)

# Generates the total amount of unique IPs, total amount of accesses and how unique each IP is in percentage
totalIPs = len(hits)
totalAccess = sum(hits.values())
IPpercentage = 1/(len(hits))*100

# Creates lists that will be used for the HTML table
IPs = [x[0] for x in MostCommon]
hitCount = [x[1] for x in MostCommon]
PercentageAccess = []
for x in MostCommon:
    percentage = round(hits[x[0]] / totalAccess * 100, 3)
    PercentageAccess.append(percentage)

# Creates a string containing the base HTML table
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

# Appends data cells to the table headers for the 20 most common IPs
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

# Appends the final HTML code to the html_table string
html_table += """</table>
</body>
</html>
"""

# Creates a "table.html" file and writes the data from the html_table string to the file
with open("table.html", "w") as file:
    file.write(html_table)

print('Done! Results saved in table.html')
