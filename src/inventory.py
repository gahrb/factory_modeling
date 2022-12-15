from __future__ import annotations

import copy
import datetime as dt
from abc import abstractmethod
from typing import Callable

import uuid
from dataclasses import dataclass, field
import logging
import unyt as u

logger = logging.getLogger(__name__)


def unit_list_to_dict(unit_list: list[u.Unit]) -> dict[str, u.Unit]:
    if len(unit_list):
        return {
            f"input_{str(item.units.expr).replace('/', '_').replace('**', '').lower()}":
                item for item in unit_list
        }
    return {}


@dataclass
class InventoryType:
    """
    Class for defining an inventory type.
    An inventory type is a resource that can be used to operate a factory. It is defined by a name, the resources
    required to operate it (Units class), the resources that are produced (Units class), and the
    expected deprecation time.
    """
    type_name: str
    type_id: uuid.uuid4 = uuid.uuid4()
    nominal_input: list[u.Unit] = field(default_factory=list)
    expected_deprecation_time: dt.timedelta = dt.timedelta(days=365 * 4)
    cache = {}  # make the machine stateful

    @abstractmethod
    def system_function(self, *args, **kwargs) -> list[u.Unit]:
        raise NotImplementedError("system_function must be initialized")

    def __hash__(self):
        return hash(self.type_id)


@dataclass
class InventoryItem(InventoryType):
    """
    Class for the actual physical inventory item.
    An InventoryItem inherits from InventoryType and consists of a name, a unique identifier, a price per item,
    its connections to other inventory items, the actual deprecation time, and the date of investment.
    An InventoryItem is a node in a graph. The input_connections define the children, the output_connections define
    the parents of the node.
    """
    inventory_type: InventoryType = field(default_factory=InventoryType)
    item_name: str = field(default_factory=str)
    inventory_item: uuid.uuid4 = uuid.uuid4()
    price_per_unit: float = 0.0
    actual_deprecation_time: dt.timedelta = dt.timedelta(days=4 * 365)
    date_of_investment: dt.date = dt.date.today()
    input_connections: list = field(default_factory=list)
    end_of_operation: dt.date = None

    def __post_init__(self):
        super().__init__(
            self.inventory_type
        )
        self.item_name = self.inventory_type.type_name + "-" + str(self.inventory_item)[:4]
        self.input_connections: list[InventoryItem]

    def __hash__(self):
        return hash(self.inventory_item)

    def duplicate(self, item_name: str):
        new_item = copy.deepcopy(self)
        new_item.item_name = item_name
        return new_item

    def get_capacity(self) -> list[u.Unit]:
        """
        A recursive function showing at how much capacity the inventory item can be used based on the
        nominal_input of the InventoryItem. The input-output relationship is defined via the inventory_type's
        resource_relationship function. The capacity is calculated by subtracting the output of resource_relationship()
        from the output run under nominal_input conditions. The remaining InventorType's production capacity limits
        the capacity. No negative capacity is allowed, non-existing input_connections lead to full capacity.
        """

        required_resources = copy.deepcopy(self.inventory_type.nominal_input)
        # nominal_output = self.inventory_type.system_function(**unit_list_to_dict(required_resources))

        given_resources = []
        for child_inventory_item in self.input_connections:
            for value in child_inventory_item.get_capacity():
                required_indices = [x.units.get_base_equivalent() for x in required_resources]
                if value.units.get_base_equivalent() not in required_indices:
                    logger.warning(
                        f"{child_inventory_item.item_name} has {value.units} as production output which is not a "
                        f"required resource for the connected {self.item_name}."
                    )
                    continue
                required_index = required_indices.index(value.units.get_base_equivalent())

                given_indices = [x.units.get_base_equivalent() for x in given_resources]
                if value.units.get_base_equivalent() not in given_indices:
                    # Unit has not yet been added to the given resources. We append it.
                    given_resources.append(min(value, required_resources[required_index]))
                    continue

                given_index = given_indices.index(value.units.get_base_equivalent())
                given_resources[given_index] += min(
                    value,
                    required_resources[required_index] - given_resources[given_index]
                )
        return self.inventory_type.system_function(**unit_list_to_dict(given_resources))

    def get_cost(self, start_date: dt.date = None, end_date: dt.date = None) -> float:
        """
        Returns the cost of the inventory item.
        """
        if not start_date:
            start_date = self.date_of_investment
        if not end_date:
            end_date = dt.date.today()
        total_cost = 0.0
        for child_inventory_item in self.input_connections:
            total_cost += child_inventory_item.get_cost(
                start_date=start_date, end_date=end_date
            )
        if start_date <= self.date_of_investment <= end_date:
            total_cost += self.price_per_unit
        return total_cost


@dataclass
class FactoryUnitInventory:
    """
    The FactoryUnitInventory class represents the inventory of a unit. It is a collection of InvventoryItems and has
    functions to add items, look up each inventory item and check for its existence, calculate the unit's productivity,
    calculate the unit's entire cost, and return the active items at a given date.
    It can further return the expected replacement date for an inventory item.
    """

    unit_name: str
    inventory_output_items: list[InventoryItem] = field(default_factory=list)
    unit_inventory: uuid.uuid4 = uuid.uuid4()
    date_of_construction: dt.date = dt.date.today()

    def get_capacity(self) -> list[u.Unit]:
        """
        Calculates the capacity of the unit inventory.
        """
        capacity = []
        for inventory_item in self.inventory_output_items:
            item_capacity = inventory_item.get_capacity()
            # Find indices of the item's capacity and add them.
            capacity_units = [x.units for x in capacity]
            for value in item_capacity:
                unit = value.units
                if unit not in capacity_units:
                    capacity.append(value)
                else:
                    index = capacity_units.index(unit)
                    capacity[index] += value
        return capacity

    def get_total_cost(
            self, start_date: dt.date = None, end_date: dt.date = None
    ) -> float:
        """
        Calculates the total cost of the unit inventory. Can be filtered by a start and end date.
        """
        if not start_date:
            start_date = self.date_of_construction
        if not end_date:
            end_date = dt.date.today()
        total_cost = 0.0
        for inventory_item in self.inventory_output_items:
            total_cost += inventory_item.get_cost(
                start_date=start_date, end_date=end_date
            )
        return total_cost

    def active_items(self, date: dt.date = None) -> list[InventoryItem]:
        """
        Returns the active items of the unit inventory at a given date.
        """
        if date is None:
            date = dt.date.today()
        active_items = []
        for inventory_item in self.inventory_output_items:
            if date <= inventory_item.date_of_investment:
                active_items.append(inventory_item)
        return active_items
