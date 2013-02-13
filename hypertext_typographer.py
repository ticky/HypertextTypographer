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

#Set whether the plugin is on or off
ts_settings = sublime.load_settings('hypertext_typographer.sublime-settings')
hypertext_typographer_enabled = bool(ts_settings.get('hypertext_typographer_enabled', DEFAULT_IS_ENABLED))

# Determine if the view is a find results view
def is_find_results(view):
    return view.settings().get('syntax') and "Find Results" in view.settings().get('syntax')

def is_hypertext_type(view):
    return (view.settings().get('syntax') and ("HTML" in view.settings().get('syntax') or "XML" in view.settings().get('syntax')) or view.file_name() != None and "aspx" in view.file_name())

# Return an array of regions matching trailing spaces.
def find_hypertext_typographer(view):
    return view.find_all(u'[“”‘’…‒–—―½¼¾]')


# Highlight trailing spaces
def highlight_hypertext_typographer(view):
    max_size = ts_settings.get('hypertext_typographer_file_max_size', DEFAULT_MAX_FILE_SIZE)
    color_scope_name = ts_settings.get('hypertext_typographer_highlight_color', DEFAULT_COLOR_SCOPE_NAME)
    if view.size() <= max_size and is_hypertext_type(view) and not is_find_results(view):
        regions = find_hypertext_typographer(view)
        view.add_regions('HypertextTypographerHighlightListener', regions, color_scope_name, sublime.DRAW_EMPTY)


# Clear all trailing spaces
def clear_hypertext_typographer_highlight(window):
    for view in window.views():
        view.erase_regions('HypertextTypographerHighlightListener')


# Toggle the event listner on or off
class ToggleTypographyHighlightCommand(sublime_plugin.WindowCommand):
    def run(self):
        global hypertext_typographer_enabled
        hypertext_typographer_enabled = False if hypertext_typographer_enabled else True

        # If toggling on, go ahead and perform a pass,
        # else clear the highlighting in all views
        if hypertext_typographer_enabled:
            highlight_hypertext_typographer(self.window.active_view())
        else:
            clear_hypertext_typographer_highlight(self.window)


# Highlight matching regions.
class HypertextTypographerHighlightListener(sublime_plugin.EventListener):
    def on_modified(self, view):
        if hypertext_typographer_enabled:
            highlight_hypertext_typographer(view)

    def on_activated(self, view):
        if hypertext_typographer_enabled:
            highlight_hypertext_typographer(view)

    def on_load(self, view):
        if hypertext_typographer_enabled:
            highlight_hypertext_typographer(view)


 # Replace matching regions. Method depends on configuration.
 class ReplaceTypographyCommand(sublime_plugin.TextCommand):
     def run(self, edit):
         regions = find_hypertext_typographer(self.view)
         if regions:
             # deleting a region changes the other regions positions, so we
             # handle this maintaining an offset
             offset = 0
             for region in regions:
                 r = sublime.Region(region.a + offset, region.b + offset)
                 self.view.erase(edit, sublime.Region(r.a, r.b))
                 offset -= r.size()

             msg_parts = {"nbRegions": len(regions),
                          "plural":    's' if len(regions) > 1 else ''}
             msg = "Replaced %(nbRegions)s special character%(plural)s" % msg_parts
         else:
             msg = "No special characters to replace!"

         sublime.status_message(msg)
