"""Command line interface for the association application."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

from .manager import AssociationManager

DEFAULT_STORAGE = Path("associations.json")


def _load_from_file(manager: AssociationManager, path: Path) -> None:
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    for left, rights in data.items():
        manager.add(left)
        for right in rights:
            manager.associate(left, right)


def _save_to_file(manager: AssociationManager, path: Path) -> None:
    path.write_text(json.dumps(manager.to_serializable(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _cmd_add(manager: AssociationManager, item: str, storage: Path) -> None:
    manager.add(item)
    _save_to_file(manager, storage)
    print(f"Added '{item}'.")


def _cmd_associate(manager: AssociationManager, left: str, right: str, storage: Path) -> None:
    manager.associate(left, right)
    _save_to_file(manager, storage)
    print(f"Associated '{left}' with '{right}'.")


def _cmd_show(manager: AssociationManager, item: str) -> None:
    related = manager.related_items(item)
    if related:
        print(f"{item} -> {', '.join(related)}")
    else:
        print(f"No associations found for '{item}'.")


def _cmd_list(manager: AssociationManager) -> None:
    items = manager.items()
    if items:
        for item in items:
            print(f"- {item}")
    else:
        print("No items stored.")


def _cmd_common(manager: AssociationManager, left: str, right: str) -> None:
    common = manager.common_items(left, right)
    if common:
        print(f"Common associations: {', '.join(common)}")
    else:
        print(f"No common associations found between '{left}' and '{right}'.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simple association manager.")
    parser.add_argument(
        "--storage",
        type=Path,
        default=DEFAULT_STORAGE,
        help=f"Path to the JSON file used for persistence (default: {DEFAULT_STORAGE}).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new item to the store.")
    add_parser.add_argument("item", help="Name of the item to add.")

    associate_parser = subparsers.add_parser("associate", help="Associate two items together.")
    associate_parser.add_argument("left", help="Source item.")
    associate_parser.add_argument("right", help="Target item.")

    show_parser = subparsers.add_parser("show", help="Show associations for an item.")
    show_parser.add_argument("item", help="Item whose associations should be listed.")

    subparsers.add_parser("list", help="List all stored items.")

    common_parser = subparsers.add_parser("common", help="Show common associations for two items.")
    common_parser.add_argument("left", help="First item to inspect.")
    common_parser.add_argument("right", help="Second item to inspect.")

    return parser


def execute(manager: AssociationManager, args: argparse.Namespace) -> None:
    storage = args.storage
    _load_from_file(manager, storage)

    if args.command == "add":
        _cmd_add(manager, args.item, storage)
    elif args.command == "associate":
        _cmd_associate(manager, args.left, args.right, storage)
    elif args.command == "show":
        _cmd_show(manager, args.item)
    elif args.command == "list":
        _cmd_list(manager)
    elif args.command == "common":
        _cmd_common(manager, args.left, args.right)
    else:
        raise ValueError(f"Unknown command: {args.command}")


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    manager = AssociationManager()
    execute(manager, args)


if __name__ == "__main__":
    main()
