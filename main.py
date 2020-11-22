import numpy as np

def reach_the_exit(entity , exit):
    if exit[0]==15:
        if (entity.r[0] <= exit[0]) or (entity.r[1] < exit[1] - 0.5) or (entity.r[1] > exit[1] + 0.5):
            return False
    else:
        if (entity.r[0] >= exit[0]) or (entity.r[1] < exit[1] - 0.5) or (entity.r[1] > exit[1] + 0.5):
            return False
    return True


#####################################################################################################
#1

class Entity:
    def __init__(self, r):
        self.e = [0,0]
        self.v = [0,0]
        self.r = r
        self.v0 = 4/10
        self.acceleration_time = 0.5

    def update_e(self, exit):
        size = ((exit[0]-self.r[0])**2+(exit[1]-self.r[1])**2)**0.5
        self.e = [(exit[0]-self.r[0])/size, (exit[1]-self.r[1])/size]

    def update_v(self):
        self.v = [self.v[0]+(self.v0*self.e[0]-self.v[0])*0.01/self.acceleration_time, self.v[1]+(self.v0*self.e[1]-self.v[1])*0.01/self.acceleration_time]

    def update_r(self):
        self.r = [self.r[0]+self.v[0]*0.01, self.r[1]+self.v[1]*0.01]


def simulate_one_entity(entity, exit):
    k=0
    v = []
    r = []
    entity.update_e(exit)
    while not reach_the_exit(entity, exit):
        v.append(entity.v)
        r.append(entity.r)
        entity.update_v()
        entity.update_r()
        k = k + 1
    # print(v)
    # print(r)
    return k
# # #A
# exit = [15,15/2]
# entity = Entity([15/2, 15/2])
# k= simulate_one_entity(entity, exit)
# print(k)

# #B
# np.random.seed(0)
# random0 = np.random.uniform(0,15,200)
# np.random.seed(2)
# random1 = np.random.uniform(0,15,200)
# k_array = []
# exit = [15,15/2]
# for i in range(200):
#     entity = Entity([random0[i],random1[i]])
#     k_array.append(simulate_one_entity(entity,exit))
# print(k_array)
# print(max(k_array))

#######################################################################################################

#2

class Entity2:
    def __init__(self, r , v0=4/10):
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
        if (not entity is e) and (get_distance_from_exit(entity)>get_distance_from_exit(e)) and (  abs(entity.r[0]-e.r[0])<0.5 or abs(entity.r[1]-e.r[1])<0.5):
            return False
    return True

def get_entities(n , v0=4/10):
    np.random.seed(0)
    random0 = np.random.uniform(0,15,n)
    np.random.seed(2)
    random1 = np.random.uniform(0,15,n)
    entities=[]
    for i in range(n):
        entities.append(Entity2([random0[i],random1[i]] , v0=v0))
    return entities

def get_entities_with_old(n, v0=4/10):
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

def simulate_many_entities(entities):
    k = 0
    q = entities
    q = sorted(q, key=get_distance_from_exit)
    while not len(q) == 0:
        # print(k)
        # print(len(q))
        for entity in q:
            entity.update_e([15, 7.5])
            entity.update_v()
            entity.update_r()
            if not is_legal_move(entity, q):
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
# entities = get_entities(50, v0=1/10)
# k= simulate_many_entities(entities)
# print("v0=1 " , k)
#
# entities = get_entities(50, v0=2/10)
# k= simulate_many_entities(entities)
# print("v0=2 " , k)
#
# entities = get_entities(50, v0=3/10)
# k= simulate_many_entities(entities)
# print("v0=3 " , k)
#
# entities = get_entities(50, v0=4/10)
# k= simulate_many_entities(entities)
# print("v0=4 ", k)

# #C
# entities = get_entities_with_old(20, v0=1/10)
# k= simulate_many_entities(entities)
# print("v0=1, 20 entities " , k)
#
# entities = get_entities_with_old(50, v0=1/10)
# k= simulate_many_entities(entities)
# print("v0=1, 50 entities " , k)
#
# entities = get_entities_with_old(100, v0=1/10)
# k= simulate_many_entities(entities)
# print("v0=1, 100 entities " , k)
#
# entities = get_entities_with_old(20, v0=2/10)
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

