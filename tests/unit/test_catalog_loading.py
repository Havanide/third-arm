from third_arm.domain.object_model import clear_object_catalog_cache, get_object, load_object_catalog
from third_arm.domain.slot_model import clear_slot_catalog_cache, get_slot, load_handover_zone, load_slot_catalog


def setup_function():
    clear_object_catalog_cache()
    clear_slot_catalog_cache()


def test_load_slot_catalog_from_default_yaml():
    slots = load_slot_catalog()
    assert 'slot_A' in slots
    assert slots['slot_A'].enabled is True


def test_load_handover_zone_from_default_yaml():
    zone = load_handover_zone()
    assert zone.label == 'Operator handover point'
    assert zone.clearance_radius_mm == 80


def test_load_object_catalog_from_default_yaml():
    objects = load_object_catalog()
    assert 'obj_mug_ceramic' in objects
    assert objects['obj_mug_ceramic'].default_slot == 'slot_B'


def test_lookup_helpers_use_yaml_catalogues():
    assert get_slot('slot_B') is not None
    assert get_object('obj_tablet_ipad') is not None
