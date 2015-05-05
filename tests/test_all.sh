# call all tests
# eq.:
#     ./test_all.sh [-v]

./test_record.py $*
./test_users.py $*
./test_messages.py $*
