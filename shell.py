import defs
import networkx as nx
import matplotlib.pyplot as plt
import random

# enter members first
print('lets start by entering who is in your group \n one at a time')
members = []
user_name = input("")
members.append(defs.Person(user_name, []))
cont = input("enter y to add another person, enter any to stop  ")
while cont == 'y':
    user_name = input("the name is ")
    members.append(defs.Person(user_name, []))
    cont = input("enter y to add another person, enter any to stop ")

# enter bills
print('now let us add some bills to be paid')

bills = []
amount = float(input("how much was the bill? "))
raw_paid_by = str(input("who paid for the bill? enter name with comma in between: ")).split(',')
raw_shared_by = str(input("who should pay for the bill? enter name with comma in between: ")).split(',')

bills.append(defs.bill(amount, [m for m in members if m.name in raw_paid_by],
                       [m for m in members if m.name in raw_shared_by]))
bills[-1].assign_link()
cont = input("enter y to add another bill, enter any to stop  ")
while cont == 'y':
    amount = float(input("how much was the bill? "))
    raw_paid_by = str(input("who paid for the bill? enter name with comma in between: ")).split(',')
    raw_shared_by = str(input("who should pay for the bill? enter name with comma in between: ")).split(',')
    bills.append(defs.bill(amount, [m for m in members if m.name in raw_paid_by],
                           [m for m in members if m.name in raw_shared_by]))
    bills[-1].assign_link()
    cont = input("enter y to add another person, enter any to stop ")

nodes = defs.calculate(members)
G = defs.create_graph(nodes)
pos=nx.spring_layout(G) # pos = nx.nx_agraph.graphviz_layout(G)
nx.draw_networkx(G, pos)
labels = nx.get_edge_attributes(G, 'capacity')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

plt.show()