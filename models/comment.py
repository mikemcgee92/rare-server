class Comment:
    """Database model for comments"""

    def __init__(self, id, author_id, post_id, content):
        self.id = id
        self.author_id = author_id
        self.post_id = post_id
        self.content = content
