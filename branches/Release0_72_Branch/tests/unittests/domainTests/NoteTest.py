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

import test
from taskcoachlib import patterns
from taskcoachlib.domain import note


class NoteTest(test.TestCase):
    def setUp(self):
        self.note = note.Note()
        self.child = note.Note()
        self.events = []
        
    def onEvent(self, event):
        self.events.append(event)
        
    def testDefaultSubject(self):
        self.assertEqual('', self.note.subject())
        
    def testGivenSubject(self):
        aNote = note.Note(subject='Note')
        self.assertEqual('Note', aNote.subject())
        
    def testSetSubject(self):
        self.note.setSubject('Note')
        self.assertEqual('Note', self.note.subject())
        
    def testSubjectChangeNotification(self):
        patterns.Publisher().registerObserver(self.onEvent, 
            self.note.subjectChangedEventType())
        self.note.setSubject('Note')
        self.assertEqual(patterns.Event(self.note, 
            self.note.subjectChangedEventType(), 'Note'), self.events[0])
        
    def testDefaultDescription(self):
        self.assertEqual('', self.note.description())
        
    def testGivenDescription(self):
        aNote = note.Note(description='Description')
        self.assertEqual('Description', aNote.description())
        
    def testSetDescription(self):
        self.note.setDescription('Description')
        self.assertEqual('Description', self.note.description())
        
    def testDescriptionChangeNotification(self):
        patterns.Publisher().registerObserver(self.onEvent, 
            self.note.descriptionChangedEventType())
        self.note.setDescription('Description')
        self.assertEqual(patterns.Event(self.note, 
            self.note.descriptionChangedEventType(), 'Description'), 
            self.events[0])
        
    def testAddChild(self):
        self.note.addChild(self.child)
        self.assertEqual([self.child], self.note.children())

    def testRemoveChild(self):
        self.note.addChild(self.child)
        self.note.removeChild(self.child)
        self.assertEqual([], self.note.children())
        
    def testAddChildNotification(self):
        patterns.Publisher().registerObserver(self.onEvent, 
            note.Note.addChildEventType())
        self.note.addChild(self.child)
        self.assertEqual(patterns.Event(self.note, 
            note.Note.addChildEventType(), self.child), self.events[0])
        
    def testRemoveChildNotification(self):
        patterns.Publisher().registerObserver(self.onEvent, 
            note.Note.removeChildEventType())
        self.note.addChild(self.child)
        self.note.removeChild(self.child)
        self.assertEqual(patterns.Event(self.note, 
            note.Note.removeChildEventType(), self.child), self.events[0])
        
    def testNewChild(self):
        child = self.note.newChild(subject='child')
        self.assertEqual('child', child.subject())
        
    def testGetState(self):
        self.assertEqual(dict(id=self.note.id(), subject='', description='', parent=None,
            categories=set(), attachments=[], children=self.note.children(),
            status=self.note.getStatus(), color=None),
            self.note.__getstate__())
        
    def testSetState(self):
        self.note.__setstate__(dict(id='id', subject='new', description='new', 
            parent=None, children=[], status=42, attachments=[],
            color=(0,0,0,255)))
        self.assertEqual('new', self.note.description())
        
        
class NoteOwnerTest(test.TestCase):
    def setUp(self):
        self.note = note.Note(subject='Note')
        self.noteOwner = note.NoteOwner()
        self.events = []
        
    def onEvent(self, event):
        self.events.append(event)
        
    def registerObserver(self):
        patterns.Publisher().registerObserver(self.onEvent,
            note.NoteOwner.notesChangedEventType())
        
    def testAddNote(self):
        self.noteOwner.addNote(self.note)
        self.assertEqual([self.note], self.noteOwner.notes())

    def testAddNoteNotification(self):
        self.registerObserver()
        self.noteOwner.addNote(self.note)
        self.assertEqual(patterns.Event(self.noteOwner, 
            note.NoteOwner.notesChangedEventType(), self.note), self.events[0])
        
    def testRemoveNote(self):
        self.noteOwner.addNote(self.note)
        self.noteOwner.removeNote(self.note)
        self.failIf(self.noteOwner.notes())

    def testRemoveNoteNotification(self):
        self.noteOwner.addNote(self.note)
        self.registerObserver()
        self.noteOwner.removeNote(self.note)
        self.assertEqual(patterns.Event(self.noteOwner, 
            note.NoteOwner.notesChangedEventType(), *self.noteOwner.notes()), 
            self.events[0])
            
    def testGetState(self):
        self.noteOwner.addNote(self.note)
        self.assertEqual(dict(notes=[self.note]), self.noteOwner.__getstate__())

    def testSetState(self):
        self.noteOwner.addNote(self.note)
        state = self.noteOwner.__getstate__()
        self.noteOwner.removeNote(self.note)
        self.noteOwner.__setstate__(state)
        self.assertEqual([self.note], self.noteOwner.notes())
        
    def testSetState_CausesNotification(self):
        self.noteOwner.addNote(self.note)
        state = self.noteOwner.__getstate__()
        self.noteOwner.removeNote(self.note)
        self.registerObserver()
        self.noteOwner.__setstate__(state)
        self.assertEqual(patterns.Event(self.noteOwner, 
            note.NoteOwner.notesChangedEventType(), self.note), self.events[0])
            
    def testInitializeNotesViaConstructor(self):
        noteOwner = note.NoteOwner(notes=[self.note])
        self.assertEqual([self.note], noteOwner.notes())

    def testCopy(self):
        self.noteOwner.addNote(self.note)
        copy = note.NoteOwner(**self.noteOwner.__getcopystate__())
        self.assertNotEqual(copy.notes()[0].id(), self.note.id())
        self.assertEqual(copy.notes()[0].subject(), self.note.subject())

    def testCopy_NoteOwnerWithNoteWithSubNote(self):
        child = note.Note(subject='child')
        self.note.addChild(child)
        self.noteOwner.addNote(self.note)
        copy = note.NoteOwner(**self.noteOwner.__getcopystate__())
        childCopy = copy.notes()[0].children()[0]
        self.assertNotEqual(childCopy.id(), child.id())
        self.assertEqual(childCopy.subject(), child.subject())
