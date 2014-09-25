import requests

# cf. https://sendgrid.com/docs/API_Reference/Web_API/index.html

class SendGridWebAPIClient(object):
	def __init__(self, username, password):
		self.username = username
		self.password = password

	def _execute_req(self, module, action, format, method, data):
		if(module != 'credentials'):
			url = 'https://api.sendgrid.com/api/%s.%s.%s' % (module, action, format)
		else:
			url = 'https://api.sendgrid.com/api/%s/%s.%s' % (module, action, format)
		data['api_user'] = self.username
		data['api_key'] = self.password
		if(method == 'GET'):
			dstr = '&'.join([k + '=' + v for k, v in data.iteritems()])
			r = requests.get(url + '?' + dstr)
		else:
			r = requests.post(url, data=data)
		if(format == 'json'):
			return(r.status_code, r.json())
		return(r.status_code, r)

	def send(self, req, format='json'):
		return(self._execute_req(req.module, req.action, format, req.method, req.args))

class WebAPIRequest(object):
	def __init__(self, **kwargs):
		self.module = ''
		self.action = ''
		self.method = ''
		self.args = {}
		self.__dict__.update(kwargs)

	def set_data(self, action, method, **kwargs):
		self.action = action
		self.method = method
		self.args = kwargs
		return(self)

	@staticmethod
	def flatten(key, args):
		if(key in args.keys()):
			args[key] = '&'.join(key + '[]=' + x for x in args[key])
		else:
			args[key] = ''
		return(args)

class Blocks(WebAPIRequest):
	def __init__(self, **kwargs):
		super(Blocks, self).__init__(module='blocks', **kwargs)

	def get(self, **kwargs):
		return(self.set_data('get', 'GET', **kwargs))

	def delete(self, **kwargs):
		return(self.set_data('delete', 'POST', **kwargs))

	def count(self, **kwargs):
		return(self.set_data('count', 'GET', **kwargs))


class Bounces(WebAPIRequest):
	def __init__(self, **kwargs):
		super(Bounces, self).__init__(module='bounces', **kwargs)

	def get(self, **kwargs):
		return(self.set_data('get', 'GET', **kwargs))

	def delete(self, **kwargs):
		return(self.set_data('delete', 'POST', **kwargs))

	def count(self, **kwargs):
		return(self.set_data('count', 'GET', **kwargs))

class FilterCommands(WebAPIRequest):
	def __init__(self, **kwargs):
		super(FilterCommands, self).__init__(module='filter', **kwargs)

	def get_available(self, **kwargs):
		return(self.set_data('getavailable', 'GET', **kwargs))

	def activate_app(self, **kwargs):
		return(self.set_data('activate', 'POST', **kwargs))

	def deactivate_app(self, **kwargs):
		return(self.set_data('deactivate', 'POST', **kwargs))

	def setup_app(self, **kwargs):
		return(self.set_data('setup', 'POST', **kwargs))

	def get_app_settings(self, **kwargs):
		return(self.set_data('getsettings', 'GET', **kwargs))

class FilterSettings(WebAPIRequest):
	def __init__(self, **kwargs):
		super(FilterSettings, self).__init__(module='filter', **kwargs)

	def address_whitelist(self, **kwargs):
		kwargs = WebAPIRequest.flatten('list', kwargs)
		return(self.set_data('setup', 'POST', **kwargs))

	def bcc(self, **kwargs):
		return(self.set_data('setup', 'POST', **kwargs))
	# ... and the rest -- NOT IMPLEMENTED

class InvalidEmails(WebAPIRequest):
	def __init__(self, **kwargs):
		super(InvalidEmails, self).__init__(module='invalidemails', **kwargs)

	def get(self, **kwargs):
		return(self.set_data('get', 'GET', **kwargs))

	def count(self, **kwargs):
		return(self.set_data('count', 'GET', **kwargs))

	def delete(self, **kwargs):
		return(self.set_data('delete', 'POST', **kwargs))

# should in general use the provided python lib
class Mail(WebAPIRequest):
	def __init__(self, **kwargs):
		super(Mail, self).__init__(module='mail', **kwargs)

	def send(self, **kwargs):
		kwargs = WebAPIRequest.flatten('to', kwargs)
		kwargs = WebAPIRequest.flatten('toname', kwargs)
		kwargs = WebAPIRequest.flatten('cc', kwargs)
		kwargs = WebAPIRequest.flatten('bcc', kwargs)
		# am NOT formatting files, headers, etc.
		return(self.set_data('send', 'POST', kwargs))

