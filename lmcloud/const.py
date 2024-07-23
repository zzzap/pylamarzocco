"""Constants for La Marzocco Cloud."""

from enum import IntEnum, StrEnum
from typing import Final


class MachineModel(StrEnum):
    """La Marzocco Coffee Machine Models."""

    GS3_AV = "GS3 AV"
    GS3_MP = "GS3 MP"
    LINEA_MINI = "Linea Mini"
    LINEA_MICRA = "Micra"


class GrinderModel(StrEnum):
    """La Marzocco Grinder Models."""

    PICO = "Pico"


class FirmwareType(StrEnum):
    """La Marzocco updateable firmware components."""

    MACHINE = "machine"
    GATEWAY = "gateway"


class BoilerType(StrEnum):
    """La Marzocco Coffee Machine Boilers."""

    COFFEE = "CoffeeBoiler1"
    STEAM = "SteamBoiler"


class PrebrewMode(StrEnum):
    """Enum for prebrew infusion mode"""

    DISABLED = "Disabled"
    PREBREW = "Enabled"
    PREINFUSION = "TypeB"


class PhysicalKey(IntEnum):
    """Describe the physical keys of the La Marzocco devices."""

    A = 1
    B = 2
    C = 3
    D = 4


class SteamLevel(IntEnum):
    """Enum for steam level."""

    LEVEL_1 = 126
    LEVEL_2 = 128
    LEVEL_3 = 131


class WeekDay(StrEnum):
    """Enum for days of the week."""

    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class SmartStandbyMode(StrEnum):
    """Enum for smart standby mode."""

    LAST_BREWING = "LastBrewing"
    POWER_ON = "PowerOn"


KEYS_PER_MODEL: Final = {
    MachineModel.LINEA_MICRA: 0,
    MachineModel.LINEA_MINI: 0,
    MachineModel.GS3_AV: 4,
    MachineModel.GS3_MP: 0,
}


# Base URL for La Marzocco Cloud
TOKEN_URL: Final = "https://cms.lamarzocco.io/oauth/v2/token"
CUSTOMER_URL: Final = "https://cms.lamarzocco.io/api/customer"
GW_BASE_URL: Final = "https://gw-lmz.lamarzocco.io/v1/home"
GW_MACHINE_BASE_URL: Final = f"{GW_BASE_URL}/machines"
GW_AWS_PROXY_BASE_URL: Final = f"{GW_BASE_URL}/aws-proxy"

DEFAULT_CLIENT_ID: Final = "7_1xwei9rtkuckso44ks4o8s0c0oc4swowo00wgw0ogsok84kosg"
DEFAULT_CLIENT_SECRET: Final = "2mgjqpikbfuok8g4s44oo4gsw0ks44okk4kc4kkkko0c8soc8s"
DEFAULT_PORT: Final = 8081

WEBSOCKET_RETRY_DELAY: Final = 20


# bluetooth
BT_MODEL_PREFIXES: Final = ("MICRA", "MINI", "GS3", "LINEA")
SETTINGS_CHARACTERISTIC: Final = "050b7847-e12b-09a8-b04b-8e0922a9abab"
AUTH_CHARACTERISTIC: Final = "090b7847-e12b-09a8-b04b-8e0922a9abab"
