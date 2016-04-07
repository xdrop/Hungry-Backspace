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
    cursor = view.sel()[0]
    if cursor.empty():
        consume_backspace(view, edit, cursor)
    else:
        default_backspace(view)


def default_backspace(view):
    view.run_command("left_delete")


def reindent(view):
    view.run_command("reindent")


def consume_backspace(view, edit, cursor):
    (old_line_contents, old_line) = get_cur_line(view, cursor, True)
    old_line_no_leading_space = old_line_contents.lstrip()
    # calculated spaces until first character
    spaces = len(old_line_contents) - len(old_line_no_leading_space)
    # check if it contains just spaces
    if spaceRe.match(old_line_contents):
        # get the upper line
        (upper_line_contents, upper_line) = get_upper_line(view, cursor, False)
        # remove the line under this selection
        view.erase(edit, old_line)
        # clear the selection
        view.sel().clear()
        offset = 0
        # check if previous line is empty
        if spaceRe.match(upper_line_contents):
            offset = reinsert_indent(
                view, edit, (upper_line, upper_line_contents), old_line_contents)
        # move cursor
        view.sel().add(sublime.Region(upper_line.end() + offset))
    # if we are at the begining of the line
    elif (old_line.begin() + spaces) == cursor.end():
        should_reindent = is_right_left_bck()
        # get the upper line
        (upper_line_contents, upper_line) = get_upper_line(view, cursor, True)
        upper_len = len(upper_line_contents)
        upper_spaces = upper_len - len(upper_line_contents.lstrip())
        passthrough = False
        # if right to left reindent is enabled and spaces on
        # this line are different from spaces on the above line
        if should_reindent and not is_force_line_move() and spaces >= upper_spaces:
            reindent(view)
            new_cursor_pos = view.sel()[0]
        else:
            passthrough = True
        if passthrough or new_cursor_pos == cursor:
            if spaceRe.match(upper_line_contents) and is_consume_above():
                view.erase(edit, upper_line)
                view.sel().clear()
                view.sel().add(sublime.Region(cursor.begin() - upper_len))
            elif is_bck_line_move() and spaces >= upper_spaces:
                new_merged_line = upper_line_contents.rstrip(
                    "\r\n") + old_line_no_leading_space
                view.erase(edit, old_line)
                view.replace(edit, upper_line, '')
                view.insert(edit, upper_line.begin(), new_merged_line)
                move_cursor(view, upper_line.end() - 1)
            else:
                default_backspace(view)
    else:
        default_backspace(view)


def reinsert_indent(view, edit, upper, spaces):
    (upper_line, upper_line_contents) = upper
    upper_len = len(upper_line_contents)
    # if the upper line doesn't contain any indent
    if upper_len == 0:
        # if it's empty get ready to re-insert indentation
        # clear it first
        view.replace(edit, upper_line, '')
        # re-insert indentation characters
        offset = view.insert(
            edit, upper_line.begin(), spaces.rstrip("\r\n"))
    elif is_force_indent_at_upper():
        # get ready to re-insert indentation
        # clear it first
        view.replace(edit, upper_line, '')
        # re-insert indentation characters
        sz = view.insert(edit, upper_line.begin(), spaces.rstrip("\r\n"))
        offset = sz - upper_len
    return offset


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
    return s.get('right_to_left_backspacing')


def is_consume_above():
    return s.get('consume_above_line')


def is_bck_line_move():
    return s.get('backspace_line_content_move') in ["enabled","forced", True]

def is_force_line_move():
    return s.get('backspace_line_content_move') == "forced"


def get_cur_line(view, region, full):
    if full:
        line = view.full_line(region)
    else:
        line = view.line(region)
    return (view.substr(line), line)


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
