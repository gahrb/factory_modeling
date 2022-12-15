#!/usr/bin/python3.11
import datetime as dt

from default_types import (
    solar_panel,
    # battery,
    desalination_membrane,
    # water_tank,
    saltwater_pump,
    converter,
    kw,
)
from src.inventory import InventoryItem, FactoryUnitInventory


def main():

    # Define the inventory items
    solar_panel_1 = InventoryItem(
        item_name="solar_panel_1",
        inventory_type=solar_panel,
        type_name=solar_panel.type_name,
        price_per_unit=solar_panel.system_function([])[0] / kw,  # 1$/kw
        actual_deprecation_time=dt.timedelta(days=365 * 5),
        date_of_investment=dt.date.today(),
    )

    # battery_1 = InventoryItem(
    #     item_name="battery_1",
    #     inventory_type=battery,
    #     price_per_unit=123.0,
    #     date_of_investment=dt.date.today(),
    #     input_connections=[
    #         solar_panel_1,

    #     ],
    # )

    converter_1 = InventoryItem(
        item_name="converter_1",
        inventory_type=converter,
        type_name=converter.type_name,
        price_per_unit=15000.0,
        date_of_investment=dt.date.today(),
        input_connections=[
            solar_panel_1,
        ],
    )
    # Post assignment of converter input. CHANGE THIS
    converter_1.inventory_type.nominal_input = [solar_panel.system_function()[0]]

    saltwater_pump_1 = InventoryItem(
        inventory_type=saltwater_pump,
        type_name=saltwater_pump.type_name,
        item_name="saltwater_pump_1",
        price_per_unit=1500.0,
        date_of_investment=dt.date.today(),
        input_connections=[
            solar_panel_1,
        ],
    )
    desalination_membrane_1 = InventoryItem(
        inventory_type=desalination_membrane,
        type_name=desalination_membrane.type_name,
        item_name="desalination_membrane_1",
        price_per_unit=1_843_792,
        actual_deprecation_time=dt.timedelta(days=365 * 4),
        date_of_investment=dt.date.today(),
        input_connections=[
            solar_panel_1,
            saltwater_pump_1,
        ],
    )
    # water_tank_1 = InventoryItem(
    #     inventory_type=water_tank,
    #     item_name="water_tank_1",
    #     price_per_unit=373.0 *,
    #     actual_deprecation_time=dt.timedelta(days=365 * 10),
    #     date_of_investment=dt.date.today(),
    #     input_connections=[desalination_membrane_1],
    # )

    factory_1 = FactoryUnitInventory(
        unit_name="factory_1",
        inventory_output_items=[
            # water_tank_1,
            converter_1,
            desalination_membrane_1,
        ],
    )

    # Perform some capacity calculations:
    print(
        f"Solar panels: {solar_panel_1.item_name}, "
        f"with required input: {solar_panel_1.inventory_type.nominal_input}, "
        f"With capacity: {solar_panel_1.get_capacity()}"
    )
    print(
        f"Converter: {converter_1.item_name}, "
        f"with required input: {converter_1.inventory_type.nominal_input}, "
        f"With capacity: {converter_1.get_capacity()}"
    )
    print(
        f"Saltwater pump: {saltwater_pump_1.item_name}, "
        f"with required input: {saltwater_pump_1.inventory_type.nominal_input}, "
        f"With capacity: {saltwater_pump_1.get_capacity()}"
    )
    print(
        f"Desalination Membrane: {desalination_membrane_1.item_name}, "
        f"with required input: {desalination_membrane_1.inventory_type.nominal_input}, "
        f"With capacity: {desalination_membrane_1.get_capacity()}"
    )

    print(
        f"Factory: {factory_1.unit_name}, "
        f"with capacity: {factory_1.get_capacity()} "
        f"and total cost: {factory_1.get_total_cost():,.2f}"
    )


if __name__ == "__main__":
    main()
