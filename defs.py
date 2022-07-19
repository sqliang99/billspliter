#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class link:
    def __init__(self,pfrom,pto,amount):
        self.amount = amount
        self.pfrom = pfrom
        self.pto = pto
    def speak(self):
        print(self.pfrom.name, 'owns',self.pto.name,self.amount)


# In[ ]:


class Person:
    def __init__(self, name,links):
        self.name = name
        self.links = links
    def say_name(self):
        print('my name is',self.name)
    def say_links(self):
        for l in self.links:
            l.speak()


# In[ ]:


class bill:
    def __init__(self, amount,paid_by,shared_by):
        self.amount = amount
        self.paid_by = paid_by
        self.shared_by = shared_by
    def say_paid_by(self):
        print('the bill is paid by',','.join([p.name for p in self.paid_by]))
    def say_shared_by(self):
        print('the bill is shared by',','.join([p.name for p in self.shared_by]))
    def assign_link(self):
        for p in self.shared_by:
            for r in self.paid_by:
                if(r == p):
                    break
                else:
                    l = link(p,r,(self.amount/len(self.shared_by)))
                    p.links.append(l)
                    l2 = link(r,p,-(self.amount/len(self.shared_by)))
                    r.links.append(l2)
        print('link assignment: done')


# In[ ]:


def compile_links(people):
    all_links = []
    for person in people:
        all_links.extend(person.links)
    return all_links


# In[ ]:


class node(Person):
    def __init__(self, Person):
        self.name = Person.name
        self.person = Person
        self.links = []
    def say_name(self):
        print('my name is',self.name)


# In[ ]:


def calculate(people):
    all_links = compile_links(people)
    nodes = []
    for p in people:
        n = node(p)
        nodes.append(n)
        for pto in set([links.pto for links in all_links if links.pfrom == p]):
            n.links.append(link(p,pto,sum([links.amount for links in all_links if links.pfrom == p and links.pto == pto])))
    return nodes


# In[ ]:


import networkx as nx
def create_graph(nodes):
    G = nx.DiGraph()
    final_links = [link for link in compile_links(nodes) if link.amount > 0]
    for i in final_links:
        G.add_edge(i.pfrom.name, i.pto.name, capacity=i.amount)
    return G

#this code to build residual network is taken from https://networkx.org/documentation/stable/_modules/networkx/algorithms/flow/utils.html#build_residual_network

def build_residual_network(G, capacity):
    """Build a residual network and initialize a zero flow.

    The residual network :samp:`R` from an input graph :samp:`G` has the
    same nodes as :samp:`G`. :samp:`R` is a DiGraph that contains a pair
    of edges :samp:`(u, v)` and :samp:`(v, u)` iff :samp:`(u, v)` is not a
    self-loop, and at least one of :samp:`(u, v)` and :samp:`(v, u)` exists
    in :samp:`G`.

    For each edge :samp:`(u, v)` in :samp:`R`, :samp:`R[u][v]['capacity']`
    is equal to the capacity of :samp:`(u, v)` in :samp:`G` if it exists
    in :samp:`G` or zero otherwise. If the capacity is infinite,
    :samp:`R[u][v]['capacity']` will have a high arbitrary finite value
    that does not affect the solution of the problem. This value is stored in
    :samp:`R.graph['inf']`. For each edge :samp:`(u, v)` in :samp:`R`,
    :samp:`R[u][v]['flow']` represents the flow function of :samp:`(u, v)` and
    satisfies :samp:`R[u][v]['flow'] == -R[v][u]['flow']`.

    The flow value, defined as the total flow into :samp:`t`, the sink, is
    stored in :samp:`R.graph['flow_value']`. If :samp:`cutoff` is not
    specified, reachability to :samp:`t` using only edges :samp:`(u, v)` such
    that :samp:`R[u][v]['flow'] < R[u][v]['capacity']` induces a minimum
    :samp:`s`-:samp:`t` cut.

    """
    if G.is_multigraph():
        raise nx.NetworkXError("MultiGraph and MultiDiGraph not supported (yet).")

    R = nx.DiGraph()
    R.add_nodes_from(G)

    inf = float("inf")
    # Extract edges with positive capacities. Self loops excluded.
    edge_list = [
        (u, v, attr)
        for u, v, attr in G.edges(data=True)
        if u != v and attr.get(capacity, inf) > 0
    ]
    # Simulate infinity with three times the sum of the finite edge capacities
    # or any positive value if the sum is zero. This allows the
    # infinite-capacity edges to be distinguished for unboundedness detection
    # and directly participate in residual capacity calculation. If the maximum
    # flow is finite, these edges cannot appear in the minimum cut and thus
    # guarantee correctness. Since the residual capacity of an
    # infinite-capacity edge is always at least 2/3 of inf, while that of an
    # finite-capacity edge is at most 1/3 of inf, if an operation moves more
    # than 1/3 of inf units of flow to t, there must be an infinite-capacity
    # s-t path in G.
    inf = (
        3
        * sum(
            attr[capacity]
            for u, v, attr in edge_list
            if capacity in attr and attr[capacity] != inf
        )
        or 1
    )
    if G.is_directed():
        for u, v, attr in edge_list:
            r = min(attr.get(capacity, inf), inf)
            if not R.has_edge(u, v):
                # Both (u, v) and (v, u) must be present in the residual
                # network.
                R.add_edge(u, v, capacity=r)
                R.add_edge(v, u, capacity=0)
            else:
                # The edge (u, v) was added when (v, u) was visited.
                R[u][v]["capacity"] = r
    else:
        for u, v, attr in edge_list:
            # Add a pair of edges with equal residual capacities.
            r = min(attr.get(capacity, inf), inf)
            R.add_edge(u, v, capacity=r)
            R.add_edge(v, u, capacity=r)

    # Record the value simulating infinity.
    R.graph["inf"] = inf

    return R
