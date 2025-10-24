"""Core logic for managing associations between items."""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Set


class AssociationManager:
    """Stores and queries relationships between items.

    The manager keeps a bidirectional association graph, meaning that when
    ``associate("a", "b")`` is called, ``"a"`` is linked to ``"b"`` and vice
    versa. Associations are stored case sensitively to keep the behaviour
    predictable for CLI users.
    """

    def __init__(self) -> None:
        self._associations: Dict[str, Set[str]] = defaultdict(set)

    def add(self, item: str) -> None:
        """Ensure ``item`` exists in the association graph."""

        if not item:
            raise ValueError("Item name cannot be empty.")
        self._associations.setdefault(item, set())

    def associate(self, left: str, right: str) -> None:
        """Create a bidirectional association between ``left`` and ``right``.

        Raises
        ------
        ValueError
            If either ``left`` or ``right`` is empty or if both refer to the
            same item.
        """

        if not left or not right:
            raise ValueError("Both items must be provided for an association.")
        if left == right:
            raise ValueError("Cannot associate an item with itself.")

        self.add(left)
        self.add(right)

        self._associations[left].add(right)
        self._associations[right].add(left)

    def disassociate(self, left: str, right: str) -> bool:
        """Remove the association between ``left`` and ``right`` if present."""

        removed = False
        if left in self._associations and right in self._associations[left]:
            self._associations[left].remove(right)
            removed = True
        if right in self._associations and left in self._associations[right]:
            self._associations[right].remove(left)
            removed = True
        return removed

    def related_items(self, item: str) -> List[str]:
        """Return a sorted list of items associated with ``item``."""

        return sorted(self._associations.get(item, set()))

    def items(self) -> List[str]:
        """Return all items known to the manager."""

        return sorted(self._associations)

    def import_associations(self, pairs: Iterable[Iterable[str]]) -> None:
        """Load multiple associations from an iterable of pairs."""

        for pair in pairs:
            left, right = pair
            self.associate(left, right)

    def common_items(self, left: str, right: str) -> List[str]:
        """Return sorted list of items associated with both ``left`` and ``right``."""

        left_set = set(self._associations.get(left, set()))
        right_set = set(self._associations.get(right, set()))
        return sorted(left_set.intersection(right_set))

    def to_serializable(self) -> Dict[str, List[str]]:
        """Return a JSON-serialisable representation of the graph."""

        return {item: sorted(associations) for item, associations in self._associations.items()}
