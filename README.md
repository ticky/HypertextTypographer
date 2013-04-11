# Hypertext Typographer

For [Sublime Text 2](http://www.sublimetext.com/2).

**Highlight typographical errors in HTML and fix them in a flash.**

Copywriters and clients use Microsoft Word to compose copy for websites.
This is a sad but unavoidable fact of life.
This Sublime Text 2 plugin is intended to detect such errors in realtime, and
allow easy replacement of the most common special characters inserted by rich
text editors.

The intent is not to function as a dumb html_escape function, nor is it to
replace or enhance the built-in HTML syntax error highlighting.
It is instead intended to stop only the frustrating and difficult to spot
typographical issues in their tracks.

## What is detected?

* "Smart" or "Typographers'" quotes (`“`, `”`, `‘`, `’`)
* Horizontal Ellipses (`…`)
* Dashes (`‒`, `–`, `—`, `―`)
* Fractions (`½`, `¼`, `¾`)

## What is *not* detected?

As this is intended for detecting issues *within copy*, specifically, several
characters which you should usually be escaping or replacing with character
entities are not highlighted or replaced by Hypertext Typographer by default.

* Ampersands (`&`)
* Standard Quotes (`"`, `'`)
* Greater Than (`>`) and Less Than (`<`) signs.

The reason behind this is that the highlighting logic is blunt; it matches any
of these characters in HTML and HTML-like files without context sensitivity, and
because generally your syntax highlighting will show these anyway.

You can always add these to your configuration file, or any other replacements
you wish to include.

## Installation

Go to your `Packages` subdirectory under ST2's data directory:

* Windows: `%APPDATA%\Sublime Text 2`
* OS X: `~/Library/Application Support/Sublime Text 2`
* Linux: `~/.config/sublime-text-2`
* Portable Installation: `Sublime Text 2/Data`

Then clone this repository:

    git clone git://github.com/geoffstokes/HypertextTypographer.git

That's it!

## Options

Several options are available to customise the behaviour and appearance.
The config keys are in the config files accessible through the "Preferences"
menu.

### Bind the escape command to a shortcut

In order to use the escape feature, one must add the mapping by hand (this
should go into "Key Bindings - User"):

``` js
{
	"keys": ["ctrl+shift+t"],
	"command": "escape_typography"
}
```

Here, pressing `Ctrl` + `Shift` + `T` will replace any invalid HTML typography
detected with plan alternatives.

If you want full XML escaping, you can instead use:

``` js
{
	"keys": ["ctrl+shift+t"],
	"command": "escape_typography",
	"args": {
		"mode": "escape"
	}
}
```

### Change the highlighting color

One may also change the highlighting color, providing a scope name such
as "invalid", "comment"... in "File Settings - User":

``` js
{ "hypertext_typographer_highlight_color": "invalid" }
```

Actually, "invalid" is the default value. If you'd like to use a custom color,
it should be defined as a color scope in your theme file.

### Disabling highlighting for large files

Highlighting may be disabled for large files. The default threshold is around 1M
chars. This is configurable (in "File Settings - User"); unit is number of
chars:

``` js
{
	"hypertext_typographer_file_max_size": 1000
}
```

Even though the typographical issues are not highlighted, one can still use
either replacement command as normal.

## Acknowledgements

This is based upon
[Trailing Spaces](https://github.com/SublimeText/TrailingSpaces) by Jean-Denis
Vauguet.
