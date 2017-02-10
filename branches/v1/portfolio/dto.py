class portfoliodto():
    title = ""
    subtitle=""
    snapshot=""
    desc=""
    totalprojects = 0
    public=False
    id=0
    uuid=0
    url=""
    portfolioobj = None

    def __init__(self):
        self.title=""
        self.desc=""
        self.snapshot=""
        self.subtitle = ""
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
        dto.desc = portfolio.desc
        dto.snapshot = portfolio.snapshot
        dto.subtitle = portfolio.subtitle
        dto.public = portfolio.public
        dto.id = portfolio.id
        dto.uuid = portfolio.uuid
        return dto