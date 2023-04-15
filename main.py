import argparse
import yaml
from os.path import isfile
from typing import Any

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual.widgets import Button, Header, Footer, Static, Label

parser = argparse.ArgumentParser(
    prog='shiny-spoon',
    description='5e Character Sheet Renderer',
    epilog=':)')

parser.add_argument('filename')

TERMINAL_ARGUMENTS = parser.parse_args()
CHARACTER_SHEET_FILEPATH = TERMINAL_ARGUMENTS.filename
VERSION = 'PRE-ALPHA AS FUCK'


class CharacterInfo(Static):
    """Widget to display basic character information"""

    def __init__(self, character: dict):
        super().__init__()
        self.character = character

    def compose(self) -> ComposeResult:
        """Create child widgets containing character info"""
        with Horizontal(id="character-info"):
            yield Static(f"{self.character['name']}", id='character-name')
            yield ClassesWidget(self.character['classes'])
            yield InfoWidget(f"Race", self.character['race'])
            yield InfoWidget(f"Background", self.character['background'])
            yield InfoWidget(f"Alignment", self.character['alignment'])


class ClassesWidget(Container):
    """Displays character classes"""

    def __init__(self, classes: dict):
        super().__init__()
        self.classes_text = ', '.join(f"{_class} {_level}" for _class, _level in classes)

    def compose(self) -> ComposeResult:
        """Create child widgets containing classes info"""
        yield Static(f"Class")
        yield Static(self.classes_text)


class InfoWidget(Container):
    """Displays certain pieces of character information"""

    def __init__(self, field: str, info: any):
        super().__init__()
        self.field = field
        self.info = info

    def compose(self) -> ComposeResult:
        """Create child widgets containing field and info"""
        yield Static(self.field)
        yield Static(self.info)


class CharacterBody(Static):
    """Widget to display character info necessary to gameplay."""

    def __init__(self, character: dict):
        super().__init__()
        self.character = character

    def compose(self) -> ComposeResult:
        """Creates a grid of child widgets."""
        with Container(id='charachter-body'):
            yield StatsWidget(self.character['stats'])


class StatsWidget(Container):
    """Displays certain pieces of character information"""

    def __init__(self, stats: dict):
        super().__init__()
        self.stats = stats

    def compose(self) -> ComposeResult:
        """Create child widgets containing field and info"""
        yield Static(f"STR: {self.stats['STR']:2d} ({stat_modifier(self.stats['STR']):+d})")
        yield Static(f"DEX: {self.stats['DEX']:2d} ({stat_modifier(self.stats['DEX']):+d})")
        yield Static(f"CON: {self.stats['CON']:2d} ({stat_modifier(self.stats['CON']):+d})")
        yield Static(f"INT: {self.stats['INT']:2d} ({stat_modifier(self.stats['INT']):+d})")
        yield Static(f"WIS: {self.stats['WIS']:2d} ({stat_modifier(self.stats['WIS']):+d})")
        yield Static(f"CHA: {self.stats['CHA']:2d} ({stat_modifier(self.stats['CHA']):+d})")


class CharacterSheet5E(App):
    """A Textual app to render character sheets."""

    character = None

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    CSS_PATH = "style.css"

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header(show_clock=True, name=f'5e Character Sheet - {VERSION}')
        yield CharacterInfo(self.character)
        yield CharacterBody(self.character)
        yield Footer()

    def load_character_sheet(self, filename: str):
        """Loads character sheet from filename"""

        if not isfile(filename):
            raise OSError("Character file not found!")

        with open(filename, "r") as f:
            self.character = yaml.safe_load(f)


def stat_modifier(stat: int):
    return (stat - 10) // 2


if __name__ == "__main__":
    app = CharacterSheet5E()
    app.load_character_sheet(CHARACTER_SHEET_FILEPATH)
    app.run()
