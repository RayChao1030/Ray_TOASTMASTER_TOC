from transitions import Machine
from transitions.extensions import GraphMachine
from flask import Flask, jsonify, request, abort, send_file
try:
    import pygraphviz as pgv
except ImportError:
    raise
import requests
machine = TocMachine(
    states=["user", "menu","chinese", "english", "C_indroduction", "C_join","C_time", "C2_requirement","C2_recentactivity","show_fsm_photo","E_indroduction", "E_join","E_time", "E2_requirement","E2_recentactivity"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        { #2-1
            "trigger": "advance",
            "source": "menu",
            "dest": "chinese",
            "conditions": "is_going_to_chinese",
        },
        { #2-2
            "trigger": "advance",
            "source": "menu",
            "dest": "english",
            "conditions": "is_going_to_english",
        },
        { #3-1-1
            "trigger": "advance",
            "source": "chinese",
            "dest": "C_indroduction",
            "conditions": "is_going_to_C_indroduction",
        },
        { #3-1-2
            "trigger": "advance",
            "source": "chinese",
            "dest": "C_join",
            "conditions": "is_going_to_C_join",
        },
        { #3-1-3
            "trigger": "advance",
            "source": "chinese",
            "dest": "C_time",
            "conditions": "is_going_to_C_time",
        },
        { #4-1-1-1
            "trigger": "advance",
            "source": "C_indroduction",
            "dest": "C2_requirement",
            "conditions": "is_going_to_C2_requirement",
        },
        { #4-1-1-2
            "trigger": "advance",
            "source": "C_indroduction",
            "dest": "C2_recentactivity",
            "conditions": "is_going_to_C2_recentactivity",
        },
        { #4-1-2-1
            "trigger": "advance",
            "source": "C_join",
            "dest": "C2_requirement",
            "conditions": "is_going_to_C2_requirement",
        },
        { #4-1-2-2
            "trigger": "advance",
            "source": "C_join",
            "dest": "C2_recentactivity",
            "conditions": "is_going_to_C2_recentactivity",
        },
        { #4-3-1
            "trigger": "advance",
            "source": "C_time",
            "dest": "C2_requirement",
            "conditions": "is_going_to_C2_requirement",
        },
        { #4-3-2
            "trigger": "advance",
            "source": "C_time",
            "dest": "C2_recentactivity",
            "conditions": "is_going_to_C2_recentactivity",
        },
        { #3-2-1
            "trigger": "advance",
            "source": "english",
            "dest": "E_indroduction",
            "conditions": "is_going_to_E_indroduction",
        },
        { #3-2-2
            "trigger": "advance",
            "source": "english",
            "dest": "E_join",
            "conditions": "is_going_to_E_join",
        },
        { #3-2-3
            "trigger": "advance",
            "source": "english",
            "dest": "E_time",
            "conditions": "is_going_to_E_time",
        },
        { #4-1-1
            "trigger": "advance",
            "source": "E_indroduction",
            "dest": "E2_requirement",
            "conditions": "is_going_to_E2_requirement",
        },
        { #4-1-2
            "trigger": "advance",
            "source": "E_indroduction",
            "dest": "E2_recentactivity",
            "conditions": "is_going_to_E2_recentactivity",
        },
        { #4-2-1
            "trigger": "advance",
            "source": "E_join",
            "dest": "E2_requirement",
            "conditions": "is_going_to_E2_requirement",
        },
        { #4-2-2
            "trigger": "advance",
            "source": "E_join",
            "dest": "E2_recentactivity",
            "conditions": "is_going_to_E2_recentactivity",
        },
        { #4-3-1
            "trigger": "advance",
            "source": "E_time",
            "dest": "E2_requirement",
            "conditions": "is_going_to_E2_requirement",
        },
        { #4-3-2
            "trigger": "advance",
            "source": "E_time",
            "dest": "E2_recentactivity",
            "conditions": "is_going_to_E2_recentactivity",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "show_fsm_photo",
            "conditions": "is_going_to_show_fsm_photo",
        },
        {"trigger": "go_back", "source": ["menu","chinese","english","C_indroduction","C_join","C_time","C2_requirement","C2_recentactivity","show_fsm_photo","E_indroduction", "E_join","E_time", "E2_requirement","E2_recentactivity"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)
machine.get_graph().draw("fsm.png", prog="dot", format="png")
