'''
Task Coach - Your friendly task manager
Copyright (C) 2004-2008 Frank Niessink <frank@niessink.com>

Task Coach is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Task Coach is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from taskcoachlib.i18n import _
from taskcoachlib.domain import note
import base


class NewNoteCommand(base.BaseCommand):
    def name(self):
        return _('New note')

    def __init__(self, *args, **kwargs):
        self.categories = kwargs.get('categories',  None)
        super(NewNoteCommand, self).__init__(*args, **kwargs)
        self.items = self.createNewNotes()
        
    def createNewNotes(self):
        return [note.Note(subject=_('New note'), categories=self.categories)]
        
    def do_command(self):
        self.list.extend(self.items)

    def undo_command(self):
        self.list.removeItems(self.items)

    def redo_command(self):
        self.list.extend(self.items)


class NewSubNoteCommand(NewNoteCommand):
    def name(self):
        return _('New subnote')
            
    def createNewNotes(self):
        return [parent.newChild(subject=_('New subnote')) for parent in self.items]


class EditNoteCommand(base.EditCommand):
    def name(self):
        return _('Edit note')
    
    def getItemsToSave(self):
        return self.items
    
    
class DragAndDropNoteCommand(base.DragAndDropCommand):
    def name(self):
        return _('Drag and drop note')
