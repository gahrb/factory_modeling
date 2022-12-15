import datetime as dt
from src.inventory import InventoryType
import unyt as u

# Required units
h = u.Unit("hour")
kw = u.Unit("kilowatt")
m3 = u.Unit("meter") ** 3
liter = u.Unit("decimeter") ** 3
psi = u.Unit("psi")

# Relation
kwh = kw * h
m3ph = m3 / h


def solar_panel_productivity(*args, **kwargs) -> list[u.Unit]:
    return [1000 * kw]


# Required Inventory Types
solar_panel = InventoryType(
    type_name="solar_panel",
    expected_deprecation_time=dt.timedelta(days=365 * 5),
)
solar_panel.system_function = solar_panel_productivity


# def battery_productivity(input_kw: kw) -> list[u.Unit]:
#     return [input_kw / 10 * 7]
#
#
# battery = InventoryType(
#     name="battery",
#     resource_relationship=[10*kw],
#     expected_deprecation_time=dt.timedelta(days=365 * 2),
#     productivity_relation=battery_productivity,
# )


def converter_productivity(input_kw: kw) -> list[u.Unit]:
    return [input_kw / 2]


converter = InventoryType(
    type_name="converter",
    nominal_input=[],
    expected_deprecation_time=dt.timedelta(days=365 * 5),
)
converter.system_function = converter_productivity


def m03_g_productivity(input_kw: kw) -> list[u.Unit]:
    if input_kw < 10:
        return [0 * psi, 0 * m3ph]
    return [1000.0 * psi, 11.7 * liter * 60 / h]


saltwater_pump = InventoryType(
    type_name="M03-G Wanner Pump",
    nominal_input=[0.2025 * kw],
    expected_deprecation_time=dt.timedelta(days=365 * 3),
)
saltwater_pump.system_function = m03_g_productivity


def flexedr_e150_productivity(
    input_kw: kw, input_m3_hr: m3ph, input_psi: psi
) -> [u.Unit]:
    if input_kw < 1132.23 or input_psi < 45:
        return [0 * m3ph]
    return [min(input_m3_hr, 9.75 * m3ph)]


desalination_membrane = InventoryType(
    type_name="FlexEDR E150",
    nominal_input=[
        45 * psi,
        9.75 * m3ph,  # 234 / 24,
        1132.23 * kw,  # 8.03 * 2.35 * 60,
    ],
    expected_deprecation_time=dt.timedelta(days=365 * 4),
)
desalination_membrane.system_function = flexedr_e150_productivity

# def water_tank_productivity(input_m3ph: m3ph, input_duration: h) -> [u.Unit]:
#     return [input_m3ph * input_duration]
#
#
# water_tank = InventoryType(
#     name="water_tank",
#     resource_relationship=[1000*m3ph],
#     productivity_relation=water_tank_productivity,
#     expected_deprecation_time=dt.timedelta(days=365 * 10),
# )
