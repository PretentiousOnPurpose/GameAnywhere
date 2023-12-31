from abc import ABC, abstractmethod
from game_anywhere.include.core.game import html
from itertools import count
from typing import Optional, Dict

ComponentId = str

class Component(ABC):
    components : Dict[ComponentId, 'Component'] = {}
    _next_id = count()

    def __init__(self, id : Optional[ComponentId] = None):
        if id is None:
            while (id := hex(next(Component._next_id))[2:]) in Component.components:
                pass
        else:
            assert id not in Component.components
        Component.components[id] = self
        self.id = id

    @abstractmethod
    def html(self) -> html:
        raise NotImplementedError()
