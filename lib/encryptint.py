# encrypt integers into 12 char strings
#
# Algorithm:
#   TRANS represents 10 random chars that map digits 0-9
#   MUS contains three list of random chars used as space fillers
#
#   1. For each digit in number, translate using TRANS
#   2. Right fill up to 12 chars using MUS[0], MUS[1], or MUS[2] based on 
#        original number mod 3
#   3. Then reverse the pattern

TRANS = 'smvenjtu9p'
MUS   = ['vowBfqkxzryA',
         'igbdahcCl05J',
         'YRZXKQFWOVD8']

class EncryptIntError(Exception): pass

def encrypt_int(i):
    if not isinstance(i, (int, long)):
        raise EncryptIntError('%s is not an int or long' % i)

    pat = ''
    for c in str(i):
        pat += TRANS[int(c)]
    s = 12-len(pat)
    pat2 =  pat + MUS[i%3][len(pat):]
    return pat2[::-1]

def decrypt_int(pat):
    if not isinstance(pat, str):
        raise EncryptIntError("%s is not a string" % pat)
    int_str = ''
    for c in pat[::-1]:
        if c not in TRANS:
            continue
        int_str += str(TRANS.index(c))
    if not int_str:
        raise EncryptIntError('Unable to decrypt_int(%s)' % pat)
    return int(int_str)

def test():
    for i in range(1000, 1050):
        pat = encrypt_int(i)
        #print i, pat, decrypt_int(pat)
        assert(i == decrypt_int(pat))
    print 'test passed'

if __name__ == '__main__':
    #test()

    import sys
    if len(sys.argv) < 2:
        print 'not integer given'
        sys.exit(1)

    i = int(sys.argv[1])
    print '%s: %s' % (i, encrypt_int(i))

