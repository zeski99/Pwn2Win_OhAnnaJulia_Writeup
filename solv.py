from pwn import remote

r = remote("oh-anna-julia.pwn2win.party", 1337)

for _ in range(4):
    tmp = r.recvuntil(b"Exit")
    r.sendline("1")

tmp = r.recvuntil(b"Exit")

r.sendline("3")
q = int(r.recvuntil(b"Exit").decode("utf-8").split("\n")[3][3:])

flag = ""

arr = [list() for _ in range(41)]

j = 0
while j < 256:
    r.sendline("2")
    tmp = r.recvuntil(b"secret:").decode("utf-8")
    r.sendline(chr(j) * 40)
    tmp = r.recvuntil(b"Exit").decode("utf-8")
    for i in range(1,41):
        r.sendline("4")
        tmp = r.recvuntil(b"encrypt?").decode("utf-8")
        r.sendline(str(i))
        tmp = r.recvuntil(b"Exit").decode("utf-8").split("\n")[1]
        c = int(tmp[tmp.index("(")+1:tmp.index(",")])
        d = int(tmp[tmp.index(",")+2:tmp.index(")")])
        arr[i].append(pow(d, -1, q) * c % q)
        print(i, j)
    j *= 2
    if j == 0: j = 1

for i in range(1, 41):
    inv = pow(arr[i][0], -1, q)
    ch = ""
    for j in range(1,9):
        s =  arr[i][j] * inv % q
        if s == 2 ** (2**(j-1)):
            ch += "0"
        else:
            ch += "1"
    flag += chr(int(ch[::-1], 2))

print(flag)