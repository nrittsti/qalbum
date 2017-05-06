# qalbum (Quick Album)

A Python script for renaming pictures by [EXIF](https://en.wikipedia.org/wiki/Exif) creation timestamp.  
Usecase:  
Import pictures from different sources like cameras and mobile phones into a single directory.  
Run qalbum.py for auto renaming and subdir creation.


![ScreenShot](https://raw.github.com/nrittsti/qalbum/master/qalbum.png)

Main features: 
-------------------
  - Rename pictures by [EXIF](https://en.wikipedia.org/wiki/Exif) creation timestamp
  - Group pictures by image day
  - Create photo albums
  
System Requirements :
----------------------

 - Python 3
 - Python package easygui
 - Python package exifread

```
$ pip install easygui
$ pip install exifread
```

Launch from command line:
--------------------------

```
python qalbum.py
```

Project Web site :
--------------------

https://github.com/nrittsti/qalbum/

--------------------------------------------------------------------------------
Licence:
--------------------------------------------------------------------------------

This file is part of qalbum (picture renaming script).  

qalbum is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, either version 3 of the License, or  
(at your option) any later version.  

qalbum is distributed in the hope that it will be useful,  
but WITHOUT ANY WARRANTY; without even the implied warranty of  
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the  
GNU General Public License for more details.  

You should have received a copy of the GNU General Public License  
along with qalbum.  If not, see <http://www.gnu.org/licenses/>.  

Copyright 2017, Nico Rittstieg

--------------------------------------------------------------------------------
Third party libraries used by Quick Album
--------------------------------------------------------------------------------

https://pypi.python.org/pypi/easygui  
https://pypi.python.org/pypi/ExifRead

--------------------------------------------------------------------------------
End of document

