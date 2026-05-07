from dataclasses import dataclass


@dataclass(slots=True)
class OfflineSettings:
    offline_mode: bool = True
    use_fixtures: bool = True
    enable_live_providers: bool = False
