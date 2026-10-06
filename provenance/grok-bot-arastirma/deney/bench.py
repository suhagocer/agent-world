import time, random, math, hashlib, statistics
import py_trees, gtpyhop
from transitions import Machine
gtpyhop.verbose = 0 if hasattr(gtpyhop,'verbose') else None
def timeit(fn, reps):
    ts=[]
    for _ in range(5):
        t=time.perf_counter(); fn(reps); ts.append((time.perf_counter()-t)/reps)
    return statistics.median(ts)*1e6  # microseconds per call

# 1) Utility AI (IAUS-style): 8 actions x 4 considerations, multiplicative + compensation
def curve(x,k): return x**k
ACTIONS=[[(j%4, 1+((i+j)%3)) for j in range(4)] for i in range(8)]
def utility_decide(state):
    best=-1;bi=0
    for i,cons in enumerate(ACTIONS):
        s=1.0
        for inp,k in cons: s*=curve(state[inp],k)
        s=s+(1-s)*(1-1/len(cons))*s  # Dave Mark-style compensation factor
        if s>best: best=s;bi=i
    return bi
rng=random.Random(1); states=[[rng.random() for _ in range(4)] for _ in range(1000)]
def u(reps):
    for r in range(reps): utility_decide(states[r%1000])

# 2) FSM (transitions)
class A: pass
def make_fsm():
    a=A(); Machine(model=a, states=['idle','bidding','working','verifying'],
        transitions=[['bid','idle','bidding'],['win','bidding','working'],['submit','working','verifying'],['done','verifying','idle']], initial='idle')
    return a
fa=make_fsm()
def f(reps):
    for _ in range(reps): fa.bid(); fa.win(); fa.submit(); fa.done()

# 3) Behaviour tree (py_trees) tick of a 7-node tree
class Cond(py_trees.behaviour.Behaviour):
    def __init__(s,n,ok): super().__init__(n); s.ok=ok
    def update(s): return py_trees.common.Status.SUCCESS if s.ok else py_trees.common.Status.FAILURE
root=py_trees.composites.Selector("root",memory=False,children=[
    py_trees.composites.Sequence("do_task",memory=False,children=[Cond("has_task",False),Cond("work",True)]),
    py_trees.composites.Sequence("verify",memory=False,children=[Cond("has_verif",False),Cond("check",True)]),
    Cond("bid",True)])
tree=py_trees.trees.BehaviourTree(root)
def b(reps):
    for _ in range(reps): tree.tick()

# 4) HTN (GTPyhop) plan: take task -> (buy tool if needed) -> work -> submit
dom=gtpyhop.Domain('agentworld')
def a_bid(s,ag,t):
    if s.task_owner.get(t) is None: s.task_owner[t]=ag; return s
def a_buy(s,ag,tool):
    if s.coins[ag]>=5: s.coins[ag]-=5; s.tools[ag].add(tool); return s
def a_work(s,ag,t):
    if s.task_owner[t]==ag and s.need[t] in s.tools[ag]: s.done.add(t); return s
def a_submit(s,ag,t):
    if t in s.done: s.submitted.add(t); return s
gtpyhop.declare_actions(a_bid,a_buy,a_work,a_submit)
def m_complete(s,ag,t):
    steps=[('a_bid',ag,t)]
    if s.need[t] not in s.tools[ag]: steps.append(('a_buy',ag,s.need[t]))
    return steps+[('a_work',ag,t),('a_submit',ag,t)]
gtpyhop.declare_task_methods('complete',m_complete)
def mkstate():
    s=gtpyhop.State('s'); s.task_owner={'t1':None}; s.coins={'ag':10}; s.tools={'ag':set()}; s.need={'t1':'hammer'}; s.done=set(); s.submitted=set(); return s
import io,contextlib
def h(reps):
    for _ in range(reps):
        with contextlib.redirect_stdout(io.StringIO()):
            plan=gtpyhop.find_plan(mkstate(),[('complete','ag','t1')])
with contextlib.redirect_stdout(io.StringIO()):
    print_plan=gtpyhop.find_plan(mkstate(),[('complete','ag','t1')])
res={"utility_decide_8x4_us":timeit(u,20000),"fsm_4_transitions_us":timeit(f,5000),
     "py_trees_tick_7nodes_us":timeit(b,5000),"gtpyhop_plan_4steps_us":timeit(h,1000)}
# determinism check: two seeded runs of 1000 agents x 100 ticks produce identical decision hash
def run(seed):
    r=random.Random(seed); hsh=hashlib.sha256()
    st=[[r.random() for _ in range(4)] for _ in range(1000)]
    for tick in range(100):
        for s in st:
            a=utility_decide(s); hsh.update(bytes([a]))
            s[a%4]=min(1.0,max(0.0,s[a%4]+r.uniform(-0.1,0.1)))
    return hsh.hexdigest()[:16]
res["determinism_same_seed"]=run(7)==run(7); res["different_seed_differs"]=run(7)!=run(8)
print(res); print("plan:",print_plan)
