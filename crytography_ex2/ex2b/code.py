# ================= AES CONSTANTS =================
S_BOX = [
0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16
]

RCON = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1b,0x36]*5  # extended

# ================= HELPERS =================
def hex_to_bytes(s):
    return [int(s[i:i+2],16) for i in range(0,len(s),2)]

def bytes_to_hex(arr):
    return ''.join(f'{b:02x}' for b in arr)

def gmul(a,b):
    p=0
    for _ in range(8):
        if b&1: p^=a
        hi=a&0x80
        a<<=1
        if hi: a^=0x1b
        b>>=1
    return p&0xff

# ================= KEY EXPANSION (16 ROUNDS) =================
def key_expansion(key):
    w=[key[i:i+4] for i in range(0,16,4)]
    for i in range(4,68):  # 16 rounds → 68 words
        temp=w[i-1][:]
        if i%4==0:
            temp=temp[1:]+temp[:1]
            temp=[S_BOX[b] for b in temp]
            temp[0]^=RCON[i//4-1]
        w.append([w[i-4][j]^temp[j] for j in range(4)])
    return w

# ================= STATE =================
def to_state(b):
    return [[b[r+4*c] for c in range(4)] for r in range(4)]

def from_state(s):
    return [s[r][c] for c in range(4) for r in range(4)]

# ================= CORE =================
def sub_bytes(s):
    return [[S_BOX[b] for b in row] for row in s]

def shift_rows(s):
    return [s[0],
            s[1][1:]+s[1][:1],
            s[2][2:]+s[2][:2],
            s[3][3:]+s[3][:3]]

def mix_columns(s):
    for c in range(4):
        a=[s[r][c] for r in range(4)]
        s[0][c]=gmul(2,a[0])^gmul(3,a[1])^a[2]^a[3]
        s[1][c]=a[0]^gmul(2,a[1])^gmul(3,a[2])^a[3]
        s[2][c]=a[0]^a[1]^gmul(2,a[2])^gmul(3,a[3])
        s[3][c]=gmul(3,a[0])^a[1]^a[2]^gmul(2,a[3])
    return s

def add_round_key(s,w,r):
    for c in range(4):
        for r_i in range(4):
            s[r_i][c]^=w[r*4+c][r_i]
    return s

def print_state(label, s):
    print(label, bytes_to_hex(from_state(s)))

# ================= ENCRYPT =================
def aes_encrypt_16_rounds(pt,key):
    pt=hex_to_bytes(pt)
    key=hex_to_bytes(key)
    w=key_expansion(key)

    print("\nAES (CUSTOM 16 ROUNDS)\n")
    print("Plaintext:", bytes_to_hex(pt))
    print("Key:      ", bytes_to_hex(key))

    s=to_state(pt)

    print("\n--- Initial AddRoundKey ---")
    s=add_round_key(s,w,0)
    print_state("State:", s)

    # 15 main rounds
    for r in range(1,16):
        print(f"\n--- Round {r} ---")
        s=sub_bytes(s)
        print_state("After SubBytes:", s)

        s=shift_rows(s)
        print_state("After ShiftRows:", s)

        s=mix_columns(s)
        print_state("After MixColumns:", s)

        s=add_round_key(s,w,r)
        print_state("After AddRoundKey:", s)

    # Final round (no MixColumns)
    print("\n--- Round 16 (Final) ---")
    s=sub_bytes(s)
    print_state("After SubBytes:", s)

    s=shift_rows(s)
    print_state("After ShiftRows:", s)

    s=add_round_key(s,w,16)
    print_state("After AddRoundKey:", s)

    print("\nCiphertext:", bytes_to_hex(from_state(s)))


# ================= TEST =================
if __name__ == "__main__":
    pt = "2b7e151628aed2a6abf7158809cf4f3c"
    key = "2b7e151628aed2a6abf7158809cf4f3c"

    aes_encrypt_16_rounds(pt, key)
[23bcs010@mepcolinux exe2b]$python3 aes.py

AES (CUSTOM 16 ROUNDS)

Plaintext: 2b7e151628aed2a6abf7158809cf4f3c
Key:       2b7e151628aed2a6abf7158809cf4f3c

--- Initial AddRoundKey ---
State: 00000000000000000000000000000000

--- Round 1 ---
After SubBytes: 63636363636363636363636363636363
After ShiftRows: 63636363636363636363636363636363
After MixColumns: 63636363636363636363636363636363
After AddRoundKey: c3999d74eb374fd240c05a5a490f1566

--- Round 2 ---
After SubBytes: 2eee5e92e99a84b509babebe3b765933
After ShiftRows: 2e9abe33e9ba599209765eb53bee84be
After MixColumns: 64eb8630d7ff4cfc63b2074265d51f40
After AddRoundKey: 962913c2ad69f5bf3a878738168ce93f

--- Round 3 ---
After SubBytes: 90a57d2595f9e6088017170747641e75
After ShiftRows: 90f9177595171e2580647d0847a5e607
After MixColumns: 4935d8af33bcd1e7c2c706929b203c84
After AddRoundKey: 74b59fd274aa2fd9dce478d6f65ab4bf

--- Round 4 ---
After SubBytes: 92d5dbb592ac15358669bcf642be8d08
After ShiftRows: 92acbc0892698db586bedb3542d515f6
After MixColumns: 640645adbc793e3820a2ca9e033abcf1
After AddRoundKey: 8b42e0ec142b654796d3efa5d83111f1

--- Round 5 ---
After SubBytes: 3d2ce1cefaf14da09066df0661c782a1
After ShiftRows: 3df1dfa1fa6682ce90c7e1a0612c4d06
After MixColumns: 0c1f91300965ca76289d75d6fde8ddce
After AddRoundKey: d8ce57c875e657f1e26fcd6aec11c872

--- Round 6 ---
After SubBytes: 618b5be89d8e5ba198a8bd02ce82e840
After ShiftRows: 618ebd409da8e8e898825ba1ce8b5b02
After MixColumns: b6fa4e10c21ddd374ccb5433582cf59d
After AddRoundKey: db72ed6ad316e3ca9732d272922c6660

--- Round 7 ---
After SubBytes: b9405502664711748823b5404f7133d0
After ShiftRows: b947b5d066233302887155744f401140
After MixColumns: c523e499987725beb9e1cf4f0fbced00
After AddRoundKey: 8b771397c728ec4d3d4780fd411a314f

--- Round 8 ---
After SubBytes: 3df57d88c634cee327a0cd5483a2c784
After ShiftRows: 3d34cd84c6a0c78827a27de383f5ce54
After MixColumns: 6f9d1fad2347703d2d1c416b836f0d0d
After AddRoundKey: 854f6c8c96cacaef1c37b40bfce22422

--- Round 9 ---
After SubBytes: 97845064907474df9c9a8d2bb0983693
After ShiftRows: 97748d93909a36649c9850dfb084742b
After MixColumns: b7604c66dc81cacf1f98ded2b314a16d
After AddRoundKey: 1b172a95c57b16ee3749f793e448a103

--- Round 10 ---
After SubBytes: aff0e52aa62147289a3b68dc6952327b
After ShiftRows: af21687ba63b322a9a52e52869f047dc
After MixColumns: 352ed35502ac87ac14226152428768af
After AddRoundKey: e53a2afdcb42a225f51d6d9af4e46409

--- Round 11 ---
After SubBytes: d980e5541f2c3a3fe6a43cb8bf694301
After ShiftRows: d92c3c011fa44354e669e53fbf803ab8
After MixColumns: e0c48e62deddc16eb63f1fc37c52980b
After AddRoundKey: ca2e53843dd93901b404eb64c80a600a

--- Round 12 ---
After SubBytes: 7431ed5f2735127c8df2e943e867d067
After ShiftRows: 7435e96727f2d05f8d67ed7ce8311243
After MixColumns: 3959218eccec8ff53913affec9ff3886
After AddRoundKey: 7bf280e56d43d6f19a87025dde336d24

--- Round 13 ---
After SubBytes: 2189cdd93c1af6a1b817774c1dc33c36
After ShiftRows: 211a77363c173cd9b8c3cda11d89f64c
After MixColumns: 2dba8f62a48f23c659c802840059b7c0
After AddRoundKey: 20ed14f90877e15956a46db818f98d5e

--- Round 14 ---
After SubBytes: b755fa9930f5f8cbb1493c6cad995d58
After ShiftRows: b7f53c5830495d99b199facbad55f86c
After MixColumns: 155ad2bb7fdc736df84681262a78a799
After AddRoundKey: f08d428d36f321c4be05bcb3749ba092

--- Round 15 ---
After SubBytes: 8c5d2c5d050dfd1cae6b656d9214e04f
After ShiftRows: 8c0d654f056be05dae142c1c925dfd6d
After MixColumns: 3e769a790ab5523e4beec6e9485999d7
After AddRoundKey: da642117a788bbf9a09012bbfdc44a8e

--- Round 16 (Final) ---
After SubBytes: 5743fdf05cc4ea99e060c9ea541cd619
After ShiftRows: 57c4c9195c60d6f0e01cfd995443eaea
After AddRoundKey: cdb0b9a26b294f8c3c2bb0b73de9749d

Ciphertext: cdb0b9a26b294f8c3c2bb0b73de9749d
