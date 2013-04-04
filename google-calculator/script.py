import sys
import urllib
import urllib2
import yaml
from xml.sax.saxutils import escape

xml_tpl = '''<?xml version="1.0"?>
<items>
  <item uid="%(uid)s" arg="%(arg)s" valid="YES">
    <title>%(title)s</title>
    <subtitle>%(subtitle)s</subtitle>
    <icon>icon.png</icon>
  </item>
</items>'''

def xml(uid, arg, title, subtitle=""):
    return xml_tpl % ({"uid": escape(uid), "arg": escape(arg), "title": title, "subtitle": subtitle})
    

try:
    q = "{query}"
    if len(sys.argv) > 1:
        q = sys.argv[1]
    
    params = urllib.urlencode({"q": q})
    # faking browser user agent necessary to get back utf-8 encoding
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    request = urllib2.Request("http://www.google.com/ig/calculator?hl=en&" + params, None, headers)
    response = urllib2.urlopen(request).read()
    response = response.decode("utf-8")
    # replace magic thousand delimiter char
    response = response.replace(u"\u00A0", ".")
    
    data = yaml.load(response)
    
    error = data["error"]
    exp = data["lhs"]
    result = data["rhs"]
    
    title = q
    if error == "":
        result = result.replace("<sup>", "^").replace("</sup>", "")
        title = result
        subtitle = exp + " = " + result
    else:
        try:
            errorcode = int(error)
        except:
            errorcode = -1
        
        if errorcode == -1:
            #subtitle = "Oh, Google says: " + error
            subtitle = "..."
        elif errorcode == 0:
            subtitle = q
            #subtitle = "Please complete expression..."
        elif errorcode == 4:
            subtitle = "..."
            #subtitle = "Sorry, cannot calculate that..."
        else:
            subtitle = "Google reported error code " + str(errorcode)

    print xml("calc {query}", result, title, subtitle)

except BaseException, e:
    print xml("calc {query}", "error", title, "Unexpected error", str(e))
