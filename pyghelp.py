import pygame
import math


pygame.font.init()
DEBUG_FONT = pygame.font.Font(None, 22)


def get_surface(obj):
    """ Returns a Surface representing the parameter.

    if obj is the filename of an image, a surface containing the image will be returned.
    if obj is a Surface, it will be returned unchanged.
    """
    if isinstance(obj, pygame.Surface):
        return obj

    return pygame.image.load(obj)


def get_anchor(obj, anchor):
    """ Returns the point representing the anchor on the given Surface or Rect.

    obj can be a Surface or Rect.
    anchor should be a string of one of the point attributes (e.g. 'topleft', 
        'center', 'midbottom', etc.).
    """

    if anchor not in ['topleft', 'bottomleft', 'topright', 'bottomright',
                      'midtop', 'midleft', 'midbottom', 'midright', 'center']:
        raise ValueError('Invalid anchor')
        
    try:
        return getattr(obj.get_rect(), anchor)
    except AttributeError:
        return getattr(obj, anchor)


def blit_anchors(dest, dest_anchor, src, src_anchor):
    """ Blits the source onto the destination such that their anchors align.

    src_anchor and dest_anchor can be strings of one of the point attributes (topleft, center,
    midbottom, etc.) or a position on their respective surfaces (e.g [100, 200]).
    """
    try:
        src_anchor = get_anchor(src, src_anchor)
    except ValueError:
        pass # Assume src_anchor is already a point. If not, it will fail in the map().

    try:
        dest_anchor = get_anchor(dest, dest_anchor)
    except ValueError:
        pass # Assume dest_anchor is already a point. If not, it will fail in the map().

    topleft = map(lambda a,b,c: a - b + c, src.get_rect().topleft, src_anchor, dest_anchor)
    dest.blit(src, topleft)


def get_color(obj):
    """ Returns a Color object representing the parameter.
    """
    try:
        return pygame.Color(obj)
    except ValueError:
        if isinstance(obj, basestring): # Invalid color name
            raise
        elif len(obj) not in range(1, 5):
            raise ValueError('Object does not represent a color')
        else:
            return obj


def draw_fps(surface, clock, anchor='topright', color='red'):
    """ Draws an FPS counter on a surface at the given anchor.
    """
    fps_surface = DEBUG_FONT.render(str(int(clock.get_fps())), True, get_color(color))
    blit_anchors(surface, anchor, fps_surface, anchor)


def font_render_multiline(font, text, antialias, color, background=None, justify='left', line_spacing=0):
    """ Returns a Surface containing the text in the given font.

    The first five parameters are the ones used to render single line text.
    justify can be 'left', 'right', or 'center'.
    line_spacing is how much space to leave between lines in units of the font's height.
    """
    anchors = {'left':'topleft', 'right':'topright', 'center':'center'}

    lines = text.split('\n')

    width = max([font.size(line)[0] for line in lines])

    line_height = font.size('')[1]
    height = math.ceil(line_height * (len(lines) + line_spacing * (len(lines) - 1)))

    multiline = pygame.Surface((width, height))
    if background is not None:
        multiline.set_colorkey(background)
        multiline.fill(background)
    else:
        multiline.convert_alpha()
        multiline.fill([128, 128, 128, 0])

    anchor_x = getattr(multiline.get_rect(), justify)
    try:
        anchor_x = anchor_x[0]
    except:
        pass

    y = 0
    while len(lines):
        if background is None:
            line = font.render(lines.pop(0), antialias, color)
        else:
            line = font.render(lines.pop(0), antialias, color, background)

        dest_anchor = [anchor_x, int(y)]
        blit_anchors(multiline, dest_anchor, line, anchors[justify])

        y += (1 + line_spacing) * line_height

    return multiline


def offset(point, offset):
    """ Offsets a point by an amount.
    Equivalent to adding vectors.
    """
    return map(sum, zip(point, offset))


def rect_largest_fit(inner, outer):
    """ Moves and resizes a Rect to the largest it can be while still fitting in another Rect and maintaining its aspect ratio.
    """
    # TODO: check behavior when inner is larger than outer in one or both dimensions
    inner.topleft = outer.topleft

    w_ratio = outer.w / inner.w
    h_ratio = outer.h / inner.h

    if w_ratio < h_ratio:
        inner.w = outer.w
        inner.h *= w_ratio
    else:
        inner.h = outer.h
        inner.w *= h_ratio


