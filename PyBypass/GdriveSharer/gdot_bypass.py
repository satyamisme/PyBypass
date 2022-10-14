import re
import base64
import requests 
from urllib.parse import urlparse, parse_qs

"""
credits: https://github.com/xcscxr/gdtot_scraper

regex: https?://(.+)\.gdtot\.(.+)\/\S+\/\S+

https://new.gdtot.cfd/file/374103862
https://new2.gdtot.sbs/file/105111102182

crypt_example: b0lDek5LSCt6ZjVRR2EwZnY4T1EvVndqeDRtbCtTWmMwcGNuKy8wYWpDaz0%3D
"""


def gdtot_bypass(url : str, crypt: str) -> str:
	
	url = url[:-1] if url[-1] == '/' else url	
	client  = requests.Session()
	match = re.findall(r"https?://(.+)\.gdtot\.(.+)\/\S+\/\S+", url)[0]
	client.cookies.update({ "crypt": crypt})
	
	
	response = client.get(url)
	response = client.get(f"https://{match[0]}.gdtot.{match[1]}/dld?id={url.split('/')[-1]}")
	
	url = re.findall(r'URL=(.*?)"', response.text)[0]
	params = parse_qs(urlparse(url).query)	
	
	if "gd" not in params or not params["gd"] or params["gd"][0] == "false":
		return "Something went wrong. Could not generate GDrive URL for your GDTot Link"
	else:
	       try: decoded_id = base64.b64decode(str(params["gd"][0])).decode("utf-8")    
	       except : return  "Something went wrong. Could not generate GDrive URL for your GDTot Link"
	       
	       drive_link = f"https://drive.google.com/open?id={decoded_id}"
	       return drive_link
	       


