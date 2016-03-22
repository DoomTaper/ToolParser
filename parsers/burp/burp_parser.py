"""
This is just a sample algorithm which will parse the burp saved data into required fields
Currently it writes output to a file.
"""

from lxml import etree
import re

base64 = True # In burp by default it is true
tree = etree.parse("./sample2.xml")
xml_data = etree.tostring(tree.getroot())
xml_tree = etree.fromstring(xml_data)

response = xml_tree.find('.//response')
if not response.attrib['base64']:
	base64 = False

request = xml_tree.findall('.//request')
request = [g.text for g in request]
if base64:
	request = [g.decode('base64') for g in request]

responses = xml_tree.findall('.//response')
responses = [g.text for g in responses]
if base64:
	responses = [g.decode('base64') for g in responses]

length = len(responses)
responses_headers = []
responses_body = []
for response in responses:
	pattern = re.compile(r"(?P<headers>HTTP.*?)\n(?=\r\n)(?P<data>.*)", re.S) #copied from hoppy parser :D
	parse = pattern.search(response)
	responses_headers.append(parse.group('headers'))
	responses_body.append(parse.group('data'))

status = xml_tree.findall('.//status')
status = [g.text for g in status]

file = open('./output.txt', 'a')
for i in range(length):
	file.write('request\t'+str(request[i])+'\n\n'+'response_headers\t'+str(responses_headers[i])
			+'\n\n'+'response_body\t'+str(responses_body[i]+'\n\n')
		)

file.close()







