import dateutil.parser
import bisect
import datetime

ONE_DAY = datetime.timedelta(days=1)

with open("is_playing.log", "r") as f:
    lines = f.readlines()

times = []
vals = []
for line in lines:
    sp = line.split("|")
    t = dateutil.parser.parse(sp[0])
    v = sp[1].strip() == "true"
    times.append(t)
    vals.append(v)

def was_playing(t):
    i = bisect.bisect(times, t)
    if i == 0:
        return False
    return vals[i-1]

# Get frequency of music playing vs time of day
for hours in xrange(24):
    for minutes in xrange(60):
        c = 0
        date = datetime.datetime(2015, 4, 1, hours, minutes)
        while date < datetime.datetime(2015, 8, 1):
            if was_playing(date):
                c += 1
            date += ONE_DAY
        print("%02d:%02d,%d" % (hours, minutes, c))

# Get frequency of music playing vs day of week
import collections
dwmap = collections.defaultdict(int)
for hours in xrange(24):
    for minutes in xrange(60):
        date = datetime.datetime(2015, 4, 1, hours, minutes)
        while date < datetime.datetime(2015, 8, 1):
            if was_playing(date):
                dwmap[date.weekday()] += 1
            date += ONE_DAY
day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
for dow in dwmap:
    print("%s,%d" % (day_names[dow], dwmap[dow]))
