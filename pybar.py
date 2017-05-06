# -*- coding: UTF-8 -*-
#
# This file is part of pybar (terminal progress bar for Python 3).
#
# pybar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pybar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pybar.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2017, Nico Rittstieg

def show_progress(count, total, status='', terminal_width = 80, bar_len = 30, bar_char = '█'):
    """
    Shows a simple terminal progress bar     
 
    Args:
        count (int): Current progress
        total (int): Maximum value
        status (str): Status label (default='')
        terminal_width (int): Terminal window width (default=80)
        bar_len (int): Progress bar width (default=30)
        bar_char (char): Used bar character (default='█')
    """
    percents = round(100.0 * count / float(total), 1)
    filled_bar_len = int(round(bar_len * count / float(total)))
    bar =  bar_char * filled_bar_len + '_' * (bar_len - filled_bar_len)
    line = "{0:5.1f}% |{1}| {2}".format(percents, bar, status)    
    if len(line) >= terminal_width:
        line = line[:terminal_width-1]
    elif len(line) < terminal_width -1:
        line += ' ' * (terminal_width - len(line) - 1)
    print(line, end = '\r')
    if count == total:
        print()