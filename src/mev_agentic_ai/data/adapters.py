class LiveProviderDisabledError(RuntimeError):
    pass


class ProviderAdapter:
    def fetch(self) -> dict:
        raise LiveProviderDisabledError("Live provider mode is not implemented in scaffold.")
