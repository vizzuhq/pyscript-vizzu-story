
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

plugin = MyPlugin("pyVizzu")

@plugin.register_custom_element("py-vizzu")
class PyVizzu:
    def __init__(self, element):
        self.element = element
        self.chart = Vizzu.default.new(self.element)

    def connect(self):
        print("CONNECTED----->")
        self.html = dedent(self.element.innerHTML)

        animations = self.html.split('----')
        for anim in animations:
            print(f"Animations {anim}")
            json_anim = json.loads(anim)
            self.animate(json_anim)

           
        self.element.innerHTML = ""
        self.element.style.display = "block"
        print(self.html)

    def animate(self, target):
        self.chart.animate(to_js(target, dict_converter=Object.fromEntries))
