from models import Photo, Slide, Transition

filenames = [
    'examples/a_example.txt',
    # 'examples/b_lovely_landscapes.txt',
    # 'examples/c_memorable_moments.txt',
    # 'examples/d_pet_pictures.txt',
    # 'examples/e_shiny_selfies.txt',
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


def _has_common_tags(slide1, slide2):
    return len(slide1.tags & slide2.tags) > 0


def build_transitions(slides):
    transitions = set()
    idx = 0
    slides = list(slides)

    while idx < len(slides):
        idx2 = idx + 1
        while idx2 < len(slides):
            if _has_common_tags(slide1=slides[idx], slide2=slides[idx2]):
                transitions.add(Transition(slide1=slides[idx], slide2=slides[idx2]))
            idx2 += 1
        idx += 1

    return transitions


def _get_max_transition(transitions, slide):
    max_transition = None
    max_points = 0

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
    return slideshow, slide


def get_slideshow(transitions, slides):
    slideshow = list()
    slides = list(slides)

    slides_points = _get_slide_points(slides=slides, transitions=transitions)
    max_idx = _get_idx_max(slides_points)
    slide = slides[max_idx]

    slideshow, slide =_add_slide(slideshow, slide)
    transition, total = _get_max_transition(transitions, slide)

    while transition:
        slideshow, slide = _add_slide(slideshow, transition)
        transition, points = _get_max_transition(transitions, slide)

        total += points

    return slideshow, total


def write_output(filename, slideshow):
    output = str(len(slideshow))

    for slide in slideshow:
        output += '\n' + str(slide.photo1.id)

        if slide.photo2:
            output += ' ' + str(slide.photo2.id)

    with open(filename[:-4] + 'output.txt', 'w') as file:
        file.write(output)


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

        write_output(filename=filename, slideshow=slideshow)

        total += points

    print('Total: ' + str(total))

