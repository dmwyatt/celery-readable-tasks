import json
from typing import Callable

from pkg_resources import resource_stream
import random

from celery import Task

animals = json.loads(resource_stream(__name__, 'animals.json').read().decode('utf-8'))
adjectives = json.loads(resource_stream(__name__, 'adjectives.json').read().decode('utf-8'))
verbs = json.loads(resource_stream(__name__, 'verbs.json').read().decode('utf-8'))

def unique_str():
	return '{adj1}{adj2}{animal}{verb}'.format(adj1=random.choice(adjectives).capitalize(),
	                                             adj2=random.choice(adjectives).capitalize(),
	                                             animal=random.choice(animals).capitalize(),
	                                             verb=random.choice(verbs).capitalize())

class ReadableTask(Task):
	def __init__(self, id_generator: Callable[[], str]=unique_str):
		self.generate_id = id_generator

	def apply_async(self, *args, **kwargs):
		kwargs.setdefault('task_id', self.generate_id())
		return super(ReadableTask, self).apply_async(*args, **kwargs)

	def s(self, *args, **kwargs):
		ret = super(ReadableTask, self).s(*args, **kwargs)
		ret.set(task_id=self.generate_id())
		return ret

	def si(self, *args, **kwargs):
		ret = super(ReadableTask, self).si(*args, **kwargs)
		ret.set(task_id=self.generate_id())
		return ret