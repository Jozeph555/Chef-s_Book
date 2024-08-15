import unittest

from src.modules.models.fields.note_field import NoteField


class TestNote(unittest.TestCase):
    def test_valid_note(self):
        note = NoteField("here should be some text")
        self.assertEqual(note.value, "here should be some text")

    def test_invalid_note(self):
        with self.assertRaises(ValueError):
            NoteField("12")
        with self.assertRaises(ValueError):
            NoteField("as")
