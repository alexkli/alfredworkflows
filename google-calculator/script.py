import httplib
import urllib
import json
import re
from xml.dom.minidom import Document

q = "{query}"
params = urllib.urlencode({"q": q})
conn = httplib.HTTPConnection("www.google.com", 80)
conn.request("GET", "/ig/calculator?hl=en&amp;"+params)
response = conn.getresponse()
data = response.read()
conn.close()

data = re.sub(r"{\s*(\w)", r'{"\1', data)
data = re.sub(r",\s*(\w)", r',"\1', data)
data = re.sub(r"(\w):", r'\1":', data)

dataobj = json.loads(data)
doc = Document()
items = doc.createElement("items")
xmlitem = doc.createElement("item")
if dataobj["error"] == "":
	output = dataobj["lhs"] + " = " + dataobj["rhs"]
else:
	output = "Error"
xmlitem.setAttribute("uid", dataobj["lhs"])
xmlitem.setAttribute("arg", dataobj["rhs"])
xmlitem.setAttribute("valid", "YES")
attr = doc.createElement("title")
attr.appendChild(doc.createTextNode(output))
xmlitem.appendChild(attr)
attr = doc.createElement("subtitle")
attr.appendChild(doc.createTextNode(q))
xmlitem.appendChild(attr)
attr = doc.createElement("icon")
attr.appendChild(doc.createTextNode("icon.png"))
xmlitem.appendChild(attr)
items.appendChild(xmlitem)

doc.appendChild(items)
print unicode(doc.toxml()).encode("utf-8")