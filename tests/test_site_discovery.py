"""Offline crawlability, bilingual identity, and visible structured-data checks."""

from datetime import date
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import subprocess
import unittest
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://awesomejev.github.io"
ROUTES = ("/", "/zh/", "/guide/", "/zh/guide/", "/papers/", "/zh/papers/")
PAIRS = (("/", "/zh/"), ("/guide/", "/zh/guide/"), ("/papers/", "/zh/papers/"))


def words(value):
    return re.sub(r"\s+", " ", value).strip()


def objects(value):
    """Walk inline JSON-LD graphs, including nested mainEntity ItemLists."""
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


def has_type(value, wanted):
    kind = value.get("@type", "")
    return wanted in kind if isinstance(kind, list) else kind == wanted


class CrawlPage(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.language = ""
        self.canonicals = []
        self.alternates = []
        self.robots = []
        self.cards = []
        self.headings = []
        self.structured = []
        self.body_text = []
        self.ids = []
        self.links = []
        self._in_body = False
        self._script = None
        self._script_text = []
        self._h1 = None
        self._card = None
        self._card_title = False
        self._style = False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        classes = set(attrs.get("class", "").split())
        if tag == "html":
            self.language = attrs.get("lang", "")
        elif tag == "body":
            self._in_body = True
        elif tag == "link":
            relation = attrs.get("rel", "").split()
            if "canonical" in relation:
                self.canonicals.append(attrs.get("href", ""))
            if "alternate" in relation and "hreflang" in attrs:
                self.alternates.append((attrs["hreflang"], attrs.get("href", "")))
        elif tag == "meta" and attrs.get("name", "").lower() in {"robots", "googlebot", "bingbot"}:
            self.robots.append(attrs.get("content", ""))
        elif tag == "script":
            self._script = attrs.get("type", "other")
            self._script_text = []
        elif tag == "style":
            self._style = True
        elif tag == "h1":
            self._h1 = []
        elif tag == "article" and "resource-row" in classes:
            self._card = {"url": "", "name": [], "hidden": "hidden" in attrs or attrs.get("aria-hidden") == "true"}
        elif tag == "h3" and self._card is not None:
            self._card_title = True
        elif tag == "a" and self._card is not None and self._card_title:
            self._card["url"] = attrs.get("href", "")

    def handle_endtag(self, tag):
        if tag == "script":
            if self._script == "application/ld+json":
                self.structured.append(json.loads("".join(self._script_text)))
            self._script = None
        elif tag == "style":
            self._style = False
        elif tag == "body":
            self._in_body = False
        elif tag == "h1" and self._h1 is not None:
            self.headings.append(words("".join(self._h1)))
            self._h1 = None
        elif tag == "h3":
            self._card_title = False
        elif tag == "article" and self._card is not None:
            self._card["name"] = words("".join(self._card["name"]))
            self.cards.append(self._card)
            self._card = None

    def handle_data(self, value):
        if self._script is not None:
            self._script_text.append(value)
            return
        if self._style:
            return
        if self._in_body:
            self.body_text.append(value)
        if self._h1 is not None:
            self._h1.append(value)
        if self._card is not None and self._card_title:
            self._card["name"].append(value)


class SiteDiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {}
        for route in ROUTES:
            path = ROOT / "site" / route.strip("/") / "index.html"
            cls.pages[route] = CrawlPage(path.read_text(encoding="utf-8"))

    def test_homepages_publish_the_curated_collection_without_javascript(self):
        for route in ("/", "/zh/"):
            with self.subTest(route=route):
                cards = self.pages[route].cards
                self.assertGreaterEqual(len(cards), 60)
                self.assertTrue(all(card["name"] and not card["hidden"] for card in cards))
                self.assertTrue(all(urlsplit(card["url"]).scheme in {"http", "https"} and urlsplit(card["url"]).netloc for card in cards))
                self.assertEqual(len({card["url"] for card in cards}), len(cards))
        self.assertEqual([c["url"] for c in self.pages["/"].cards], [c["url"] for c in self.pages["/zh/"].cards])

    def test_each_language_page_has_a_distinct_self_canonical_and_reciprocal_alternates(self):
        observed = []
        for english, chinese in PAIRS:
            for route in (english, chinese):
                with self.subTest(route=route):
                    page = self.pages[route]
                    self.assertEqual(page.canonicals, [BASE + route])
                    observed.extend(page.canonicals)
                    alternates = dict(page.alternates)
                    self.assertEqual(len(alternates), len(page.alternates))
                    self.assertEqual(alternates.get("en"), BASE + english)
                    self.assertEqual(alternates.get("zh-CN"), BASE + chinese)
                    if "x-default" in alternates:
                        self.assertEqual(alternates["x-default"], BASE + english)
                    self.assertTrue(page.language.lower().startswith("zh" if route.startswith("/zh/") else "en"))
                    self.assertEqual(len(page.headings), 1)
        self.assertEqual(len(set(observed)), len(ROUTES))

    def test_chinese_routes_contain_translated_body_text_before_scripts_run(self):
        for route in ("/zh/", "/zh/guide/", "/zh/papers/"):
            with self.subTest(route=route):
                self.assertGreater(len(re.findall(r"[\u4e00-\u9fff]", "".join(self.pages[route].body_text))), 30)

    def test_homepage_translation_preserves_interactive_controls(self):
        required = {"resource-search", "resource-list", "result-count", "corpus-search", "corpus-list", "start", "copy-code", "copy-status"}
        for route in ("/", "/zh/"):
            with self.subTest(route=route):
                ids = self.pages[route].ids
                self.assertTrue(required.issubset(ids), "A translation/build replacement removed a required interaction target")
                self.assertEqual(len(ids), len(set(ids)), "Generated HTML must not duplicate interaction IDs")

    def test_item_lists_match_visible_link_titles_order_and_counts(self):
        for route in ("/", "/zh/", "/papers/", "/zh/papers/"):
            with self.subTest(route=route):
                page = self.pages[route]
                self.assertGreaterEqual(len(page.cards), 20)
                item_lists = [item for block in page.structured for item in objects(block) if has_type(item, "ItemList")]
                self.assertEqual(len(item_lists), 1)
                listing = item_lists[0]
                items = listing["itemListElement"]
                self.assertEqual(listing["numberOfItems"], len(page.cards))
                self.assertEqual(len(items), len(page.cards))
                for number, (item, card) in enumerate(zip(items, page.cards), 1):
                    self.assertTrue(has_type(item, "ListItem"))
                    self.assertEqual(item["position"], number)
                    self.assertEqual(item["url"], card["url"])
                    self.assertEqual(words(item["name"]), card["name"])

    def test_guide_article_headline_matches_visible_page_heading(self):
        for route in ("/guide/", "/zh/guide/"):
            with self.subTest(route=route):
                page = self.pages[route]
                articles = [item for block in page.structured for item in objects(block) if has_type(item, "Article")]
                self.assertEqual(len(articles), 1)
                self.assertEqual(words(articles[0]["headline"]), page.headings[0])
                citations = articles[0].get("citation", [])
                self.assertTrue(citations, "The research guide must expose its source citations")
                self.assertTrue(set(citations).issubset(page.links), "Structured citations must also be visible page links")
                self.assertTrue(all(urlsplit(url).scheme in {"http", "https"} and urlsplit(url).netloc for url in citations))

    def test_search_and_answer_engine_crawlers_are_not_blocked(self):
        robots_text = (ROOT / "site/robots.txt").read_text()
        rules = RobotFileParser()
        rules.parse(robots_text.splitlines())
        for agent in ("Googlebot", "Bingbot", "OAI-SearchBot"):
            for route, page in self.pages.items():
                with self.subTest(agent=agent, route=route):
                    self.assertTrue(rules.can_fetch(agent, BASE + route))
                    self.assertFalse(any(set(re.split(r"[,\s]+", value.lower())) & {"noindex", "none"} for value in page.robots))
        self.assertIn(BASE + "/sitemap.xml", rules.site_maps() or [])

    def test_sitemap_lists_all_six_canonical_pages(self):
        tree = ET.fromstring((ROOT / "site/sitemap.xml").read_bytes())
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locations = [node.text for node in tree.findall("sm:url/sm:loc", ns)]
        self.assertEqual(set(locations), {BASE + route for route in ROUTES})
        self.assertEqual(len(locations), len(set(locations)))
        for modified in tree.findall("sm:url/sm:lastmod", ns):
            date.fromisoformat(modified.text[:10])

    def test_generated_discovery_artifacts_are_current(self):
        node = shutil.which("node")
        self.assertIsNotNone(node, "Node.js is required to verify generated site artifacts")
        result = subprocess.run([node, "scripts/build_site.mjs", "--check"], cwd=ROOT, capture_output=True, text=True, timeout=45)
        output = (result.stdout + result.stderr).replace(str(ROOT), ".")[:1500]
        self.assertEqual(result.returncode, 0, output)


if __name__ == "__main__":
    unittest.main()
