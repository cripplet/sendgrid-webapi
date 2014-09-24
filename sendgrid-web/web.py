import requests

class SendGridWebAPIClient(object):
	def __init__(self, username, password):
		self.username = username
		self.password = password

	def _build_req(self, module, action, format, method, data={}):
		url = 'https://api.sendgrid.com/api/' + '.'.join([module, action, format])
		data['api_user'] = self.username
		data['api_key'] = self.password
		if(method == 'GET'):
			dstr = '&'.join([k + '=' + v for k, v in data.iteritems()])
			r = requests.get(url + '?' + dstr)
		else:
			r = requests.post(url, data=data)
		return(r.status_code, r.json())
