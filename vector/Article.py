from Tag import Tag

class Article:
    def __init__(self, x):
        self.id     = x                 # an 'id' is actually not needed at all

        self.tags   = {}                # a dictionary containing all the tags
                                        # in an article

    def take_this_tag(self, tag_name, tag_text, tag_tokens):
        self.tags[tag_name] = Tag(tag_name, tag_text, tag_tokens)
        # should we make sure whether there is already a tag with this name? It
        # could become an issue for tags such as <D> of which there might
        # already be a copy
