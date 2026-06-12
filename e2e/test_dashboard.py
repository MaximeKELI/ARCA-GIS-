"""Tests E2E Playwright — dashboard ARCA-GIS."""

import pytest

pytest.importorskip("playwright")

from playwright.sync_api import sync_playwright


@pytest.fixture(scope="module")
def browser_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        browser.close()


def test_dashboard_login_page(browser_page):
    page = browser_page
    page.goto("http://localhost:8003/dashboard/")
    assert page.locator("text=Connexion Admin").is_visible()


def test_developers_portal(browser_page):
    page = browser_page
    page.goto("http://localhost:8003/developers/")
    assert page.locator("text=Portail Développeurs").is_visible()
