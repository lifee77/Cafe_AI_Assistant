from multiprocessing import Process, Manager
import time

from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Label, RadioButton, RadioSet, Button
from textual.reactive import reactive

from logic import run_expert_system

shared_data = {"curr_question": {"text": "Hello", "type": "single_choice", "options": [], "default": "None"}}


# def init_worker(data):
#     # declare scope of a new global variable
#     global shared_data
#     # store argument in the global variable for this process
#     shared_data = data


# def get_shared():
#     global shared_data
#     return shared_data


# def set_shared(k, v):
#     global shared_data
#     shared_data[k] = v


# def task(shared_data):
#     # shared_data = get_shared()
#     while True:
#         now = datetime.now()
#         if 0 <= now.time().second <= 30:
#             shared_data["curr_question"] = "What is your name?"
#         else:
#             shared_data["curr_question"] = "Who are you?"


class RadioSetChangedApp(App[None]):
    CSS_PATH = "tut.tcss"
    selected_value = reactive(shared_data["curr_question"]["default"])

    def compose(self) -> ComposeResult:
        # with VerticalScroll():
        with Horizontal():
            yield Label(shared_data["curr_question"]["text"], id="curr_question")
        with Horizontal():
            with RadioSet(id="focus_me"):
            	for opt in shared_data["curr_question"]["options"]:
            		yield RadioButton(opt,)
                
        with Horizontal():
            yield Label(self.selected_value, id="selected")
            yield Button("Next", id="start", variant="success")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        shared_data[f"{shared_data['curr_question']['text']}_response"] = [
            self.selected_value
        ]
        time.sleep(0.1)  # maybe wait for prolog?
        self.query_one("#curr_question", Label).update(shared_data["curr_question"]["text"])
        for btn in self.query("RadioButton"):
        	btn.remove()
        for opt in shared_data["curr_question"]["options"]:
        	self.query_one("#focus_me").mount(RadioButton(opt, )) # value = opt==shared_data["curr_question"]["default"]

    def on_mount(self) -> None:
        self.query_one(RadioSet).focus()

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        self.selected_value = str(event.pressed.label)
        self.query_one("#selected", Label).update(
            f"Selected label: {self.selected_value}"
        )


if __name__ == "__main__":
    manager = Manager()
    shared_data = manager.dict({"curr_question": {"text": "Hello", "type": "single_choice", "options": [], "default": "None"}})
    p1 = Process(target=run_expert_system, args=(shared_data,))
    # p2 = Process(target=app_func, args=(shared_data,))
    p1.start()
    RadioSetChangedApp().run()
    # p2.start()
    p1.join()
    # p2.join()


