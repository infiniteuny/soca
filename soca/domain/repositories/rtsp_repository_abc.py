from abc import ABC, abstractmethod


class RtspRepositoryABC(ABC):
    """
    Abstract base livestream repository
    """

    @abstractmethod
    def stream(self, camera_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def capture(self, camera_id: int, duration: int = 5) -> str:
        raise NotImplementedError

    @abstractmethod
    def snapshot(self, camera_id: int) -> str:
        raise NotImplementedError
