import sublime, sublime_plugin, re

spaceRe = re.compile(r'^\s*$');

class HungryBackspaceCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    for region in view.sel():
      # if this is the current cursor location
      if region.empty():
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
          # if we are on a character just remove 1
          ch = sublime.Region(region.begin(),region.end()-1)
          view.erase(edit,ch)
    else:
      # if this is a selection just erase
      view.erase(edit,region)



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
