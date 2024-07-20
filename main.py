from openskill.models import PlackettLuce
model = PlackettLuce()

p1 = model.rating(name='john123')
p2 = model.rating(name='jane234')
p3 = model.rating(name='joe546')
p4 = model.rating(name='jill678')

players =[p1,p2,p3,p4]
print([players])

team1 = [p1, p2]
team2 = [p3, p4]

match = [team1, team2]
[team1, team2] = model.rate(match)
[p1, p2] = team1
[p3, p4] = team2

print([players])