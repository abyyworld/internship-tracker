"""The published pages that hold someone's CV and API key.

docs/studio.html is the version of the editor that needs nothing installed, so
it is the one page in this project that holds a reader's CV and their provider
key inside a page served from the public internet. What it must never do is
load code from anywhere else, or send that data anywhere but the endpoint the
reader chose. Those are properties of the file, so they are checked here rather
than in a browser harness that has to be run by hand.
"""

from pathlib import Path
import re
import unittest


DOCS = Path(__file__).resolve().parent.parent / "docs"
STUDIO = DOCS / "studio.html"
OPENER = DOCS / "open.html"


class StudioIsSelfContainedTests(unittest.TestCase):
    def setUp(self):
        self.source = STUDIO.read_text(encoding="utf-8")

    def test_it_loads_no_code_or_assets_from_anywhere_else(self):
        # A CDN script on this page could read the CV and the key out of
        # storage. There is no version of that which is acceptable, so there
        # are no external sources at all.
        for pattern in (r'<script[^>]+\bsrc=', r'<link[^>]+stylesheet[^>]*href="https?:',
                        r'@import\b', r'<iframe'):
            self.assertIsNone(re.search(pattern, self.source, re.I),
                              f"studio.html pulls in {pattern}")

    def test_the_only_places_it_sends_anything_are_chosen_by_the_reader(self):
        # Every fetch in the file: the provider endpoint the reader configured,
        # and the loopback probe that asks whether the better editor is running.
        targets = re.findall(r'fetch\(\s*([^,)]+)', self.source)
        self.assertTrue(targets)
        for target in targets:
            self.assertTrue(
                "endpoint" in target or "BRIDGE" in target,
                f"studio.html sends a request somewhere unexpected: {target}")

    def test_the_key_is_never_put_in_a_url(self):
        # A key in a query string ends up in history, in referrers, and in any
        # log the endpoint keeps. It goes in the Authorization header only.
        self.assertIn('"Authorization": `Bearer ${key}`', self.source)
        self.assertNotRegex(self.source, r"[?&]key=\$\{")

    def test_everything_it_stores_is_namespaced_and_removable(self):
        keys = set(re.findall(r'"(studio\.[a-z]+)', self.source))
        self.assertTrue(keys, "the storage keys are not recognisable")
        self.assertIn("studio.cv", keys)
        # "Forget everything on this device" must catch all of them, which it
        # can only do if every key really does share the prefix.
        self.assertIn('key.startsWith("studio.")', self.source)

    def test_the_pdf_is_written_here_not_asked_for_from_the_browser(self):
        # A print dialog is not an export: it asks the reader to find the right
        # menu, pick A4, turn off headers and footers, and hope. The page
        # writes the file itself, in the base-14 fonts every reader has, so
        # nothing has to be embedded and nothing has to be downloaded.
        for marker in ("/BaseFont /Times-Roman", "/BaseFont /Helvetica-Bold",
                       "/MediaBox [0 0 ${PAGE.w} ${PAGE.h}]", "WinAnsiEncoding",
                       "startxref"):
            self.assertIn(marker, self.source, f"the PDF writer lost: {marker}")
        self.assertIn('link.download = pdfName()', self.source)
        # The same measurements as the local editor's renderer.
        self.assertRegex(self.source, r"PAGE = \{w: 595\.28, h: 841\.89, left: 42\.52")

    def test_the_document_is_set_the_way_it_prints(self):
        # Not a list of lines in a box: A4 at true size, with the typography
        # autoapply/cv_render.py uses, so what is edited is what comes out.
        self.assertIn("width:595.28pt", self.source)
        self.assertIn("--accent:#14324F", self.source)
        for block in (".name", ".contact", ".section", ".entry", ".bullet",
                      ".title", ".sub"):
            self.assertIn(f"#sheet {block}", self.source, f"no styling for {block}")

    def test_it_reads_the_cv_someone_already_has(self):
        # Retyping a CV that exists as a PDF is not an editor. Both formats are
        # read in the browser with what the browser already has, so the file
        # never leaves the machine and no library has to be fetched.
        for marker in ("DecompressionStream", "ASCII85Decode", "/FlateDecode",
                       "word/document.xml", "looksLikeText"):
            self.assertIn(marker, self.source, f"the importer lost: {marker}")
        # The positions are what turn fragments back into lines.
        for operator in ('case "cm"', 'case "Tm"', 'case "TJ"', 'case "T*"'):
            self.assertIn(operator, self.source, f"the PDF reader ignores {operator}")

    def test_a_rebuilt_cv_keeps_the_shape_of_the_one_that_went_in(self):
        # The faults a side-by-side comparison found, each pinned:
        #   job titles were being set as section heads, in accent blue over a
        #   rule, because they were short and capitalised;
        #   "May 2026 – Present" was split at the dash, putting half the range
        #   in the margin;
        #   the wide gaps that are the only evidence of a column — the date at
        #   the right, the label beside its skills — were collapsed away before
        #   anything could read them.
        self.assertIn("SECTION_WORDS", self.source)
        self.assertIn("DATE_RANGE", self.source)
        self.assertRegex(self.source, r"tail\.length > best\.when\.length")
        self.assertRegex(self.source, r'replace\(/\[ \\t\]\{2,\}/g, "  "\)')
        self.assertIn("function pairOf", self.source)

    def test_the_model_list_comes_from_the_endpoint_not_from_here(self):
        # Three model names written into a page are current for about a month.
        # What the reader's own key can reach is asked for, and anything the
        # endpoint does not list can still be typed in by hand.
        self.assertIn('"/models"', self.source)
        self.assertIn("KEY.models(provider.id)", self.source)
        # Google lists "models/gemini-2.5-flash"; the chat endpoint wants the tail.
        self.assertIn(r'replace(/^models\//, "")', self.source)
        self.assertIn("NOT_CHAT", self.source)      # an embedder cannot rewrite a CV
        self.assertIn("Type a model name", self.source)

    def test_a_request_cannot_run_forever_and_can_be_given_up_on(self):
        # "its taking too long seems stuck": a page that says Rewriting… and
        # nothing else is indistinguishable from one that has died. There is a
        # deadline, the seconds are shown, and the button becomes the way out.
        self.assertIn("const DEADLINE", self.source)
        self.assertIn("AbortController", self.source)
        self.assertRegex(self.source, r'button\.textContent = "Stop"')
        self.assertRegex(self.source, r"running\.abort\(")
        self.assertRegex(self.source, r"setInterval\(")
        # Gemini's flash models think before answering unless told not to, and
        # that thinking is the wait.
        self.assertIn('reasoning_effort: "none"', self.source)

    def test_a_rewrite_that_only_reworded_is_not_offered(self):
        # "the changes are almost identical to the previous version". A model
        # asked to rewrite returns something for every line, and half of those
        # are the same sentence with two words swapped.
        self.assertIn("function tooSimilar", self.source)
        self.assertRegex(self.source, r"tooSimilar\(line\.text, item\.text\)")
        # But a line that gains the advert's own term — ROS 2, C++, a number —
        # has genuinely changed, however little else moved.
        self.assertIn("function addedTerms", self.source)
        self.assertRegex(self.source, r"addedTerms\(before, after\)\.length\) return false")

    def test_how_hard_to_go_is_the_reader_choice(self):
        for name in ("touch:", "full:", "hard:"):
            self.assertIn(name, self.source, f"no {name} mode")
        self.assertIn("MODES[mode].order", self.source)
        self.assertIn('mode: "studio.mode"', self.source)   # remembered next time
        self.assertIn("What the applicant asked for", self.source)

    def test_an_answer_that_ran_out_of_room_is_not_thrown_away(self):
        # A model that hits the token limit leaves complete suggestions and one
        # half-written one. The complete ones are still advice.
        self.assertIn("function salvage", self.source)
        self.assertRegex(self.source, r"catch \(error\) \{ payload = salvage\(text\); \}")

    def test_a_bulleted_cv_comes_back_bulleted(self):
        # ReportLab — which is what this project's own CV generator uses, and
        # what wrote the reader's real CV — draws a list bullet as byte 127.
        # WinAnsi leaves that code undefined, and an undefined code IS a bullet
        # by the encoding's own rule. Read as Latin-1 it is an invisible
        # control character, so every bullet in a real CV came back as a
        # two-column row and exported as "?".
        self.assertRegex(self.source, r'0x7F: "\\u2022"')
        self.assertIn('#sheet .bullet', self.source)

    def test_the_headline_under_the_name_is_set_as_one(self):
        # A CV puts what you are in one centred italic line under the name.
        # Set as an ordinary subtitle it lands left-aligned and small, which is
        # the first thing anyone notices is wrong.
        self.assertIn('return "tagline"', self.source)
        self.assertIn("#sheet .tagline", self.source)
        self.assertRegex(self.source, r'kind === "tagline"[\s\S]{0,200}CONTENT_W - widthOf')

    def test_a_sentence_broken_by_the_old_measure_is_put_back(self):
        # A PDF has no paragraphs, only rows. A row ending in a comma or a
        # colon is continued by the next one whatever case it starts in, and a
        # link left alone on a row — "GitHub" — belongs to the line above it.
        self.assertIn("const dangling", self.source)
        self.assertIn("const tail", self.source)

    def test_more_than_one_cv_can_be_kept_and_a_posting_remembers_its_own(self):
        # Nobody applies with one CV. There is a robotics one and a research
        # one, and which of them a posting wants is a property of the posting —
        # so the CVs are a library and each posting remembers the one it used.
        self.assertIn('cvs: "studio.cvs"', self.source)
        self.assertRegex(self.source, r"pick: `studio\.pick\.\$\{jobKey\}`")
        self.assertIn("function library()", self.source)
        self.assertIn('id="cvPick"', self.source)
        # The edits made for one posting belong to that posting AND that CV.
        self.assertRegex(self.source, r"draft: id => `studio\.draft\.\$\{jobKey\}\.\$\{id\}`")
        # Whatever the single-CV version of this page saved is still found.
        self.assertRegex(self.source, r'const only = store\.get\(KEY\.cv, ""\)')

    def test_a_rewrite_may_also_be_to_take_the_line_out(self):
        # The strongest edit a CV can get is often a cut. It is still a
        # proposal: nothing leaves the document without being accepted.
        self.assertIn('"text":""', self.source.replace(" ", ""))
        self.assertIn("Cut this line", self.source)
        self.assertRegex(self.source, r"cut: item\.text === \"\"")
        self.assertRegex(self.source, r"lines\.splice\(at, 1\)")
        # And an accepted cut is kept the way every other edit is, which an
        # index-keyed draft could not do — every index after it shifts.
        self.assertRegex(self.source, r"lines\.map\(line => \[line\.original, line\.text\]\)")

    def test_it_says_where_the_reader_data_goes(self):
        # The trade is: nothing to install, but the CV and the advert go
        # straight to a third party. Saying so is not optional.
        for phrase in ("stored in this browser", "never uploaded",
                       "directly to the provider"):
            self.assertIn(phrase, self.source,
                          f"studio.html does not say: {phrase}")


