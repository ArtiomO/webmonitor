import abc
import typing as tp


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    async def save(self, instance):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_list(self) -> tp.List[any]:
        raise NotImplementedError
