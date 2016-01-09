# call all tests
# eq.:
#     ./test_all.sh [-v]

./test_record.py $*
./test_users.py $*
./test_messages.py $*
./test_registration.py $*
#./test_server.py $*
./test_urls.py $*
