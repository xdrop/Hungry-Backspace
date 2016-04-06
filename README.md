Hungry Backspace for Sublime Text
------------------------------------

### Overview

This small plugin brings to Sublime Text the "hungry backspace" feature from IntelliJ. The hungry backspace retains the scope (indentation) when the backspace key is pressed on an empty line. 

### Live demo

![](http://i.imgur.com/raML27M.gif)

### Warning

This plugin is **NOT** meant to replace backspace entirely, it is meant to be used in conjunction with the original backspace function which is now accessed by **Shift+Backspace**

### Version

1.0.6

### Installation


1. Having installed [Package Control](https://packagecontrol.io/installation) access the `Command Pallete` (`Ctrl+Shift+P`), select `Install package` and then select `Hungry Backspace`.

2. Try it by pressing backspace on some empty lines!

3. You can change the key bindings by going to `Preferences` then `Package Settings` then `Hungry Backspace`, and select they keymap option

*Alternatively* if you have not installed Package control:

1. Go to **Preferences | Browse packages...**
2. While inside the **Packages** directory, clone the theme repository using the command below: 

    `git clone https://github.com/xdrop/Hungry-Backspace.git "Hungry Backspace"`

### Key bindings
By default this plugin overrides your backspace with the "hungry" one however, as mentioned previously the plugin is meant to be used in conjunction with the default backspace which is now accessible via `SHIFT+BACKSPACE`. You can flip between space and shift-backspace at any time by pressing **CTRL+.(dot)**

```
[
  // the hungry backspace
  { "keys": ["backspace"], "command": "hungry_backspace" },
  // the default backspace
  { "keys": ["shift+backspace"], "command": "default_backspace"},
  // flipping the hungry and default backspace actions
  { "keys": ["ctrl+."], "command": "flip_hungry_backspace_key_bindings"}
]
```

### Settings
```
{
  // enable/disable plugin
  "enabled": true,
  // filetypes with these extensions don't have hungry backspacing (typically indented languages)
  "excluded_filetypes": ["hs", "py"],
  // controls whether the default/hungry backspace bindings should be flipped
  "flipped_key_bindings": false
}

```


### License

Copyright (c) 2016 xdrop


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:


The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.


THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

