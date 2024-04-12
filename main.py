from multiprocessing import Process, Manager
import time

from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import (
    Label,
    RadioButton,
    RadioSet,
    Button,
    SelectionList,
    Header,
    Footer,
)
from textual.reactive import reactive
from textual import on

from logic import run_expert_system

shared_data = {"curr_question": {"default": "None"}}


class RecommenderApp(App[None]):
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        ("n", "go_next", "Go to Next Question"),
    ]
    selected_values = reactive([shared_data["curr_question"]["default"]])
    about_to_finish = False
    started = False
    has_radio = True

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Horizontal():
            yield Label(shared_data["curr_question"]["text"], id="curr_question")
        with Horizontal(id="focus_me"):
            pass
        with Horizontal():
            yield Button("Next", id="next_btn", variant="success")

    def action_go_next(self) -> None:
        if self.about_to_finish:
            self.exit()
            return
        shared_data[f"{shared_data['curr_question']['id']}_response"] = (
            self.selected_values
        )

        time.sleep(0.1)  # maybe wait for prolog?
        if not shared_data.get("done"):
            self.query_one("#curr_question", Label).update(
                shared_data["curr_question"]["text"]
            )

        if self.started and self.has_radio:
            self.query_one(RadioSet).remove()
        elif self.started:
            self.query_one(SelectionList).remove()

        if shared_data.get("done"):
            rec = shared_data["rec"]
            link = rec["link"] if rec else None
            self.query_one("#focus_me").remove()
            self.query_one("#next_btn", Button).label = "Finish"
            upd_message = (
                f"I recommend {rec['name']}."
                + ("" if not link else f" Check out the cafe here: {link}")
                if rec
                else "I don't have a recommendation for your preferences."
            )
            self.query_one("#curr_question", Label).update(upd_message)
            self.about_to_finish = True
        else:
            self.started = True
            if shared_data["curr_question"]["type"] == "single_choice":
                radioset = RadioSet()
                self.query_one("#focus_me").mount(radioset)
                self.selected_values = [shared_data["curr_question"]["default"]]
                for opt in shared_data["curr_question"]["options"]:
                    radioset.mount(
                        RadioButton(
                            opt["text"],
                            id=opt["id"],
                            value=opt["id"] == shared_data["curr_question"]["default"],
                        )
                    )
                    radioset.focus()
                self.has_radio = True
            else:
                self.query_one("#focus_me").mount(
                    SelectionList(
                        *[
                            (
                                opt["text"],
                                opt["id"],
                                opt["id"] == shared_data["curr_question"]["default"],
                            )
                            for opt in shared_data["curr_question"]["options"]
                        ]
                    )
                )
                self.selected_values = [shared_data["curr_question"]["default"]]
                self.has_radio = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.action_go_next()

    def on_mount(self) -> None:
        self.query_one("#focus_me").focus()

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        self.selected_values = [str(event.pressed.id)]

    @on(SelectionList.SelectedChanged)
    def update_selected_values(self) -> None:
        self.selected_values = self.query_one(SelectionList).selected


if __name__ == "__main__":
    manager = Manager()
    shared_data = manager.dict(
        {
            "curr_question": {
                "text": "Hello and welcome to the AI Cafe Recommender Assistant.\n\
I can recommend a lovely cafe in London based on your preferences.\nClick Next to begin.",
                "type": "single_choice",
                "options": [],
                "default": "None",
            }
        }
    )
    p1 = Process(target=run_expert_system, args=(shared_data,))
    p1.start()
    RecommenderApp().run()
    p1.join()
