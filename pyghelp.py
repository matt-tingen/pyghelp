# Copyright (c) 2012 Matt Tingen

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pygame


pygame.font.init()
DEBUG_FONT = pygame.font.Font(None, 22)


def load_file_or_surface(obj):
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
        elif len(obj) not in [3, 4]:
            raise ValueError('Object does not represent a color')
        else:
            return obj


def draw_fps(surface, clock, anchor='topright', color='red'):
    """ Draws an FPS counter on a surface at the given anchor.
    """
    fps_surface = DEBUG_FONT.render(str(int(clock.get_fps())), True, get_color(color))
    blit_anchors(surface, anchor, fps_surface, anchor)
