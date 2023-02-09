
import html
from textwrap import dedent

from pyscript import Plugin, js
from pyodide.ffi import to_js, create_proxy
from js import Object, console, Vizzu

import re
import json


js.console.warn(
    "WARNING: This plugin is still in a very experimental phase and will likely change"
    " and potentially break in the future releases. Use it with caution."
)

PAGE_SCRIPT = """
    (async () => {
        VizzuModule = await import('https://cdn.jsdelivr.net/npm/vizzu@latest/dist/vizzu.min.js');
        window.Vizzu = VizzuModule.default;
        console.log("Vizzu loaded")
    })()
"""

class MyPlugin(Plugin):
    def configure(self, config):
        js.console.log(f"configuration received: {config}")

    def afterStartup(self, runtime):
        js.console.log(f"runtime received: {runtime}")

plugin = MyPlugin("pyVizzu")

@plugin.register_custom_element("py-vizzu")
class PyVizzu:
    def __init__(self, element):
        # js.eval(PAGE_SCRIPT)
        self.element = element
        self.chart = Vizzu.default.new(self.element)
        self.animations = []
        # self.inject_js()

    def inject_js(self):
        script = js.document.createElement("script")
        script.type = "text/javascript"
        script.src = "https://cdn.jsdelivr.net/npm/vizzu@latest/dist/vizzu.min.js"
        js.document.head.appendChild(script)

    def connect(self):
        print("CONNECTED----->")
        self.element.animate = self.animate
        self.html = dedent(self.element.innerHTML)

        animations = self.html.split('----')
        for anim in animations:
            print(f"Animations {anim}")
            json_anim = json.loads(anim)
            self.animations.append(json_anim)
            self.animate(json_anim)

           
        self.element.innerHTML = ""
        self.element.style.display = "block"
        print(self.html)

    def animate(self, target):
        self.chart.animate(to_js(target, dict_converter=Object.fromEntries))
       

    def append_script_to_page(self):
        el = js.document.createElement("script")
        el.type = "text/javascript"
        try:
            el.appendChild(js.document.createTextNode(PAGE_SCRIPT))
        except BaseException:
            el.text = PAGE_SCRIPT

        js.document.body.appendChild(el)
