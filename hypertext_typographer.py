# coding: utf-8
'''
Provides a highlighter for potentially invalid web typography.

Config summary (see README.md for details):

    # key binding
    { "keys": ["ctrl+shift+t"], "command": "delete_hypertext_typographer" }

    # file settings
    {
      "hypertext_typographer_highlight_color": "invalid",
      "hypertext_typographer_file_max_size": 1000
    }

@author: Jean-Denis Vauguet <jd@vauguet.fr>, Oktay Acikalin <ok@ryotic.de>, Geoff Stokes <geoff@geoffstokes.net>
@license: MIT (http://www.opensource.org/licenses/mit-license.php)
@since: 2011-02-25
'''

import sublime
import sublime_plugin

DEFAULT_MAX_FILE_SIZE = 1048576
DEFAULT_COLOR_SCOPE_NAME = "invalid"
DEFAULT_IS_ENABLED = True

DEFAULT_REPLACEMENTS = {
    # Typographers' Quotes
    u"“": "\"",
    u"”": "\"",
    u"‘": "'",
    u"’": "'",
    # Ellipses and dashes
    u"…": "...",
    u"‒": "-",
    u"–": "-",
    u"—": "-",
    u"―": "-",
    # Fractions
    u"½": "1/2",
    u"¼": "1/4",
    u"¾": "3/4"
}

#Set whether the plugin is on or off
ht_settings = sublime.load_settings('hypertext_typographer.sublime-settings')
hypertext_typographer_enabled = bool(ht_settings.get('hypertext_typographer_enabled', DEFAULT_IS_ENABLED))
replacements = dict((unicode(key, 'utf-8'), value) for (key, value) in ht_settings.get('hypertext_typographer_replacements', DEFAULT_REPLACEMENTS).items())

# Determine if the view is a find results view
def is_find_results(view):
    return view.settings().get('syntax') and "Find Results" in view.settings().get('syntax')

def is_hypertext_type(view):
    return (view.settings().get('syntax') and ("HTML" in view.settings().get('syntax') or "XML" in view.settings().get('syntax')) or view.file_name() != None and "aspx" in view.file_name())

# Return an array of regions matching problematic characters.
def find_problem_characters(view):
    return view.find_all(u'[%s]' % "".join(replacements.keys()))

# Highlight problematic characters
def highlight_problem_characters(view):
    max_size = ht_settings.get('hypertext_typographer_file_max_size', DEFAULT_MAX_FILE_SIZE)
    color_scope_name = ht_settings.get('hypertext_typographer_highlight_color', DEFAULT_COLOR_SCOPE_NAME)
    if view.size() <= max_size and is_hypertext_type(view) and not is_find_results(view):
        regions = find_problem_characters(view)
        view.add_regions('HypertextTypographerHighlightListener', regions, color_scope_name, sublime.DRAW_EMPTY)


# Clear all highlights
def highlight_clear(window):
    for view in window.views():
        view.erase_regions('HypertextTypographerHighlightListener')

# --- Event Listeners ---

# Highlight matching regions.
class HypertextTypographerHighlightListener(sublime_plugin.EventListener):
    def on_modified(self, view):
        if hypertext_typographer_enabled:
            highlight_problem_characters(view)

    def on_activated(self, view):
        if hypertext_typographer_enabled:
            highlight_problem_characters(view)

    def on_load(self, view):
        if hypertext_typographer_enabled:
            highlight_problem_characters(view)

# --- Commands ---

# Toggle the event listner on or off
class ToggleTypographyHighlightCommand(sublime_plugin.WindowCommand):
    def run(self):
        global hypertext_typographer_enabled
        hypertext_typographer_enabled = False if hypertext_typographer_enabled else True

        # If toggling on, go ahead and perform a pass,
        # else clear the highlighting in all views
        if hypertext_typographer_enabled:
            highlight_problem_characters(self.window.active_view())
        else:
            highlight_clear(self.window)


# Either Replace matching regions with plain replacements or HTML Escape matching regions.
class EscapeTypographyCommand(sublime_plugin.TextCommand):
    def run(self, edit, mode="replace"):
        global replacements
        regions = find_problem_characters(self.view)
        if regions:
            # replacing a region changes the other regions positions, so we
            # handle this maintaining an offset
            offset = 0
            for region in regions:
                r = sublime.Region(region.a + offset, region.b + offset)
                t = self.view.substr(r)
                tr = t
                if mode == "escape":
                    tr = t.encode('ascii','xmlcharrefreplace')
                elif mode == "replace":
                    tr = "".join(replacements.get(c,c) for c in t)
                self.view.replace(edit, r, tr)
                offset += len(tr) - r.size()

            msg_parts = {"nbRegions": len(regions),
                         "plural":    's' if len(regions) > 1 else ''}
            msg = "Escaped %(nbRegions)s special character%(plural)s" % msg_parts
        else:
            msg = "No special characters to escape!"

        sublime.status_message(msg)