class FloatRect(object):
    def __init__(self, topleft, size):
        self._left, self._top = map(float, topleft)
        self._width, self._height = map(float, size)
        self._half_height, self._half_width = [a / 2.0 for a in size]
        self._centerx = self._left + self._half_height
        self._centery = self._top + self._half_width
        self._right = self._left + self._width
        self._bottom = self._top + self._height

    def left():
        doc = "The left property."
        def fget(self):
            return self._left
        def fset(self, value):
            flt = float(value)
            self._right += flt - self._left
            self._left = flt
            self._centerx = flt + self._half_width
        def fdel(self):
            del self._left
        return locals()
    left = property(**left())

    def right():
        doc = "The right property."
        def fget(self):
            return self._right
        def fset(self, value):
            flt = float(value)
            self._left += flt - self._right
            self._right = flt
            self._centerx = self._left + self._half_width
        def fdel(self):
            del self._right
        return locals()
    right = property(**right())

    def top():
        doc = "The top property."
        def fget(self):
            return self._top
        def fset(self, value):
            flt = float(value)
            self._bottom += flt - self._top
            self._top = flt
            self._centery = flt + self._half_height
        def fdel(self):
            del self._top
        return locals()
    top = property(**top())

    def bottom():
        doc = "The bottom property."
        def fget(self):
            return self._bottom
        def fset(self, value):
            flt = float(value)
            self._top += flt - self._bottom
            self._bottom = flt
            self._centery = self._top + self._half_height
        def fdel(self):
            del self._bottom
        return locals()
    bottom = property(**bottom())

    def centerx():
        doc = "The centerx property."
        def fget(self):
            return self._centerx
        def fset(self, value):
            flt = float(value)
            self._left = flt - self._half_width
            self._right = flt + self._half_width
            self._centerx = flt
        def fdel(self):
            del self._centerx
        return locals()
    centerx = property(**centerx())

    def centery():
        doc = "The centery property."
        def fget(self):
            return self._centery
        def fset(self, value):
            flt = float(value)
            self._top = flt - self._half_height
            self._bottom = flt + self._half_height
            self._centery = flt
        def fdel(self):
            del self._centery
        return locals()
    centery = property(**centery())

    def width():
        doc = "The width property."
        def fget(self):
            return self._width
        def fset(self, value):
            flt = float(value)
            self._width = flt
            self._half_width = flt / 2
            self.centerx = self.centerx # Set left and right
        def fdel(self):
            del self._width
        return locals()
    w = width = property(**width())

    def height():
        doc = "The height property."
        def fget(self):
            return self._height
        def fset(self, value):
            flt = float(value)
            self._height = flt
            self._half_height = flt / 2
            self.centery = self.centery # Set top and bottom
        def fdel(self):
            del self._height
        return locals()
    h = height = property(**height())

    def size():
        doc = "The size property."
        def fget(self):
            return [self.width, self.height]
        def fset(self, value):
            self.width, self.height = value
        return locals()
    size = property(**size())

    def topleft():
        doc = "The topleft property."
        def fget(self):
            return [self.left, self.top]
        def fset(self, value):
            self.left, self.top = value
        return locals()
    topleft = property(**topleft())

    def bottomleft():
        doc = "The bottomleft property."
        def fget(self):
            return [self.left, self.bottom]
        def fset(self, value):
            self.left, self.bottom = value
        return locals()
    bottomleft = property(**bottomleft())

    def topright():
        doc = "The topright property."
        def fget(self):
            return [self.right, self.top]
        def fset(self, value):
            self.right, self.top = value
        return locals()
    topright = property(**topright())

    def bottomright():
        doc = "The bottomright property."
        def fget(self):
            return [self.right, self.bottom]
        def fset(self, value):
            self.right, self.bottom = value
        return locals()
    bottomright = property(**bottomright())

    def midtop():
        doc = "The midtop property."
        def fget(self):
            return [self.centerx, self.top]
        def fset(self, value):
            self.centerx, self.top = value
        return locals()
    midtop = property(**midtop())

    def midleft():
        doc = "The midleft property."
        def fget(self):
            return [self.left, self.centery]
        def fset(self, value):
            self.left, self.centery = value
        return locals()
    midleft = property(**midleft())

    def midbottom():
        doc = "The midbottom property."
        def fget(self):
            return [self.centerx, self.bottom]
        def fset(self, value):
            self.centerx, self.bottom = value
        return locals()
    midbottom = property(**midbottom())

    def midright():
        doc = "The midright property."
        def fget(self):
            return [self.right, self.centery]
        def fset(self, value):
            self.right, self.centery = value
        return locals()
    midright = property(**midright())

    def __repr__(self):
        return 'FloatRect(%s, %s)' % (str(self.bottomleft), str(self.size))


class RectDivider(object):
    """ Given a large Rect and a small one, allow iteration through non-overlapping locations of the small Rect
    """

    returned_start = False

    def __init__(self, outer, inner, direction='horizontal', horizontal='right', vertical='down', zigzag=False):
        """
        outer is the outer Rect.
        inner is the inner Rect and the first return value.
        direction is whether to move 'vertically' or 'horizontally' first.
        horizontal is whether to move 'left' or 'right' when moving horizontally.
        vertical is whether to move 'up' or 'down' when moving vertically.
        zigzag is whether to zigzag when reaching an edge rather than reset to the other side.
        """

        self.outer = outer.copy()
        self.inner = inner.copy()
        self.zigzag = zigzag

        # Resize self.outer so inner fits without any left over.
        # This makes zigzagging simpler.
        self.outer.w -= self.outer.w % self.inner.w
        self.outer.h -= self.outer.h % self.inner.h

        dir_err = ValueError('Invalid direction')
        if direction == 'vertical':
            self.d = 'v'
        elif direction == 'horizontal':
            self.d = 'h'
        else:
            raise dir_err
        if horizontal == 'left':
            self.h = -1
        elif horizontal == 'right':
            self.h = 1
        else:
            raise dir_err
        if vertical == 'up':
            self.v = -1
        elif vertical == 'down':
            self.v = 1
        else:
            raise dir_err

    def __iter__(self): return self

    def next(self):
        if not self.returned_start:
            self.returned_start = True
            return self.inner

        if self.d == 'h':
            self.inner.left += self.h * self.inner.w
            clamped = self.inner.clamp(self.outer)
            if clamped != self.inner:
                self.inner.top += self.v * self.inner.h
                if self.zigzag:
                    self.h *= -1
                if self.h == 1:
                    self.inner.left = self.outer.left
                else:
                    self.inner.right = self.outer.right
        else:
            self.inner.top += self.v * self.inner.h
            clamped = self.inner.clamp(self.outer)
            if clamped != self.inner:
                self.inner.left += self.h * self.inner.w
                if self.zigzag:
                    self.v *= -1
                if self.v == 1:
                    self.inner.top = self.outer.top
                else:
                    self.inner.bottom = self.outer.bottom

        clamped = self.inner.clamp(self.outer)
        if clamped != self.inner:
            raise StopIteration

        return self.inner
