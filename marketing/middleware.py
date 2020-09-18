from .models import MarketingMessage


class DisplayMarketing():
	def __init__(self, next_layer=None):
		self.get_response = next_layer


	def process_request(self, request):
		# print(datetime.datetime.now())
		try:
			request.marketing_message = MarketingMessage.objects.get_featured_item().message
		except:
			request.marketing_message = False

	def process_response(self, request, response):
		# Do something with response, possibly using request.
		return response

	def __call__(self, request):
		response = self.process_request(request)
		if response is None:
			response = self.get_response(request)
		response = self.process_response(request, response)
		return response

