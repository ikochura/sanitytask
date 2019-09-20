from calendar import HTMLCalendar

from permission import get_user_permission_object


class ContestCalendar(HTMLCalendar):

    def formatmonth(self, theyear, themonth, user, withyear=True):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="table">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, theyear, themonth, user))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def formatweek(self, theweek, theyear, themonth, user):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, theyear, themonth, user) for (d, wd) in theweek)
        return '<tr align="center">%s</tr>' % s

    def formatday(self, day, weekday, year, month, user):
        """
        Return a day as a table cell.
        """
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            perm = get_user_permission_object(user)

            if perm.get_alarm_check(year, month, day, user):
                td_srt = '<td class="%s alert alert-danger " align="center">%s</td>'
            else:
                td_srt = '<td class="%s alert alert-success " align="center">%s</td>'

            return td_srt % (self.cssclasses[weekday], '<a href="/calendar/%s/%s/%s/">%d</a>' % (year, month, day, day))
