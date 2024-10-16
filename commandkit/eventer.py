from typing import Callable, Any

class Eventer(object):
	def __init__(self,events={}):
		self.extra_events: dict[str, list[Callable]] = events

	def dispatch(self, event_name: str, /, *args, **kwargs):
		ev = "on_" + event_name
		for event in self.extra_events.get(ev, []):
			self.schedule_event(event, ev, *args, **kwargs)

	def schedule_event(self,event, ev,  /,*args,**kwargs):
		return event(*args, **kwargs)

	def add_listen(self, func: Callable, name: str=None):
		return self.listen(name=name)(func)

	def remove_listen(self, func: Callable, name: str=None):
			name = func.__name__ if name is None else name
			if name in self.extra_events:
				try:
					self.extra_events[name].remove(func)
				except ValueError:
					pass

	def listen(self, *args, **kw):
		def inner(func):
			name = kw.get("name",None)
			name = func.__name__ if name is None else name
			if name in self.extra_events:
				self.extra_events[name].append(func)
			else:
				self.extra_events[name] = [func]
		return inner

	def event(self,func: Callable):
		return self.listen()(func)


