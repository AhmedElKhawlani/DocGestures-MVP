#!/usr/bin/python3

def get_text_from_text_widget(widget, pos):
    if pos == -1:
        return widget.get("1.0", "end") + "'"
    return "'" + widget.get("1.0", "end") + "', "


def get_text_from_entry_widget(widget, pos):
    if pos == -1:
        return widget.get() + "'"
    return "'" + widget.get() + "', "
