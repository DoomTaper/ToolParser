"""
This is just a sample of algorithm which I am going to use to parse Hoppy result data from the file 
*.spider or *.attack.Later this algorithm will parsed_output used and a module is made out of it which will 
parsed_output directly used in the hoppy parser file.
Currently parsed_output is the required output of below form:
parsed_output {request:"all the requests", response':{'status_code':all status_codes, 
											'headers':all response headers,
											'data':all responses data} }
"""

import re
#print dir(netliparsed_output.http.http1.read)
rfi = open("/root/Desktop/hoppy.attack", 'r')
data = rfi.read()
rfi.close()
pattern = re.compile(r"(GET /.*?)\n(?=\n\t\D{3} Parsed Response:)", re.S)
output = pattern.findall(data)
#print output
req_filename = "req.txt"
req_file_address = "/root/Desktop/"+req_filename
res_filename = "res.txt"
res_file_address = "/root/Desktop/"+res_filename
length = len(output)
parsed_output = [0]*length
for i in range(length):
	req_pattern = re.compile(r"(GET /.*?)\n(?=Server)", re.S)
	request = req_pattern.search(output[i])
	request = request.group().strip()+'\n\n'
	res_pattern = re.compile(r"(?<=Responded:\n\n)(.*)", re.S)
	response = res_pattern.search(output[i])
	response = response.group()+'\n\n'
	res_status_code_pattern = re.compile(r"(?<=HTTP/\w.\w )(.*)")
	res_status_code = res_status_code_pattern.search(response)
	res_status_code = res_status_code.group().strip()+'\n\n'
	res_parse_pattern = re.compile(r"(?P<headers>HTTP.*?)\n(?=\r\n)(?P<data>.*)", re.S)
	res_parse = res_parse_pattern.search(response)
	res_headers = res_parse.group('headers').strip()+'\n\n'
	res_data = res_parse.group('data').strip()+'\n\n'
	parsed_output[i] = {'request':request, 'response':{'status_code':res_status_code, 
											'headers':res_headers,
											'data':res_data 
											}
			}
print parsed_output[1]['request']
print parsed_output[1]['response']['status_code']
print parsed_output[1]['response']['headers']
print parsed_output[1]['response']['data']
for i in range(length):
	req_file = open(req_file_address, 'a')
	req_file.write(parsed_output[i]['request'])
	req_file.close()
	res_file = open(res_file_address, 'a')
	res_file.write(parsed_output[i]['response']['status_code'])
	res_file.write(parsed_output[i]['response']['headers'])
	res_file.write(parsed_output[i]['response']['data'])
	res_file.close()

#r"(?<=HTTP/\w.\w )(.*)"