class MultipleCredentials(WebAPIRequest):
	def __init__(self, **kwargs):
		super(MultipleCredentials, self).__init__(module='credentials')

	def get(self, **kwargs):
		return(self.set_data('get', 'GET', kwargs))

	def add(self, **kwargs):
		return(self.set_data('add', 'POST', kwargs))

	def edit(self, **kwargs):
		return(self.set_data('edit', 'POST', kwargs))

	def delete(self, **kwargs):
		return(self.set_data('remove', 'POST', kwargs))

class ParseWebhookSettings(WebAPIRequest):
	def __init__(self, **kwargs):
		super(ParseWebhookSettings, self).__init__(module='parse', **kwargs)

	def get(self, **kwargs):
		return(self.set_data('get', 'GET', kwargs))

	def set(self, **kwargs):
		return(self.set_data('set', 'POST', kwargs))

	def delete(self, **kwargs):
		return(self.set_data('delete', 'POST', kwargs))

class Profile(WebAPIRequest):
	def __init__(self, **kwargs):
		super(Profile, self).__init__(module='profile', **kwargs)

	def get(self, **kwargs):
		return(self.set_data('get', 'GET', kwargs))

	def set(self, **kwargs):
		return(self.set_data('set', 'POST', kwargs))

	def set_password(self, **kwargs):
		self.module = 'password'
		r = self.set_data('set', 'POST', kwargs)
		self.module = 'profile'
		return(r)

	def set_username(self, **kwargs):
		return(self.set_data('setUsername', 'POST', kwargs))

	def set_email(self, **kwargs):
		return(self.set_data('setEmail', 'POST', kwargs))

	def delete(self, **kwargs):
		return(self.set_data('delete', 'POST', kwargs))

class SpamReports(WebAPIRequest):
	def __init__(self, **kwargs):
		super(SpamReports, self).__init__(module='spamreports', **kwargs)

	def get(self, **kwargs):
		return(self.set_data('get', 'GET', **kwargs))

	def count(self, **kwargs):
		return(self.set_data('count', 'POST', **kwargs))

	def delete(self, **kwargs):
		return(self.set_data('delete', 'POST', **kwargs))

class Unsubscribes(WebAPIRequest):
	def __init__(self, **kwargs):
		super(Unsubscribes, self).__init__(module='unsubscribes', **kwargs)

	def get(self, **kwargs):
		return(self.set_data('get', 'GET', **kwargs))

	def add(self, **kwargs):
		return(self.set_data('add', 'POST', **kwargs))

	def delete(self, **kwargs):
		return(self.set_data('delete', 'POST', **kwargs))

class GeneralStatistics(WebAPIRequest):
	def __init__(self, **kwargs):
		super(GeneralStatistics, self).__init__(module='stats', **kwargs)

	def get(self, **kwargs):
		return(self.set_data('get', 'GET', **kwargs))

	def category_list(self, **kwargs):
		return(self.set_data('get', 'POST', list=True, **kwargs))

class AdvancedStatistics(WebAPIRequest):
	def __init__(self, **kwargs):
		super(AdvancedStatistics, self).__init__(module='stats', **kwargs)

	def get_advanced(self, **kwargs):
		return(self.set_data('getAdvanced', 'POST', **kwargs))


if __name__ == '__main__':
	u = 'foo'
	p = 'bar'
	c = SendGridWebAPIClient(username=u, password=p)
	(stat, resp) = c.send(Blocks().get(email='foo@bar.com'))
	assert(stat > 0)
	(stat, resp) = c.send(Bounces().get(email='foo@bar.com'))
	assert(stat > 0)
	(stat, resp) = c.send(FilterSettings().address_whitelist(name='foo', list=['minke.zhang@gmail.com', 'foo@bar.com']))
	assert(stat > 0)
	(stat, resp) = c.send(InvalidEmails().get())
	assert(stat > 0)
	(stat, resp) = c.send(GeneralStatistics().category_list())
	assert(stat > 0)
