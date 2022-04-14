from django.views import View
from django.http import HttpResponse

from price.domain import new_batch

class PriceView(View):
    def new_cron_batch(self):
        new_batch()
        return HttpResponse('')

    