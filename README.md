# Hypertext Typographer

For [Sublime Text 2](http://www.sublimetext.com/2).

**Highlight typographical errors in HTML and fix them in a flash.**

Copywriters and clients use Microsoft Word to compose copy for websites.
This is a sad but unavoidable fact of life. This Sublime Text 2 plugin is
intended to detect such errors in realtime, and allow easy replacement of the
most common special characters inserted by rich text editors.

The intent is not to function as a dumb html_escape function, nor is it to
replace or enhance the built-in HTML syntax error highlighting.
It is instead intended to stop only the frustrating and difficult to spot
typographical issues in their tracks.

## What is detected?

* "Smart" or "Typographers'" quotes (`“`, `”`, `‘`, `’`)
* Horizontal Ellipses (`…`)
* Dashes (`‒`, `–`, `—`, `―`)
* Fractions (`½`, `¼`, `¾`)

## Installation

Go to your `Packages` subdirectory under ST2's data directory:

* Windows: `%APPDATA%\Sublime Text 2`
* OS X: `~/Library/Application Support/Sublime Text 2/Packages`
* Linux: `~/.config/sublime-text-2`
* Portable Installation: `Sublime Text 2/Data`

Then clone this repository:

    git clone git://github.com/ticky/HypertextTypographer.git

That's it!

## Options

_Note: The following sections have not yet been updated for this plug-in._

Several options are available to customize the plugin look 'n feel. The
config keys goes into config files accessible throught the "Preferences"
menu.

### Bind the deletion command to a shortcut

In order to use the deletion feature, one must add the mapping by hand
(this should probably go into "Key Bindings - User"):

``` js
{ "keys": ["ctrl+shift+t"], "command": "delete_trailing_spaces" }
```

Here, pressing Ctrl + Shift + t will delete all trailing spaces.

### Change the highlighting color

One may also change the highlighting color, providing a scope name such
as "invalid", "comment"... in "File Settings - User":

``` js
{ "trailing_spaces_highlight_color": "invalid" }
```

Actually, "invalid" is the default value. If you'd like to use a custom color,
it should be defined as a color scope in your theme file. Feel free to ask me
how to do it.

### Disabling highlighting for large files

Highlighting may be disabled for large files. The default threshold is around
1M chars. This is configurable (in "File Settings - User"); unit is number of chars:

``` js
{ "trailing_spaces_file_max_size": 1000}
```

Even though the trailing spaces are not highlighted, one can still delete them
using the deletion command.
