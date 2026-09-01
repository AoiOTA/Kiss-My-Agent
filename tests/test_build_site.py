from __future__ import annotations

from html.parser import HTMLParser
import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_site", ROOT / "scripts/build_site.py")
assert SPEC is not None and SPEC.loader is not None
build_site = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build_site)


class _PageInspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.html_lang = ""
        self.article_class = ""
        self.intro_align = ""
        self.links: list[dict[str, str]] = []
        self.images: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value for name, value in attrs if value is not None}
        if tag == "html":
            self.html_lang = values.get("lang", "")
        if tag == "article":
            self.article_class = values.get("class", "")
        if tag == "div" and values.get("class") == "readme-intro":
            self.intro_align = values.get("align", "")
        if tag in {"a", "link"}:
            self.links.append(values)
        if tag == "img":
            self.images.append(values)


class BuildSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temporary.name) / "site"
        build_site.build(cls.output)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def inspect(self, route: str) -> _PageInspector:
        parser = _PageInspector()
        parser.feed((self.output / route).read_text(encoding="utf-8"))
        return parser

    def test_builds_all_sixteen_pages(self) -> None:
        html_pages = sorted(path.relative_to(self.output).as_posix() for path in self.output.rglob("*.html"))
        self.assertEqual(len(html_pages), 16)
        self.assertIn("index.html", html_pages)
        self.assertIn("zh-CN/index.html", html_pages)

    def test_language_switch_and_alternates_are_reciprocal(self) -> None:
        english = self.inspect("installation.html")
        chinese = self.inspect("zh-CN/installation.html")
        self.assertEqual(english.html_lang, "en")
        self.assertEqual(chinese.html_lang, "zh-CN")
        self.assertTrue(any(link.get("hreflang") == "zh-CN" and link.get("href") == "zh-CN/installation.html" for link in english.links))
        self.assertTrue(any(link.get("hreflang") == "en" and link.get("href") == "../installation.html" for link in chinese.links))

    def test_fragment_rewrite_preserves_fragment(self) -> None:
        routes, _ = build_site.document_routes()
        rewriter = build_site.LinkRewriter("docs/FAQ.md", routes["docs/FAQ.md"], routes)
        self.assertEqual(rewriter.rewrite("../README.md#quick-start"), "index.html#quick-start")
        self.assertEqual(rewriter.rewrite("#ci-status"), "#ci-status")

    def test_hero_is_copied_and_rewritten_for_both_languages(self) -> None:
        self.assertTrue((self.output / "assets/kiss-my-agent-hero.png").is_file())
        english = self.inspect("index.html")
        chinese = self.inspect("zh-CN/index.html")
        self.assertTrue(any(image.get("class") == "hero" and image.get("src") == "assets/kiss-my-agent-hero.png" for image in english.images))
        self.assertTrue(any(image.get("class") == "hero" and image.get("src") == "../assets/kiss-my-agent-hero.png" for image in chinese.images))

    def test_home_intro_centering_is_scoped_to_both_home_pages(self) -> None:
        self.assertEqual(self.inspect("index.html").article_class, "content home-content")
        self.assertEqual(self.inspect("zh-CN/index.html").article_class, "content home-content")
        self.assertEqual(self.inspect("installation.html").article_class, "content")
        self.assertEqual(self.inspect("index.html").intro_align, "center")
        self.assertEqual(self.inspect("zh-CN/index.html").intro_align, "center")

        stylesheet = (self.output / "assets/style.css").read_text(encoding="utf-8")
        self.assertIn(".home-content > .readme-intro", stylesheet)
        self.assertIn("justify-content: center", stylesheet)

    def test_repository_files_and_directories_use_blob_and_tree(self) -> None:
        links = [link.get("href", "") for link in self.inspect("index.html").links]
        self.assertIn("https://github.com/AoiOTA/Kiss-My-Agent/blob/main/LICENSE", links)
        self.assertIn("https://github.com/AoiOTA/Kiss-My-Agent/tree/main/.codex/agents", links)

    def test_every_local_link_and_fragment_is_closed(self) -> None:
        routes, counterparts = build_site.document_routes()
        build_site.validate_output(self.output, routes, counterparts)

    def test_every_page_has_current_navigation_and_no_javascript(self) -> None:
        for page in self.output.rglob("*.html"):
            markup = page.read_text(encoding="utf-8")
            self.assertIn('aria-current="page"', markup, page)
            self.assertNotIn("<script", markup.lower(), page)

    def test_nonempty_unmarked_output_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "user-content"
            nested = output / "nested"
            nested.mkdir(parents=True)
            (output / "notes.txt").write_text("keep me\n", encoding="utf-8")
            (nested / "data.bin").write_bytes(b"\x00\x01keep")
            before = {
                path.relative_to(output): path.read_bytes()
                for path in output.rglob("*")
                if path.is_file()
            }

            with self.assertRaisesRegex(build_site.BuildError, "non-empty unmarked"):
                build_site.build(output)

            after = {
                path.relative_to(output): path.read_bytes()
                for path in output.rglob("*")
                if path.is_file()
            }
            self.assertEqual(after, before)

    def test_unsafe_raw_html_and_urls_fail_fast(self) -> None:
        routes, _ = build_site.document_routes()
        cases = {
            "script": "<script>alert(1)</script>",
            "event": '<p onclick="alert(1)">unsafe</p>',
            "javascript": '[unsafe](javascript:alert(1))',
            "scheme-relative": "[unsafe](//example.invalid/attack)",
        }
        for name, source_text in cases.items():
            with self.subTest(name=name):
                with self.assertRaises(build_site.BuildError):
                    build_site.render_markdown(
                        source_text,
                        "README.md",
                        routes["README.md"],
                        routes,
                    )


if __name__ == "__main__":
    unittest.main()
