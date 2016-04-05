import sublime, sublime_plugin, re

spaceRe = re.compile(r'^\s*$');

s = sublime.load_settings("Hungry Backspace.sublime-settings")


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
      hungry_backspace(view,edit)
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
  for region in view.sel():
          # if this is the current cursor location
          if region.empty():
              consume_backspace(view, edit ,region)
          else:
           default_backspace(view)


def default_backspace(view):
  view.run_command("left_delete")

def consume_backspace(view, edit, region):
  (old_line_contents, old_line) = get_cur_line(view, region, True)
  # check if it contains just spaces
  if spaceRe.match(old_line_contents):
    # get the upper line
    (upper_line_contents,upper_line) = get_upper_line(view, region, False)
    # remove the line under this selection
    view.erase(edit,old_line)
    # clear the selection
    view.sel().clear()
    sz = 0
    # check if previous line is empty
    if(spaceRe.match(upper_line_contents)):
      # if it's empty get ready to re-insert indentation
      # clear it first
      view.replace(edit, upper_line, '')
      # re-insert indentation characters
      sz = view.insert(edit, upper_line.begin(), old_line_contents[:-1])
    # move cursor
    view.sel().add(sublime.Region(upper_line.end() + sz))
  else:
    default_backspace(view)
    
def is_active_file_type(filename):
  if filename == None:
    return True
  excluded_filetypes = s.get('excluded_filetypes')
  parts = filename.split('.')
  if len(parts) < 2:
    return True
  else:
    if parts[-1] in excluded_filetypes:
      return False
    else:
      return True

def is_swapped():
  return s.get('flipped_key_bindings')
  

def is_enabled():
  return s.get('enabled')


def get_cur_line(view, region, full):
  if full:
    line = view.full_line(region)
  else:
    line = view.line(region)
  return (view.substr(line),line)

def get_upper_line(view, region, full):
  # get the current row,col
  (row,col) = view.rowcol(view.sel()[0].begin())
  # create a new region on the prev line
  new_region = sublime.Region(view.text_point(row-1, 0))
  # get the full prev line
  if full:
    new_region_line = view.full_line(new_region)
  else:
    new_region_line = view.line(new_region)
  return (view.substr(new_region_line),new_region_line)  



def plugin_loaded():
  global s
  s = sublime.load_settings("Hungry Backspace.sublime-settings")