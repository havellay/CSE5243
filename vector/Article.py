from Tag import Tag

class Article:
    def __init__(self, x=None):
        self.id     = x                 # an 'id' is actually not needed at all

        self.tags   = {}                # a dictionary containing all the tags
                                        # in an article

    def take_this_tag(
            self, tag_name=None, tag_text=None, tag_monograms=None,
            tag_bigrams=None, tag_trigrams=None,
            tag_topiclist=None, tag_placelist=None,
        ):
        self.tags[tag_name] = Tag(
                name=tag_name,
                text=tag_text,
                monograms=tag_monograms,
                bigrams=tag_bigrams,
                trigrams=tag_trigrams, 
                topiclist=tag_topiclist,
                placelist=tag_placelist,
            )
        # should we make sure whether there is already a tag with this name? It
        # could become an issue for tags such as <D> of which there might
        # already be a copy
