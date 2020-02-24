from models import Photo, Slide, Transition

filenames = [
    'examples/a_example.txt',
]


def build_photo(id, line):
    elements = line.split()

    orientation = elements[0]
    tags = set(elements[2:2+int(elements[1])])

    return Photo(id=id, orientation=orientation, tags=tags)


def _build_horizontal_slides(photos):
    slides = set()

    for photo in photos:
        slides.add(Slide(photo))

    return slides


def _build_vertical_slides(photos):
    slides = set()
    idx = 0
    photos = list(photos)
    while idx < len(photos):
        idx2 = idx + 1
        while idx2 < len(photos):
            slides.add(Slide(photo1=photos[idx], photo2=photos[idx2]))
            idx2 += 1
        idx += 1

    return slides


def build_slides(photo_set):

    horizontal_photos = {photo for photo in photo_set if photo.orientation == 'H'}
    vertical_photos = {photo for photo in photo_set if photo.orientation == 'V'}

    slides = _build_horizontal_slides(horizontal_photos)
    slides = slides | _build_vertical_slides(vertical_photos)

    return slides


def build_transitions(slides):
    transitions = set()
    idx = 0
    slides = list(slides)

    while idx < len(slides):
        idx2 = idx + 1
        while idx2 < len(slides):
            transitions.add(Transition(slide1=slides[idx], slide2=slides[idx2]))
            idx2 += 1
        idx += 1

    return transitions


def _get_max_transition(transitions, slide=None):
    max_transition = None
    max_points = -1

    for transition in transitions:
        if transition.can_use(slide) and transition.points > max_points:
            max_transition = transition
            max_points = transition.points

    return max_transition, max_points


def _calculate_points(slide, transitions):

    points = 0
    for transition in transitions:
        if slide == transition.slide1 or slide == transition.slide2:
            points += transition.points

    return points


def _get_slide_points(slides, transitions):
    idx = 0
    points = list()
    while idx < len(slides):
        slide_points = _calculate_points(slide=slides[idx], transitions=transitions)
        points.append(slide_points)
        idx += 1

    return points


def _get_idx_max(points):
    max_value = max(points)
    return points.index(max_value)


def _add_slide(slideshow, element):
    if isinstance(element, Slide):
        slide = element
    elif isinstance(element, Transition):
        slide = element.slide1
        if not slide.can_use():
            slide = element.slide2

    slide.use()
    slideshow.append(slide)
    return slideshow


def get_slideshow(transitions, slides):
    slideshow = list()
    slides = list(slides)
    slides_points = _get_slide_points(slides=slides, transitions=transitions)
    max_idx = _get_idx_max(slides_points)
    slide = slides[max_idx]

    slideshow =_add_slide(slideshow, slide)

    # put into loop
    transition, points = _get_max_transition(transitions, slide)
    slideshow = _add_slide(slideshow, transition)

    return (slideshow, points)


if __name__ == '__main__':

    total = 0
    for filename in filenames:

        with open(filename, 'r') as file:
            lines = file.readlines()

        photo_set = set()
        id = 0
        for line in lines[1:]:
            photo = build_photo(id=id, line=line)
            photo_set.add(photo)
            id += 1

        slides = build_slides(photo_set)
        transitions = build_transitions(slides)

        slideshow, points = get_slideshow(transitions=transitions, slides=slides)

        print('slideshow: ' + str(slideshow))
        print(filename + ': ' + str(points))
        total += points

    print('Total: ' + str(total))

