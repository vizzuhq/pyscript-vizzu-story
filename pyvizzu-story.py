
import html
from textwrap import dedent

from pyscript import Plugin, js
from pyodide.ffi import to_js
from js import Object, Vizzu

import json

js.console.warn(
    "WARNING: This plugin is still in a very experimental phase and will likely change"
    " and potentially break in the future releases. Use it with caution."
)

class MyPlugin(Plugin):
    def configure(self, config):

        js.console.log(f"configuration received: {config}")

    def afterStartup(self, runtime):
        js.console.log(f"runtime received: {runtime}")

plugin = MyPlugin("pyVizzuStory")

@plugin.register_custom_element("py-vizzu-story")
class PyVizzu:
    def __init__(self, element):
        self.element = element
        self.chart = Vizzu.default.new(self.element)

    def connect(self):
        print("CONNECTED----->")
        self.html = dedent(self.element.innerHTML)
        story = self.html
        json_story = json.loads(story)
        js_story = to_js(json_story, dict_converter=Object.fromEntries)
        self.element.innerHTML = "<vizzu-player controller></vizzu-player>"
        self.element.firstElementChild.slides = js_story;
        self.element.style.display = "block"
        print(self.html)

