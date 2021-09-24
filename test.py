import server
import client
import controller
import update
import var
#test vector for all non socket, threading functions
#socket tested via multiple instance of the program
#no easy way to test 

def test_update():
    assert(update.verify_address('0.0.0.0', 1))
    assert(update.verify_address('225.225.225.225', 2**16-1))
    assert(not update.verify_address('0.0.0', 1))
    assert(not update.verify_address('0.0.0.0', -1))
    print('Passed verify_address tests')

    h,p = '127.0.0.1', 1234
    addr = h+':'+str(p)
    #parse_address, checkoldtime, checknewtime, checkip, updateentry, updatemap

    var.table = {}
    var.ip = {}
    


def test_client():
    pass 
    #blacklistnode

def test_controller():
    pass #format input

print('testing')
test_update()