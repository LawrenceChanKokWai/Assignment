
CC 	= gcc
CFLAGS 	= -Wall -Wextra -std=c++20
LDFLAGS = -lstdc++

APP	= reverse
TEST	= test

all: $(APP) $(TEST)

$(APP): s_reverse.cpp main.cpp
	$(CC) $(CFLAGS) main.cpp s_reverse.cpp -o $(APP) $(LDFLAGS)

$(TEST): s_reverse.cpp test.cpp
	$(CC) $(CFLAGS) test.cpp s_reverse.cpp -o $(TEST) $(LDFLAGS)

exec: $(APP) 
	@./$(APP)

run_test: $(TEST)
	@./$(TEST)

clean: 
	@rm -f $(APP) $(TEST)
