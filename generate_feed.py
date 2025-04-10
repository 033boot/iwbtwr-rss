import re, requests, xml.etree.ElementTree as ET
from datetime import datetime

URL = "https://borntoworkretail.com/js/comic_settings.js"
response = requests.get(URL)
text = response.text

varstart = text.find('const pgData = [')
text = text[varstart+16:text.find(']', varstart)]

entries = re.findall(r'{.*?}', text, re.DOTALL)
entries = [
    (int(re.search(r'pgNum: ([0-9]*?),', entry).group(1)),
    (re.search(r'title: ("|`)(.*?)("|`),', entry).group(2)),
    datetime.strptime(re.search(r'date: writeDate\((.*?)\),', entry).group(1), '%Y, %m, %d'))
    for entry in entries
]
entries.reverse()


rss = ET.Element("rss", {
    "version": "2.0",
    "xmlns:atom": "http://www.w3.org/2005/Atom"
})
ET.register_namespace("atom", "http://www.w3.org/2005/Atom")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "atom:link", {
    "href": "https://033boot.github.io/iwbtwr-rss/rss.xml",
    "rel": "self",
    "type": "application/rss+xml"
})
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
