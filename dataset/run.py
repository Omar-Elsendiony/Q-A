S=list(input())
m=list('abcdefghijklmnopqrstuvwxyz')[::-1]

if len(S)<26:
    for i in m[::-1]:
        if i not in S:
            S.append(i)
            break
    print(''.join(S))
else:
    x=S[-1]
    for i in range(25)[::-1]:
        if x>S[i]:
            y=m.index(S[i])
            S=S[:i]
            for j in range(y)[::-1]:
                if m[j] not in S:
                    S.append(m[j])
                    break
            break
        else:
            x=S[i]
        
        if i==0:
            print(-1)
            exit()
    print(''.join(S))
