import re, requests, xml.etree.ElementTree as ET
from datetime import datetime

URL = "https://borntoworkretail.com/js/comic_settings.js"
response = requests.get(URL)
text = response.text

entries = re.findall(
    r'pgNum:\s*(\d+),\s*title:\s*["`](.*?)["`],\s*date:\s*writeDate\((\d+),\s*(\d+),\s*(\d+)\)', 
    text
)
entries = [
    (int(pgNum), title, datetime(int(year), int(month), int(day)))
    for pgNum, title, year, month, day in entries
]
entries.sort(key=lambda x: x[2], reverse=True)


rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "I Was Born To Work Retail"
ET.SubElement(channel, "link").text = "https://borntoworkretail.com/"
ET.SubElement(channel, "description").text = "Auto-generated from borntoworkretail.com/js/comic_settings.js"

for pgNum, title, date in entries:
    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = f"{pgNum} - {title}"
    ET.SubElement(item, "link").text = f"https://borntoworkretail.com/?pg={pgNum}#showComic"
    guid = ET.SubElement(item, "guid")
    guid.text = f"pg{pgNum}"
    guid.set("isPermaLink", "false")    
    ET.SubElement(item, "pubDate").text = date.strftime("%a, %d %b %Y 00:00:00 +0000")

tree = ET.ElementTree(rss)
tree.write("docs/rss.xml", encoding="utf-8", xml_declaration=True)
