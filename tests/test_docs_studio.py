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

    def test_nothing_this_page_does_can_fail_silently(self):
        # The notice bar is at the top of the page; the button that starts a
        # rewrite is at the bottom of a long column. A reason printed three
        # screens away is indistinguishable from nothing happening at all, so
        # every failure is also printed under the button, and one request can
        # be sent on its own to say whether it is the key or the CV.
        self.assertIn("function trouble", self.source)
        self.assertRegex(self.source, r'\$\("status"\)\.classList\.add\("bad"\)')
        self.assertIn(".hint.bad", self.source)
        self.assertIn('id="test"', self.source)
        # Even an error thrown before the request is made reaches the reader.
        self.assertRegex(self.source, r"pending\.catch\(error => trouble")

    def test_the_three_settings_are_three_different_things(self):
        # "go hard and full rewrite means the same thing wth" — they did, once
        # the line caps went. The difference that can be held in the head is
        # that only one of them takes anything away.
        self.assertIn("Wording only", self.source)              # touch up
        self.assertIn("nothing is taken away", self.source)      # full rewrite
        self.assertIn("takes things away", self.source)          # go hard
        # Exactly one of the three removes anything.
        self.assertEqual(self.source.count("cuts: true"), 1)
        self.assertEqual(self.source.count("cuts: false"), 2)
        # And a cut offered under a setting that does not cut is not shown.
        self.assertRegex(self.source, r"if \(item\.cut && !MODES\[mode\]\.cuts\) continue")

    def test_the_model_is_shown_the_whole_cv_not_only_the_lines_to_change(self):
        # Rewriting a bullet without the heading above it, the employer it was
        # for or the dates it ran between is writing blind, and blind rewrites
        # are the bland ones.
        self.assertIn("function rewritable", self.source)
        self.assertRegex(self.source, r'Lines marked > are the ones you may rewrite')
        # A worked example beats three sentences of description.
        self.assertIn("before: Worked on the grasp planner", self.source)
        # And the cheapest model in a family is named as what it is.
        self.assertIn("WEAK_MODEL", self.source)

    def test_there_is_always_a_way_back_to_the_cv_that_was_saved(self):
        # Edits are kept per posting, which is right — but a draft with no way
        # out of it is a trap, and the reader hit it.
        self.assertIn('id="revert"', self.source)
        self.assertRegex(self.source, r'\$\("revert"\)\.onclick[\s\S]{0,400}store\.drop\(KEY\.draft')
        # And a tailored version worth keeping becomes a CV of its own.
        self.assertIn('id="saveVersion"', self.source)
        self.assertRegex(self.source, r'addCv\(name\.trim\(\) \|\| suggested, rawText\(\)\)')

    def test_the_library_holds_what_is_sent_out_and_nothing_else(self):
        # A CV is regenerated far more often than it is replaced by a different
        # one. Reading the same file again must leave one entry, not two: a
        # list of near-identical copies is how the wrong one gets sent.
        self.assertIn("function keepCv", self.source)
        self.assertIn("replaced rather than copied", self.source)
        # And the last CV can be removed too — a library with no way to empty
        # it is not a library.
        self.assertNotRegex(self.source, r'\$\("dropCv"\)\.classList\.toggle\("hidden"')
        self.assertRegex(self.source, r"const last = list\.length === 1")

    def test_the_studio_is_lit_the_way_the_reader_asked_for(self):
        for marker in ("prefers-color-scheme:dark", '[data-theme="dark"]', '"radar.theme"',
                       'id="themeBtn"'):
            self.assertIn(marker, self.source, f"the studio lost: {marker}")
        # The sheet is paper: it does not change colour with the room.
        # (--d, the density multiplier, now leads the rule.)
        self.assertRegex(self.source, r"#sheet\{[^}]*width:595\.28pt[^}]*background:#fff")

    def test_it_says_how_much_of_the_advert_the_cv_answers(self):
        # The one thing every CV tool is asked for, and the one it must not
        # fake: a score anybody can reproduce by reading the two documents.
        # Done here rather than by a model — it costs nothing, needs no key,
        # and can be checked.
        self.assertIn("function advertTerms", self.source)
        self.assertIn("function matchAgainstAdvert", self.source)
        self.assertIn("Asked for, not in your CV", self.source)
        # It counts words appearing, and says so rather than implying more.
        self.assertIn("counts words, not truth", self.source)
        # A phrase is answered by a line carrying its words, not only by one
        # that repeats them in order: "closed-loop policy evaluation" answers
        # "closed-loop evaluation".
        self.assertIn("const perLine", self.source)
        # And a pair of words only counts when the advert put them together.
        self.assertIn("const clausesOf", self.source)

    def test_a_line_can_be_worked_on_by_itself(self):
        # The whole-CV pass is the wrong tool for one weak line: it costs a
        # minute and buries the answer among twenty others.
        self.assertIn("function rewriteLine", self.source)
        self.assertIn("function moveLine", self.source)
        self.assertIn("function cutLine", self.source)
        # The controls must never become part of the text they sit beside.
        self.assertIn('tools.contentEditable = "false"', self.source)
        self.assertRegex(self.source, r'hold\.append\(node, rowTools\(index\)\)')

    def test_the_page_count_comes_from_the_writer(self):
        # A count measured any other way can say "one page" and then hand over
        # two. This one is whatever the file turned out to be.
        self.assertIn("pagesWritten = pages.length", self.source)
        self.assertIn("function pageNote", self.source)
        # Density is one number driving both the sheet and the file, so what is
        # on screen stays what comes out.
        self.assertIn("--d:1", self.source)
        self.assertRegex(self.source, r"font-size:calc\(9\.7pt \* var\(--d\)\)")
        self.assertIn("scaled(spec, density)", self.source)
        self.assertIn("density: id => `studio.density.${id}`", self.source)

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
