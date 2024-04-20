from copy import deepcopy
from dataclasses import asdict
from json import dump, loads
from typing import Any
from uuid import uuid4

from alive_progress import alive_bar as abr
from consts import DEST, DESTM, RAW_DB, Status, pprint
from dacite import from_dict
from librensetsu.formatter import remove_empty_keys
from librensetsu.models import Date, MediaInfo, RelationMaps


def process_item(item: Any, old_uuid: str | None = None) -> MediaInfo:
    """
    Process the item to MediaInfo object
    :param item: The item to process
    :type item: Any
    :param old_uuid: The old UUID to replace
    :type old_uuid: str | None
    :return: The processed item
    :rtype: MediaInfo
    """
    # import logic here
    return MediaInfo(
        uuid=old_uuid or str(uuid4()),
    )


def lookup_uuid(items: list[Any], old_items: list[Any]) -> list[MediaInfo]:
    """
    Lookup the UUID of the items
    :param items: The items to lookup
    :type items: list[Any]
    :param old_items: The old items to lookup
    :type old_items: list[Any]
    :param lookup_key: The lookup key
    :type lookup_key: str
    :return: The list of MediaInfo
    :rtype: list[MediaInfo]
    """
    loi = len(old_items)
    new_data: list[MediaInfo] = []
    pprint.print(Status.INFO, "Processing items")
    with abr(total=len(items)) as bar:  # type: ignore
        for item in items:
            bar()
            media_id = item.media_id
            # Edit         ^^^^^^^^^
            uuid = None
            if loi > 0:
                for old_item in old_items:
                    if media_id == old_item["mappings"][""]:
                        # Edit                         ^^^^
                        uuid = old_item["uuid"]
                        break
            final = process_item(item, uuid)
            new_data.append(final)
    return new_data


def dump_json(final_data: list[dict[str, Any]]) -> None:
    """
    Dump the JSON file
    :param final_data: The final data to dump
    :type final_data: list[dict[str, Any]]
    """
    pprint.print(Status.INFO, f"Dumping JSON file to {DEST}")
    with open(DEST, "w") as f:
        dump(final_data, f, ensure_ascii=False)
    pprint.print(Status.INFO, f"Dumping Minified JSON file to {DESTM}")
    mininfo = remove_empty_keys(deepcopy(final_data))  # type: ignore
    with open(DESTM, "w") as f:
        dump(mininfo, f, ensure_ascii=False)


def do_loop() -> list[MediaInfo]:
    """
    Loops all the object to convert as a list of MediaInfo
    :return: List of `MediaInfo`
    :rtype: MediaInfo
    """
    try:
        with open(DEST, "r") as f:
            old_data: list[dict[str, Any]] = loads(f.read())
    except FileNotFoundError:
        old_data = []
    with open(RAW_DB, "r") as f:
        data = loads(f.read())
    final_data = lookup_uuid(data, old_data)
    new_data = [asdict(x) for x in final_data]
    # sort
    pprint.print(Status.INFO, "Sorting data")
    new_data.sort(key=lambda x: x["mappings"][""])  # type: ignore
    #                           EDIT         ^^^^
    dump_json(new_data)
    return final_data
