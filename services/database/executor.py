"""
On It Database Service - Executor Class

Provides a data integrity layer for table operations with pre- and post-processing.

The Executor class is responsible for creating, getting, filtering, updating, and deleting records
in the database. It uses pre- and post-processors to handle data before and after the operation.
"""

from components.preprocessors import PreProcessor
from components.postprocessors import PostProcessor
from services.database.table import Table


class TableExecutor():
    """Provides a data integrity layer for table operations with pre- and post-processing"""

    def __init__(self, table):
        self.table = table

    def all(
        self,
        select_related=None,
        prefetch_related=None,
        processor="Table:Get:MultipleRecords",
        post_processor=None
    ):
        """Method to get all records"""
        # Delegate to table
        data = self.table.all(select_related, prefetch_related)

        # Post-processing
        post_processor = post_processor if post_processor else processor
        if post_processor:
            post_processor = PostProcessor.get_processor(
                implementation=post_processor, table=self.table
            )
            if post_processor:
                data = post_processor.process(data)

        return data

    def create(self, item, processor="Table:Create", pre_processor=None, post_processor=None):
        """Method to create a record"""
        # Pre-processing
        pre_processor = pre_processor if pre_processor else post_processor or processor
        if pre_processor:
            pre_processor = PreProcessor.get_processor(
                implementation=pre_processor, table=self.table
            )
            if pre_processor:
                pre_processor.process(item)

        # Delegate to table
        instance = self.table.create(item)

        # Post-processing
        post_processor = post_processor if post_processor else pre_processor or processor
        if post_processor:
            post_processor = PostProcessor.get_processor(
                implementation=post_processor, table=self.table
            )
            if post_processor:
                instance = post_processor.process(instance.id, item)

        return instance

    def get(self, query, processor="Table:Get:SingleRecord", post_processor=None):
        """Method to get records"""
        # Delegate to table
        instance = self.table.get(query)

        # Post-processing
        post_processor = post_processor if post_processor else processor
        if post_processor:
            post_processor = PostProcessor.get_processor(
                implementation=post_processor, table=self.table
            )
            if post_processor:
                instance = post_processor.process(instance.id, instance)

        return instance

    def filter(
        self,
        query,
        select_related=None,
        prefetch_related=None,
        processor="Table:Get:MultipleRecords",
        post_processor=None
    ):
        """Method to filter records"""
        # Delegate to table
        data = self.table.filter(query, select_related, prefetch_related)

        # Post-processing
        post_processor = post_processor if post_processor else processor
        if post_processor:
            post_processor = PostProcessor.get_processor(
                implementation=post_processor, table=self.table
            )
            if post_processor:
                data = post_processor.process(data)

        return data

    def update(
        self,
        query,
        item,
        reason=None,
        processor="Table:Update",
        pre_processor=None,
        post_processor=None
    ):
        """Method to update records"""
        # Pre-processing
        pre_processor = pre_processor if pre_processor else post_processor or processor
        if pre_processor:
            pre_processor = PreProcessor.get_processor(
                implementation=pre_processor, table=self.table
            )
            if pre_processor:
                pre_processor.process(item)

        # Delegate to table
        instance = self.table.update(query, item, reason)

        # Post-processing
        post_processor = post_processor if post_processor else pre_processor or processor
        if post_processor:
            post_processor = PostProcessor.get_processor(
                implementation=post_processor, table=self.table
            )
            if post_processor:
                instance = post_processor.process(
                    instance=instance.id,
                    item=item,
                    reason=reason if reason else "Update"
                )

        return instance

    def delete(self, query, processor="Table:Delete", pre_processor=None):
        """Method to delete records"""
        # Pre-processing
        pre_processor = pre_processor if pre_processor else processor
        if pre_processor:
            pre_processor = PreProcessor.get_processor(
                implementation=pre_processor, table=self.table
            )
            if pre_processor:
                pre_processor.process(query)

        # Delegate to table
        self.table.delete(query)