###################################################################################################
#3

class Entity3:
    def __init__(self , r, exit ,  v0=4/10, blind=False):
        self.e = [0,0]
        self.v = [0,0]
        self.prev_v=[0,0]
        self.prev_r=r
        self.r = r
        self.v0 = v0
        self.acceleration_time = 0.5
        self.exit = exit
        self.blind = blind

    def update_e(self):
        size = ((self.r[0]-self.exit[0])**2 + (self.r[1]-self.exit[1])**2)**0.5
        self.e = [(self.exit[0]-self.r[0])/size,(self.exit[1]-self.r[1])/size]

    def update_blind_e(self, q):
        x=0
        y=0
        for e in q:
            x = x + e.e[0]
            y = y + e.e[1]
        size = (x**2 + y**2)**0.5
        if size==0:
            self.e=[0,0]
        else:
            self.e = [x / size, y / size]

    def update_v(self):
        self.prev_v = self.v
        self.v = [self.v[0]+(self.v0*self.e[0]-self.v[0])*0.01/self.acceleration_time, self.v[1]+(self.v0*self.e[1]-self.v[1])*0.01/self.acceleration_time]

    def update_r(self):
        self.prev_r = self.r
        self.r = [self.r[0]+self.v[0]*0.01, self.r[1]+self.v[1]*0.01]


def get_distance_from_exit_two_doors(entity):
    return ((entity.r[0] - entity.exit[0]) ** 2 + (entity.r[1] - entity.exit[1]) ** 2) ** 0.5

def is_legal_move_two_doors(entity, q):
    for e in q:
        if (not entity is e) and (get_distance_from_exit_two_doors(entity)>get_distance_from_exit_two_doors(e)) and (abs(entity.r[0]-e.r[0])<0.5 or abs(entity.r[1]-e.r[1])<0.5):
            return False
    return True

def get_entities_two_doors(n , v0=4/10):
    np.random.seed(0)
    random0 = np.random.uniform(0,15,n)
    np.random.seed(2)
    random1 = np.random.uniform(0,15,n)
    entities=[]
    for i in range(n):
        if random0[i]<7.5:
            entities.append(Entity3([random0[i],random1[i]], [0,7.5] , v0=v0))
        else:
            entities.append(Entity3([random0[i],random1[i]] ,[15,7.5] ,v0=v0))
    return entities

def get_entities_two_doors_blind(n , v0=4/10):
    np.random.seed(0)
    random0 = np.random.uniform(0,15,n)
    np.random.seed(2)
    random1 = np.random.uniform(0,15,n)
    entities=[]
    for i in range(n):
        if random0[i]<7.5:
            if i%2==0:
                entities.append(Entity3([random0[i], random1[i]], [0, 7.5], v0=v0, blind=True))
            else:
                entities.append(Entity3([random0[i], random1[i]], [0, 7.5], v0=v0))
        else:
            if i%2==0:
                entities.append(Entity3([random0[i], random1[i]], [15, 7.5], v0=v0, blind=True))
            else:
                entities.append(Entity3([random0[i], random1[i]], [15, 7.5], v0=v0))
    return entities

def get_entities_one_doors_blind(n , v0=4/10):
    np.random.seed(0)
    random0 = np.random.uniform(0,15,n)
    np.random.seed(2)
    random1 = np.random.uniform(0,15,n)
    entities=[]
    for i in range(n):
        if i%2==0:
            entities.append(Entity3([random0[i], random1[i]], [15, 7.5], v0=v0, blind=True))
        else:
            entities.append(Entity3([random0[i], random1[i]], [15, 7.5], v0=v0))
    return entities

def get_stupid_entities_two_doors(n, v0=4/10):
    np.random.seed(0)
    random0 = np.random.uniform(0,15,n)
    np.random.seed(2)
    random1 = np.random.uniform(0,15,n)
    entities=[]
    for i in range(n):
        if i%2==0 or random0[i]>7.5:
            entities.append(Entity3([random0[i], random1[i]], [15, 7.5], v0=v0))
        else:
            entities.append(Entity3([random0[i],random1[i]] ,[0,7.5] ,v0=v0))
    return entities

