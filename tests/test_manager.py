import pytest

from association_app.manager import AssociationManager


def test_associate_creates_bidirectional_link():
    manager = AssociationManager()
    manager.associate("Python", "Programlama")

    assert manager.related_items("Python") == ["Programlama"]
    assert manager.related_items("Programlama") == ["Python"]


def test_disassociate_removes_links():
    manager = AssociationManager()
    manager.associate("A", "B")

    assert manager.disassociate("A", "B") is True
    assert manager.related_items("A") == []
    assert manager.related_items("B") == []


def test_common_items():
    manager = AssociationManager()
    manager.associate("Elma", "Meyve")
    manager.associate("Armut", "Meyve")
    manager.associate("Elma", "Tatli")

    assert manager.common_items("Elma", "Armut") == ["Meyve"]


def test_prevents_self_association():
    manager = AssociationManager()
    with pytest.raises(ValueError):
        manager.associate("A", "A")


def test_import_associations():
    manager = AssociationManager()
    manager.import_associations([["A", "B"], ("B", "C")])

    assert manager.common_items("A", "C") == ["B"]
