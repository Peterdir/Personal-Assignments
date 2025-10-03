def forward_checking_generator(N):
    def fc(state, domains):
        yield ("visit", state)
        
        if len(state) == N:
            yield ("found", tuple(state))
            return
        
        row = len(state)
        for col in range(N):
            if col in domains[row]:
                new_domains = [d.copy() for d in domains]
                
                new_state = state + [col]
                
                consistent = True
                for r in range(row + 1, N):
                    new_domains[r] -= {col, col + (r - row), col - (r - row)}
                    if not new_domains[r]:
                        consistent = False
                        break
                
                if consistent:
                    yield from fc(new_state, new_domains)
    
    domains = [set(range(N)) for _ in range(N)]
    yield from fc([], domains)