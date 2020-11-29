import numpy as np

def reach_the_exit(entity , exit):
    if exit[0]==15:
        if (entity.r[0] <= exit[0]) or (entity.r[1] < exit[1] - 0.5) or (entity.r[1] > exit[1] + 0.5):
            return False
    else:
        if (entity.r[0] >= exit[0]) or (entity.r[1] < exit[1] - 0.5) or (entity.r[1] > exit[1] + 0.5):
            return False
    return True


class Entity2:
    def __init__(self, r , v0=1.5):
        self.e = [0,0]
        self.v = [0,0]
        self.prev_v=[0,0]
        self.prev_r=r
        self.r = r
        self.v0 = v0
        self.acceleration_time = 0.5

    def update_e(self, exit):
        size = ((exit[0]-self.r[0])**2+(exit[1]-self.r[1])**2)**0.5
        self.e = [(exit[0]-self.r[0])/size, (exit[1]-self.r[1])/size]

    def update_v(self):
        self.prev_v = self.v
        self.v = [self.v[0]+(self.v0*self.e[0]-self.v[0])*0.01/self.acceleration_time, self.v[1]+(self.v0*self.e[1]-self.v[1])*0.01/self.acceleration_time]

    def update_r(self):
        self.prev_r = self.r
        self.r = [self.r[0]+self.v[0]*0.01, self.r[1]+self.v[1]*0.01]


def get_distance_from_exit(entity):
    return ((entity.r[0]-15)**2+(entity.r[1]-7.5)**2)**0.5


def is_legal_move(entity, q):
    for e in q:
        if ((entity.r[0]-e.r[0])**2 + (entity.r[1]-e.r[1])**2 )**0.5 < 0.5:
        # if abs(entity.r[0]-e.r[0])<0.5 or abs(entity.r[1]-e.r[1])<0.5:
            return False
    return True

def get_entities(n , v0=1.5):
    np.random.seed(0)
    random0 = np.random.uniform(0,15,n)
    np.random.seed(2)
    random1 = np.random.uniform(0,15,n)
    entities=[]
    for i in range(n):
        entities.append(Entity2([random0[i],random1[i]] , v0=v0))
    return entities

def get_entities_with_old(n, v0=1.5):
    np.random.seed(0)
    random0 = np.random.uniform(0,15,n)
    np.random.seed(2)
    random1 = np.random.uniform(0,15,n)
    entities=[]
    for i in range(n):
        if i%5==0:
            entities.append(Entity2([random0[i], random1[i]], v0=v0/3))
        else:
            entities.append(Entity2([random0[i],random1[i]] , v0=v0))
    return entities

def get_other(entity, q):
    to_return=[]
    for e in q:
        if get_distance_from_exit(e)<get_distance_from_exit(entity):
            to_return.append(e)
    return to_return

def simulate_many_entities(entities):
    k = 0
    q = entities
    q = sorted(q, key=get_distance_from_exit)
    while not len(q) == 0:
        # print(k)
        # print(len(q))
        for entity in q:
            other=get_other(entity,q)
            entity.update_e([15, 7.5])
            entity.update_v()
            entity.update_r()
            if not is_legal_move(entity, other):
                entity.v = entity.prev_v
                entity.r = entity.prev_r
            if reach_the_exit(entity, [15,7.5]):
                q.remove(entity)
        k = k+1

    return k

# #A
#
# entities = get_entities(20)
# k= simulate_many_entities(entities)
# print("20 entities " , k)
#
# entities = get_entities(50)
# k= simulate_many_entities(entities)
# print("50 entities " , k)
#
# entities = get_entities(100)
# k= simulate_many_entities(entities)
# print("100 entities " , k)
#
# entities = get_entities(200)
# k= simulate_many_entities(entities)
# print("200 entities " , k)