def get_neighbors(entity,q):
    neighbors=[]
    for e in q:
        if (not e is entity) and e.blind==False and ((e.r[0]-entity.r[0])**2+(e.r[1]-entity.r[1])**2)**0.5<5:
            neighbors.append(e)
    return neighbors


def simulate_many_entities_two_doors(entities , print_how_many_dies=False):
    k = 0
    q = entities
    q = sorted(q, key=get_distance_from_exit_two_doors)
    while not len(q) == 0:
        if k==9000 and print_how_many_dies:
            print(len(q)," dies")
        # print(k)
        # print(len(q))
        for entity in q:
            if entity.blind==True and get_distance_from_exit_two_doors(entity)>5 :
                neighbors = get_neighbors(entity,q)
                if len(neighbors)==0:
                    entity.update_e()
                    print("aaa")
                else:
                    entity.update_blind_e(neighbors)
            else:
                entity.update_e()
            entity.update_v()
            entity.update_r()
            if (not is_legal_move_two_doors(entity, q)) and entity.blind==False:
                entity.v = entity.prev_v
                entity.r = entity.prev_r
            if reach_the_exit(entity, [0,7.5]) or reach_the_exit(entity, [15,7.5]):
                q.remove(entity)
        k = k+1
    return k


# #A
# entities = get_entities_two_doors(20)
# k= simulate_many_entities_two_doors(entities)
# print("20 entities " , k)
#
# entities = get_entities_two_doors(50)
# k= simulate_many_entities_two_doors(entities)
# print("50 entities " , k)
#
# entities = get_entities_two_doors(100)
# k= simulate_many_entities_two_doors(entities)
# print("100 entities " , k)
#
# entities = get_entities_two_doors(200)
# k= simulate_many_entities_two_doors(entities)
# print("200 entities " , k)
#
# #B
# entities = get_stupid_entities_two_doors(20)
# k= simulate_many_entities_two_doors(entities)
# print("20 entities " , k)
#
# entities = get_stupid_entities_two_doors(50)
# k= simulate_many_entities_two_doors(entities)
# print("50 entities " , k)
#
# entities = get_stupid_entities_two_doors(100)
# k= simulate_many_entities_two_doors(entities)
# print("100 entities " , k)
#
# entities = get_stupid_entities_two_doors(200)
# k= simulate_many_entities_two_doors(entities)
# print("200 entities " , k)
#
# #C
#
# print("two doors")
# entities = get_entities_two_doors_blind(20)
# print("20 entities checking dies")
# k= simulate_many_entities_two_doors(entities, print_how_many_dies=True)
# print("20 entities " , k)
#
# entities = get_entities_two_doors_blind(50)
# print("50 entities checking dies")
# k= simulate_many_entities_two_doors(entities, print_how_many_dies=True)
# print("50 entities " , k)
#
# entities = get_entities_two_doors_blind(100)
# print("100 entities checking dies")
# k= simulate_many_entities_two_doors(entities, print_how_many_dies=True)
# print("100 entities " , k)
#
# entities = get_entities_two_doors_blind(200)
# print("200 entities checking dies")
# k= simulate_many_entities_two_doors(entities, print_how_many_dies=True)
# print("200 entities " , k)
#
# print("one doors")
# entities = get_entities_one_doors_blind(20)
# print("20 entities checking dies")
# k= simulate_many_entities_two_doors(entities, print_how_many_dies=True)
# print("20 entities " , k)
#
# entities = get_entities_one_doors_blind(50)
# print("50 entities checking dies")
# k= simulate_many_entities_two_doors(entities, print_how_many_dies=True)
# print("50 entities " , k)
#
# entities = get_entities_one_doors_blind(100)
# print("100 entities checking dies")
# k= simulate_many_entities_two_doors(entities, print_how_many_dies=True)
# print("100 entities " , k)
#
# entities = get_entities_one_doors_blind(200)
# print("200 entities checking dies")
# k= simulate_many_entities_two_doors(entities, print_how_many_dies=True)
# print("200 entities " , k)