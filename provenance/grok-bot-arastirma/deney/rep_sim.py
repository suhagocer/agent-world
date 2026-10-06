"""Toy experiment: task market with verification + reputation. Deterministic (seeded)."""
import random, statistics, json, sys
import numpy as np

def run(policy, seed, n=100, frac_bad=0.2, p_wrong=0.5, tasks=5000, sybil_collude=True):
    rng = random.Random(seed)
    bad = set(rng.sample(range(n), int(n*frac_bad)))
    alpha = [1.0]*n; beta = [1.0]*n         # Beta reputation (Josang&Ismail)
    cv = [0]*n                               # BOINC consecutive valid
    local = np.zeros((n,n))                  # EigenTrust local sat counts
    pre = [i for i in range(n) if i not in bad][:5]  # pre-trusted honest seeds
    accepted_wrong = 0; executions = 0; bad_share_assign = 0; load=[0]*n
    et = np.ones(n)/n
    def result(i):  # True=correct
        return not (i in bad and rng.random() < p_wrong)
    def pick(k, exclude=()):
        cands = [i for i in range(n) if i not in exclude]
        if policy == "none":
            w = [1]*len(cands)
        elif policy.startswith("eigen"):
            w = [et[i]+1e-6 for i in cands]
        else:
            w = [alpha[i]/(alpha[i]+beta[i]) for i in cands]
            w = [x**4 for x in w]  # sharpen
        out=[]
        for _ in range(k):
            j = rng.choices(range(len(cands)), weights=w)[0]
            out.append(cands.pop(j)); w.pop(j)
        return out
    for t in range(tasks):
        if policy.startswith("eigen") and t % 250 == 0:
            C = local.copy()
            if sybil_collude:   # malicious collective rates each other high
                for i in bad:
                    for j in bad:
                        if i!=j: C[i,j] += 50
            rs = C.sum(1)
            p = np.zeros(n); p[pre] = 1/len(pre)
            for i in range(n):
                C[i] = C[i]/rs[i] if rs[i]>0 else p
            a = 0.15 if policy=="eigen_pre" else 0.0
            v = p.copy() if a>0 else np.ones(n)/n
            for _ in range(50):
                v = (1-a)*C.T@v + a*p
            et = v
        if policy in ("none", "beta_q1"):
            w = pick(1)[0]; executions += 1; load[w]+=1
            bad_share_assign += w in bad
            ok = result(w)
            if not ok: accepted_wrong += 1
            continue
        first = pick(1)[0]; bad_share_assign += first in bad
        replicate = True
        if policy == "beta_adaptive":
            replicate = not (cv[first] >= 10 and rng.random() > 1/cv[first])
        ws = [first] + (pick(1, exclude=(first,)) if replicate else [])
        res = {w: result(w) for w in ws}; executions += len(ws)
        for w in ws: load[w]+=1
        if len(ws) == 1:
            if not res[first]: accepted_wrong += 1
            continue
        a_, b_ = ws
        if res[a_] == res[b_]:
            # agreement: accepted. Two wrong answers assumed to collude/match (worst case)
            if not res[a_]: accepted_wrong += 1
            for w in ws:
                alpha[w] += 1; cv[w] += 1
                local[a_ if w==b_ else b_, w] += 1
        else:
            # disagreement -> third tie-breaker from honest-weighted pick
            c = pick(1, exclude=tuple(ws))[0]; executions += 1; load[c]+=1
            rc = result(c)
            for w in ws:
                if res[w] == rc:
                    alpha[w] += 1; cv[w] += 1; local[c, w] += 1
                else:
                    beta[w] += 1; cv[w] = 0; local[c, w] -= 0  # EigenTrust clips negatives
            if not rc: accepted_wrong += 1
    return dict(wrong_rate=accepted_wrong/tasks, exec_per_task=executions/tasks,
                bad_assign_share=bad_share_assign/tasks,
                top10_load_share=sum(sorted(load)[-n//10:])/sum(load))

def sweep(fb, pw):
    res={}
    for pol in ["none","beta_q2","beta_adaptive","eigen_nopre_q2","eigen_pre"]:
        rs=[run(pol,s,frac_bad=fb,p_wrong=pw) for s in range(20)]
        res[pol]={k:(round(statistics.mean(r[k] for r in rs),4),round(statistics.pstdev(r[k] for r in rs),4)) for k in rs[0]}
    return res
if __name__ == "__main__":
    allres={}
    for fb,pw in [(0.2,0.5),(0.4,0.5),(0.2,0.1)]:
        allres[f"bad={fb},p_wrong={pw}"]=r=sweep(fb,pw)
        for k,v in r.items(): print(fb,pw,k,v,flush=True)
    json.dump(allres,open("rep_sim_results.json","w"),indent=1)
    sys.exit()
    out = {}
    for pol in ["none", "beta_q1", "beta_q2", "beta_adaptive", "eigen_nopre_q2", "eigen_pre"]:
        pname = pol
        rs = [run("beta_q2" if pol=="beta_q2" else ("eigen_pre" if pol=="eigen_pre" else pol), s) for s in range(20)]
        out[pname] = {k: (round(statistics.mean(r[k] for r in rs),4), round(statistics.pstdev(r[k] for r in rs),4)) for k in rs[0]}
        print(pname, out[pname], flush=True)
    json.dump(out, open("rep_sim_results.json","w"), indent=1)
