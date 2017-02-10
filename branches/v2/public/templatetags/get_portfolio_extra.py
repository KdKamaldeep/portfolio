from django import template
from hitcount.models import HitCount
from portfolio.models import relProjectPortfolio
register = template.Library()

@register.simple_tag
def get_portfolio_public_url(portfolio, request):
    protocol = 'http'
    if request.is_secure():
        protocol = 'https'

    url = '{2}://{0}/public/portfolio/{1}'.format(request.META['HTTP_HOST'],
                                                  portfolio.uuid, protocol)
    return url

@register.simple_tag
def get_portfolio_views(portfolio):
   return  HitCount.objects.get_for_object(portfolio).hits

@register.simple_tag
def get_portfolio_projects(portfolio):
    projects = relProjectPortfolio.objects.filter(portfolio__id=portfolio.id)
    return len(projects)

