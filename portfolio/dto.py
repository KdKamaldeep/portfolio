class portfoliodto():
    title = ""
    subtitle=""

    portfolio_url=""
    portfolio_host = ""
    totalprojects = 0
    public=False
    id=0
    uuid=0
    url=""
    portfolioobj = None

    def __init__(self):
        self.title=""

        self.portfolio_url = ""
        self.portfolio_host = ""
        self.totalprojects = 0
        self.public = False
        self.id = 0
        self.uuid = 0
        self.url = ""
        self.portfolioobj = None
        self.hitcount = 0


    def copy(self, portfolio):
        dto = portfoliodto()
        dto.portfolioobj = portfolio
        dto.title = portfolio.title
        dto.portfolio_url =  portfolio.portfolio_url
        dto.portfolio_host =  portfolio.portfolio_host

        dto.public = portfolio.public
        dto.id = portfolio.id
        dto.uuid = portfolio.uuid
        return dto