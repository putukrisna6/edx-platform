"""
Tests for signal handlers in the contentstore.
"""

from datetime import datetime

from opaque_keys.edx.locator import CourseLocator
from openedx_events.content_authoring.data import CourseCatalogData, CourseScheduleData

import cms.djangoapps.contentstore.signals.handlers as sh
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import SampleCourseFactory


class TestCatalogInfoSignal(ModuleStoreTestCase):
    """
    Test functionality of triggering catalog info signals (and events) from course_published signal.
    """

    def setUp(self):
        super().setUp()
        self.course = SampleCourseFactory.create(
            org='TestU',
            number='sig101',
            name='Signals 101',
            run='Summer2022',
        )
        self.course_key = self.course.id

        self.expected_data = CourseCatalogData(
            course_key=CourseLocator(org='TestU', course='sig101', run='Summer2022', branch=None, version_guid=None),
            name='Run 0',
            schedule_data=CourseScheduleData(
                start=datetime.fromisoformat('2030-01-01T00:00+00:00'),
                pacing='instructor',
                end=None,
                enrollment_start=None,
                enrollment_end=None),
            short_description=None,
            effort=None,
            hidden=False,
            invitation_only=False
        )

    def test_regular_course(self):
        assert sh.create_catalog_data_for_signal(self.course_key) == self.expected_data
