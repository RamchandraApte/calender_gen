import argparse, logging, re, itertools, ics, arrow
def chunks(x, n):
	for i in range(0, len(x), n):
		yield x[i:i+n]
def not_empty(s):
	return not all(map(str.isspace, s))

logging.basicConfig(level = logging.DEBUG, format = "%(filename)s:%(funcName)s:%(lineno)s %(message)s")

# Calendar parsing functions produce ics.Calendar object from texts copy-pasted from websites

arrow_cfg = dict(tzinfo = arrow.now().tzinfo)

def class_cal(sched):
	cal = ics.Calendar()
	rows = re.split(r"(^\d{2}:\d{2}$)", sched, flags = re.MULTILINE)
	dates = [23,24,25,26,
			23,24,25,26,
			27,
			23,25,
			25,
			27,
			25]
			
	idx = 0
	for row in rows[2::2]:
		row = tuple(filter(not_empty, row.splitlines()))
		for name, full_name, type_, duration, location in chunks(row, 5):
			def parse_time(time_str):
				nonlocal idx
				time = arrow.get(f"{dates[idx]} {time_str}", "D HH:mm", **arrow_cfg)
				return time.replace(**{attr: getattr(arrow.now(), attr) for attr in ("year", "month")})
			begin, end = map(parse_time, duration.replace(" ", "").split("-"))
			idx+=1
			logging.debug(name)
			logging.debug(begin.humanize())
			cal.events.add(ics.Event(name=name+"\n"+full_name, begin = begin, end = end, location = location))
		logging.debug("\n")
	return cal

def eecs_lab_cal(sched):
	cal = ics.Calendar()
	for class_ in chunks(sched.splitlines(), 6):
		logging.debug(class_)
		cal.events.add(ics.Todo(name = class_[1][10:], due = arrow.get(class_[4][4:], "DD MMM YYYY hh:mm:ss a", **arrow_cfg)))
	return cal

def main():
	for type_ in ("class", "eecs_lab"):
		with open(f"{type_}.txt") as in_file, open(f"{type_}.cal", "w") as out_file:
			print(globals()[f"{type_}_cal"](in_file.read()), file = out_file)

if __name__=="__main__":
	main()
