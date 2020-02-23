class Photo(object):

    def __init__(self, orientation, tags):
        self.orientation = orientation
        self.tags = tags
        self.used = False

    def tag_numbers(self):
        return len(self.tags)

    def use(self):
        self.used = True

    def is_used(self):
        return self.used

    def __repr__(self):
        return self.orientation + ' ' + str(self.tags) + ' ' + str(self.is_used())


class Slide(object):

    def __init__(self, photo1: Photo, photo2: Photo = None):
        if photo2 and 'H' in [photo1.orientation, photo2.orientation]:
            raise Exception("This shouldn't occurs")

        self.photo1 = photo1
        self.photo2 = photo2
        self.tags = photo1.tags

        if photo2:
            self.tags = self.tags | photo2.tags

    def use(self):
        self.photo1.use()

        if self.photo2:
            self.photo2.use()

    def can_use(self):
        return not self.photo1.is_used() and (not self.photo2 or not self.photo2.is_used())

    def __repr__(self):
        return '\n<Photo1: ' + str(self.photo1) + '; Photo2: ' + str(self.photo2) + '; TAGS: ' + str(self.tags) + '>'


class Transition(object):

    def __init__(self, slide1: Slide, slide2: Slide):
        self.slide1 = slide1
        self.slide2 = slide2

    def points(self):
        common = Transition._get_common_points(self.slide1.tags, self.slide2.tags)
        first = Transition._get_exclusion_points(self.slide1.tags, self.slide2.tags)
        second = Transition._get_common_points(self.slide2.tags, self.slide1.tags)

        return min([common, first, second])

    def can_use(self):
        return self.slide1.can_use() and self.slide2.can_use()

    def use(self):
        self.slide1.use()
        self.slide2.use()

    def contains(self, slide):
        return not slide or self.slide1 == slide or self.slide2 == slide

    @staticmethod
    def _get_common_points(set1, set2):
        return len(set1 & set2)

    @staticmethod
    def _get_exclusion_points(set1, set2):
        return len(set1 - set2)

    def __repr__(self):
        return '\n\n[Slide1: ' + str(self.slide1) + ';\nSlide2: ' + str(self.slide2) + ';\nPOINTS: ' + str(self.points()) + ']'
