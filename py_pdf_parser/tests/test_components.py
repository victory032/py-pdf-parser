from ddt import ddt, data
from unittest import TestCase

from py_pdf_parser.common import BoundingBox

from utils import create_pdf_element


@ddt
class TestPDFElement(TestCase):
    element_bbox = BoundingBox(2, 5, 2, 5)

    def test_index(self):
        element = create_pdf_element(index=1)
        self.assertEqual(element.index, 1)

        with self.assertRaises(AttributeError):
            element.index = 2

    def test_page_number(self):
        element = create_pdf_element(page_number=1)
        self.assertEqual(element.page_number, 1)

        with self.assertRaises(AttributeError):
            element.page_number = 2

    def test_font_name(self):
        element = create_pdf_element(font_name="test_font")
        self.assertEqual(element.font_name, "test_font")

    def test_font_size(self):
        element = create_pdf_element(font_size=2)
        self.assertEqual(element.font_size, 2)

    def test_font(self):
        element = create_pdf_element(font_name="test_font", font_size=2)
        self.assertEqual(element.font, "test_font,2")

        element = create_pdf_element(
            font_name="test_font",
            font_size=3,
            font_mapping={"test_font,3": "test_named_font"},
        )
        self.assertEqual(element.font, "test_named_font")

        element = create_pdf_element(
            font_name="test_font",
            font_size=2,
            font_mapping={"test_font,3": "test_named_font"},
        )
        self.assertEqual(element.font, "test_font,2")

    def test_text(self):
        element = create_pdf_element(text="test")
        self.assertEqual(element.text, "test")

    def test_add_tag(self):
        element = create_pdf_element()
        self.assertEqual(element.tags, set())

        element.add_tag("foo")
        self.assertEqual(element.tags, set(["foo"]))

        element.add_tag("foo")
        self.assertEqual(element.tags, set(["foo"]))

        element.add_tag("bar")
        self.assertEqual(element.tags, set(["foo", "bar"]))

    def test_repr(self):
        element = create_pdf_element(font_name="test_font", font_size=2)
        self.assertEqual(repr(element), "<PDFElement tags: set(), font: 'test_font,2'>")

        element.add_tag("foo")
        self.assertEqual(
            repr(element), "<PDFElement tags: {'foo'}, font: 'test_font,2'>"
        )

        element.ignore = True
        self.assertEqual(
            repr(element), "<PDFElement tags: {'foo'}, font: 'test_font,2', ignored>"
        )

    @data(
        BoundingBox(1, 6, 1, 6),  # This box fully encloses the element
        BoundingBox(1, 6, 0, 3),  # This box intersects the bottom of the element
        BoundingBox(1, 6, 0, 2),  # This box touches the bottom of the element
        BoundingBox(1, 6, 4, 6),  # This box intersects the top of the element
        BoundingBox(1, 6, 5, 6),  # This box touches the top of the element
        BoundingBox(1, 6, 3, 4),  # This box goes through center horizontally
        BoundingBox(1, 3, 1, 6),  # This box intersects the left of the element
        BoundingBox(1, 2, 1, 6),  # This box touches the left of the element
        BoundingBox(4, 6, 1, 6),  # This box intersects the left of the element
        BoundingBox(5, 6, 1, 6),  # This box touches the left of the element
        BoundingBox(3, 4, 1, 6),  # This box goes through the center vertically
        BoundingBox(3, 4, 3, 4),  # This box is enclosed inside the element
    )
    def test_partially_within_true(self, bounding_box):
        element = create_pdf_element(self.element_bbox)
        self.assertTrue(element.partially_within(bounding_box))

    @data(
        BoundingBox(1, 6, 0, 1),  # This box is underneath the element
        BoundingBox(1, 6, 6, 7),  # This box is above the element
        BoundingBox(0, 1, 1, 6),  # This box is to the left of the element
        BoundingBox(6, 7, 1, 6),  # This box is to the lerightft of the element
    )
    def test_partially_within_false(self, bounding_box):
        element = create_pdf_element(self.element_bbox)
        self.assertFalse(element.partially_within(bounding_box))

    @data(BoundingBox(1, 6, 1, 6))  # This box fully encloses the element
    def test_entirely_within_true(self, bounding_box):
        element = create_pdf_element(self.element_bbox)
        self.assertTrue(element.entirely_within(bounding_box))

    @data(
        BoundingBox(1, 6, 0, 3),  # This box intersects the bottom of the element
        BoundingBox(1, 6, 0, 2),  # This box touches the bottom of the element
        BoundingBox(1, 6, 4, 6),  # This box intersects the top of the element
        BoundingBox(1, 6, 5, 6),  # This box touches the top of the element
        BoundingBox(1, 6, 3, 4),  # This box goes through center horizontally
        BoundingBox(1, 3, 1, 6),  # This box intersects the left of the element
        BoundingBox(1, 2, 1, 6),  # This box touches the left of the element
        BoundingBox(4, 6, 1, 6),  # This box intersects the left of the element
        BoundingBox(5, 6, 1, 6),  # This box touches the left of the element
        BoundingBox(3, 4, 1, 6),  # This box goes through the center vertically
        BoundingBox(1, 6, 0, 1),  # This box is underneath the element
        BoundingBox(1, 6, 6, 7),  # This box is above the element
        BoundingBox(0, 1, 1, 6),  # This box is to the left of the element
        BoundingBox(6, 7, 1, 6),  # This box is to the lerightft of the element
        BoundingBox(3, 4, 3, 4),  # This box is enclosed inside the element
    )
    def test_entirely_within_false(self, bounding_box):
        element = create_pdf_element(self.element_bbox)
        self.assertFalse(element.entirely_within(bounding_box))