#B
# v_many_entities=[]
# k_many_entities=[]
# entities = get_entities(50, v0=0.6)
# k= simulate_many_entities(entities)
# v_many_entities.append(0.6)
# k_many_entities.append(k)
# print("v0=0.6 " , k)
#
# entities = get_entities(50, v0=1)
# k= simulate_many_entities(entities)
# v_many_entities.append(1)
# k_many_entities.append(k)
# print("v0=1 " , k)
#
# entities = get_entities(50, v0=1.5)
# k= simulate_many_entities(entities)
# v_many_entities.append(1.5)
# k_many_entities.append(k)
# print("v0=1.5 " , k)
#
# entities = get_entities(50, v0=2)
# k= simulate_many_entities(entities)
# v_many_entities.append(2)
# k_many_entities.append(k)
# print("v0=2 ", k)
#
# entities = get_entities(50, v0=2.5)
# k= simulate_many_entities(entities)
# v_many_entities.append(2.5)
# k_many_entities.append(k)
# print("v0=2.5 ", k)
#
# entities = get_entities(50, v0=4)
# k= simulate_many_entities(entities)
# v_many_entities.append(4)
# k_many_entities.append(k)
# print("v0=4 ", k)
#
# entities = get_entities(50, v0=10)
# k= simulate_many_entities(entities)
# v_many_entities.append(10)
# k_many_entities.append(k)
# print("v0=10 ", k)
#
# import matplotlib.pyplot as plt
#
# # x axis values
# x1 = v_many_entities
# # corresponding y axis values
# y1 = k_many_entities
# # plotting the points
# plt.plot(x1, y1)
# # naming the x axis
# plt.xlabel('x - v0')
# # naming the y axis
# plt.ylabel('y - time(k)')
# # giving a title to my graph
# plt.title('question A - 1')
# # function to show the plot
# plt.show()

# #C
number_entities=[]
k_many_entities=[]
entities = get_entities_with_old(20, v0=1.5)
k= simulate_many_entities(entities)
number_entities.append(20)
k_many_entities.append(k)
print("v0=1.5, 20 entities " , k)

entities = get_entities_with_old(25, v0=1.5)
k= simulate_many_entities(entities)
number_entities.append(25)
k_many_entities.append(k)
print("v0=1.5, 25 entities " , k)

entities = get_entities_with_old(30, v0=1.5)
k= simulate_many_entities(entities)
number_entities.append(30)
k_many_entities.append(k)
print("v0=1.5, 30 entities " , k)

entities = get_entities_with_old(33, v0=1.5)
k= simulate_many_entities(entities)
number_entities.append(33)
k_many_entities.append(k)
print("v0=1.5, 33 entities " , k)

entities = get_entities_with_old(35, v0=1.5)
k= simulate_many_entities(entities)
number_entities.append(35)
k_many_entities.append(k)
print("v0=1.5, 35 entities " , k)



import matplotlib.pyplot as plt

# x axis values
x1 = number_entities
# corresponding y axis values
y1 = k_many_entities
# plotting the points
plt.plot(x1, y1)
# naming the x axis
plt.xlabel('x - number of entities')
# naming the y axis
plt.ylabel('y - time(k)')
# giving a title to my graph
plt.title('question B')
# function to show the plot
plt.show()
#************************************not sure if to add
# entities = get_entities_with_old(80, v0=2/10)
# k = simulate_many_entities(entities)
# print("v0=2 20 entities ", k)
#
# entities = get_entities_with_old(50, v0=2/10)
# k = simulate_many_entities(entities)
# print("v0=2 50 entities ", k)
#
# entities = get_entities_with_old(100, v0=2/10)
# k = simulate_many_entities(entities)
# print("v0=2 100 entities ", k)
#
# entities = get_entities_with_old(20, v0=3/10)
# k = simulate_many_entities(entities)
# print("v0=3 20 entities ", k)
#
# entities = get_entities_with_old(50, v0=3/10)
# k = simulate_many_entities(entities)
# print("v0=3 50 entities ", k)
#
# entities = get_entities_with_old(100, v0=3/10)
# k = simulate_many_entities(entities)
# print("v0=3 100 entities ", k)
#
# entities = get_entities_with_old(20, v0=4/10)
# k = simulate_many_entities(entities)
# print("v0=4 20 entities", k)
#
# entities = get_entities_with_old(50, v0=4/10)
# k = simulate_many_entities(entities)
# print("v0=4 50 entities", k)
#
# entities = get_entities_with_old(100, v0=4/10)
# k = simulate_many_entities(entities)
# print("v0=4 100 entities", k)