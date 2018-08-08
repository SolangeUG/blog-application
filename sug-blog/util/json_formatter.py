import json


def format_entry_as_json(entry):
    """
    Return a blog entry in a JSON format
    :param entry: input blog
    :return: JSON format of the entry
    """
    if entry:
        entry_as_json = {"subject": entry.subject, "content": entry.content,
                         "date": entry.created.strftime('%b %d, %Y - %H:%M')}
        return json.dumps(entry_as_json, indent=4, separators=(',', ':'))
    else:
        return json.dumps({"subject": "", "content": "", "date": ""}, indent=4)