class NoDeadEndsTests(unittest.TestCase):
    def test_a_posting_goes_to_the_studio_unless_the_helper_can_do_the_job(self):
        opener = OPENER.read_text(encoding="utf-8")
        self.assertIn("./studio.html", opener)
        # The decision is made on what the helper can do, not on whether
        # something is listening — an old build answers a liveness probe just
        # as happily and then refuses the posting.
        self.assertIn("/can/adopt-any-posting.png", opener)
        self.assertRegex(opener, r"location\.replace\(studioUrl")
        self.assertRegex(opener, r"capable === true.*location\.replace\(editorUrl\)")

    def test_the_studio_is_told_which_of_the_two_it_is(self):
        opener = OPENER.read_text(encoding="utf-8")
        self.assertRegex(opener, r'"stale"\s*:\s*"absent"')
        studio = STUDIO.read_text(encoding="utf-8")
        # A stale helper must not be offered as a place to go: that is the
        # editor the reader was just refused by.
        self.assertIn('helperState === "stale"', studio)
        self.assertRegex(studio, r'helperState === "stale"[\s\S]{0,600}helperLink"\)\.classList\.add\("hidden"\)')

    def test_the_local_editor_offers_it_when_it_cannot_load(self):
        # The last page that could still dead-end: the local editor itself,
        # when something on this machine is wrong. Whatever that is, the reader
        # still wants this posting tailored, and the browser studio cannot be
        # affected by it.
        from autoapply.editor_ui import EDITOR_PAGE

        self.assertIn("studio.html", EDITOR_PAGE)
        self.assertIn("Tailor this CV in the browser instead", EDITOR_PAGE)
        # Carrying the posting, or it lands somewhere that knows nothing.
        self.assertRegex(EDITOR_PAGE, r'carried\.set\("url",\s*jobUrl\)')

    def test_the_dashboard_offers_it_without_a_role(self):
        index = DOCS / "index.html"
        if not index.exists():  # generated; a fresh checkout may not have it yet
            self.skipTest("docs/index.html has not been generated here")
        self.assertIn("./studio.html", index.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
