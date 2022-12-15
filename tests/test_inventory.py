"""
classes and methods to test the classes specified in inventory.py
"""
import datetime as dt

import pytest

from src.inventory import InventoryType, InventoryItem


class TestInventoryType:
    # Create the inventory types
    solar_panel = InventoryType(
        name="solar_panel",
        expected_deprecation_time=dt.timedelta(days=365 * 5),
    )
    desalination_pump = InventoryType(
        name="desalination_pump",
        expected_deprecation_time=dt.timedelta(days=365 * 4),
    )
    battery = InventoryType(
        name="battery",
        expected_deprecation_time=dt.timedelta(days=365 * 2),
    )
    water_tank = InventoryType(
        name="water_tank",
        expected_deprecation_time=dt.timedelta(days=365 * 10),
    )

    # Set the relationship of the inventory type
    # A water tank can take up to 4 desalination pumps
    # One desalination pump runs at 500kW a battery delivers up to 40kW
    # One solar panel delivers up to 100kW
    water_tank.nominal_input = {
        desalination_pump: 4,
    }
    desalination_pump.nominal_input = {
        battery: 13,
    }
    battery.nominal_input = {
        solar_panel: 5,
    }

    # Methods to test the InventoryType class under the above conditions
    def test_inventory_type_relationship(self):
        assert self.desalination_pump.nominal_input == {
            self.battery: 13,
        }
        assert self.battery.nominal_input == {
            self.solar_panel: 5,
        }
        assert self.water_tank.nominal_input == {
            self.desalination_pump: 4,
        }

    def test_inventory_type_implied_resources(self):
        # Test the implied resources for the water tank on the desalination pump, the battery and the solar panel
        assert self.water_tank.implide_resources(self.desalination_pump) == 4
        assert self.water_tank.implide_resources(self.battery) == 13 * 4
        assert self.water_tank.implide_resources(self.solar_panel) == 5 * 4 * 13


class TestInventoryItem(TestInventoryType):
    # Define the four InventoryTypes
    solar_panel = InventoryType(
        name="solar_panel",
        expected_deprecation_time=dt.timedelta(days=365 * 5),
    )
    desalination_pump = InventoryType(
        name="desalination_pump",
        expected_deprecation_time=dt.timedelta(days=365 * 4),
    )
    battery = InventoryType(
        name="battery",
        expected_deprecation_time=dt.timedelta(days=365 * 2),
    )
    water_tank = InventoryType(
        name="water_tank",
        expected_deprecation_time=dt.timedelta(days=365 * 10),
    )
    water_tank.nominal_input = {
        desalination_pump: 4,
    }
    desalination_pump.nominal_input = {
        battery: 13,
    }
    battery.nominal_input = {
        solar_panel: 5,
    }

    # Define the inventory items
    solar_panel_1 = InventoryItem(
        inventory_type=solar_panel,
        item_name="solar_panel_1",
        price_per_unit=100.0,
        actual_deprecation_time=dt.timedelta(days=365 * 5),
        date_of_investment=dt.date.today(),
    )
    solar_panel_2 = InventoryItem(
        inventory_type=solar_panel,
        name="solar_panel_2",
        price_per_unit=100.0,
        actual_deprecation_time=dt.timedelta(days=365 * 5),
        date_of_investment=dt.date.today(),
    )
    desalination_pump_1 = InventoryItem(
        inventory_type=desalination_pump,
        name="desalination_pump_1",
        price_per_unit=100.0,
        actual_deprecation_time=dt.timedelta(days=365 * 4),
        date_of_investment=dt.date.today(),
    )
    desalination_pump_2 = InventoryItem(
        inventory_type=desalination_pump,
        name="desalination_pump_2",
        price_per_unit=100.0,
        actual_deprecation_time=dt.timedelta(days=365 * 4),
        date_of_investment=dt.date.today(),
    )
    battery_1 = InventoryItem(
        inventory_type=battery,
        name="battery_1",
        price_per_unit=100.0,
        actual_deprecation_time=dt.timedelta(days=365 * 2),
        date_of_investment=dt.date.today(),
    )
    battery_2 = InventoryItem(
        inventory_type=battery,
        name="battery_2",
        price_per_unit=100.0,
        actual_deprecation_time=dt.timedelta(days=365 * 2),
        date_of_investment=dt.date.today(),
    )
    water_tank_1 = InventoryItem(
        inventory_type=water_tank,
        name="water_tank_1",
        price_per_unit=100.0,
        actual_deprecation_time=dt.timedelta(days=365 * 10),
        date_of_investment=dt.date.today(),
    )
    water_tank_2 = InventoryItem(
        inventory_type=water_tank,
        name="water_tank_2",
        price_per_unit=100.0,
        actual_deprecation_time=dt.timedelta(days=365 * 10),
        date_of_investment=dt.date.today(),
    )
    water_tank_3 = InventoryItem(
        inventory_type=water_tank,
        name="water_tank_3",
        price_per_unit=100.0,
        actual_deprecation_time=dt.timedelta(days=365 * 10),
        date_of_investment=dt.date.today(),
    )
    water_tank_4 = InventoryItem(
        inventory_type=water_tank,
        name="water_tank_4",
        price_per_unit=100.0,
        actual_deprecation_time=dt.timedelta(days=365 * 10),
        date_of_investment=dt.date.today(),
    )
    water_tank_5 = InventoryItem(
        name="water_tank_5",
        price_per_unit=100.0,
        actual_deprecation_time=dt.timedelta(days=365 * 10),
        date_of_investment=dt.date.today(),
    )
    water_tank_6 = InventoryItem(
        name="water_tank_6",
        price_per_unit=100.0,
        actual_deprecation_time=dt.timedelta(days=365 * 10),
        date_of_investment=dt.date.today(),
    )

    # Set the relationship of the inventory items
    battery_1.resource_relationship = {
        solar_panel: [solar_panel_1, solar_panel_2],
    }
    battery_2.resource_relationship = {
        solar_panel: [solar_panel_1, solar_panel_2],
    }
    desalination_pump_1.resource_relationship = {battery: [battery_1]}
    desalination_pump_2.resource_relationship = {battery: [battery_2]}
    water_tank_1.resource_relationship = {
        desalination_pump: [desalination_pump_1, desalination_pump_2],
    }
    water_tank_2.resource_relationship = {
        desalination_pump: [desalination_pump_1, desalination_pump_2],
    }
    water_tank_3.resource_relationship = {
        desalination_pump: [desalination_pump_1, desalination_pump_2],
    }
    water_tank_4.resource_relationship = {
        desalination_pump: [desalination_pump_1, desalination_pump_2],
    }
    water_tank_5.resource_relationship = {
        desalination_pump: [desalination_pump_1, desalination_pump_2],
    }
    water_tank_6.resource_relationship = {
        desalination_pump: [desalination_pump_1, desalination_pump_2],
    }

    @pytest.mark.parametrize(
        "inventory_item, expected_capacity",
        [
            (solar_panel_1, 1),
            (solar_panel_2, 1),
            (desalination_pump_1, 1),
            (desalination_pump_2, 1),
            (battery_1, 1),
            (battery_2, 1),
            (water_tank_1, 1),
            (water_tank_2, 1),
            (water_tank_3, 1),
            (water_tank_4, 1),
            (water_tank_5, 1),
            (water_tank_6, 1),
        ],
    )
    def test_capacity(self, inventory_item, expected_capacity):
        assert inventory_item.capacity() == expected_capacity
