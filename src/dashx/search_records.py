"""Builder for searchRecords API options."""

from typing import Any, Callable, Dict, List, Optional


class SearchRecordsInputBuilder:
    """
    Fluent builder for searchRecords options. Call .all() or .one() to execute.
    """

    def __init__(
        self,
        resource: str,
        callback: Callable[[Dict[str, Any]], Any],
    ):
        self._resource = resource
        self._callback = callback
        self._options = {'resource': resource}

    def limit(self, by: Optional[int]) -> 'SearchRecordsInputBuilder':
        self._options['limit'] = by
        return self

    def filter(self, by: Optional[Dict[str, Any]]) -> 'SearchRecordsInputBuilder':
        self._options['filter'] = by if by is not None else {}
        return self

    def order(self, by: Optional[List[Dict[str, Any]]]) -> 'SearchRecordsInputBuilder':
        self._options['order'] = by
        return self

    def language(self, to: Optional[str]) -> 'SearchRecordsInputBuilder':
        self._options['language'] = to
        return self

    def fields(self, identifiers: Optional[List[str]]) -> 'SearchRecordsInputBuilder':
        self._options['fields'] = identifiers
        return self

    def include(self, identifiers: Optional[List[str]]) -> 'SearchRecordsInputBuilder':
        self._options['include'] = identifiers
        return self

    def exclude(self, identifiers: Optional[List[str]]) -> 'SearchRecordsInputBuilder':
        self._options['exclude'] = identifiers
        return self

    def preview(self, value: bool = True) -> 'SearchRecordsInputBuilder':
        self._options['preview'] = value
        return self

    def all(self, with_options: Optional[Dict[str, Any]] = None) -> Any:
        opts = dict(self._options)
        if with_options:
            opts.update(with_options)
        return self._callback(opts)

    def one(self, with_options: Optional[Dict[str, Any]] = None) -> Any:
        opts = dict(self._options)
        if with_options:
            opts.update(with_options)
        data = self._callback(opts)
        if isinstance(data, list) and len(data) > 0:
            return data[0]
        return None
