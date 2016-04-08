import sublime
import sublime_plugin
import re

spaceRe = re.compile(r'^\s*$')


class HungryBackspaceCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        # if this filetype is excluded restore normal backspace behaviour
        if is_enabled() and is_active_file_type(view.file_name()) and not is_swapped():
            hungry_backspace(view, edit)
        else:
            default_backspace(view)


class DefaultBackspaceCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        if is_enabled() and is_swapped() and is_active_file_type(view.file_name()):
            hungry_backspace(view, edit)
        else:
            default_backspace(view)


class FlipHungryBackspaceKeyBindingsCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        prev = s.get('flipped_key_bindings')
        if prev:
            s.set('flipped_key_bindings', False)
        else:
            s.set('flipped_key_bindings', True)
        sublime.save_settings("Hungry Backspace.sublime-settings")


def hungry_backspace(view, edit):
    selections = view.sel()
    cursor = view.sel()[0]
    # disable for multiple-cursor selection
    if cursor.empty() and len(selections) == 1:
        consume_backspace(view, edit, cursor)
    else:
        default_backspace(view)


def default_backspace(view):
    view.run_command("left_delete")


def reindent(view):
    view.run_command("reindent")


def consume_backspace(view, edit, cursor):
    (cur_line_contents, cur_line) = get_cur_line(view, cursor, True)
    # calculated indent until first character
    current_indent = calc_indent(cur_line_contents)
    # check if it contains just spaces
    if spaceRe.match(cur_line_contents):
        # get the upper line
        (upper_line_contents, upper_line) = get_upper_line(view, cursor, False)
        # check if the upper line is empty
        upper_empty = spaceRe.match(upper_line_contents)
        # if force right to left is enabled
        if is_force_reindent():
            upper_indent = calc_indent(upper_line_contents)
            # if the indent level of this line is higher than the line
            # above we will re-indent it instead of removing it
            if current_indent > upper_indent and not upper_empty:
                reindent(view)
                return
        # remove the line under this selection
        view.erase(edit, cur_line)
        offset = 0
        # check if previous line is empty
        if upper_empty:
            offset = reinsert_indent(
                view, edit,
                (upper_line, upper_line_contents),
                cur_line_contents)
        # move cursor
        move_cursor(view, upper_line.end() + offset)
    # if we are at the begining of the line
    elif (cur_line.begin() + current_indent) == cursor.end():
        should_reindent = is_right_left_bck() and not is_force_line_move()
        # get the upper line
        (upper_line_contents, upper_line) = get_upper_line(view, cursor, True)
        upper_indent = calc_indent(upper_line_contents)
        passthrough = False
        # if right to left reindent is enabled
        # && and spaces on this line are more from spaces on the above line
        # && backspace_line_content_move is not set to forced
        if should_reindent and current_indent >= upper_indent:
            reindent(view)
            # reobtain the cursor position
            new_cursor_pos = view.sel()[0]
        else:
            passthrough = True
        # if the re-indent didn't run or it run but nothing changed
        # that means we can perform one of the other actions
        if passthrough or new_cursor_pos.end() == cursor.end():
            # we check that the upper line is empty
            # then we can move this line up
            if spaceRe.match(upper_line_contents) and is_consume_above():
                view.erase(edit, upper_line)
                move_cursor(view, cursor.begin() - len(upper_line_contents))
            # if the upper line is not empty and we have enabled the option
            # to move line contents up on backspace
            elif is_bck_line_move() and current_indent >= upper_indent:
                # strip the line end from the above line
                # and append the current line without the leading space
                new_merged_line = upper_line_contents.rstrip(
                    "\r\n") + cur_line_contents.lstrip()
                view.erase(edit, cur_line)
                view.replace(edit, upper_line, '')
                view.insert(edit, upper_line.begin(), new_merged_line)
                # move the cursor to the new position
                move_cursor(view, upper_line.end() - 1)
            else:
                default_backspace(view)
    else:
        default_backspace(view)


def reinsert_indent(view, edit, upper, indent):
    (upper_line, upper_line_contents) = upper
    upper_len = len(upper_line_contents)
    # if the upper line doesn't contain any indent
    if upper_len == 0:
        # if it's empty get ready to re-insert indentation
        # clear it first
        view.replace(edit, upper_line, '')
        # re-insert indentation characters
        offset = view.insert(
            edit, upper_line.begin(), indent.rstrip("\r\n"))
    elif is_force_indent_at_upper():
        # get ready to re-insert indentation
        # clear it first
        view.replace(edit, upper_line, '')
        # re-insert indentation characters
        sz = view.insert(edit, upper_line.begin(), indent.rstrip("\r\n"))
        offset = sz - upper_len
    return offset


def calc_indent(line):
    # remove end of line characters
    line_noeol = line.rstrip("\r\n")
    # remove start spacing
    line_trim = line_noeol.lstrip()
    # calculated spaces until first character
    return len(line_noeol) - len(line_trim)


def move_cursor(view, pos):
    view.sel().clear()
    view.sel().add(sublime.Region(pos))


def is_active_file_type(filename):
    if filename is None:
        return True
    excluded_filetypes = s.get('excluded_filetypes')
    parts = filename.split('.')
    if len(parts) < 2:
        return True
    else:
        return parts[-1] not in excluded_filetypes


def is_force_indent_at_upper():
    return s.get('force_indent_at_upper_level')


def is_swapped():
    return s.get('flipped_key_bindings')


def is_enabled():
    return s.get('enabled')


def is_right_left_bck():
    return s.get('right_to_left_backspacing') in ["enabled", "forced", True]


def is_force_reindent():
    return s.get('right_to_left_backspacing') == "forced"


def is_consume_above():
    return s.get('consume_above_line')


def is_bck_line_move():
    return s.get('backspace_line_content_move') in ["enabled", "forced", True]


def is_force_line_move():
    return s.get('backspace_line_content_move') == "forced"


def get_cur_line(view, region, full):
    if full:
        line = view.full_line(region)
    else:
        line = view.line(region)
    return (view.substr(line), line)


def as_hex(s):
    return ":".join("{:02x}".format(ord(c)) for c in s)


def get_upper_line(view, region, full):
    # get the current row,col
    (row, col) = view.rowcol(view.sel()[0].begin())
    # create a new region on the prev line
    new_region = sublime.Region(view.text_point(row - 1, 0))
    # get the full prev line
    if full:
        new_region_line = view.full_line(new_region)
    else:
        new_region_line = view.line(new_region)
    return (view.substr(new_region_line), new_region_line)


def plugin_loaded():
    global s
    s = sublime.load_settings("Hungry Backspace.sublime-settings")
