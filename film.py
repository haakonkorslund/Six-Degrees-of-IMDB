class Film:
    def __init__(self, id, name, rate, votes) -> None:
        self.id = id
        self.name = name
        self.rate = rate
        self.votes = votes
        self.nodes = []
