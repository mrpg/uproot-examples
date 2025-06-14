"""
Docs are available at https://uproot.science/
Examples are available at https://github.com/mrpg/uproot-examples

This example app is under the 0BSD license. You can use it freely and build on it
without any limitations and without any attribution. However, these two lines must be
preserved in any uproot app (the license file is automatically installed in a project):

Third-party dependencies:
- uproot: LGPL v3+, see ../uproot_license.txt
"""

from uproot.fields import *
from uproot.smithereens import *
from uproot.types import Page

DESCRIPTION = "Upload your curriculum vitæ"


class Upload(Page):
    fields = dict(
        cv=FileField(  # FileField are ALWAYS handled by handle_stealth_fields
            label="Please upload your curriculum vitæ.",
        ),
    )

    @classmethod
    async def handle_stealth_fields(page, player, cv: "UploadFile"):
        # Please see https://www.starlette.io/requests/#request-files to learn about UploadFile

        # this method could write the uploaded file to a separate file, or do whatever else
        # however, since this is just an example, it just prints some info:
        print(
            f"New upload: {player} uploaded a file called '{cv.filename}' of "
            f"size {cv.size} bytes and content-type {cv.content_type}"
        )

        # this is how you actually get the contents of the file:
        # contents = await cv.read()
        # you can use the resulting bytes in whatever way you want

        # note: you cannot stop the player from proceeding - for that, you would have to
        # build a custom WTForms validator


page_order = [Upload]
